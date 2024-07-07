import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

import vobject

def create_vcard(name, title, phone, email, company, website, linkedin, youtube):
    vcard = vobject.vCard()
    vcard.add('n')
    vcard.n.value = vobject.vcard.Name(family=name.split()[-1], given=name.split()[0])
    vcard.add('fn')
    vcard.fn.value = name
    vcard.add('title')
    vcard.title.value = title
    vcard.add('tel')
    vcard.tel.value = phone
    vcard.tel.type_param = "CELL"
    vcard.add('email')
    vcard.email.value = email
    vcard.add('org')
    vcard.org.value = [company]
    
    url_work = vcard.add('url')
    url_work.value = website
    url_work.type_param = "WORK"
    
    url_linkedin = vcard.add('url')
    url_linkedin.value = linkedin
    url_linkedin.type_param = "LinkedIn"

    url_youtube = vcard.add('url')
    url_youtube.value = youtube
    url_youtube.type_param = "YouTube"

    return vcard.serialize()

def generate_qr_code(vcard_data, company, filename, logo_path=None):
    # Create QR code
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(vcard_data)
    qr.make(fit=True)

    # Create QR code image with brand colors
    img = qr.make_image(fill_color='#FF8138', back_color="white").convert('RGB')

    # Change black pixels to #FF8138
    orange_rgb = (255, 129, 56)  # RGB values for #FF8138
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixels[i, j] == (0, 0, 0, 255):  # If the pixel is black
                pixels[i, j] = orange_rgb + (255,)  # Change to orange, keep alpha at 255

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
        draw.text(text_pos, company, font=font, fill="#33627D")

    # Add a frame
    framed = ImageOps.expand(img, border=10, fill='#33627D')
    draw = ImageDraw.Draw(framed)
    draw.rectangle([0, 0, framed.width, framed.height], outline="#FF8138", width=5)

    # Add call-to-action
    # cta_font = ImageFont.truetype(font_path, 34) if os.path.exists(font_path) else ImageFont.load_default()
    # cta_text = "Scan to connect!"
    # text_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    # text_width = text_bbox[2] - text_bbox[0]
    # draw.text(((framed.width - text_width) // 2, framed.height - 30), cta_text, font=cta_font, fill="#0047AB")

    # Round the corners
    mask = Image.new('L', framed.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, framed.width, framed.height], 20, fill=255)
    output = ImageOps.fit(framed, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    output.save(filename)

# Generate QR code
company_name = "DBAX"
vcard_data = create_vcard(
    "Ilia Ryzhkov", 
    "Technical and Data Architect", 
    "+447479563847", 
    "ilia.ryzhkov@dbax.co.uk", 
    company_name, 
    "https://dbax.co.uk",
    "https://www.linkedin.com/in/ryzhkovilya/",
    "https://www.youtube.com/@DBAXLTD"
)
generate_qr_code(vcard_data, company_name, "contact_qr.png", logo_path="Logo.png")