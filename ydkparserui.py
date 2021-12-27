from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrintDialog,QPrinter
from PyQt5.QtGui import *
from mainProductPicMaker import PicInfo,PostMaker
import sys
import os
from ydk2list import ydkParser
class Ui_MainWindow(QMainWindow):
	def __init__(self):
		super(Ui_MainWindow,self).__init__()
		self.setupUi(self)
		#self.retranslateUi(self)

	def setupUi(self, MainWindow):
		self.setObjectName("YDKParser")
		self.setWindowTitle("YDKParser")
		self.resize(300, 200)
		w = QWidget(self)
		self.setCentralWidget(w)
		self.selectYDKButton = QPushButton("选择YDK")
		self.pathLabel = QLabel()
		self.adlabel = QLabel("欢迎加入绯雪卡牌群666563329 盒子靠谱")
		grid = QGridLayout()
		grid.setSpacing(10)

		grid.addWidget(self.selectYDKButton, 0, 0)
		grid.addWidget(self.pathLabel,1,0)
		grid.addWidget(self.adlabel,2,0)
		w.setLayout(grid)
		self.selectYDKButton.clicked.connect(self.chooseBase)



	def chooseBase(self):
		filepath,filetype = QFileDialog.getOpenFileName(self,"选择YDK",os.getcwd(),"All Files (*);;YDK (*.ydk)")
		print(filepath)
		self.ydkpath = filepath
		self.pathLabel.setText(filepath)
		p = ydkParser(filepath)
		p.parser()
		p.reportResult()
		#sys.out.flush()
		p.drawCardName("1.png",os.getcwd()+"\\o.png")
		self.pathLabel.setText(filepath + " 生成完成")
		return








if __name__ == '__main__':
	app = QApplication(sys.argv)
	windows = Ui_MainWindow()
	windows.show()
	sys.exit(app.exec_())