*********
Changelog
*********

TODO
----

* SVG parser to give different svg picture to make a video.


Version 0.4.3, Patch & Parse
------------------------------------

:Date: July 0, 2020

Bug fixes and add a svg parser, *parse_svg* take a SVG file and convert to SVGVideoMaker

Bug Fix
=======
* SVG custom style
* Patch group animation
* Comment in some file
* Reset of animation

Version 0.4.2, Stroke Dash array
--------------------------------

:Date: July 02, 2020

Add stroke dash array

Version 0.4.1, Bug Fixes
------------------------

:Date: July 02, 2020

Bug Fixes Update

Bug Fixes
=========
* Exclude last frame of make_movie. Ex: 30 frames : 0 -> 30
* Update Rectangle to have a width and a height store and modification on internal structure
* Clean up some comments
* Patch creation of segment with segments() methods of polygon and change name to get_segments()
* Patch bug on hash of point

Version 0.4, Transform Update, Gradient
---------------------------------------

:Date: June 30, 2020

New animation with transform SVG ! And amazing Gradient !

Features
=======
* SVG Transform use for rotation and translation
* Implementation of gradient
* SVG background color can be change
* Simplification for add animation

Bug Fixes
=========
* Stroke-width who cant be set to 0
* Wait pipe to FFMPEG finish before kill program


Version 0.3, New Shape, EllipseArc and structure update
-------------------------------------------------------

:Date: June 25, 2020

New shape release, EllipseArc ! And simplify import.

Features
========
* Structure update, simplify everything with

.. code:: Python

    import SVGVideoMaker

* Implementations of a new shape, the EllipseArc. An ellipse where you can give what part to display from X degrees to Y degrees.
* New animation for EllipseArc, EllipseArcAnimation who support angles modification.
* Add new style attribute, stroke-linecaps
* Modification on animation structure

Bug Fixes
=========
* Fix bug who don't play animation if it's only on 1 frame.

Version 0.2.1, Intern structure update
--------------------------------------

:Date: June 6, 2020

Modification of intern structure and documentation.
Add Debug structure to have more information about shape (see more in debug.py).

Version 0.1, First Release
--------------------------

:Date: June 3, 2020

Description of all element of first version of SVGVideoMaker.

Features
========
* Implementation of various shape (circle, point, polygon...).
* Saving picture with cairosvg (png, svg).
* Displaying of picture in terminal.
* Animation
    * Translation (Movement).
    * Inflation (Size).
    * Reshape (Shape description specially for polygon).
* Saving video with ffmpeg.
