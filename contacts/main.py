import sys 

from PyQt5.QtWidgets import QApplication

from .database import createConnection
from .view import Window

def main():
	# Create the application
	app = QApplication(sys.argv)
	# Connect to the database before creating any window
	if not createConnection("contacts.sqlite"):
		sys.exit(1)
	# Create the main window if the connection succeeded
	win = Window()
	win.show()
	sys.exit(app.exec_())