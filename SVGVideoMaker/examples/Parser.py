from SVGVideoMaker import parse_svg, Video, Polygon

def main():
	fps = 30
	seconds = 5
	svg = parse_svg("./in.svg")
	svg_anim = parse_svg("./anim.svg")
	# Add modification with second svg
	for node, anim in zip(svg, svg_anim):
		if isinstance(node, Polygon):
			node.add_modification(fps * seconds, anim.points)

	width, height = svg.svg_dimensions
	video = Video(svg, width, height, fps=fps)
	video.save_movie(name="AnimFrom2SVG", ext="mp4")

if __name__ == '__main__':
	main()
