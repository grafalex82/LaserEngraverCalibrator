import sys
import numpy


# Constants and parameters
area_width = 95. 	# Width of the calibration image
area_height = 90.	# Height of the calibration image

ruler_width	= 5.	# Actual image will be 5+2 mm wider and heigher due to ruler
ruler_height = 5.	#
ruler_spacing = 2.	# gap between image and ruler
ruler_step = 5.		# Step in mm
ruler_step_mul = 2	# how many ruler_steps for a bigger mark 
ruler_speed = 400	# speed/power for drawing ruler
ruler_power = 200	#  

min_speed = 100		# speed in mm/min
max_speed = 1000
speed_grades = 37	# Number of speed gradations (over X axis)

min_power =  100	# Laser power 0-1000
max_power = 1000
power_grades = 19	# number of power gradations (over Y axis)


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


def generate_X_ruler(f):
	f.write('\n;X ruler')
	f.set_speed(ruler_speed)
	
	y = area_height + ruler_spacing
	index = 0
	for x in numpy.linspace(0, area_width, int(area_width/ruler_step) + 1):
		len = ruler_height if (index % ruler_step_mul == 0) else ruler_height/2

		f.fast_go_to(x, y)
		f.set_power(ruler_power)
		f.go_to(x, y + len)
		f.laser_off()
		
		index += 1

		
def generate_Y_ruler(f):
	f.write('\n;Y ruler')
	f.set_speed(ruler_speed)

	x = area_width + ruler_spacing
	index = 0
	for y in numpy.linspace(0, area_height, int(area_height/ruler_step) + 1):
		len = ruler_width if (index % ruler_step_mul == 0) else ruler_width/2

		f.fast_go_to(x, y)
		f.set_power(ruler_power)
		f.go_to(x + len, y)
		f.laser_off()
		
		index += 1


def generate_image(f):
	f.write('\n;The image')
	for y_idx in range(speed_grades):
		y = numpy.linspace(0, area_height, speed_grades)[y_idx]
		speed = numpy.linspace(min_speed, max_speed, speed_grades)[y_idx]
		
		f.write("; speed {}".format(speed))
		f.fast_go_to(0, y)
		f.set_speed(speed)
		
		for x_idx in range(power_grades):
			x = numpy.linspace(0, area_width, power_grades+1)[x_idx]
			len = area_width / power_grades
			power = numpy.linspace(min_power, max_power, power_grades)[x_idx]

			f.set_power(power)
			f.go_to(x + len, y)

		f.laser_off()
		
		
def generate_gcode(f):
	# Generate header
	f.write('M05 S0 			; Turn off the laser')
	f.write('G90	 			; Absolute positioning')
	f.write('G21 				; units - mm')
	f.write('G92 X0 Y0			; Use current position as origin')
	
	# generate ruler
	generate_X_ruler(f)
	generate_Y_ruler(f)
	
	# generate image
	generate_image(f)

	f.write('')
	f.write('M05 S0 			; Turn off the laser')
	f.write('G0 X0 Y0			; return to origin')
	f.write('M18				; Disable all stepper motors')
	
	
def main():
	if len(sys.argv) < 2:
		print("Output file name required")
		exit(1)
	
	f = GCodeGenerator(sys.argv[1])
	generate_gcode(f)
	
if __name__ == "__main__":
	main()