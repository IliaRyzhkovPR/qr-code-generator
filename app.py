from flask import Flask, render_template, request, send_file
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont, ImageOps
import vobject
import io
import requests
import tempfile
import os

app = Flask(__name__)

def get_google_font(font_name):
    try:
        url = f"https://fonts.googleapis.com/css?family={font_name.replace(' ', '+')}"
        print(f"Fetching font from URL: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        
        # Try to find the font URL in the response
        font_url = None
        for line in response.text.split('\n'):
            if 'url(' in line and '.ttf' in line:
                font_url = line.split('url(')[1].split(')')[0]
                print(f"Found font URL: {font_url}")
                break
        
        if font_url:
            font_response = requests.get(font_url)
            font_response.raise_for_status()
            print(f"Successfully fetched font file from: {font_url}")
            
            # Save the font to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as temp_font_file:
                temp_font_file.write(font_response.content)
                print(f"Saved font to temporary file: {temp_font_file.name}")
                return temp_font_file.name
        else:
            print(f"Could not find font URL for {font_name}")
            return None
    except Exception as e:
        print(f"Error fetching Google Font: {str(e)}")
        return None
    
def generate_vcard_qr(name, title, email, phone=None, company=None, website=None, linkedin=None, youtube=None, 
                      qr_color='#FF8138', frame_color='#33627D', frame_width=10, corner_radius=20, font_name='Roboto', font_size=100):
    # Create vCard
    vcard = vobject.vCard()
    vcard.add('n').value = vobject.vcard.Name(family=name.split()[-1], given=name.split()[0])
    vcard.add('fn').value = name
    vcard.add('title').value = title
    vcard.add('email').value = email

    if phone:
        vcard.add('tel').value = phone
        vcard.tel.type_param = "CELL"
    if company:
        vcard.add('org').value = [company]
    if website:
        url_work = vcard.add('url')
        url_work.value = website
        url_work.type_param = "WORK"
    if linkedin:
        url_linkedin = vcard.add('url')
        url_linkedin.value = linkedin
        url_linkedin.type_param = "LinkedIn"
    if youtube:
        url_youtube = vcard.add('url')
        url_youtube.value = youtube
        url_youtube.type_param = "YouTube"

    vcard_data = vcard.serialize()

    # Create QR code
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(vcard_data)
    qr.make(fit=True)

    # Create QR code image with specified color
    img = qr.make_image(fill_color=qr_color, back_color="white").convert('RGB')

    # Calculate center area to clear
    size = img.size[0]
    center_size = size // 3  # Use half of the QR code size for the clear area
    center_pos = (size - center_size) // 2

    # Clear center area
    draw = ImageDraw.Draw(img)
    draw.rectangle([center_pos, center_pos, center_pos + center_size, center_pos + center_size], fill="white")

    # Add company name or initials if no company
    text_to_draw = company if company else ''.join([name[0] for name in name.split() if name])

     # Get and use the Google Font
    font_path = get_google_font(font_name)
    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
    except IOError:
        print(f"Error loading font {font_name}. Using default font.")
        font = ImageFont.load_default()  

    # Calculate text position
    text_bbox = font.getbbox(text_to_draw)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_pos = (center_pos + (center_size - text_width) // 2, 
                center_pos + (center_size - text_height) // 2)

    # Draw the text
    draw.text(text_pos, text_to_draw, font=font, fill=frame_color)

    # Clean up the temporary font file
    if font_path and os.path.exists(font_path):
        os.unlink(font_path)

    # Add a frame
    framed = ImageOps.expand(img, border=frame_width, fill=frame_color)
    draw = ImageDraw.Draw(framed)
    draw.rectangle([0, 0, framed.width, framed.height], outline=qr_color, width=5)

    # Round the corners
    mask = Image.new('L', framed.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, framed.width, framed.height], corner_radius, fill=255)
    output = ImageOps.fit(framed, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    # Save to BytesIO object
    img_io = io.BytesIO()
    output.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        qr_image = generate_vcard_qr(
            name=request.form['name'],
            title=request.form['title'],
            email=request.form['email'],
            phone=request.form.get('phone', ''),
            company=request.form.get('company', ''),
            website=request.form.get('website', ''),
            linkedin=request.form.get('linkedin', ''),
            youtube=request.form.get('youtube', ''),
            qr_color=request.form['qr_color'],
            frame_color=request.form['frame_color'],
            font_name=request.form['font'],
            font_size=int(request.form['font_size'])
        )
        return send_file(qr_image, mimetype='image/png', as_attachment=True, download_name='qr_code.png')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))