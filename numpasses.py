import sys
import numpy

num_pass_min = 1		# Min and Max number of passes
num_pass_max = 10

min_speed = 100
max_speed = 500
speed_steps = 5

width = 45
height = 50

laser_power = 1000

def set_power(power):
	return "M3 S{}\n".format(power)

def laser_off():
	return "M5 S0\n"

	
def go_to(x, y, speed):
	return "G1 X{} Y{} F{}\n".format(x, y, speed)

	
def fast_go_to(x, y):
	return "G0 X{} Y{}\n".format(x, y)
	

def set_speed(speed):
	return "G1 F{}\n".format(speed)


def generate_gcode(f):
	# Generate header
	f.write('M05 S0 			; Turn off the laser\n')
	f.write('G90	 			; Absolute positioning\n')
	f.write('G21 				; units - mm\n')
	f.write('G92 X0 Y0			; Use current position as origin\n')

	for x_idx in range(num_pass_max - num_pass_min + 1):
		x = numpy.linspace(0, width, num_pass_max - num_pass_min + 1)[x_idx]
		pass_count = x_idx + 1
		f.write('\n;{} passes at X={}\n'.format(pass_count, x))
	
		for cur_pass in range(pass_count):
			f.write('\n; pass {}\n'.format(cur_pass+1))
			f.write(fast_go_to(x, 0))
			f.write(set_power(laser_power))
			
			len = height / speed_steps
			for y_idx in range(speed_steps):
				y = range(0, height, len)[y_idx]
				speed = numpy.linspace(min_speed, max_speed, speed_steps)[y_idx]
				f.write(go_to(x, y+len, speed))
			
			f.write(laser_off())
	
def main():
	if len(sys.argv) < 2:
		print "Output file name required"
		exit(1)
	
	with open(sys.argv[1], "w+") as f:
		generate_gcode(f)
	
if __name__ == "__main__":
	main()