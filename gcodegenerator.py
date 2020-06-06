class GCodeGenerator:
	f = None

	def __init__(self, filename):
		self.f = open(filename, "w+")


	def __del__(self):
		if self.f:
			self.f.close()


	def set_power(self, power):
		self.f.write("M3 S{}\n".format(power))


	def laser_off(self):
		self.f.write("M5 S0\n")

		
	def go_to(self, x, y):
		self.f.write("G1 X{} Y{}\n".format(x, y))

		
	def fast_go_to(self, x, y):
		self.f.write("G0 X{} Y{}\n".format(x, y))
		

	def set_speed(self, speed):
		self.f.write("G1 F{}\n".format(speed))


	def write(self, gcode):
		self.f.write(gcode + "\n")
