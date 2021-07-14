from PyQt5.QtWidgets import (
	QAbstractItemView,
	QDialog,
	QDialogButtonBox,
	QFormLayout,
	QHBoxLayout,
	QLineEdit,
	QMainWindow,
	QMessageBox,
	QPushButton,
	QTableView,
	QVBoxLayout,
	QWidget,
)
from PyQt5.QtCore import Qt
from .model import ContactsModel

class Window (QMainWindow):
	def __init__(self,parent = None):
		super().__init__(parent)
		self.setWindowTitle('Contacts')
		self.resize(550,250)
		self.centralWidget = QWidget()
		self.setCentralWidget(self.centralWidget)
		self.layout = QHBoxLayout()
		self.centralWidget.setLayout(self.layout)
		self.contactsModel = ContactsModel()
		self.setupUI()

		
	def setupUI(self):
		"""Setup the main window's GUI."""
		# Create the table view widget
		self.table = QTableView()
		#to connect the model with the table view
		self.table.setModel(self.contactsModel.model)
		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table.resizeColumnsToContents()
		# Create buttons
		self.addButton = QPushButton('Add...')
		"""
		connects the .clicked() signal of the Add button 
		to the newly created slot, .openAddDialog().
		This way, a click on the button will automatically 
		call the slot.
		"""
		self.addButton.clicked.connect(self.openAddDialog)
		self.deleteButton = QPushButton('Delete')
		self.addButton.clicked.connect(self.deleteContact)
		self.clearButton = QPushButton('Clear All')
		self.clearButton.clicked.connect(self.clearContacts)
		# Lay out the GUI
		layout = QVBoxLayout()
		layout.addWidget(self.addButton)
		layout.addWidget(self.deleteButton)
		layout.addStretch()
		layout.addWidget(self.clearButton)
		self.layout.addWidget(self.table)
		self.layout.addLayout(layout)

	def clearContacts(self):
		"""Remove all contacts from the database."""
		messageBox = QMessageBox.warning(
			self,
			"Warning!",
			"Do you want to remove all your contacts?",
			QMessageBox.Ok | QMessageBox.Cancel,
		)

		if messageBox == QMessageBox.Ok:
			self.contactsModel.clearContacts()

	def deleteContact(self):
		row = self.table.currentIndex().row()
		if row < 0:
			return

		messageBox = QMessageBox.warning(
			self,
			'Warning',
			'Do you want to remove selected contact?',
			QMessageBox.Ok | QMessageBox.Cancel,
		)

		if messageBox == QMessageBox.Ok:
			self.contactsModel.deleteContact(row)

	def openAddDialog(self):
		"""Open the Add Contact dialog."""
		dialog = AddDialog(self)
		if dialog.exec() == QDialog.Accepted:
			self.contactsModel.addContact(dialog.data)
			self.table.resizeColumnsToContents()


class AddDialog(QDialog):
	#add contact dialog
	def __init__(self, parent=None):
		#initializer
		super().__init__(parent=parent)
		self.setWindowTitle('Add Contact')
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)
		self.data = None

		self.setupUI()
		
	def setupUI(self):
		"""Setup the Add Contact dialog's GUI."""
		# Create line edits for data fields
		self.nameField = QLineEdit()
		self.nameField.setObjectName("Name")
		self.jobField = QLineEdit()
		self.jobField.setObjectName("Job")
		self.emailField = QLineEdit()
		self.emailField.setObjectName("Email")
		# Lay out the data fields
		layout = QFormLayout()
		layout.addRow("Name:", self.nameField)
		layout.addRow("Job:", self.jobField)
		layout.addRow("Email:", self.emailField)
		self.layout.addLayout(layout)
		# Add standard buttons to the dialog and connect them
		self.buttonsBox = QDialogButtonBox(self)
		self.buttonsBox.setOrientation(Qt.Horizontal)
		self.buttonsBox.setStandardButtons(
			QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.buttonsBox.accepted.connect(self.accept)
		self.buttonsBox.rejected.connect(self.reject)
		self.layout.addWidget(self.buttonsBox)


	def accept(self):
		#accepting the data provaifing through dialog
		#initializes .data to an empty list ([]). This list will store the user’s input data.
		self.data = [] 
		for field in (self.nameField, self.jobField, self.emailField):
			if  not field.text():
				QMessageBox.critical(
					self,
					"error",
					f"you must provide a contact's {field.objectName()}",
				)
				self.data = None #reset .data
				return 

			# adds the user’s input for each field to .data.
			self.data.append(field.text())

		if not self.data:
			return 

		super().accept()
