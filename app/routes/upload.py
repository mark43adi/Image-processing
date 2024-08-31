from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import uuid
from app import db
from app.models import ProcessingRequest
from app.services.csv_service import validate_csv, process_csv
from app.tasks.process_images import process_images_task
import io 

bp = Blueprint('upload', __name__)

@bp.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        
        file_contents = file.read()
        print(file_contents)
        
        file_obj = io.BytesIO(file_contents)
        print(file_obj)
        
        try:
            if not validate_csv(file_obj):
                return jsonify({"error": "Invalid CSV format"}), 400

            file_obj.seek(0)
            csv_data = process_csv(file_obj)
            print("csv after csv service: ", csv_data)
            request_id = str(uuid.uuid4())
            db_request = ProcessingRequest(request_id=request_id, status="pending")
            print(db_request)
            db.session.add(db_request)
            db.session.commit()

            
            process_images_task.delay(request_id, csv_data)
            # process_images_task(request_id, csv_data)

            return jsonify({"request_id": request_id}), 202
        except Exception as e:
            return jsonify({"error": str(e)}), 400