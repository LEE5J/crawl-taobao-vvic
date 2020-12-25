from crawl_vvic import init, vvic_search, crawl_a_item
from rapidapi import search_taobao_by_rapidapi
from crawl_taobao import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap ,QColor , QIcon
from naver_api import kor2cn
from selenium import webdriver
import sys, os, time

# if getattr(sys, 'frozen', False):
#     chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
#     driver = webdriver.Chrome(chromedriver_path)
# else:
#     driver = webdriver.Chrome()


class main_frame(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('타오바오 크롤링')
        self.setGeometry(300, 300, 400, 300) # ax: int, ay: int, aw: int, ah: int
        text_label = QLabel("검색어: ", self)
        text_label.move(10, 10)
        # 검색어 입력
        self.ledit = QLineEdit(self)
        self.ledit.move(10, 40)
        self.ledit.textChanged[str].connect(self.text_changed)
        self.ledit.returnPressed.connect(self.input_text)
        # 변역결과 창
        self.label = QLabel(self)
        self.label.move(10, 80)
        self.label.setText('검색어를 입력하시고 enter를 누르면 번역결과와 검색창이 활성화 됩니다.')

        # 검색 대상 사이트 선택
        self.cbox = QComboBox(self)
        self.cbox.addItem('타오바오&tmall')
        self.cbox.addItem('vvic')
        # self.cbox.addItem('1688')
        self.cbox.move(10, 100)

        # 검색 시작 버튼
        self.search_start = QPushButton(self)
        self.search_start.setText("검색 시작")
        self.search_start.setEnabled(False)
        self.search_start.move(10,250)
        self.search_start.clicked.connect(self.start_search)


        self.show()
    def start_search(self):
        if self.cbox.currentIndex() == 0:# 타오바오
            crawl_items_taobaoWselenium(str(self.label.text()))
        elif self.cbox.currentIndex() == 1:# vvic
            vvic_search(str(self.label.text()))
    def input_text(self):
        self.label.setText(self.ledit.text()) # 지금 뒷글자가 짤리는 이슈가 발생 이를 고치고 나면 아래방식을 적용
        self.search_start.setEnabled(True)
        self.label.setText(kor2cn(self.ledit.text()))
        self.label.adjustSize()
    def text_changed(self):
        self.label.setText("검색어를 입력하시고 enter 누르세요")
        self.search_start.setEnabled(False)
        self.label.adjustSize() # 멘 마지막으로 와야됨
if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = main_frame()
   sys.exit(app.exec_())
