
"""
Test different function of SVGVideoMaker
"""

# region Imports
from video import Video
from geo.animation import AnimationType
from geo.circle import Circle
from geo.svg import SVG
from geo.group import Group
from geo.polygon import Polygon
from geo.point import Point
from geo.point import Point2D
from geo import Arc
# endregion Imports


def main():

    # SVG with display
    fps = 5

    svg = SVG()

    g = Group()
    arc = Arc(Point2D(50, 50), Point2D(0, 0), Point2D(150, 50))
    g.append(Polygon([Point([0, 0]), Point([0, 10]), Point([10, 10]), Point([10, 0])]),
          Point([75, 50]), Circle([50, 50], 25), arc)

    p = Point([-150, -150])
    square = Polygon.square(0, 10, 50)

    svg.append(g, p, Polygon([Point([0, 0]), Point([0, 50]), Point([50, 50]), Point([50, 0])]), square)

    poly = Polygon([Point([0, 0]), Point([0, 50]), Point([50, 50]), Point([50, 0])])

    pautre = Polygon([Point([35.1,16.51]),
                     Point([35.1,16.51]),
                     Point([45.1,16.51]),
                     Point([54.9,16.51]),
                     Point([54.9,17.49]),
                     Point([44.9,17.49]),
                     Point([35.1,17.49]),
                     Point([35.1,17.49])
                     ])

    svg.append(poly)
    svg.append(pautre)

    # Make animation
    video = Video(svg, fps=fps)

    # Add all animations
    p.animations.add_animation_by_frame(10 * fps, Point([100, 50]))
    p.animations.add_animation_by_frame(20 * fps, Point([100, 50]))
    p.animations.add_animation_by_frame(10 * fps, 30, AnimationType.INFLATION)
    pautre.animations.add_animation_by_frame(50 * fps, 0, AnimationType.DISPLAY)

    g.add_animation_by_frame(20 * fps, Point([100, 50]))

    square.animations.add_animation_by_frame(2 * fps, Point([100, 100]))
    square.animations.add_animation_by_frame(4 * fps, Point([-100, -100]))
    square.animations.add_animation_by_frame(10 * fps, Point([100, 100]))
    square.animations.add_animation_by_frame(11 * fps, Point([-100, -100]))
    square.animations.add_animation_by_frame(20 * fps, Point([100, 100]))

    poly.animations.add_animation_by_frame(1 * fps,
                       [Point([-10, -10]), Point([-10, 10]), Point([10, 10]), Point([10, -10])],
                       AnimationType.MODIFICATION
                       )

    poly.animations.add_animation_by_frame(5 * fps,
                       [Point([1, 1]), Point([1, 1]), Point([1, 1]), Point([1, 1])],
                       AnimationType.MODIFICATION
                       )

    revert_triangle = [Point([0, 10]), Point([-10, -10]), Point([10, -10])]
    poly.animations.add_animation_by_frame(10 * fps,
                       revert_triangle,
                       AnimationType.MODIFICATION
                       )

    nice_shape = [Point([10, 20]), Point([-10, 20]), Point([-20, 10]), Point([-20, -10]), Point([-10, -20]), Point([10, -20]), Point([20, -10]), Point([20, 10])]
    poly.animations.add_animation_by_frame(20 * fps,
                       nice_shape,
                       AnimationType.MODIFICATION
                       )
    poly.animations.add_animation_by_frame(22 * fps, revert_triangle, AnimationType.MODIFICATION)
    poly.animations.add_animation_by_frame(round(22.5 * fps), nice_shape, AnimationType.MODIFICATION)
    poly.animations.add_animation_by_frame(23 * fps, revert_triangle, AnimationType.MODIFICATION)
    poly.animations.add_animation_by_frame(round(23.25 * fps), nice_shape, AnimationType.MODIFICATION)
    poly.animations.add_animation_by_frame(round(23.5 * fps), revert_triangle, AnimationType.MODIFICATION)
    poly.animations.add_animation_by_frame(24 * fps, nice_shape, AnimationType.MODIFICATION)
    poly.animations.add_animation_by_frame(round(24.1 * fps), revert_triangle, AnimationType.MODIFICATION)
    poly.animations.add_animation_by_frame(round(24.2 * fps), nice_shape, AnimationType.MODIFICATION)
    poly.animations.add_animation_by_frame(30 * fps, revert_triangle, AnimationType.MODIFICATION)

    poly.animations.add_animation_by_frame(22 * fps, revert_triangle, AnimationType.MODIFICATION)
    poly.animations.add_animation_by_frame(30 * fps, nice_shape, AnimationType.MODIFICATION)

    pautre.animations.add_animation_by_frame(5 * fps, [
        Point([25.1, 16.51]),
        Point([35.1, 16.51]),
        Point([45.1, 16.51]),
        Point([54.9, 16.51]),
        Point([54.9, 17.49]),
        Point([44.9, 17.49]),
        Point([34.9, 17.49]),
        Point([25.1, 17.49])
    ], AnimationType.MODIFICATION)

    pautre.animations.add_animation_by_frame(10 * fps, [
        Point([25.1, 16.51]),
        Point([35.1, 16.51]),
        Point([35.1, 16.51]),
        Point([45.1, 16.51]),
        Point([45.1, 16.51]),
        Point([54.9, 16.51]),
        Point([54.9, 17.49]),
        Point([44.9, 17.49]),
        Point([34.9, 17.49]),
        Point([25.1, 17.49])
    ], AnimationType.MODIFICATION)

    pautre.animations.add_animation_by_frame(15 * fps, [
        Point([25.1, 16.51]),
        Point([35.1, 16.49]),
        Point([35.1, 15.51]),
        Point([44.9, 15.51]),
        Point([45.1, 16.51]),
        Point([54.9, 16.51]),
        Point([54.9, 17.49]),
        Point([44.9, 17.49]),
        Point([34.9, 17.49]),
        Point([25.1, 17.49])
    ], AnimationType.MODIFICATION)

    arc.animations.add_animation_by_frame(50 * fps, Point2D(-250, -250))
    arc.animations.add_animation_by_frame(60 * fps, Point2D(50, 50))
    print(poly.animations.display_animations())
    print(arc.animations.display_animations())
    video.save_movie(name="my_out", max_time=70)


if __name__ == '__main__':
    main()
