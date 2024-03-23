import sys
import subprocess
import io
import base64

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PIL"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        from autocorrect import Speller
    except subprocess.CalledProcessError:
        print("Failed to install 'PIL' module. Please install it manually using 'pip install PIL'")
        sys.exit(1)

def process_image_with_string(image_path, text_string):
    # Open the image
    image = Image.open(image_path)
    # Convert image to RGBA if not already in that mode
    image = image.convert("RGBA")

    # Define text and font properties
    text = text_string.upper()
    font_size = 40
    font = ImageFont.truetype("arial.ttf", font_size)
    text_width = font.getmask(text).getbbox()[2]  # Estimate text width
    text_position = ((image.width - text_width) // 2, 20)  # Center horizontally, 50 pixels from the top

    # Create a transparent layer for the text
    text_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)

    # Draw embossed text
    shadowcolor = 'black'
    draw.text((text_position[0]-2, text_position[1]-2), text, fill=shadowcolor, font=font)
    draw.text((text_position[0]+2, text_position[1]-2), text, fill=shadowcolor, font=font)
    draw.text((text_position[0]-2, text_position[1]+2), text, fill=shadowcolor, font=font)
    draw.text((text_position[0]+2, text_position[1]+2), text, fill=shadowcolor, font=font)

    draw.text(text_position, text, fill="white", font=font)

    # Composite the text layer onto the original image
    image_with_text = Image.alpha_composite(image, text_layer)

    # Convert the image to JPEG format
    output_image_data = io.BytesIO()
    image_with_text.convert("RGB").save(output_image_data, format="JPEG")
    output_image_data = output_image_data.getvalue()

    # Encode the processed image data to base64
    output_image_data_base64 = base64.b64encode(output_image_data).decode('utf-8')

    text = "This is String Outside Image"
    return output_image_data_base64, text

if __name__ == "__main__":
    # Read the image path from command line argument
    image_path = sys.argv[1]
    # Process the image with a sample text
    output_image_data, text = process_image_with_string(image_path, "This is String inside image")
    # Print the processed image data and text
    print(output_image_data)
    print(text)
