import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import vobject

def generate_vcard_qr(name, title, phone, email, company, website, linkedin, youtube, 
                      output_filename, logo_path=None, qr_color='#FF8138', 
                      frame_color='#33627D', frame_width=10, corner_radius=20):
    # Create vCard
    vcard = vobject.vCard()
    vcard.add('n').value = vobject.vcard.Name(family=name.split()[-1], given=name.split()[0])
    vcard.add('fn').value = name
    vcard.add('title').value = title
    vcard.add('tel').value = phone
    vcard.tel.type_param = "CELL"
    vcard.add('email').value = email
    vcard.add('org').value = [company]
    vcard.add('url').value = website
    vcard.url.type_param = "WORK"
    vcard.add('url').value = linkedin
    vcard.url.type_param = "LinkedIn"
    vcard.add('url').value = youtube
    vcard.url.type_param = "YouTube"

    vcard_data = vcard.serialize()

    # Create QR code
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(vcard_data)
    qr.make(fit=True)

    # Create QR code image with specified color
    img = qr.make_image(fill_color=qr_color, back_color="white").convert('RGB')

    # Calculate center area to clear
    size = img.size[0]
    center_size = size // 3
    center_pos = (size - center_size) // 2

    # Clear center area
    draw = ImageDraw.Draw(img)
    draw.rectangle([center_pos, center_pos, center_pos + center_size, center_pos + center_size], fill="white")

    # Add logo if provided
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)
        logo = logo.resize((center_size, center_size))
        img.paste(logo, (center_pos, center_pos), logo if logo.mode == 'RGBA' else None)
    else:
        # If no logo, add company name
        font_path = os.path.join("Montserrat", "static", "Montserrat-Bold.ttf")
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, center_size // 4)
        else:
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), company, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_pos = ((size - text_width) // 2, (size - text_height) // 2)
        draw.text(text_pos, company, font=font, fill=frame_color)

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

    output.save(output_filename)
    print(f"QR code has been generated as '{output_filename}'")

# Example usage
generate_vcard_qr(
    name="John Doe",
    title="Software Engineer",
    phone="+1234567890",
    email="john.doe@example.com",
    company="Tech Co",
    website="https://example.com",
    linkedin="https://www.linkedin.com/in/johndoe/",
    youtube="https://www.youtube.com/@johndoe",
    output_filename="john_doe_qr.png",
    logo_path="techco_logo.png",
    qr_color='#00FF00',
    frame_color='#0000FF',
    frame_width=15,
    corner_radius=30
)