# Implementation from https://github.com/jansonh/Voronoi
# Update to compute animation

# region Imports
import heapq
from itertools import count
import math
from random import seed, randint
from SVGVideoMaker import Point2D as Point, Segment as S, Arc as A
from SVGVideoMaker import Video as Video, display
from SVGVideoMaker import SVG
from SVGVideoMaker import AnimationType
from SVGVideoMaker import Rectangle
# endregion Imports

class Segment:
	def __init__(self, y):
		self.start = y
		self.end = None
		self.done = False
		self.segment = None

	def compute_bound(self, seg):
		for pt in [seg.intersect_point(S(Point(0, 0), Point(width, 0))),
		           seg.intersect_point(S(Point(0, 0), Point(0, height))),
		           seg.intersect_point(S(Point(width, 0), Point(width, height))),
		           seg.intersect_point(S(Point(0, height), Point(width, height)))]:
			if pt:
				if not bounds.is_in(seg.endpoints[0]):
					seg.endpoints[0] = round(pt, 3)
				elif not bounds.is_in(seg.endpoints[1]): # movement endpoints[1]
					seg.endpoints[1] = round(pt, 3)

	def compute_segment(self):
		# Round and reorient segment
		self.start, self.end = round(self.start, 3), round(self.end, 3)
		seg = S(self.start, self.end) if self.start < self.end else S(self.end, self.start)

		# Crop segment to map to size
		self.compute_bound(seg)
		start_frame = int(seg.endpoints[0].x / speed)
		end_frame = int(seg.endpoints[1].x / speed)

		if start_frame != end_frame:
			# Draw segment by inflation
			segment = S(seg.endpoints[0], seg.endpoints[0])
			segment.set_style(stroke_color="blue")
			segment.animations.add_animation(start_frame, Point(0, 0), AnimationType.INFLATION)

			movement = seg.endpoints[1] - seg.endpoints[0]
			segment.animations.add_animation(end_frame, movement, AnimationType.INFLATION)

			if bounds.is_in(segment.endpoints[0]) and bounds.is_in(segment.endpoints[1]):
				global last_frame
				last_frame = max(last_frame, end_frame)
		else:
			# Draw segment by pop
			segment = S(seg.endpoints[0], seg.endpoints[1], opacity=0)
			segment.set_style(stroke_color="blue")
			segment.animations.add_animation(start_frame - 1 if start_frame > 0 else 0, 0, AnimationType.OPACITY)
			segment.animations.add_animation(end_frame, 1, AnimationType.OPACITY)

		self.segment = segment

	def set_end(self, end, is_finish):
		self.end = end
		self.done = is_finish
		self.compute_segment()

	def finish(self, p):
		if self.done:
			return
		self.set_end(p, True)

	def get_segment(self):
		return self.segment

class Event:
	def __init__(self, x, p, a):
		self.x = x
		self.p = p
		self.a = a
		self.valid = True

class Arc(A):
	def __init__(self, p, a=None, b=None):
		super().__init__(0, 0, 0)
		self.p = p
		self.pprev = a
		self.pnext = b
		self.e = None
		self.s0 = None
		self.s1 = None

class PriorityQueue:
	def __init__(self):
		self.pq = []
		self.entry_finder = {}
		self.counter = count()

	def push(self, item):
		# check for duplicate
		if item in self.entry_finder:
			return
		# use x-coordinate as a primary key (heapq in python is min-heap)
		entry = [item.x, next(self.counter), item]
		self.entry_finder[item] = entry
		heapq.heappush(self.pq, entry)

	def remove_entry(self, item):
		entry = self.entry_finder.pop(item)
		entry[-1] = 'Removed'

	def pop(self):
		while self.pq:
			_, _, item = heapq.heappop(self.pq)
			if item != 'Removed':
				del self.entry_finder[item]
				return item
		raise KeyError('pop from an empty priority queue')

	def top(self):
		while self.pq:
			_, _, item = heapq.heappop(self.pq)
			if item != 'Removed':
				del self.entry_finder[item]
				self.push(item)
				return item
		raise KeyError('top from an empty priority queue')

	def empty(self):
		return not self.pq

class Line:
	def __init__(self):
		self.line = S(Point(0, 0), Point(0, height), id="Defilement Line")
		self.line.set_style(stroke_color="red")
		self.previous_x_line = 0

	def compute_line(self, frame, x):
		# Add animation only if line move from his previous position
		if width >= x > self.previous_x_line:
			self.line.animations.add_animation(frame, Point(x - self.previous_x_line, 0))
			self.previous_x_line = x

	def get_line(self):
		return self.line

