# Implementation Guillaume Raffin
# Make correspond to my SVGVideoMaker lib

# region Imports
import sys
from random import randint, seed as rand_seed, choice

from math import sqrt

from SVGVideoMaker.video import Video
from SVGVideoMaker.geo.animation import AnimationType
from SVGVideoMaker.geo.point import Point
from SVGVideoMaker.geo.polygon import Polygon
from SVGVideoMaker.geo.svg import SVG
# endregion Imports

class Vector(Point):
	"""
    2D vector.
    """

	def __init__(self, x: float, y: float):
		super().__init__([x, y])
		self.x = x
		self.y = y

	def copy(self) -> "Vector":
		"""Copies the vector"""
		return Vector(*self.coordinates)

	def distance_to(self, other):
		total = sum(((c1 - c2) ** 2 for c1, c2 in zip(self.coordinates, other.coordinates)))
		return abs(sqrt(total))

	def orthogonal(self):
		return Vector(-self.coordinates[1], self.coordinates[0])

	def __iter__(self):
		for coord in self.coordinates:
			yield coord

	def __add__(self, vec):
		return Vector(self.coordinates[0] + vec.coordinates[0], self.coordinates[1] + vec.coordinates[1])

	def __sub__(self, vec):
		return Vector(self.coordinates[0] - vec.coordinates[0], self.coordinates[1] - vec.coordinates[1])

	def __mul__(self, k):
		return Vector(self.coordinates[0] * k, self.coordinates[1] * k)

	def __truediv__(self, k):
		return Vector(self.coordinates[0] / k, self.coordinates[1] / k)

	def __neg__(self):
		return Vector(-self.coordinates[0], -self.coordinates[1])

	def __abs__(self):
		return Vector(abs(self.coordinates[0]), abs(self.coordinates[1]))

	def __eq__(self, other):
		return isinstance(other, Vector) \
		       and other.coordinates[0] == self.coordinates[0] \
		       and other.coordinates[1] == self.coordinates[1]

	def __ne__(self, other):
		return not isinstance(other, Vector) \
				or other.coordinates[0] != self.coordinates[0] \
			    or other.coordinates[1] != self.coordinates[1]

	def __hash__(self):
		return 31 * hash(self.coordinates[0]) + hash(self.coordinates[1])

	def __str__(self) -> str:
		return f"({self.coordinates})"

	def __repr__(self) -> str:
		return f"V({self.coordinates})"


marked = set()


class Agent:
	def __init__(self, position, forward_unit):
		self.position = position
		self.forward_vec = forward_unit

	def move(self, direction, new_position):
		self.forward_vec = direction
		self.position = new_position

	def forward(self):
		return self.forward_vec

	def backward(self):
		return -self.forward_vec

	def right(self):
		return self.forward_vec.orthogonal()

	def left(self):
		return -self.forward_vec.orthogonal()

	@staticmethod
	def cell_coords(pos):
		return Vector(int(pos.x), int(pos.y))


class Player:
	def __init__(self, id, pos, static):
		self.id = id
		self.position = pos
		self.spawn = pos
		self.static = static
		self.topleft = None
		self.parent = None
		self.parent_blacklist = set()
		self.boundaries = None

	def __str__(self):
		return f"Player({self.id})"


