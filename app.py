from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image, ImageEnhance
import io

app = Flask(__name__)

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def adjust_saturation(image, factor):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def remove_bg(image):
    output=remove(image)
    return output 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    try:
        img = Image.open(file)
    except IOError:
        return "File is not a valid image",400
    
    output_remove = remove_bg(img)
    output = io.BytesIO()
    output_remove.save(output,format='png')
    output.seek(0)
    return send_file(output, mimetype='image/png')



@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    img = Image.open(file)
    adjusted_brightness = adjust_brightness(img, 1.5)
    adjusted_contrast = adjust_contrast(adjusted_brightness, 1.2)
    adjusted_saturation = adjust_saturation(adjusted_contrast, 1.5)

    output = io.BytesIO()
    adjusted_saturation.save(output, format='JPEG')
    output.seek(0)

    return send_file(output, mimetype='image/jpeg')

#Comment for Deployment file

# if __name__ == '__main__':
#     app.run(debug=True)