class Voronoi:
	def __init__(self, points):
		self.output = []  # list of line segment
		self.arc = None  # binary tree for parabola arcs

		# Display
		self.segments_outputs = []  # list of animate segment

		self.points = PriorityQueue()  # site events
		self.event = PriorityQueue()  # circle events

		# bounding box
		self.x0 = -50.0
		self.x1 = -50.0
		self.y0 = 550.0
		self.y1 = 550.0

		# insert points to site event
		for point in points:
			self.points.push(point)
			# keep track of bounding box size
			if point.x < self.x0:
				self.x0 = point.x
			if point.y < self.y0:
				self.y0 = point.y
			if point.x > self.x1:
				self.x1 = point.x
			if point.y > self.y1:
				self.y1 = point.y

		# add margins to the bounding box
		dx = (self.x1 - self.x0 + 1) / 5.0
		dy = (self.y1 - self.y0 + 1) / 5.0
		self.x0 = self.x0 - dx
		self.x1 = self.x1 + dx
		self.y0 = self.y0 - dy
		self.y1 = self.y1 + dy

	def process(self):
		while not self.points.empty():
			if not self.event.empty() and (self.event.top().x <= self.points.top().x):
				self.process_event()  # handle circle event

			else:
				self.process_point()  # handle site event

		# after all points, process remaining circle events
		while not self.event.empty():
			self.process_event()

		self.finish_edges()
		line.compute_line(last_frame, width)
		# Add an extra translation to make disappear the bar
		line.line.animations.add_animation(last_frame + fps, Point(20, 0))

	def process_point(self):
		# get next event from site pq
		p = self.points.pop()
		# add new arc (parabola)
		self.arc_insert(p)

	def process_event(self):
		# get next event from circle pq
		e = self.event.pop()

		if e.valid:
			# start new edge
			s = Segment(e.p)
			self.output.append(s)

			# remove associated arc (parabola)
			a = e.a
			if a.pprev is not None:
				a.pprev.pnext = a.pnext
				a.pprev.s1 = s
			if a.pnext is not None:
				a.pnext.pprev = a.pprev
				a.pnext.s0 = s

			# finish the edges before and after a
			if a.s0 is not None:
				a.s0.finish(e.p)
			if a.s1 is not None:
				a.s1.finish(e.p)

			# recheck circle events on either side of p
			if a.pprev is not None:
				self.check_circle_event(a.pprev)
			if a.pnext is not None:
				self.check_circle_event(a.pnext)

	def arc_insert(self, p):
		if self.arc is None:
			self.arc = Arc(p)
			# self.arcs_output.append(A(None, None, None))
		else:
			# find the current arcs at p.y
			i = self.arc
			while i is not None:
				flag, z = self.intersect(p, i)
				if flag:
					# new parabola intersects arc i
					flag, zz = self.intersect(p, i.pnext)
					if (i.pnext is not None) and (not flag):
						i.pnext.pprev = Arc(i.p, i, i.pnext)
						i.pnext = i.pnext.pprev
					else:
						i.pnext = Arc(i.p, i)
					i.pnext.s1 = i.s1

					# add p between i and i.pnext
					i.pnext.pprev = Arc(p, i, i.pnext)
					i.pnext = i.pnext.pprev

					i = i.pnext  # now i points to the new arc

					# add new half-edges connected to i's endpoints
					seg = Segment(z)
					self.output.append(seg)
					i.pprev.s1 = i.s0 = seg

					seg = Segment(z)
					self.output.append(seg)
					i.pnext.s0 = i.s1 = seg

					# check for new circle events around the new arc
					self.check_circle_event(i)
					self.check_circle_event(i.pprev)
					self.check_circle_event(i.pnext)

					return

				i = i.pnext

			# if p never intersects an arc, append it to the list
			i = self.arc
			while i.pnext is not None:
				i = i.pnext
			i.pnext = Arc(p, i)

			# insert new segment between p and i
			x = self.x0
			y = (i.pnext.p.y + i.p.y) / 2.0
			start = Point(x, y)

			seg = Segment(start)
			i.s1 = i.pnext.s0 = seg
			self.output.append(seg)

	def check_circle_event(self, i):
		# look for a new circle event for arc i
		if (i.e is not None) and (i.e.x != self.x0):
			i.e.valid = False
		i.e = None

		if (i.pprev is None) or (i.pnext is None):
			return

		flag, x, o = self.circle(i.pprev.p, i.p, i.pnext.p)
		if flag and (x > self.x0):
			i.e = Event(x, o, i)
			self.event.push(i.e)

	def circle(self, a, b, c):
		# check if bc is a "right turn" from ab
		if ((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)) > 0:
			return False, None, None

		# Joseph O'Rourke, Computational Geometry in C (2nd ed.) p.189
		A = b.x - a.x
		B = b.y - a.y
		C = c.x - a.x
		D = c.y - a.y
		E = A * (a.x + b.x) + B * (a.y + b.y)
		F = C * (a.x + c.x) + D * (a.y + c.y)
		G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))

		if G == 0:
			return False, None, None  # Points are co-linear

		# point o is the center of the circle
		ox = 1.0 * (D * E - B * F) / G
		oy = 1.0 * (A * F - C * E) / G

		# o.x plus radius equals max x coord
		x = ox + math.sqrt((a.x - ox) ** 2 + (a.y - oy) ** 2)
		o = Point(ox, oy)

		return True, x, o

	def intersect(self, p, i):
		# check whether a new parabola at point p intersect with arc i
		if i is None:
			return False, None
		if i.p.x == p.x:
			return False, None

		a = 0.0
		b = 0.0

		if i.pprev is not None:
			a = (self.intersection(i.pprev.p, i.p, 1.0 * p.x)).y
		if i.pnext is not None:
			b = (self.intersection(i.p, i.pnext.p, 1.0 * p.x)).y

		if ((i.pprev is None) or (a <= p.y)) and ((i.pnext is None) or (p.y <= b)):
			py = p.y
			px = 1.0 * (i.p.x ** 2 + (i.p.y - py) ** 2 - p.x ** 2) / (2 * i.p.x - 2 * p.x)
			res = Point(px, py)
			return True, res
		return False, None

	def intersection(self, p0, p1, l):
		# get the intersection of two parabolas
		p = p0
		if p0.x == p1.x:
			py = (p0.y + p1.y) / 2.0
		elif p1.x == l:
			py = p1.y
		elif p0.x == l:
			py = p0.y
			p = p1
		else:
			# use quadratic formula
			z0 = 2.0 * (p0.x - l)
			z1 = 2.0 * (p1.x - l)

			a = 1.0 / z0 - 1.0 / z1
			b = -2.0 * (p0.y / z0 - p1.y / z1)
			c = 1.0 * (p0.y ** 2 + p0.x ** 2 - l ** 2) / z0 - 1.0 * (p1.y ** 2 + p1.x ** 2 - l ** 2) / z1

			py = 1.0 * (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)

		px = 1.0 * (p.x ** 2 + (p.y - py) ** 2 - l ** 2) / (2 * p.x - 2 * l)
		return Point(px, py)

	def finish_edges(self):
		l = self.x1 + (self.x1 - self.x0) + (self.y1 - self.y0)
		i = self.arc
		while i.pnext is not None:
			if i.s1 is not None:
				p = self.intersection(i.p, i.pnext.p, l * 2.0)
				i.s1.finish(p)
			i = i.pnext

	def get_output(self):
		return self.output

	def get_segment(self):
		return [S(Point(o.start.x, o.start.y), Point(o.end.x, o.end.y)) for o in self.output]


