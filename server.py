from flask import Flask
app = Flask(__name__)

import RPi.GPIO as gpio

pins = {
	'input': {
		'switch-1': 4,
	},
	'output': {
		'led-1': 2,
	},
}

def initialize_gpio():
	gpio.setmode(gpio.BCM);

@app.route('/')
def root():
	return 'try "/input" or "/output"'

@app.route('/rpi_info')
def rpi_info():
	return gpio.RPI_INFO.__str__()

@app.route('/input')
def list_inputs():
	return '{}'.format(list(pins['input'].keys()))

@app.route('/input/<name>')
def read_pin(name):
	try:
		channel = pins['input'][name]
	except:
		return 'could not find "{}" among {}'.format(name, list(pins['input'].keys())), 404
	gpio.setup(channel, gpio.IN)
	value = gpio.input(channel)
	return '{}'.format(value)

@app.route('/output')
def list_outputs():
	return '{}'.format(list(pins['output'].keys()))

@app.route('/output/<name>')
def read_output(name):
	try:
		channel = pins['output'][name]
	except:
		return 'could not find "{}" among {}'.format(name, list(pins['output'].keys())), 404
	gpio.setup(channel, gpio.OUT)
	value = gpio.input(channel)
	return '{}'.format(value)

@app.route('/output/<name>/<value>')
def set_output(name, value):
	try:
		channel = pins['output'][name]
	except:
		return 'could not find "{}" among {}'.format(name, list(pins['output'].keys())), 404
	gpio.setup(channel, gpio.OUT)
	try:
		value = int(value)
		if value not in (0, 1):
			raise Exception
	except:
		return 'the value should be 0 or 1', 400
	gpio.output(channel, value)
	value = gpio.input(channel)
	return '{}'.format(value)

if __name__ == '__main__':
	initialize_gpio()
	app.run(
		host = '0.0.0.0',
		port = 80,
	)

