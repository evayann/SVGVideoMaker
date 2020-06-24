"""
Test EllipseArc of SVGVideoMaker
"""

# region Imports
from geo.animation import AnimationType
from geo.arc import EllipseArc
from geo import Point2D, SVG
from video import Video
# endregion Imports


def main():

	fps = 30
	seconds = 5
	svg = SVG()

	arc1 = EllipseArc(Point2D(100, 40), Point2D(20, 20), 90, 180)
	arc1.animations.add_animation(seconds * fps, [0, 270], AnimationType.ANGLES)

	arc2 = EllipseArc(Point2D(100, 80), Point2D(30, 20), 0, 180)
	arc2.animations.add_animation(seconds * fps, [-90, 0], AnimationType.ANGLES)

	arc3 = EllipseArc(Point2D(100, 120), Point2D(30, 20), 0, 90)
	arc3.animations.add_animation(seconds * fps, [90, -90], AnimationType.ANGLES)

	arc4 = EllipseArc(Point2D(100, 160), Point2D(30, 20), 0, 270)
	arc4.animations.add_animation(seconds * fps, [-270, 0], AnimationType.ANGLES)

	arc5 = EllipseArc(Point2D(100, 200), Point2D(30, 20), -90, 90)
	arc5.animations.add_animation(seconds * fps, [90, -90], AnimationType.ANGLES)

	arc6 = EllipseArc(Point2D(100, 240), Point2D(30, 20), -180, -90)
	arc7 = EllipseArc(Point2D(100, 280), Point2D(30, 20), 45, 135)
	svg.append(Point2D(100, 0), arc1, arc2, arc3, arc4, arc5, arc6, arc7)

	video = Video(svg, fps=fps)
	video.save_movie(name="EllipseArc", max_time=seconds+1)

if __name__ == '__main__':
    main()
