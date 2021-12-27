from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrintDialog,QPrinter
from PyQt5.QtGui import *
#from mainProductPicMaker import PicInfo,PostMaker
import sys
import os
from ydk2list import ydkParser
class Ui_MainWindow(QMainWindow):
	def __init__(self):
		super(Ui_MainWindow,self).__init__()
		
		self.outputpath = os.getcwd()
		self.ydkpath = ""
		self.ydkname = ""
		self.setupUi(self)
		#self.retranslateUi(self)

	def setupUi(self, MainWindow):
		self.setObjectName("YDKParser")
		self.setWindowTitle("YDKParser")
		self.resize(300, 200)
		w = QWidget(self)
		self.setCentralWidget(w)
		self.selectYDKButton = QPushButton("选择YDK")
		self.selectOutputButton = QPushButton("选择输出路径")
		self.drawButton = QPushButton("生成")
		self.outputLabel = QLabel()
		self.drawButton.setEnabled(False)
		self.pathLabel = QLabel("输出路径: " + self.outputpath)
		self.adlabel = QLabel("欢迎加入绯雪卡牌群666563329 盒子靠谱")
		grid = QGridLayout()
		#grid.setSpacing(10)

		grid.addWidget(self.selectYDKButton, 0, 0)
		grid.addWidget(self.pathLabel,1,0)
		grid.addWidget(self.selectOutputButton,0,1)
		grid.addWidget(self.drawButton,0,2)
		grid.addWidget(self.outputLabel,2,0)
		grid.addWidget(self.adlabel,3,0)
		w.setLayout(grid)
		self.selectYDKButton.clicked.connect(self.chooseBase)
		self.selectOutputButton.clicked.connect(self.chooseOutput)
		self.drawButton.clicked.connect(self.draw)
	def draw(self):
		p = ydkParser(self.ydkpath)
		p.parser()
		p.drawCardName("1.png",self.outputpath+"/"+self.ydkname.replace(".ydk", ".png"))
		p.outputCardFile(self.outputpath+"/"+self.ydkname.replace(".ydk", ".txt"))
		self.drawButton.setEnabled(False)
		#self.pathLabel.setText(self.ydkpath + " 生成完成")
		self.ydkpath = ""
		self.ydkname = ""
		self.pathLabel.setText("当前选择的YDK文件: " + self.ydkpath )
		QMessageBox.information(self, "ydkParser","生成成功")
	def chooseOutput(self):
		dirpath = QFileDialog.getExistingDirectory(self,"选择输出文件路径",self.outputpath)
		print(dirpath)
		self.outputpath=  dirpath
		self.outputLabel.setText("输出路径: " + self.outputpath)
	def chooseBase(self):
		filepath,filetype = QFileDialog.getOpenFileName(self,"选择YDK",os.getcwd(),"All Files (*);;YDK (*.ydk)")
		print(filepath)
		fl = filepath.split("/")
		print(fl)
		ydkname = fl[-1]
		self.ydkpath = filepath
		self.ydkname = ydkname
		self.pathLabel.setText(filepath)
		self.drawButton.setEnabled(True)
		#p = ydkParser(filepath)
		#p.parser()
	#	p.reportResult()
		##sys.out.flush()
		#p.drawCardName("1.png",os.getcwd()+"\\o.png")
		self.pathLabel.setText("当前选择的YDK文件: " + self.ydkpath )
		return








if __name__ == '__main__':
	app = QApplication(sys.argv)
	windows = Ui_MainWindow()
	windows.show()
	sys.exit(app.exec_())