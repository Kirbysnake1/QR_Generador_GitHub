from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    # Check if the request method is POST
    # Verifica si el método de solicitud es POST
    if request.method == 'POST':
        # Get the URL from the form
        # Obtener el URL del formulario
        url = request.form.get('url')
        if url:
            # Generate QR code
            # Generar código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            # Convert QR code image to base64 format
            # Convertir la imagen del código QR al formato base64
            img = qr.make_image(fill='black', back_color='white')
            img_bytes = BytesIO()
            img.save(img_bytes)
            img_bytes.seek(0)
            img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
            img_data = f"data:image/png;base64,{img_base64}"

            # Render the show_qr.html template with QR code data
            # Renderiza la plantilla show_qr.html con los datos del código QR
            return render_template('show_qr.html', img_data=img_data)
    # Render the index.html template for GET requests or when URL is not provided
    # Renderiza la plantilla index.html para solicitudes GET o cuando no se proporciona un URL
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
