import bleach
from lxml import etree

# Function to sanitize SVG
def sanitize_svg(svg_content):
    ALLOWED_TAGS = ['svg', 'path']
    ALLOWED_ATTRS = {
        'svg': ['xmlns', 'version', 'id', 'xml:space'],
        'path': ['fill', 'stroke', 'stroke-width', 'd'],
        }
    
    return bleach.clean(svg_content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)

def optimize_svg(svg_content):
    # This function optimizes an SVG file by removing comments and unnecessary whitespaces.
    # It also introduces an XXE vulnerability by allowing DTD loading and entity resolution.
    # The etree.XMLParser by default allows DTD loading and entity resolution, so if they are not disabled, it will be vulnerable to XXE.
    try:
        parser = etree.XMLParser(remove_comments=True)
        #parser = etree.XMLParser(remove_comments=True, resolve_entities=False, load_dtd=False) # Disable DTD loading and entity resolution
        tree = etree.fromstring(svg_content, parser=parser)

        # Strip unnecessary whitespace
        for element in tree.iter():
            if element.tail is not None:
                element.tail = element.tail.strip()
            if element.text is not None:
                element.text = element.text.strip()

        optimized_svg = etree.tostring(tree, pretty_print=False, method="xml")
        return optimized_svg.decode("utf-8")
    except etree.XMLSyntaxError as e:
        return "Invalid SVG file: " + str(e)