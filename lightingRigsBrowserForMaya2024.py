import os

import maya.cmds as cmds

from maya import OpenMayaUI

from shiboken2 import wrapInstance

from PySide2 import QtWidgets
from PySide2 import QtCore


def maya_main_window():

    ptr = OpenMayaUI.MQtUtil.mainWindow()

    return wrapInstance(int(ptr), QtWidgets.QWidget)


class LightingRigBrowser(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):

        super(LightingRigBrowser, self).__init__(parent)

        self.setWindowTitle("KAIM27 Lighting Rig Browser")

        self.resize(430, 510)

        
        self.rigFolder = r"T:\jm-dos\LightingToolkit\lightingRigs"

        self.create_widgets()

        self.create_layout()

        self.create_connections()

        self.refresh_list()



    def create_widgets(self):

        self.listWidget = QtWidgets.QListWidget()

        self.namespaceLine = QtWidgets.QLineEdit()

        self.namespaceLine.setText("LightRig")

        self.refreshButton = QtWidgets.QPushButton("Refresh")

        self.referenceButton = QtWidgets.QPushButton(
            "Reference Selected Rig"
        )



    def create_layout(self):

        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(QtWidgets.QLabel("KAIM27 Lighting Rigs"))

        layout.addWidget(self.listWidget)

        layout.addWidget(QtWidgets.QLabel("Namespace"))

        layout.addWidget(self.namespaceLine)

        layout.addWidget(self.refreshButton)

        layout.addWidget(self.referenceButton)


    def create_connections(self):

        self.refreshButton.clicked.connect(self.refresh_list)

        self.referenceButton.clicked.connect(
            self.reference_selected
        )



    def refresh_list(self):

        self.listWidget.clear()

        if not os.path.exists(self.rigFolder):

            cmds.warning("Folder not found.")

            return

        files = os.listdir(self.rigFolder)

        for file in sorted(files):

            if file.endswith(".ma"):

                self.listWidget.addItem(file)

            if file.endswith(".mb"):

                self.listWidget.addItem(file)


    def reference_selected(self):

        item = self.listWidget.currentItem()

        if not item:

            cmds.warning("Select a rig.")

            return

        fileName = item.text()

        fullPath = os.path.join(
            self.rigFolder,
            fileName
        )

        namespace = self.namespaceLine.text()

        cmds.file(
            fullPath,
            reference=True,
            namespace=namespace
        )

        cmds.inViewMessage(
            amg="Lighting Rig Referenced",
            pos="topCenter",
            fade=True
        )



try:
    lightingRigBrowser.close()
    lightingRigBrowser.deleteLater()

except:
    pass

lightingRigBrowser = LightingRigBrowser()

lightingRigBrowser.show()
