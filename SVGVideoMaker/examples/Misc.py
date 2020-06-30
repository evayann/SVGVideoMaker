"""
Test different function of SVGVideoMaker
"""

# region Imports
from SVGVideoMaker.video import Video
from SVGVideoMaker.geo.animation import AnimationType
from SVGVideoMaker.geo.ellipse import Circle
from SVGVideoMaker.geo.svg import SVG
from SVGVideoMaker.geo.group import Group
from SVGVideoMaker.geo.polygon import Polygon
from SVGVideoMaker.geo.point import Point
from SVGVideoMaker.geo.point import Point2D
from SVGVideoMaker.geo import Arc
# endregion Imports


def main():

    # SVG with display
    fps = 5

    svg = SVG()
    svg.set_background_color("black")

    g = Group()
    arc = Arc(Point2D(50, 50), Point2D(0, 0), end=Point2D(250, 50))

    g.append(Polygon([Point([0, 0]), Point([0, 10]), Point([10, 10]), Point([10, 0])]),
          Point([75, 50]), Circle([50, 50], 25), arc)

    p = Point([-150, -150])
    square = Polygon.square(0, 10, 50)
    poly = Polygon([Point([0, 0]), Point([0, 50]), Point([50, 50]), Point([50, 0])])
    svg.append(g, p, Polygon([Point([0, 0]), Point([0, 50]), Point([50, 50]), Point([50, 0])]), square, poly)

    # Make animation
    video = Video(svg, fps=fps)

    # Add all animations
    p.add_translation(10 * fps, x=100, y=50)
    p.add_translation(20 * fps, x=100, y=50)
    p.animations.add_animation(10 * fps, AnimationType.INFLATION, value=30)

    g.add_animation(20 * fps, value=Point([100, 50]))

    square.add_translation(2 * fps, x=100, y=100)
    square.add_translation(4 * fps, 100, -100)
    square.add_translation(10 * fps, 100, 100)
    square.add_translation(11 * fps, -100, -100)
    square.add_translation(20 * fps, 100, 100)

    revert_triangle = [Point([0, 10]), Point([-10, -10]), Point([10, -10])]
    nice_shape = [Point([10, 20]), Point([-10, 20]), Point([-20, 10]), Point([-20, -10]), Point([-10, -20]), Point([10, -20]), Point([20, -10]), Point([20, 10])]

    poly.add_modification(1 * fps, [Point([-10, -10]), Point([-10, 10]), Point([10, 10]), Point([10, -10])])
    poly.add_modification(5 * fps, [Point([1, 1]), Point([1, 1]), Point([1, 1]), Point([1, 1])])

    poly.add_modification(10 * fps, revert_triangle)
    poly.add_modification(20 * fps, nice_shape)
    poly.add_modification(22 * fps, revert_triangle)
    poly.add_modification(round(22.5 * fps), nice_shape)
    poly.add_modification(23 * fps, revert_triangle)
    poly.add_modification(round(23.25 * fps), nice_shape)
    poly.add_modification(round(23.5 * fps), revert_triangle)
    poly.add_modification(24 * fps, nice_shape)
    poly.add_modification(round(24.1 * fps), revert_triangle)
    poly.add_modification(round(24.2 * fps), nice_shape)
    poly.add_modification(30 * fps, revert_triangle)

    poly.add_modification(22 * fps, revert_triangle)
    poly.add_modification(30 * fps, nice_shape)

    video.save_movie(name="my_out")


if __name__ == '__main__':
    main()
