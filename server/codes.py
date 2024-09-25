import uuid
import os
from barcode import Code128
from barcode.writer import SVGWriter

def generate_barcode(entity, uuid_value=None):
    if entity not in ['patron', 'copy']:
        raise ValueError("Entity must be either 'patron' or 'copy'.")
    
    if uuid_value is None:
        uuid_value = uuid.uuid4()

    uuid_str = str(uuid_value)
    label_text = f"{entity}: {uuid_str}"
    
    output_dir = os.path.join(os.getcwd(), f'{entity}_barcodes')
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"barcode_{entity}_{uuid_str}.svg"
    file_path = os.path.join(output_dir, filename)
    
    barcode = Code128(uuid_str, writer=SVGWriter())
    
    barcode.save(file_path, options={
        "write_text": True, 
        "text": label_text,
        "module_width": 0.2,
        "module_height": 6,
        "quiet_zone": 1
    })
    
    return file_path

generated_path = generate_barcode('patron')
print(f"Barcode saved at: {generated_path}")
