from flask import Flask, request, send_file
import json
from style_transfer import StyleTransfer
import os
import re

style_transfer = StyleTransfer()

app = Flask(__name__)


styles_folder = 'styles'
styles = {}
for filename in os.listdir(styles_folder):
    match = re.match(r"(\d+)_([^\.]+)\.(jpe?g|png)", filename)
    style_id = int(match[1])
    image_path = os.path.join(styles_folder, filename)
    style_name = match[2].replace('-', ' ').replace('_', ' ').strip()
    styles[style_id] = {'image_path': image_path, 'style_name': style_name}


@app.route('/transfer', methods=['POST'])
def transfer():
    content_json = request.get_json()
    # content image
    content_image = content_json['content_image']
    content_image = StyleTransfer.base64_to_tensor(content_image)
    # style image
    if 'pred_style' in content_json and content_json['pred_style'] is not None:  # predefined style
        integer_pred_style = int(content_json['pred_style'])
        style_image = StyleTransfer.file_to_tensor(styles[integer_pred_style]['image_path'])
    if 'own_style' in content_json and content_json['own_style'] is not None:  # uploaded by user style
        own_style = content_json['own_style']
        style_image = StyleTransfer.base64_to_tensor(own_style)
    # transfer style
    output_image = style_transfer.transfer(style_image, content_image)
    # convert to base64
    output_image = StyleTransfer.tensor_to_image(output_image)
    img_str = StyleTransfer.pillow_to_base64(output_image)
    # return
    return json.dumps({"image": img_str})


cached_available_styles = json.dumps({k: v['style_name'] for k, v in styles.items()})
@app.route('/available_styles')
def available_styles():
    return cached_available_styles

@app.route('/')
def index():
    '''
        Este endpoint simplemente muestra el contenido de 'index.html' cuando
        se hace un pedido sin parámetros (por ejemplo desde el navegador).
        
        Sirve para probar rápidamente la API, especialmente durante su desarrollo.
        
        Cuando se disponibilice la API en producción, habría que comentar o
        borrar esta función para deshabilitar este "frontend provisorio".
    '''
    return send_file('index.html')


app.run(host="0.0.0.0", port=5000)
