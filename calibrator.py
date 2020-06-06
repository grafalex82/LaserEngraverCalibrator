import sys
import numpy
import argparse

from gcodegenerator import GCodeGenerator

args = None

def generate_box(f):
	f.write("")
	f.comment('Outer box')

	f.set_speed(args.ruler_speed)

	f.fast_go_to(0, 0)
	f.set_power(args.ruler_power)
	f.go_to(args.area_width, 0)
	f.go_to(args.area_width, args.area_height)
	f.go_to(0, args.area_height)
	f.go_to(0, 0)
	f.laser_off()



def generate_X_ruler(f):
	f.write("")
	f.comment('X ruler')
	f.set_speed(args.ruler_speed)
	
	y = args.area_height + args.ruler_spacing
	index = 0
	for x in numpy.linspace(0, args.area_width, int(args.area_width/args.ruler_step) + 1):
		len = args.ruler_height if (index % args.ruler_step_mul == 0) else args.ruler_height/2

		f.fast_go_to(x, y)
		f.set_power(args.ruler_power)
		f.go_to(x, y + len)
		f.laser_off()
		
		index += 1

		
def generate_Y_ruler(f):
	f.write("")
	f.comment('Y ruler')
	f.set_speed(args.ruler_speed)

	x = args.area_width + args.ruler_spacing
	index = 0
	for y in numpy.linspace(0, args.area_height, int(args.area_height/args.ruler_step) + 1):
		len = args.ruler_width if (index % args.ruler_step_mul == 0) else args.ruler_width/2

		f.fast_go_to(x, y)
		f.set_power(args.ruler_power)
		f.go_to(x + len, y)
		f.laser_off()
		
		index += 1


def generate_image(f):
	f.write("")
	f.comment('The image')
	for y_idx in range(args.speed_grades):
		y = numpy.linspace(0, args.area_height, args.speed_grades)[y_idx]
		speed = numpy.linspace(args.min_speed, args.max_speed, args.speed_grades)[y_idx]
		
		f.comment("speed {}".format(speed))
		f.fast_go_to(0, y)
		f.set_speed(speed)
		
		for x_idx in range(args.power_grades):
			x = numpy.linspace(0, args.area_width, args.power_grades+1)[x_idx]
			len = args.area_width / args.power_grades
			power = numpy.linspace(args.min_power, args.max_power, args.power_grades)[x_idx]

			f.set_power(power)
			f.go_to(x + len, y)

		f.laser_off()
		
		
def generate_gcode(f):
	# Generate header
	f.laser_off(comment='Turn off the laser')
	f.absolute_positioning(comment='Absolute positioning')
	f.set_units_mm(comment='units - mm')
	f.set_position(0, 0, comment='Use current position as origin')
	
	# generate outer box and ruler
	generate_box(f)
	generate_X_ruler(f)
	generate_Y_ruler(f)
	
	# generate image
	generate_image(f)

	f.write('')
	f.laser_off(comment='Turn off the laser')
	f.fast_go_to(0, 0, comment='return to origin')
	f.disable_motors(comment='Disable all stepper motors')
	
	
def main():
	global args

	# Set up argparser
	parser = argparse.ArgumentParser(description='Generate a Speed vs Laser Power calibration GCode for a laser engraver')
	parser.add_argument('filename', help='Output GCode file name')

	area_size = parser.add_argument_group('Test area size')
	area_size.add_argument('--area_width', type=float, default=95, help='Width of the calibration image (default: 95, fits 19 power grades, 5mm each')
	area_size.add_argument('--area_height', type=float, default=90, help='Width of the calibration image (default: 90, fits 37 speed grades, 2.5mm each')

	speed_params = parser.add_argument_group('Speeds to test (across Y direction)')
	speed_params.add_argument('--min_speed', type=int, default=100, help='Slowest speed mm/min (default: 100)')
	speed_params.add_argument('--max_speed', type=int, default=1000, help='Fastest speed mm/min (default: 1000)')
	speed_params.add_argument('--speed_grades', type=int, default=37, help='Number of speed grades to fit in area_height  (default: 37)')

	power_params = parser.add_argument_group('Laser powers to test (across Y direction)')
	power_params.add_argument('--min_power', type=int, default=100, help='Minimum laser power (default: 100)')
	power_params.add_argument('--max_power', type=int, default=1000, help='Maximum laser power (default: 1000)')
	power_params.add_argument('--power_grades', type=int, default=19, help='Number of power grades to fit in area_width  (default: 19)')

	ruler_params = parser.add_argument_group('Ruler parameters')
	ruler_params.add_argument('--ruler_width', type=float, default=5., help='Width of the ruler at the right (default: 5)')
	ruler_params.add_argument('--ruler_height', type=float, default=5., help='Height of the ruler at the top (default: 5)')
	ruler_params.add_argument('--ruler_spacing', type=float, default=2., help='A gap between the ruler and the image (default: 2)')
	ruler_params.add_argument('--ruler_step', type=float, default=5., help='Step in mm (default: 5)')
	ruler_params.add_argument('--ruler_step_mul', type=float, default=2, help='How often to draw bigger step marks (default: every 2 marks)')
	ruler_params.add_argument('--ruler_speed', type=int, default=400, help='Speed to use when drawing ruler (default: 400)')
	ruler_params.add_argument('--ruler_power', type=int, default=200, help='Laser power to use when drawing ruler (default: 200)')

	args = parser.parse_args()
	
	f = GCodeGenerator(args.filename)
	generate_gcode(f)
	
if __name__ == "__main__":
	main()