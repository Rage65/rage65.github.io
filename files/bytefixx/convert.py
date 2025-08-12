import re
import sys
from fpdf import FPDF
from datetime import date

today = date.today()
formatted_date = today.strftime("%m/%d/%Y")
# === Read the file ===
with open(r"C:\windows\Temp\cert.txt", "r") as f:
    data = f.read()
#arguments for username and cert name
cert_name = sys.argv[1]
username = sys.argv[2]
# === Pattern to split blocks by device ===
device_blocks = re.split(r'\n(?=Model:)', data)

# === Prepare PDF ===
pdf = FPDF()
pdf.add_page()
pdf.image(r"C:\windows\temp\logo.png", 5, 8, 124)

pdf.set_font('Arial', 'B', 16)
pdf.set_x(100)
pdf.cell(100, 5, 'Bytefixx certificate of destruction ', border=0, ln=True, align='C')
pdf.set_font('Arial', '', 12)
pdf.set_x(100)
pdf.cell(100, 12, cert_name, border=0, ln=True, align='C')
pdf.set_x(100)
pdf.cell(100, 10, formatted_date, border=0, ln=True, align='C')
# Column headers
pdf.set_font('Arial', 'B', 14)
cell_width = 45
left_margin = 12
pdf.ln(40)
pdf.set_x(left_margin)
pdf.cell(cell_width, 12, 'DEVICE MODEL', border=0)
pdf.cell(cell_width, 12, 'DEVICE SERIAL', border=0)
pdf.cell(cell_width, 12, 'DRIVE SERIAL', border=0)
pdf.cell(cell_width, 12, 'Device Status', border=0, ln=True)

# === Parse each device block ===
pdf.set_font('Arial', '', 12)
for block in device_blocks:
    header_match = re.search(r'Model:\s*(.*?),\s*Serial Number:\s*(.*?),\s*Drive Info:', block)
    if not header_match:
        continue

    # Clean device model (collapse multiple spaces to one)
    device_model = re.sub(r'\s+', ' ', header_match.group(1)).strip()
    device_serial = header_match.group(2).strip()

    # Find all drive serials in this block
    drive_matches = re.findall(r'Drive Serial Number:\s*([\w_\.]+)', block)

    # Add a row for each drive serial
    for drive_serial in drive_matches:
        pdf.set_x(left_margin)
        pdf.cell(50, 10, device_model, border=0)
        pdf.cell(38, 10, device_serial, border=0)
        pdf.cell(50, 10, drive_serial, border=0)
        pdf.cell(5300, 10, 'DOD Wiped', border=0, ln=True)

# === Footer notice ===
pdf.ln(10)
pdf.set_x(left_margin)
pdf.cell(100, 5, 'TEST ONLY NOT FOR USE', border=0, ln=True, align='C')

# === Signature image ===
pdf.ln(20)
pdf.image(r"C:\windows\temp\CertSig.png", 0, 190, 230)

# === Save PDF ===
output_path = fr'C:\Users\{username}\Desktop\{cert_name}.pdf'
pdf.output(output_path, 'F')
