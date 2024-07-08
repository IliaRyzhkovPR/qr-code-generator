# vCard QR Code Generator

This project generates a customized QR code containing vCard information, with options for custom colors, logo placement, and styling.

## Setup

1. Create a new virtual environment:
   ```
   python -m venv myenv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     myenv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source myenv/bin/activate
     ```

3. Install required packages:
   ```
   pip install qrcode[pil] vobject Pillow
   ```

4. Verify the installation:
   ```
   python -c "import vobject; import qrcode; import PIL; print(f'vobject: {vobject.__version__}, qrcode: {qrcode.__version__}, Pillow: {PIL.__version__}')"
   ```

5. (Optional) Generate a requirements.txt file:
   ```
   pip freeze > requirements.txt
   ```

## Usage

1. Place your logo image (if using) in the same directory as the script.

2. Modify the `generate_vcard_qr` function call in the script with your desired information:

   ```python
   generate_vcard_qr(
       name="Your Name",
       title="Your Title",
       phone="Your Phone Number",
       email="your.email@example.com",
       company="Your Company",
       website="https://your-website.com",
       linkedin="https://www.linkedin.com/in/yourprofile/",
       youtube="https://www.youtube.com/@yourchannel",
       output_filename="your_qr_code.png",
       logo_path="your_logo.png",
       qr_color='#FF8138',
       frame_color='#33627D',
       frame_width=10,
       corner_radius=20
   )
   ```

3. Run the script:
   ```
   python qr_code.py
   ```

4. The generated QR code will be saved with the filename specified in `output_filename`.

## Customization Options

- `qr_color`: The color of the QR code (default: '#FF8138')
- `frame_color`: The color of the frame around the QR code (default: '#33627D')
- `frame_width`: The width of the frame in pixels (default: 10)
- `corner_radius`: The radius of the rounded corners in pixels (default: 20)
- `logo_path`: Path to your logo image file (optional)

## Deactivating the Virtual Environment

When you're done, deactivate the virtual environment:
```
deactivate
```

## Notes

- Ensure that the Montserrat font is installed or available in the specified path for optimal text rendering.
- The script uses the vCard format to store contact information in the QR code.
- The generated QR code includes a frame and rounded corners for improved aesthetics.