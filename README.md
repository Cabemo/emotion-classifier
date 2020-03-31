# Reconocimiento de emociones mediante gestos faciales

# Correr el API

Para correr el API se deben seguir los siguientes pasos:

1. Clonar el repositorio
2. Seguir una de las dos opciones

## Opcion 1: Local

*nota: Se sugiere estar dentro de un entorno virtual de python*

```sh
pip3 install \
pandas \
scikit-learn \
scipy==1.1.0 \
Pillow \
tensorflow==1.13.0rc1 \
"numpy<1.17" \
h5py \
opencv-python==4.2.0.32 \
keras \
statistics \
pyyaml \
pyparsing \
cycler \
matplotlib \
Flask \
setuptools==41.0.0
```

Una vez instaladas las dependencias necesarias basta con inicar Flask

```sh
python3 src/web/main.py
```

## Opcion 2: Docker

```sh
docker pull https://hub.docker.com/repository/docker/robtry/face
docker run -d -p 8000:8000 robtry/face
```

# Como usar

## Ingesta de datos

Para el dataset se requiere un arreglo de pixeles de 1 + 2034 donde el primer elemento corresponde a la emoción visible en la imagen.

- 0 : 'Enojo',
- 1 : 'Disgusto'
- 2 : 'Miedo
- 3 : 'Felicidad
- 4 : 'Tristeza'
- 5 : 'Sorpresa'
- 6 : 'Nutral'

Los siguientes 2034 elementos corresponden a los pixeles de una imagen (48 x 48) en escala de grises, por lo tanto son valores entre 0 y 255.

### Formato del json

```json
{
	'emotion': [0-6],
	'pixels' : [ 
		pixel1,
		pixel...,
		pixel2034,
	]
}

```

## Consulta

Para hacer la prueba sobre clasificar una imagen basta con ejecutar.

```sh
curl -F "image=@image.jpg" http://0.0.0.0:8000/imagen/clasificar > image.png 
```

La salida es la imagen después de ser procesada.