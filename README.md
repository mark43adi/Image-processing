# Image Processing System

## Overview

The Image Processing System is designed to efficiently handle image data from CSV files. It offers APIs for uploading CSV files that contain product and image information, processes the images asynchronously with 50% compression, and allows you to check the status of processing requests.

## Features

- **CSV file upload and validation:** Upload CSV files containing image and product information.
- **Asynchronous image processing:** Compress images by 50% using Celery for background processing.
- **Status checking:** Monitor the status of processing requests via API endpoints.
- **Database storage:** Store product details and processed image data in a database.

## Prerequisites

- Python 3.8+
- Redis (for Celery task queue)
- PostgreSQL (or SQLite for development)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/mark43adi/Image-processing.git
    cd image-processing-system
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the Redis server:**

    ```bash
    redis-server
    ```

2. **Start the Celery worker:**

    ```bash
    celery -A app.tasks.celery worker --loglevel=info
    ```

3. **Run the Flask application:**

    ```bash
    python run.py
    ```

   The application will be available at [http://localhost:5000](http://localhost:5000).

## API Endpoints

- **POST /upload**: Upload a CSV file for processing.
  
  **Request:**
  - `Content-Type: multipart/form-data`
  - `File: CSV file`

  **Response:**
  - `200 OK` on successful upload and processing initiation.
  - `400 Bad Request` if there is an error with the file or request.

- **GET /status/<request_id>**: Check the status of a processing request.

  **Parameters:**
  - `request_id` (path parameter): The ID of the processing request.

  **Response:**
  - `200 OK` with JSON status of the request (`pending`, `processing`, `completed`, `failed`).
  - `404 Not Found` if the request ID does not exist.