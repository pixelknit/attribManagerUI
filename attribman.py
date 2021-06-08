import hou
from hutil.Qt import QtCore, QtUiTools, QtWidgets
import os

scriptpath = os.path.dirname(__file__)

class AttribManager(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        #set window size
        self.setMinimumSize(1200, 600)
        
        #laod ui
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(scriptpath + '/attribman.ui')

        #set label
        self.ui.node_lbl.setText("Node: " + self.sel_node().name())
        self.sel_node()

        #get geo attribs
        self.geo = self.sel_node().geometry()
        self.attribs = []
        self.point_values = []
        self.get_point_attribs()

        #layout
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)

        self.refreshBtn = self.ui.refresh_btn.clicked.connect(self.refresh_button)

    def get_point_attribs(self):
        point_attribs = self.geo.pointAttribs()
        att_suffix = ['x','y','z']

        for pt_attrib in point_attribs:
            point_attrib = None
            if self.geo.findPointAttrib(pt_attrib.name()) != None:
                point_attr = self.geo.findPointAttrib(pt_attrib.name())
                if point_attr.size() > 1:
                    for i in range(point_attr.size()):
                        self.ui.data_tbl.insertColumn(i)
                        self.attribs.append(point_attr.name() + "." + att_suffix[i])
                else:
                    self.ui.data_tbl.insertColumn(i)
                    self.attribs.append(point_attr.name())


        #create rows
        for i in range(len(self.geo.points())):
            self.ui.data_tbl.insertRow(i)
        col_labels = tuple(self.attribs)
        self.ui.data_tbl.setHorizontalHeaderLabels(col_labels)

        row_labels = range(len(self.geo.points()))
        row_labels = tuple(map(str, row_labels))

        #get pt data
        for point in self.geo.points():
            #iterate on attribs
            for pt_attrib in point_attribs:
                point_attr = None
                if self.geo.findPointAttrib(pt_attrib.name()) != None:
                    point_attr = self.geo.findPointAttrib(pt_attrib.name())
                    if point_attr.size() > 1:
                        for i in range(point_attr.size()):
                            self.point_values.append(point.attribValue(point_attr)[i])
                    else:
                        self.point_values.append(point.attribValue(point_attr))

        #set row labels
        self.ui.data_tbl.setVerticalHeaderLabels(row_labels)


        #populate table
        for col, attrib in enumerate(self.attribs):
            for row in range(len(self.geo.points())):
                index = (row * len(self.attribs)) + col
                
                data = float("%.6f" %self.point_values[index])
                item = QtWidgets.QTableWidgetItem(str(data))
                self.ui.data_tbl.setItem(row, col, item)



    
    def sel_node(self):
        try:
            return hou.selectedNodes()[0]
        except:
            print("No Nodes selected!")

    def refresh_button(self):
        self.geo = self.sel_node().geometry()
        self.attribs = []
        self.point_values = []
        self.ui.data_tbl.clear()
        self.ui.data_tbl.setRowCount(0)
        self.ui.data_tbl.setColumnCount(0)
        self.get_point_attribs()

def show():
    dialog = AttribManager()
    dialog.setParent(hou.qt.floatingPanelWindow(None), QtCore.Qt.Window)
    dialog.show()


