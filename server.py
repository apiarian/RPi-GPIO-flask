from flask import Flask
app = Flask(__name__)

try:
	import RPi.GPIO as gpio
except:
	print("using dummy gpio")
	class DummyGPIO:
		def setmode(mode):
			return 1
		def setup(channel, mode):
			return 1
		def input(channel):
			return 1
		def output(channel, level):
			return 1
	gpio = DummyGPIO
	gpio.BCM = 0
	gpio.IN = 0
	gpio.OUT = 0
	gpio.RPI_INFO = ['probably not a raspberry pi.']

pins = {
	'input': {
		'switch-1': 4,
	},
	'output': {
		'led-1': 2,
	},
}

def make_404(thing, group):
	return ('could not find "{}" among {}'.format(thing, list(group)), 404)

def make_404_pin_group(name, group):
	return make_404(name, pins[group].keys())

def channel_value_string(channel):
	value = gpio.input(channel)
	return '{}'.format(value)

def initialize_gpio():
	gpio.setmode(gpio.BCM);

@app.route('/')
def root():
	return 'try "/input", "/output", or "/rpi_info"'

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
		return make_404_pin_group(name, 'input')
	gpio.setup(channel, gpio.IN)
	return channel_value_string(channel)

@app.route('/output')
def list_outputs():
	return '{}'.format(list(pins['output'].keys()))

@app.route('/output/<name>')
def read_output(name):
	try:
		channel = pins['output'][name]
	except:
		return make_404_pin_group(name, 'output')
	gpio.setup(channel, gpio.OUT)
	return channel_value_string(channel)

@app.route('/output/<name>/<value>')
def set_output(name, value):
	try:
		channel = pins['output'][name]
	except:
		return make_404_pin_group(name, 'output')
	try:
		value = int(value)
		if value not in (0, 1):
			raise Exception
	except:
		return 'the value should be 0 or 1', 400
	gpio.setup(channel, gpio.OUT)
	gpio.output(channel, value)
	return channel_value_string(channel)

if __name__ == '__main__':
	initialize_gpio()
	app.run(
		host = '0.0.0.0',
		port = 80,
	)

