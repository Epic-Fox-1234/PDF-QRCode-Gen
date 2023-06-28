import qrcode
from tempfile import NamedTemporaryFile
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


# Function to generate a QR code image
def generate_qr_code_image(data, scale):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=scale,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    # qr_img = qr_img.resize((scale, scale))
    return qr_img

# Function to generate a PDF with a grid of QR codes
def generate_qr_code_pdf(data, output_path, qr_per_row=3,qr_per_col=3, margin=0.5, qr_scale=100):
    qr_img = generate_qr_code_image(data, qr_scale)
    qr_width = qr_img.width
    qr_height = qr_img.height

    c = canvas.Canvas(output_path, pagesize=letter)

    page_width, page_height = letter
    available_width = page_width # - 2 * inch
    available_height = page_height # - 2 * inch

    qr_margin = margin * inch
    qr_size = min((available_width - (qr_per_row - 1) * qr_margin) / qr_per_row , (available_height - (qr_per_col - 1) * qr_margin) / qr_per_col)

    x = qr_margin / 2 # + inch
    y = page_height - qr_size - qr_margin / 2 # - inch 

    for i in range(qr_per_col):
        for j in range(qr_per_row):
            with NamedTemporaryFile(delete=False) as tmp_file:
                qr_img.save(tmp_file.name, format='PNG')
                c.drawImage(tmp_file.name, x, y, qr_size, qr_size)
            x += qr_size + qr_margin

        x = qr_margin / 2 # + inch
        y -= qr_size + qr_margin

    c.save()