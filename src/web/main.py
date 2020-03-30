from flask import Flask, jsonify, make_response, request, abort, redirect, send_file
#import logging

app = Flask(__name__)

@app.route('/')
def index():
		return """
			Puedes ver las instruciones en README.md
		"""

if __name__ == '__main__':
		app.run(debug=True, host='0.0.0.0', port=8084)