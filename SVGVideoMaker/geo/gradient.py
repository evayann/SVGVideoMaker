"""
Necessary to make gradient for SVG
"""

class Gradient:
	def __init__(self, id, start=None, end=None):
		self.id = id
		if start and end:
			self.start = start
			self.end = end
		else:
			self.start = None
			self.end = None
		self.colors = {}

	def add_color(self, offset, color, opacity):
		self.colors[offset] = (color, opacity)

	def svg_content(self):
		orientation = 'x1="{}" y1="{}" x2="{}" y2="{}"'.format(*self.start, *self.end) if self.start else ""
		string = f'<linearGradient id="{self.id}" {orientation}>\n'

		for offset, (color, opacity) in self.colors.items():
			string += f'<stop offset="{offset}%" stop-color="{color}" stop-opacity="{opacity}" />\n'
		return string + "</linearGradient>"
