from ..commands import is_command
from ..svg.tags import (EMBROIDERABLE_TAGS, SVG_IMAGE_TAG, SVG_PATH_TAG,
                        SVG_POLYLINE_TAG, SVG_TEXT_TAG)
from .auto_fill import AutoFill
from .clone import Clone, is_clone
from .element import EmbroideryElement
from .empty_d_object import EmptyDObject
from .fill import Fill
from .image import ImageObject
from .polyline import Polyline
from .satin_column import SatinColumn
from .stroke import Stroke
from .text import TextObject


def node_to_elements(node):  # noqa: C901
    if node.tag == SVG_POLYLINE_TAG:
        return [Polyline(node)]

    elif is_clone(node):
        return [Clone(node)]

    elif node.tag == SVG_PATH_TAG and not node.get('d', ''):
        return [EmptyDObject(node)]

    elif node.tag in EMBROIDERABLE_TAGS:
        element = EmbroideryElement(node)

        if element.get_boolean_param("satin_column") and element.get_style("stroke"):
            return [SatinColumn(node)]
        else:
            elements = []
            fill = element.get_style("fill", "#000000")
            if fill and not element.get_style('fill-opacity', 1) == "0":
                if element.get_boolean_param("auto_fill", True):
                    elements.append(AutoFill(node))
                else:
                    elements.append(Fill(node))
            if element.get_style("stroke") and not (fill and fill.startswith("url")):
                if not is_command(element.node):
                    elements.append(Stroke(node))
            if element.get_boolean_param("stroke_first", False):
                elements.reverse()
            return elements

    elif node.tag == SVG_IMAGE_TAG:
        return [ImageObject(node)]

    elif node.tag == SVG_TEXT_TAG:
        return [TextObject(node)]

    else:
        return []


def nodes_to_elements(nodes):
    elements = []
    for node in nodes:
        elements.extend(node_to_elements(node))

    return elements