fps, width, height = 30, 500, 500
speed = 2
bounds = Rectangle(Point(0, 0), width, height)
line = Line()
last_frame = -1

def main():
	seed(1)
	nb_points = 250
	points = []
	for _ in range(nb_points):
		points.append(Point(randint(0, width), randint(0, height)))

	# points = [Point(10, 50), Point(75, 10), Point(150, 50), Point(40, 100), Point(25, 34), Point(450, 300),
	#           Point(15, 400), Point(65, 480), Point(350, 150), Point(450, 450), Point(250, 205), Point(250, 250),
	#           Point(200, 150), Point(310, 210), Point(410, 150)]
	# points = [Point(10, 10), Point(20, 10), Point(10, 20)]
	# points = [Point(10, 50), Point(75, 10), Point(150, 50), Point(40, 100), Point(25, 34)]
	# points = [Point(10, 10), Point(200, 200), Point(300, 100)]
	# points = [Point(10, 10), Point(480, 480)]
	vp = Voronoi(points)
	vp.process()

	alls = [p for p in points]

	alls.append(line.get_line())

	for out in vp.get_output():
		segment = out.get_segment()
		if bounds.is_in(segment.endpoints[0]) and bounds.is_in(segment.endpoints[1]):
			alls.append(segment)

	svg = SVG(width=width, height=height, elements=alls)
	svg.set_view_box(Point(0, 0), Point(width, height))

	display(svg, ext="png")
	video = Video(svg, fps=fps)
	video.save_movie()

if __name__ == '__main__':
	main()
