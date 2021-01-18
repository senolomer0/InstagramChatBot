from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from time import sleep
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout,QLineEdit,QSpacerItem)
from PyQt5.QtGui import QFont

class send_message(QWidget):
	def __init__(self, parent = None):
		super(send_message, self).__init__(parent)
		self.setFixedSize(350,650)
		self.setWindowTitle("Instagram ChatBot")
		self.setStyleSheet("background-color:white;")
			
		self.warning = QLabel()
		self.warning.setText("**Make sure you have written your username and\npassword correctly.\n**Any information you enter will not be saved.")
		self.warning.setStyleSheet("color:red;")
		self.warning.setFont( QFont('SansSerif', 10)) 

		self.button = QPushButton("Select Driver")
		self.button.setStyleSheet("background-color:green;color:white;font:10pt;width:20px")
		self.button.setMinimumSize(100,35)
		self.accountText = QLabel("Account:")
		self.accountText.setStyleSheet("color:green;")
		self.accountText.setFont( QFont('SansSerif', 12)) 
		self.account = QLineEdit()
		self.account.setMinimumSize(100,25)
		
		self.passwordText = QLabel("Password:")
		self.passwordText.setStyleSheet("color:green;")
		self.passwordText.setFont( QFont('SansSerif', 12)) 
		self.password = QLineEdit()
		self.password.setMinimumSize(100,25)

		self.sendText = QLabel("Account To Send:")
		self.sendText.setStyleSheet("color:green;")
		self.sendText.setFont( QFont('SansSerif', 12)) 	
		self.sendAccount = QLineEdit()
		self.sendAccount.setMinimumSize(100,25)

		self.howmanytext=QLabel("How Many Massage:")
		self.howmanytext.setStyleSheet("color:green;")
		self.howmanytext.setFont( QFont('SansSerif', 12)) 
		self.howmany = QLineEdit()
		self.howmany.setMinimumSize(100,25)

		self.messageText = QLabel("Your Message:")
		self.messageText.setStyleSheet("color:green;")
		self.messageText.setFont( QFont('SansSerif', 12)) 
		self.textarea = QTextEdit()
		self.textarea.resize(100,60)

		self.start = QPushButton("Send Message")
		self.start.setStyleSheet("background-color:green;color:white;font:10pt;width:20px")
		self.start.setMinimumSize(100,35)

		self.error = QLabel()
		self.error.setStyleSheet("color:red;")
		self.error.setFont( QFont('SansSerif', 10)) 
		spacer = QSpacerItem(0,15)

		layout = QVBoxLayout()
		layout.addWidget(self.warning)
		layout.addStretch()
		layout.addWidget(self.button)
		layout.addItem(spacer)
		layout.addWidget(self.accountText)
		layout.addWidget(self.account)
		layout.addWidget(self.passwordText)
		layout.addWidget(self.password)
		layout.addWidget(self.sendText)
		layout.addWidget(self.sendAccount)
		layout.addWidget(self.howmanytext)
		layout.addWidget(self.howmany)
		layout.addWidget(self.messageText)
		layout.addWidget(self.textarea)
		layout.addWidget(self.error)
		layout.addItem(spacer)
		layout.addWidget(self.start)
		layout.addStretch()

		self.button.clicked.connect(self.getfile)
		self.start.clicked.connect(self.control)

		self.setLayout(layout)

	def control(self):
		a=0
		b=0
		c=0
		d=0
		self.message = str(self.textarea.toPlainText())
		try:
			number = int(self.howmany.text())
			if(number>200 or number<1):
				self.error.setText("**The number of messages you want to send must be\nbetween 1-200")
			else:
				a=1
		except:
			self.error.setText("**The number of messages you want to send must be\na number.")
			
		if(len(self.message)>200 or len(self.message)<1):	
			self.error.setText("**The message you send must consist of 1-200\ncharacters.")
		else:
			b=1
		try:
			if(len(self.fname)<3):
				self.error.setText("**Select driver first.")
			else:
				c=1
		except:
			self.error.setText("**Select driver first.")

		if(len(self.account.text()) ==0 or len(self.password.text())==0 or len(self.sendAccount.text())==0):
			self.error.setText("Please fill in all the blanks.")
		else:
			d=1

		if(a==1 and b==1 and c==1 and d==1):
			self.error.setText("")
			self.send()

	def getfile(self):
		self.fname = str(QFileDialog.getOpenFileName(self, 'Open file', '/home')[0])

	def send(self):
		a=0
		try:
			driver = webdriver.Chrome(self.fname)
			a=1
		except:
			self.error.setText("**Please select a correct driver")
		if(a==1):
			self.error.setText("")
			driver.get("https://instagram.com")
			wait = WebDriverWait(driver, 600)
			driver.maximize_window()
			
			account = driver.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
			password = driver.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")

			account.send_keys(self.account.text())
			password.send_keys(self.password.text())

			button = driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]")
			button.click()

			sleep(3)
			sendperson = driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/input")
			sendperson.send_keys(self.sendAccount.text())
			sleep(2)
			sendpersonname = driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/div[4]/div/a[1]/div")
			sendpersonname.click()
			sleep(2)
			messagebutton = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/div/div[1]/div")
			messagebutton.click()
			sleep(2)
			notnow = driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]")
			notnow.click()
			sleep(2)

			for i in range(int(self.howmany.text())):
				message = driver.find_element_by_xpath("//*[@id='react-root']/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
				message.send_keys(self.message)
				send = driver.find_element_by_xpath("//*[@id='react-root']/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button")
				send.click()
				self.exit()
			
	def exit(self):
		self.close()

app = QApplication(sys.argv)
ex = send_message()
ex.show()
sys.exit(app.exec_())