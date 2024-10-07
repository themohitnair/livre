import barcode
from barcode.writer import SVGWriter
import uuid
import os

def generate_and_save_barcode(entity: str, id: uuid.UUID, name_or_title: str) -> str:
    if entity not in ["patron", "copy"]:
        raise ValueError("Wrong entity type. Entity type must be either 'patron' or 'copy'.")
    
    unique_id = str(id)
    barcode_format = barcode.get('code128', unique_id, writer=SVGWriter())

    options = {
        'text': f"{unique_id} - {name_or_title}",
        'font_size': 10,
        'text_distance': 5,
        'quiet_zone': 3, 
    }
    
    directory_name = f"{entity}_barcodes"
    os.makedirs(directory_name, exist_ok=True)
    file_name = f"{entity}-{unique_id}"

    barcode_path = os.path.join(directory_name, file_name)
    return barcode_format.save(barcode_path, options=options)

    return barcode_path