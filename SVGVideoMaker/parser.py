"""
Parser homemade to convert SVG file to SVGVideoMaker Object
"""

from re import findall
from xml.dom.minidom import parse
from SVGVideoMaker import Polygon, Segment, Point2D, Ellipse, Rectangle, Group, SVG
from SVGVideoMaker import msg, DEBUG_LEVEL

number = r"([-+]?\d*\.\d+|\d+)"

def compute_array2dict(array):
	dictionary = {}
	for el in array:
		dictionary[el[0]] = el[1]
	return dictionary

def check_element(dictionnary, key, type):
	try:
		return type(dictionnary[key])
	except KeyError:
		return None

def parse_transform(shape, attributes):
	transform = check_element(attributes, "transform", str)
	if transform:
		translate = f"translate\({number} {number}?\)"
		matching = findall(translate, transform)
		if matching:
			pt = [0, 0]
			for values in matching:
				pt = [float(v) + old_v for v, old_v in zip(values, pt)]
			shape.translation = pt

		rotate = f"rotate\({number}( {number} {number})?\)"
		matching = findall(rotate, transform)
		if matching:
			for values in matching:
				shape.rotation += float(values[0])

def parse_style(shape, attributes):
	fill_color = check_element(attributes, "fill", str)
	stroke_linecaps = check_element(attributes, "stroke-linecaps", str)
	stroke_dasharray = check_element(attributes, "stroke-dasharray", str)
	stroke_width = check_element(attributes, "stroke-width", float)
	stroke_color = check_element(attributes, "stroke", str)
	opacity = check_element(attributes, "opacity", float)
	shape.set_style(fill_color, stroke_color, stroke_width, stroke_linecaps, stroke_dasharray, opacity)

def parse_shape(shape, attributes):
	parse_transform(shape, attributes)
	parse_style(shape, attributes)

def parse_svgtag(attributes):
	p_width = check_element(attributes, "width", int)
	p_height = check_element(attributes, "height", int)
	p_vb = check_element(attributes, "viewBox", str)
	width = p_width if p_width else 500
	height = p_height if p_height else 500

	svg = SVG(width=width, height=height)
	if p_vb:
		sx, sy, ex, ey = p_vb.split()
		svg.set_view_box(Point2D(float(sx), float(sy)),
		                 Point2D(float(ex), float(ey)))

	return svg

def parse_segment(attributes):
	x1 = check_element(attributes, "x1", float)
	y1 = check_element(attributes, "y1", float)
	x2 = check_element(attributes, "x2", float)
	y2 = check_element(attributes, "y2", float)
	s = Segment(Point2D(x1, y1), Point2D(x2, y2))
	parse_shape(s, attributes)
	return s

def parse_ellipse(attributes):
	cx = check_element(attributes, "cx", float)
	cy = check_element(attributes, "cy", float)
	rx = check_element(attributes, "rx", float)
	ry = check_element(attributes, "ry", float)
	e = Ellipse(Point2D(cx, cy), rx, ry)
	parse_shape(e, attributes)
	return e

def parse_polygon(attributes):
	points_str = check_element(attributes, "points", str)
	pts = [Point2D(*list(map(float, element.split(",")))) for element in [el for el in points_str.split(" ")]]
	p = Polygon(pts)
	parse_shape(p, attributes)
	return p

def parse_rectangle(attributes):
	x = check_element(attributes, "x", float)
	y = check_element(attributes, "y", float)
	width = check_element(attributes, "width", int)
	height = check_element(attributes, "height", int)
	r = Rectangle(Point2D(x, y), width, height)
	parse_shape(r, attributes)
	return r

def parse_group(attributes):
	g = Group()
	parse_shape(g, attributes)
	return g

def parse_node(node):
	tag = node.tagName

	if tag == "g":
		parser = parse_group
	elif tag == "rect":
		parser = parse_rectangle
	elif tag == "polygon":
		parser = parse_polygon
	elif tag == "ellipse":
		parser = parse_ellipse
	elif tag == "line":
		parser = parse_segment
	else:
		msg("Tag Element isn't supported", DEBUG_LEVEL.WARNING)
		return None

	return parser(compute_array2dict(node.attributes.items()))

def parse_xml2SVG(node, parent=None):
	for el in node.childNodes:
		if el.nodeType == el.ELEMENT_NODE:
			svg_node = parse_node(el)
			if svg_node is not None:
				parent.append(svg_node)
				parse_xml2SVG(el, svg_node)

def parse_svg(file):
	to_parse = parse(file)
	first_el = to_parse.childNodes[0]
	if first_el.tagName != "svg":
		msg("First node isn't SVG tag !")
	svg = parse_svgtag(compute_array2dict(first_el.attributes.items()))
	parse_xml2SVG(first_el, svg)
	to_parse.unlink()
	return svg
