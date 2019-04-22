from nbparse.parser import Parser
parser = Parser()
parser.get_notebooks()
parser.format_math()
parser.format_javascript()
parser.format_image_links()
parser.nb2md(include_front_matter=True)