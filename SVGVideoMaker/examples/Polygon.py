"""
Test EllipseArc of SVGVideoMaker
"""

# region Imports
from SVGVideoMaker.geo import Point2D, SVG, Polygon, Rectangle
from SVGVideoMaker.video import Video
# endregion Imports

# Global values
fps = 30
seconds = 5
position_offset = 20
width, height = 110, 180
center = Point2D(width // 2, height // 2)
full_turn = 360
half_turn = 180

svg = SVG(width=width, height=height)
svg.set_view_box(Point2D(0, 0), Point2D(width, height))

def create_column(colum, sens):
	size, half_size = 10, 5
	stroke_incrementer = 0.2

	for i in range(height // position_offset):
		squarre = Polygon.square(colum - half_size, i * position_offset + int(position_offset / 2) - half_size, size)
		stroke_incrementer *= 1.5 if i <= 4 else 0.5
		if i % 2:
			for j, seg in enumerate(squarre.get_segments()):
				seg.add_rotate(seconds * fps, value=sens * full_turn)
				seg.set_style(stroke_color="red", stroke_linecaps="round")
				svg.append(seg)
		else:
			squarre.add_rotate(seconds * fps, value=sens * full_turn)
			squarre.set_style(stroke_color="black", stroke_width=1 + stroke_incrementer,
			                  stroke_linecaps="round", stroke_dasharray=f"1,2")
			svg.append(squarre)


def main():
	# First and last column
	create_column(10, 1)
	create_column(100, -1)

	nice_shape = [Point2D(10, 20), Point2D(-10, 20), Point2D(-20, 10), Point2D(-20, -10), Point2D(-10, -20),
	              Point2D(10, -20), Point2D(20, -10), Point2D(20, 10)]

	p1_offset = Point2D(center.x, position_offset + 5)
	p1_start = [el + p1_offset for el in nice_shape]
	p1_end = [el + p1_offset for el in [Point2D(0, 10), Point2D(-10, -10), Point2D(10, -10)]]
	p1 = Polygon(p1_start)
	p1.add_modification(seconds * fps, values=p1_end)

	p2 = Rectangle(Point2D(center.x - 30, center.y - 10), 60, 20)
	p2.add_modification(seconds * fps, values=[center - Point2D(10, 10),
	                                           center - Point2D(2, 0),
	                                           center - Point2D(10, -10),
	                                           center - Point2D(-10, -10),
	                                           center - Point2D(-2, 0),
	                                           center - Point2D(-10, 10)])

	p3_offset = Point2D(center.x, height - position_offset - 5)
	p3_start = [el + p3_offset for el in nice_shape]
	p3_end = [el + p3_offset for el in [Point2D(0, -10), Point2D(-10, 10), Point2D(10, 10)]]
	p3 = Polygon(p3_start)
	p3.add_modification(seconds * fps, values=p3_end)

	svg.append(p1, p2, p3)

	video = Video(svg, fps=fps, width=width*5, height=height*5)
	print(svg.display_animations())
	video.save_movie(name="polygon", end=seconds + 1, ext="gif")


if __name__ == '__main__':
	main()