class GameMap:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.size = width * height
		self.grid = [None] * self.size
		self.players = []
		self.player_positions = set()

	def __getitem__(self, position):
		x, y = position
		return self.grid[y * self.width + x]

	def __setitem__(self, key, value):
		x, y = key
		self.grid[y * self.width + x] = value

	def random_position(self):
		idx = randint(0, self.size - 1)
		x, y = idx % self.width, idx // self.width
		return idx, Vector(x, y)

	def random_empty_position(self):
		idx, vec = self.random_position()
		while self.grid[idx] is not None:
			idx, vec = self.random_position()
		return idx, vec

	def neighbors8(self, pos):
		for i in range(-1, 2):
			for j in range(-1, 2):
				if i != 0 or j != 0:
					neighbor = pos + Vector(i, j)
					if not self.out_of_bounds(neighbor):
						yield neighbor, self[neighbor]

	def neighbors4(self, pos):
		v = Vector(0, -1)
		for _ in range(4):
			neighbor = pos + v
			if not self.out_of_bounds(neighbor):
				yield neighbor, self[neighbor]
			v = v.orthogonal()

	def out_of_bounds(self, vec):
		return not (0 <= vec.x < self.width) or not (0 <= vec.y < self.height)

	@staticmethod
	def random_direction():
		directions = [Vector(-1, 0), Vector(1, 0), Vector(0, -1), Vector(0, 1)]
		return choice(directions)

	def is_valid_move(self, player, v):
		src = player.position
		dst = src + v
		if self.out_of_bounds(dst):
			return False
		if self[dst] == player or self[dst] is None:
			return True
		if dst in self.player_positions:
			return False
		up = dst + v
		right = dst + v.orthogonal()
		left = dst - v.orthogonal()
		for cell, lim in [(dst, 2), (right, 2), (left, 2), (up, 2)]:
			if not self.out_of_bounds(cell):
				cell_owner = self[cell]
				if cell_owner is not None:
					neighbors_count = sum(1 for _, owner in self.neighbors4(cell) if owner == cell_owner)
					# print(neighbors_count, "for", dst)
					if neighbors_count <= lim:
						return False
		return True

	def move_player(self, player, vec):
		oldpos = player.position
		newpos = oldpos + vec
		self.player_positions.remove(oldpos)
		self.player_positions.add(newpos)
		self[newpos] = player
		player.position = newpos

	def play_turn(self):
		for player in self.players:
			if not player.static:
				v = GameMap.random_direction()
				i = 0
				while i < 4 and not self.is_valid_move(player, v):
					v = v.orthogonal()
					i += 1

				if i < 4:  # valid move found => play it
					self.move_player(player, v)
				# else : stay here!

	def spawn_player(self, player_id, static):
		idx, position = self.random_empty_position()
		if static:
			print("STATIC", player_id, file=sys.stderr)
		player = Player(player_id, position, static)
		self.grid[idx] = player
		self.players.append(player)
		self.player_positions.add(position)

	def compute_topleft_cells(self):
		for j in range(self.height):
			for i in range(self.width):
				pos = Vector(i, j)
				owner = self[pos]
				if owner is not None:
					if owner.topleft is None or owner.topleft.x > pos.x or owner.topleft.y > pos.y:
						owner.topleft = pos

	def compute_boundaries(self):
		self.compute_topleft_cells()
		for p in self.players:
			p.boundaries = self.territory_boundaries(p)
		for p in self.players:
			parent_id = -1 if ((p.parent is None) or (p.parent in p.parent_blacklist)) else p.parent.id
			yield Polygon(p.boundaries, id=parent_id)

	def territory_boundaries(self, player):
		# 1. On positionne l'agent pour qu'il soit contre le bord, avec le bord à sa gauche.
		start_pos = player.topleft
		if start_pos is None:
			self.compute_topleft_cells()
			start_pos = player.topleft

		agent = Agent(start_pos, Vector(1, 0))

		# 2. On suit le bord pour le détecter.

		# Position relative des bords du polygone, selon l'orientation de l'agent
		d = 0.49
		border_offsets = [
			[Vector(-d, d), Vector(-d, -d), Vector(d, -d), None],
			[Vector(-d, -d), Vector(d, -d), Vector(d, d), None],
			[Vector(d, -d), Vector(d, d), Vector(-d, d), None],
			[Vector(d, d), Vector(-d, d), Vector(-d, -d), None]
		]
		# Orientations possibles
		orientations = [Vector(0, -1), Vector(1, 0), Vector(0, 1), Vector(-1, 0)]
		# Mouvements par ordre de priorité.
		moves = [Agent.left, Agent.forward, Agent.right, Agent.backward]

		# Points générés
		points = []
		points_set = set()

		# Boucle de déplacement de l'agent
		not_initialized = object()
		potential_parent = not_initialized
		run = True
		marked.add(agent.position)  # DEBUG
		while run:
			# Déplace l'agent en essayant les mouvements dans l'ordre de priorité donné ci-avant.
			orientation = orientations.index(agent.forward_vec)
			for move_provider, border_offset in zip(moves, border_offsets[orientation]):
				move_vec = move_provider(agent)
				new_position = agent.position + move_vec
				if self.out_of_bounds(new_position) or self[new_position] != player:
					# Mur rencontré

					# Détection du parent: on en a un si à chaque fois l'obstacle est le même polygone (le parent)
					# ET s'il est présent tout autour.
					# Exemple où il n'y a pas de parent: battle-100-100-100-250-424242, polygones 13 et 35
					# Exemple où il y en a un: battle-100-100-1000-250-424242, polygones 480 et 660
					# (exemples sans la fonctionnalité "static")
					if self.out_of_bounds(new_position):
						potential_parent = None  # pas de parent si on touche le bord de la grille de jeu
					else:
						other = self[new_position]
						if other is not None:
							other.parent_blacklist.add(player)

						if potential_parent is not_initialized:
							potential_parent = other

						elif other != potential_parent:
							potential_parent = None

					if border_offset is None:
						# Seul le demi-tour est possible, on n'ajoute pas de point à la frontière
						break

					# Autre déplacement, on ajoute un point à la frontière
					point = agent.position + border_offset
					if points and point == points[0]:
						# On est revenu au point de départ => terminé
						run = False
						break

					assert point not in points_set, "bug!"
					points.append(point)
					points_set.add(point)
				else:
					# La voie est libre, on continue
					agent.move(move_vec, new_position)
					marked.add(agent.position)
					break

		if potential_parent is not_initialized:  # improbable mais pas forcément impossible...
			potential_parent = None
		player.parent = potential_parent
		return points

