"""
Test Gradient of SVGVideoMaker
"""

# region Imports
from SVGVideoMaker import Circle, Rectangle, Point2D, SVG, save
# endregion Imports


def main():
	# Global values
	width, height = 500, 500

	svg = SVG(width=width, height=height)
	svg.set_view_box(Point2D(0, 0), Point2D(width, height))

	rect1 = Rectangle(Point2D(5, 5), 225, 225)
	id_g1 = "Gradient1_ID"
	svg.add_gradient(id_g1, offsets=[0, 25, 50, 100], colors=["red", "blue", "green", "purple"], opacities=[1, 1, 1, 1])
	rect1.set_style(fill_color=f"url(#{id_g1})", stroke_width=0)

	rect2 = Rectangle(Point2D(262, 262), 225, 225)
	rect2.set_style(fill_color=f"red", stroke_color="black", stroke_width=10)

	circle1 = Circle(Point2D(375, 137), 112)
	id_g3 = "Gradient3_ID"
	svg.add_gradient(id_g3, [0, 50, 100], ["red", "green", "blue"], [0, 1, 0],
	                 orientation_start=(0, 0), orientation_end=(0, 1))
	circle1.set_style(fill_color=f"url(#{id_g3})", stroke_width=0)

	circle2 = Circle(Point2D(137, 375), 112)
	id_g4 = "Gradient4_ID"
	svg.add_gradient(id_g4, [0, 75, 100], ["red", "#1A2B3C", "rgb(0, 255, 200)"], [0.5, 1, 1], (0, 0), (1, 1))
	circle2.set_style(fill_color=f"url(#{id_g4})", stroke_width=0)

	svg.append(rect1, rect2, circle1, circle2)

	save(svg.get_svg(), path="./color", ext="png")


if __name__ == '__main__':
	main()
