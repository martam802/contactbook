from PyQt5.QtCore import Qt 
from PyQt5.QtSql import QSqlTableModel

"""This module provides a model to manage the contacts table."""

class ContactsModel:
	def __init__(self):
		self.model = self._createModel()

	def clearContacts(self):
		"""
		sets the data model’s .editStrategy property 
		to QSqlTableModel.OnManualSubmit. 
		This allows you to cache all the changes 
		until you call .submitAll() later on. 
		You need to do this because you’re changing 
		everal rows at the same time.
		"""
		self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
		self.model.removeRows(0, self.model.rowCount())
		self.model.submitAll()
		"""
		resets the model’s .editStrategy property to its original 
		value, QSqlTableModel.OnFieldChange. 
		If you don’t reset this property to its 
		original value, then you won’t be able to 
		update the contacts directly in the table view.
		"""
		self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
		self.model.select()

	def deleteContact(self, row):
		self.model.removeRow(row)
		self.model.submitAll()
		self.model.select()

	def addContact(self,data):
		rows = self.model.rowCount()
		self.model.insertRows(rows, 1)
		for column, field in enumerate(data):
			self.model.setData(self.model.index(rows, column + 1), field)
		self.model.submitAll()
		self.model.select()

	@staticmethod
	def _createModel():
		tableModel = QSqlTableModel()
		tableModel.setTable('contacts')
		"""
		sets the .editStrategy property of the 
		model to QSqlTableModel.OnFieldChange. 
		With this, you ensure that the changes on 
		the model get saved into the database 
		immediately.
		"""
		tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
		tableModel.select()
		headers = ('ID', 'Name', 'Job', 'Email')
		for columnIndex, header in enumerate(headers):
			tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
		return tableModel



