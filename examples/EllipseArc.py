"""
Test EllipseArc of SVGVideoMaker
"""

# region Imports
from geo.animation import AnimationType
from geo.arc import EllipseArc
from geo import Point2D, SVG
from video import Video
# endregion Imports

# Global values
fps = 15
seconds = 5
position_offset = 20
angle_offset = 45
svg = SVG()
svg.set_view_box(Point2D(0, 0), Point2D(110, 180))

def create_column(colum, sens):
	stroke_incrementer = 0.2
	for i in range(9):
		start_angle = 90 + angle_offset * i if sens == 1 else 0 - angle_offset * i
		end_angle = 180 + angle_offset * i if sens == 1 else 90 - angle_offset * i
		arc = EllipseArc(center=Point2D(colum, i * position_offset + int(position_offset / 2)),
		                 radius=Point2D(8, 8),
		                 start_angle=start_angle, end_angle=end_angle)
		arc.animations.add_animation(seconds * fps, sens * 360, AnimationType.ROTATE)

		stroke_incrementer *= 1.5 if i <= 4 else 0.5
		arc.style.set(stroke_color="black", stroke_width=1 + stroke_incrementer, stroke_linecaps="round")

		svg.append(arc)


def main():

	# Give the center point of each ellipse and his radius (rx, ry) with a point
	# After that you can give the part of circle to draw (in degrees) like on trigonometric circle

	# arc1 = EllipseArc(center=Point2D(0, 10), radius=Point2D(8, 8), start_angle=90, end_angle=180)
	# arc1.animations.add_animation(seconds * fps, [0, 270], AnimationType.ANGLES)
	# arc1.style.set(stroke_width=1, stroke_color="green")
	#
	# arc2 = EllipseArc(Point2D(0, 30), Point2D(8, 8), 90, 180 + angle_offset)
	# arc2.animations.add_animation(seconds * fps, [-90, 0], AnimationType.ANGLES)
	# arc2.style.set(stroke_width=1.5)
	#
	# arc3 = EllipseArc(Point2D(0, 50), Point2D(8, 8), 100, 190)
	# arc3.animations.add_animation(seconds * fps, [90, -90], AnimationType.ANGLES)
	# arc3.style.set(stroke_width=2)
	#
	# arc4 = EllipseArc(Point2D(0, 70), Point2D(8, 8), 105, 195)
	# arc4.animations.add_animation(seconds * fps, [-270, 0], AnimationType.ANGLES)
	# arc4.style.set(stroke_width=1.5)
	#
	# arc5 = EllipseArc(Point2D(0, 90), Point2D(8, 8), 110, 200)
	# arc5.animations.add_animation(seconds * fps, [90, -90], AnimationType.ANGLES)
	# arc5.style.set(stroke_width=1)

	# First and last column
	create_column(10, 1)
	create_column(100, -1)

	# arc6 = EllipseArc(Point2D(100, 50), Point2D(8, 8), -180, -90)
	#
	# arc7 = EllipseArc(Point2D(0, 100), Point2D(8, 8), 45, 390)
	# arc7.animations.add_animation(seconds * fps, [390, 45], AnimationType.ANGLES)
	#
	# arc8 = EllipseArc(Point2D(50, 100), Point2D(8, 8), 45, 390)
	# arc8.animations.add_animation(seconds * fps, [390, 45], AnimationType.ANGLES)
	#
	# arc9 = EllipseArc(Point2D(100, 100), Point2D(8, 8), 45, 390)
	# arc9.animations.add_animation(seconds * fps, [390, 45], AnimationType.ANGLES)
	# svg.append(arc1, arc2, arc3, arc4, arc5, arc6, arc7, arc8, arc9)
	# svg.append(arc7)

	video = Video(svg, fps=fps)
	video.save_movie(name="EllipseArc", max_time=seconds+1)

if __name__ == '__main__':
    main()
