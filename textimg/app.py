from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    text = data.get('text', 'Text Necompletat')

    if len(text) > 40:
        text = text[:40]

    img = Image.new('RGB', (800, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    for i in range(800):
        r = int(255 - (i / 800) * (255 - 102))
        g = int(102 + (i / 800) * (153 - 102))
        b = int(153 + (i / 800) * (204 - 153))
        draw.line([(i, 0), (i, 400)], fill=(r, g, b))

    font_size = 100
    font_path = 'arialbd.ttf'  # font
    font = ImageFont.truetype(font_path, font_size)

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    outline_range = 2
    for dx in range(-outline_range, outline_range + 1):
        for dy in range(-outline_range, outline_range + 1):
            if dx != 0 or dy != 0:
                draw.text(((800 - text_width) // 2 + dx, (400 - text_height) // 2 + dy), text, fill='black', font=font)

    draw.text(((800 - text_width) // 2, (400 - text_height) // 2), text, fill='white', font=font)

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
