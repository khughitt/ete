import types
import signal

from PyQt4  import QtGui
from PyQt4  import QtCore
from qt4_gui import _GUI, _PropertiesDialog, _BasicNodeActions

import layouts
from ete_dev import Tree, PhyloTree, ClusterTree
from main import save
from qt4_render import _TreeScene, render, get_tree_img_map, init_tree_style

__all__ = ["show_tree", "render_tree"]

_QApp = None
GUI_TIMEOUT = None

def exit_gui(a,b):
    _QApp.exit(0)
    
def init_scene(t, layout, ts):
    global _QApp

    ts = init_tree_style(t, ts)
    if layout: 
        ts.layout_fn  = layout
        
    if not _QApp:
        _QApp = QtGui.QApplication(["ETE"])

    scene  = _TreeScene()
	#ts._scale = None
    return scene, ts

def show_tree(t, layout=None, tree_style=None, win_name=None):
    """ Interactively shows a tree."""
    scene, img = init_scene(t, layout, tree_style)
    tree_item, n2i, n2f = render(t, img)
    scene.init_values(t, img, n2i, n2f)

    tree_item.setParentItem(scene.master_item)
    scene.addItem(scene.master_item)
    
    mainapp = _GUI(scene)
    if win_name:
        mainapp.setObjectName(win_name)
        
    mainapp.show()
    mainapp.on_actionFit2tree_triggered()
    # Restore Ctrl-C behavior
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    if GUI_TIMEOUT is not None:
        signal.signal(signal.SIGALRM, exit_gui) 
        signal.alarm(GUI_TIMEOUT) 
   
    _QApp.exec_()
    
def render_tree(t, imgName, w=None, h=None, layout=None, 
                tree_style = None, header=None, units="px",
                dpi=90):
    """ Render tree image into a file."""
    global _QApp
    for nid, n in enumerate(t.traverse("preorder")):
        n.add_feature("_nid", nid)
    scene, img = init_scene(t, layout, tree_style)
    tree_item, n2i, n2f = render(t, img)

    scene.init_values(t, img, n2i, n2f)
    tree_item.setParentItem(scene.master_item)
    scene.master_item.setPos(0,0)
    scene.addItem(scene.master_item)
    if imgName == "%%inline":
        imgmap = save(scene, imgName, w=w, h=h, units=units, dpi=dpi)
    else:
        x_scale, y_scale = save(scene, imgName, w=w, h=h, units=units, dpi=dpi)
        imgmap = get_tree_img_map(n2i, x_scale, y_scale)
    _QApp.quit()
    _QApp = None
    return imgmap
    

def get_img(t, w=None, h=None, layout=None, tree_style = None,
            header=None, units="px", dpi=90):
    global _QApp
    scene, img = init_scene(t, layout, tree_style)
    tree_item, n2i, n2f = render(t, img)
    scene.init_values(t, img, n2i, n2f)
    
    tree_item.setParentItem(scene.master_item)
    scene.master_item.setPos(0,0)
    scene.addItem(scene.master_item)
    x_scale, y_scale, imgdata = save(scene, "%%return", w=w, h=h, units=units, dpi=dpi)
    _QApp.quit()
    _QApp = None
    return imgdata, {}

 



