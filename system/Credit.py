
import sys
import os
from os import path
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

main_dir = path.abspath(path.dirname(sys.argv[0]))  # Dir of main
icon_dir          = path.join(main_dir, "icons")
icon_disabled_dir = path.join(icon_dir, "Disabled")


class Credit():
    def Credit(self):
        #QMessageBox.setIcon(QMessageBox.Information)
        msg = QMessageBox(QMessageBox.Information, "About UNI-EM",
                            "<h1>UNI-EM Ver0.92.10</h1><BR>"
                            "(C) 2019 Hidetoshi Urakubo, Torsten Bullmann, Ryoji Miyamoto, Naoki Tamura, Ryoya Kamikawa.<BR>"
                            "This project is licensed under the GNU General Public License Version 3 (GPLv3).<BR>"
                            "UNI-EM is powered by the following software:<BR>"
                            "<a href=\"https://github.com/google/ffn\">Flood filling networks</a>,<BR> "
                            "<a href=\"https://github.com/affinelayer/pix2pix-tensorflow\">Imagetranslation-tensorflow</a>,<BR> "
                            "<a href=\"https://www.tensorflow.org/\">Tensorflow</a>,<BR>"
                            "<a href=\"http://doc.qt.digia.com/4.5/stylesheet.html\">Qt</a>,<BR>"
                            "<a href=\"https://threejs.org/\">Three.js</a>,<BR>"
                            "<a href=\"http://www.rhoana.org/dojo/\">Rhoana Dojo</a>,<BR> "
                            "<a href=\"https://opencv.org/\">Open CV</a>,<BR> "
                            "<a href=\"http://scikit-image.org/docs/dev/api/skimage.html\">Scikit-image</a><BR> "
                          )
        msg.setIconPixmap(QPixmap(path.join(icon_dir, "Mojo2_128.png")))
        exe = msg.exec_()



