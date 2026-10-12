# ColorPop — Color Matching and Identifying Web App

ColorPop is a simple, colorful Python web application for exploring color codes and sampling colors from images. It is built with Streamlit.

## Features

- Pick a color with an interactive color picker.
- Enter a HEX color code.
- View HEX and RGB values.
- See a coordinated color palette.
- Upload a PNG, JPG, JPEG, or WEBP image and sample a pixel using X/Y coordinates.
- Responsive layout for desktop and mobile browsers.

## Requirements

- Python 3.9 or newer
- Internet connection for the optional Google Fonts styling

## Install and run

1. Download all three project files into the same folder.
2. Open a terminal or command prompt in that folder.
3. (Optional but recommended) Create and activate a virtual environment.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Project files

- `app.py` — application interface and color logic
- `requirements.txt` — Python dependencies
- `README.md` — setup and usage guide

## Notes

- Image color sampling uses X and Y pixel coordinates from the image's top-left corner.
- This is a front-end project prototype. It does not require an account or database.
- Color names are approximate labels based on hue, saturation, and brightness; they are not a formal color-standard lookup.
