# vCard QR Code Generator

This project generates a customised QR code containing vCard information, with options for custom colours, font selection, and styling.

## Features

- Generate QR codes with vCard information
- Customisable QR code and frame colours
- Google Fonts integration for text styling
- Responsive web interface
- Downloadable QR code image

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/IliaRyzhkovPR/qr-code-generator
   cd qr-code-generator
   ```

2. Create a new virtual environment:
   ```
   python -m venv myenv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     myenv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source myenv/bin/activate
     ```

4. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`.

3. Fill in the form with your contact information, select colors and font, and click "Generate QR Code".

4. The generated QR code will be downloaded automatically.

## Deployment

This application is deployed on Render. Follow these steps to do the same:

1. Push your code to a GitHub repository.
2. Create a new Web Service on Render, connecting to your GitHub repo.
3. Render will automatically detect it's a Python app and set most configuration options.
4. Set the following:
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Click "Create Web Service".

## Customisation Options

- `qr_color`: The colour of the QR code
- `frame_color`: The colour of the frame around the QR code
- `font_name`: The name of the Google Font to use
- `font_size`: The size of the font for the centred text

## Licence

This project is open-source and available under the MIT Licence.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/IliaRyzhkovPR/qr-code-generator/issues).

## Demo

TBC

## Notes

- The application uses Google Fonts API to fetch fonts. If a font is unavailable, it falls back to a default font.
- The generated QR code includes a frame and rounded corners for improved aesthetics.