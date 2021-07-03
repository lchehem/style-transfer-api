# style-transfer-api

API rest en Flask que aplica style transfer de una imagen hacia otra.

Los estilos se pueden enviar a través de un endpoint de la API o se pueden cargar en un directorio específico para dicho fin. En ese caso un endpoint especial informa los estilos disponibles en el servidor, para que el frontend muestre un desplegable con los mismos.

## Endpoints


### 1. /available_styles

No tiene argumentos, retorna la lista de estilos disponibles en el servidor, informando su key/índice y nombre.

### 2. /transfer

Es el endpoint principal, realiza la transferencia de estilo.

#### Argumentos

Observación: es obligatorio que al menos uno entre 'pred_style' y 'own_style' sea enviado en el pedido.

'content_image': Obligatorio. Imagen para utilizar como 'contenido', codificada en base64.

'pred_style': Opcional. Estilo predefinido del servidor. Debe coincidir con la clave de uno de los estilos informados por el endpoint '/available_styles'.

'own_style': Opcional. Imagen propia (no predefinida) para utilizar como 'estilo', codificada en base64.

#### Respuesta

Imagen producida al aplicar el estilo 'pred_style' o 'own_style' a la imagen 'content_image'.

### 3. /

Retorna el contenido del archivo 'index.html'. Es un frontend muy básico utilizado para probar la API durante su desarrollo.
