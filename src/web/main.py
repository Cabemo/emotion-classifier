from flask import Flask, jsonify, make_response, request, abort, redirect, send_file
from csv import writer
import logging
import pathlib
from validate import validate_add_to_dataset
import emotion_gender_processor as eg_processor

# Ruta del archivo donde se almacenan los dataset via post
DATASETPATH = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/dataset/d.csv'

app = Flask(__name__)

@app.route('/')
def index():
		return """
			Puedes ver las instruciones en README.md
		"""

#curl -F "image=@imageA.jpg" http://0.0.0.0:8000/imagen/clasificar > image.png 
@app.route('/imagen/clasificar', methods=['POST'])
def upload():
	try:
		image = request.files['image'].read()
		eg_processor.process_image(image)
		return send_file(str(pathlib.Path(__file__ + '/result')) + 'predicted_image.png', mimetype='image/png')
	except Exception as err:
		logging.error('No pudimos procesar la imagen enviada')
		abort(400)


#curl -d '{"emotion": 6, "pixels": [1]}' -H "CONTENT-TYPE: application/json" http://0.0.0.0:8000/imagen/agregar
@app.route('/imagen/agregar', methods=['POST'])
def add_to_dataset():
	if not request.is_json:
		return make_response(jsonify({
			'error': '{ \'emotion\': [0-6],\'pixels\': [ pixel1, pixel2, pixeln, pixel2034 ] }',
			'message': "Revisar la documentacion si es necesario"
		}), 400)

	try:
		json_req = request.get_json()
		#print(json_req['pixels'])
		print(DATASETPATH)
		if(validate_add_to_dataset(json_req)):
			with open(DATASETPATH, 'a+', newline='') as write_obj:
				# Create a writer object from csv module
				csv_writer = writer(write_obj)
				# Add contents of list as last row in the csv file
				json_req['pixels'].insert(0, json_req['emotion'])
				csv_writer.writerow(json_req['pixels'])
			return make_response(jsonify({'message':'Insertado correctamente'}), 201)

		return make_response(jsonify({
		'error': '{ \'emotion\': [0-6],\'pixels\': [ pixel1, pixel2, pixeln, pixel2034 ] }',
		'message': "Revisar la documentacion si es necesario"
		}), 400)
		
	except Exception as err:
		logging.error('Error insertando')
		abort(400)

@app.errorhandler(400)
def bad_request(erro):
		return make_response(jsonify({'error': 'No pudimos procesar la información enviada.'}), 400)

@app.errorhandler(404)
def not_found(error):
		return make_response(jsonify({'error': 'Página no encontrada.'}), 404)


if __name__ == '__main__':
		app.run(debug=True, host='0.0.0.0', port=8000)