"""
Test EllipseArc of SVGVideoMaker
"""

# region Imports
from SVGVideoMaker.geo.animation import AnimationType
from SVGVideoMaker.geo.arc import EllipseArc
from SVGVideoMaker.geo import Point2D, SVG
from SVGVideoMaker.video import Video
# endregion Imports

# Global values
fps = 15
seconds = 5
position_offset = 20
angle_offset = 45
width, height = 110, 180
center = Point2D(width // 2, height // 2)
full_turn = 360

svg = SVG()
svg.set_view_box(Point2D(0, 0), Point2D(width, height))

def create_column(colum, sens):
	stroke_incrementer = 0.2
	for i in range(height // position_offset):
		start_angle = 90 + angle_offset * i if sens == 1 else 0 - angle_offset * i
		end_angle = 180 + angle_offset * i if sens == 1 else 90 - angle_offset * i
		# Give the center point of each ellipse and his radius (rx, ry) with a point
		# After that you can give the part of circle to draw (in degrees) like on trigonometric circle
		arc = EllipseArc(center=Point2D(colum, i * position_offset + int(position_offset / 2)),
		                 radius=Point2D(8, 8),
		                 start_angle=start_angle, end_angle=end_angle)
		arc.animations.add_animation(seconds * fps, sens * full_turn, AnimationType.ANGLES)

		stroke_incrementer *= 1.5 if i <= 4 else 0.5
		arc.set_style(stroke_color="black", stroke_width=1 + stroke_incrementer, stroke_linecaps="round")

		svg.append(arc)


def main():
	# First and last column
	create_column(10, 1)
	create_column(100, -1)

	# Fill center ellipse
	ellipse_top = EllipseArc(Point2D(width // 2, position_offset // 2), Point2D(20, 5), 0, 180)
	ellipse_top.animations.add_animation(seconds * fps, full_turn, AnimationType.ANGLES)

	ellipse_top_mid = EllipseArc(Point2D(width // 2, height // 2 - height // 4), Point2D(5, 10), 135, 405)
	ellipse_top_mid.animations.add_animation(seconds * fps, full_turn, AnimationType.ANGLES)

	ellipse_bottom = EllipseArc(Point2D(width // 2, height - position_offset // 2), Point2D(20, 5), 180, 360)
	ellipse_bottom.animations.add_animation(seconds * fps, full_turn, AnimationType.ANGLES)

	ellipse_bottom_mid = EllipseArc(Point2D(width // 2, height // 2 + height // 4), Point2D(5, 10), 315, 585)
	ellipse_bottom_mid.animations.add_animation(seconds * fps, full_turn, AnimationType.ANGLES)

	ellipse_center = EllipseArc(center, Point2D(30, 20), 180, 0)
	ellipse_center.animations.add_animation(seconds * fps, full_turn, AnimationType.ANGLES)

	ellipse_center_center = EllipseArc(center, Point2D(10, 20), 0, 180)
	ellipse_center_center.animations.add_animation(seconds * fps, full_turn, AnimationType.ANGLES)

	svg.append(ellipse_top, ellipse_top_mid, ellipse_bottom, ellipse_bottom_mid,
	           ellipse_center, ellipse_center_center)

	for element in svg:
		element.animations.add_animation((seconds * 1) * fps, 1, AnimationType.OPACITY)
		element.animations.add_animation((seconds * 2) * fps, 0, AnimationType.OPACITY)
		element.animations.add_animation((seconds * 3) * fps, 1, AnimationType.OPACITY)

	video = Video(svg, fps=fps)
	print(svg.display_animations())
	video.save_movie(name="ellipse_arc", max_time=seconds * 3 + 1)


if __name__ == '__main__':
	main()
