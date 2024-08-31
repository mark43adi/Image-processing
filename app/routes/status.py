from flask import Blueprint, jsonify
from app.models import ProcessingRequest

bp = Blueprint('status', __name__)

@bp.route('/status/<request_id>', methods=['GET'])
def get_status(request_id):
    request = ProcessingRequest.query.filter_by(request_id=request_id).first()
    
    if not request:
        return jsonify({"error": "Request not found"}), 404

    return jsonify({"status": request.status}), 200