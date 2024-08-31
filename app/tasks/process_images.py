from app import create_app, db
from app.models import ProcessingRequest, Product
from app.services.image_service import process_images
from celery import Celery

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# from app import create_app, db



# Configure Celery
celery = Celery(__name__)
celery.conf.broker_url = 'redis://localhost:6379/0'
celery.conf.result_backend = 'redis://localhost:6379/0'

import logging

logger = logging.getLogger(__name__)

@celery.task
def process_images_task(request_id, csv_data):
    app = create_app()
    with app.app_context():
        request = ProcessingRequest.query.filter_by(request_id=request_id).first()
        request.status = "processing"
        db.session.commit()

        try:
            print("yes", csv_data)
            for row in csv_data:
                print("sdfjd")
                input_urls = row["Input Image Urls"].replace('\n', '').split(",")
                logger.info(f"Input URLs: {input_urls}")

                output_urls = process_images(input_urls)
                logger.info(f"Output URLs: {output_urls}")
                
                product = Product(
                    request_id=request_id,
                    serial_number=row["S. No."],
                    name=row["Product Name"],
                    input_image_urls=",".join(input_urls),
                    output_image_urls=",".join(output_urls)
                )
                logger.info(f"Adding product: {product}")

                db.session.add(product)
                db.session.commit()

            request.status = "completed"
        except Exception as e:
            request.status = "failed"
            logger.error(f"Error processing images: {e}")
            # Optionally, log the stack trace
            import traceback
            logger.error(traceback.format_exc())

        db.session.commit()