def run_agent_battle(grid_width, grid_height, players, n_static, turns, seed):
	# Initialisation du jeu
	rand_seed(seed)
	game = GameMap(grid_width, grid_height)
	assert players < game.size
	static_count = 0
	for p in range(players):
		static = static_count < n_static
		static_count += 1
		game.spawn_player(p, static)

	# Simulation des agents
	for t in range(turns):
		game.play_turn()
		yield game.compute_boundaries()

def main():
	width = 50
	height = 50
	svg = SVG()
	fps = 30
	turn_space = 5
	polygons = []

	# iter_on_battle = run_agent_battle(width, height, players=15, n_static=0, turns=650, seed=151984854)
	iter_on_battle = run_agent_battle(width, height, players=1, n_static=0, turns=100, seed=15)
	first_turn = next(iter_on_battle)

	for i, poly in enumerate(first_turn):
		polygons.append(poly)
		svg.append(poly)

	for i, turn in enumerate(iter_on_battle):
		for j, poly in enumerate(turn):
			if i % 100 == 40:
				polygons[j].animations.add_animation((i + 1) * turn_space, 0, AnimationType.OPACITY)
			if i % 100 == 90:
				polygons[j].animations.add_animation((i + 1) * turn_space, 1, AnimationType.OPACITY)

			polygons[j].animations.add_animation(round(i + 1) * turn_space, poly.points, AnimationType.MODIFICATION)

	for p in polygons:
		print(p.animations.display_animations())

	from SVGVideoMaker.geo import set_debug, DebugLevel
	set_debug(DebugLevel.VERBOSE)
	video = Video(svg, width=width * 15, height=height * 15, fps=fps)
	video.save_movie(name="The Game")
	# video.print_frame(50)
	# video.save_frame(50)
	# video.save_frame(350)
	print("End")


if __name__ == '__main__':
	main()
