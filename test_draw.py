import sys

from ete_dev import Tree, faces
from ete_dev.treeview.main import TreeImage, NodeStyleDict
import colorsys
import random

def random_color(h=None):
    if not h:
        h = random.random()
    s = 0.5
    l = 0.5+random.random()/2
    return hls2hex(h, l, s)

def rgb2hex(rgb):
    return '#%02x%02x%02x' % rgb

def hls2hex(h, l, s):
    return rgb2hex( tuple(map(lambda x: int(x*255), colorsys.hls_to_rgb(h, l, s))))

def ly(node):
    node.img_style["size"] = 4
    node.img_style["shape"] = "square"
    
    node.img_style["bgcolor"] = random_color()
    #node.img_style["node_bgcolor"] = random_color()
    #node.img_style["faces_bgcolor"] = random_color()

    if node.is_leaf():
        #faces.add_face_to_node(faces.AttrFace("name"), node, 0, position="aligned")
        faces.add_face_to_node(faces.AttrFace("name"), node, 0, position="branch-right")
        #faces.add_face_to_node(faces.AttrFace("support", fsize=6), node, 0, position="branch-top")

    else:
        FLOAT = faces.CircleFace(random.randint(5,40), random_color(), "sphere")
        FLOAT.opacity = 0.4
        faces.add_face_to_node(FLOAT, node, 0, position="float")

def tiny(node):
    node.img_style["size"] = 7
    node.img_style["shape"] = "circle"
    node.img_style["fgcolor"] = random_color()
    if node.is_leaf():
        faces.add_face_to_node(faces.AttrFace("name"), node, 0, position="branch-right")


n = int(sys.argv[1])

I = TreeImage()
I.mode = "rect"
I.scale = n/2
I.layout_fn = ly

t2 = Tree()
t2.populate(10)
I2 = TreeImage()
I2.scale=1
I2.mode = "circular"
I2.layout_fn = tiny
I2.arc_start = 45
I2.arc_span = 360

t = Tree()
t.populate(n)

style = NodeStyleDict()
style.add_fixed_face(faces.TreeFace(t2, I2), "branch-right", 0)
t.children[1].children[0].img_style = style 


t.show(img_properties=I)

I.mode = "circular"
I2.mode = "rect"
t.render("test.png", img_properties=I)
t.show(ly, img_properties=I)
