class GCodeGenerator:
    f = None

    def __init__(self, filename):
        self.f = open(filename, "w+")

    def __del__(self):
        if self.f:
            self.f.close()

    def write(self, gcode, comment=None):
        if comment:
            self.f.write("%-30s; %s\n" % (gcode, comment))
        else:
            self.f.write(gcode + "\n")

    def comment(self, text):
        self.f.write("; " + text + "\n")

    def set_power(self, power, comment=None):
        self.write("M3 S{}".format(power), comment)

    def laser_off(self, comment=None):
        self.write("M5 S0", comment)

    def absolute_positioning(self, comment=None):
        self.write("G90", comment)

    def relative_positioning(self, comment=None):
        self.write("G91", comment)

    def set_units_inches(self, comment=None):
        self.write("G20", comment)

    def set_units_mm(self, comment=None):
        self.write("G21", comment)

    def disable_motors(self, comment=None):
        self.write("M18", comment)

    def set_position(self, x, y, comment=None):
        self.write("G92 X{} Y{}".format(x, y), comment)

    def go_to(self, x, y, comment=None):
        self.write("G1 X{} Y{}".format(x, y), comment)

    def fast_go_to(self, x, y, comment=None):
        self.write("G0 X{} Y{}".format(x, y), comment)

    def set_speed(self, speed, comment=None):
        self.write("G1 F{}".format(speed), comment)


