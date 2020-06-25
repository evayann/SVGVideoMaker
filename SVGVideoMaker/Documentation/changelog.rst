*********
Changelog
*********

Version 0.3, New Shape, EllipseArc and structure update
=======================================================

:Date: June 25, 2020

New shape release, EllipseArc ! And simplify import.

Features
--------

* Structure update, simplify everything with

.. code:: Python

    import SVGVideoMaker

* Implementations of a new shape, the EllipseArc. An ellipse where you can give what part to display from X degrees to Y degrees.
* New animation for EllipseArc, EllipseArcAnimation who support angles modification.
* Add new style attribute, stroke-linecaps
* Modification on animation structure

Bug Fixes
---------

* Fix bug who don't play animation if it's only on 1 frame.

Version 0.2.1, Intern structure update
======================================

:Date: June 6, 2020

Modification of intern structure and documentation.
Add Debug structure to have more information about shape (see more in debug.py).

Version 0.1, First Release
==========================

:Date: June 3, 2020

Description of all element of first version of SVGVideoMaker.

Features
--------

* Implementation of various shape (circle, point, polygon...).
* Saving picture with cairosvg (png, svg).
* Displaying of picture in terminal.
* Animation :
    * Translation (Movement).
    * Inflation (Size).
    * Reshape (Shape description specially for polygon).
* Saving video with ffmpeg.

TODO
----

* SVG parser to give different svg picture to make a video.
* Remove some attributes of shape (like debug...).
* Add some shape (rectangle, square, cube...).
* Check parameters when add animation.
