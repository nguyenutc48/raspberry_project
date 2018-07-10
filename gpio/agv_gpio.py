





from Adafruit_MCP230xx import Adafruit_MCP230XX

mcp0 = Adafruit_MCP230XX(address=0x20, num_gpios=16)
mcp1 = Adafruit_MCP230XX(address=0x21, num_gpios=16)
mcp2 = Adafruit_MCP230XX(address=0x22, num_gpios=16)

def setup():
	for i in range(16):
		mcp0.config(i, mcp0.INPUT)
		mcp0.pullup(i, 1)
		if i < 8:
			mcp1.config(i, mcp1.INPUT)
			mcp1.pullup(i, 1)

	for o in range(16):
		mcp2.config(o, mcp2.OUTPUT)
		mcp2.output(o, 0)
		if o > 7:
			mcp1.config(o, mcp1.OUTPUT)
			mcp1.output(o, 0)

class AGV_IO(object):

	def __init__(self):
		setup()

	def getio(self,address):
		if address < 16:
			result = mcp0.input(address)
		else:
			result = mcp1.input(address-16)
		if result == 0:
			return 1
		else:
			return 0

	def setio(self,address,value):
		if address < 16:

			mcp2.output(address, value)
		else:
			mcp1.output(address-8)