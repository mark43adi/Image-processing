import csv
import io
from typing import List, Dict


def validate_csv(file: io.BytesIO) -> bool:
    file.seek(0)
    try:
        for encoding in ['utf-8', 'iso-8859-1', 'cp1252']:
            try:
                content = file.read().decode(encoding)
                file.seek(0)
                reader = csv.reader(io.StringIO(content))
                header = next(reader)
                expected_header = ["S. No.", "Product Name", "Input Image Urls"]
               
                header = [h.strip() for h in header]
                return header == expected_header
            except UnicodeDecodeError:
                continue
        return False
    except Exception:
        return False


def process_csv(file: io.BytesIO) -> List[Dict]:
    file.seek(0)
    
    for encoding in ['utf-8', 'iso-8859-1', 'cp1252']:
        try:
            content = file.read().decode(encoding)
            print("content csv service: ",content)
            file.seek(0)  
            reader = csv.DictReader(io.StringIO(content))
            
            csv_data = [row for row in reader]
            print("reader csv service: ",csv_data)
            return csv_data
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to decode CSV file with supported encodings")