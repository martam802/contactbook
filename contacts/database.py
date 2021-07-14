# Create the main window if the connection succeeded

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def _createContactsTable():
	"""Create the contacts table in the database."""
	createTableQuery = QSqlQuery()
	return createTableQuery.exec(
		"""
		CREATE TABLE IF NOT EXISTS contacts (
			id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
			name VARCHAR(40) NOT NULL,
			job VARCHAR(50),
			email VARCHAR(40) NOT NULL
		)
		"""
	)

def createConnection(databaseName):
	connection = QSqlDatabase.addDatabase('QSQLITE')
	connection.setDatabaseName(databaseName)

	if not connection.open():
		QMessageBox.warning(
			None,
			'Contact',
			f"Database error: {conection.lastError().text()}",
		)
		return False
	_createContactsTable()
	return True


"""
in the command line to crate connection
>>> from rpcontacts.database import createConnection

>>> # Create a connection
>>> createConnection("contacts.sqlite")
True

>>> # Confirm that contacts table exists
>>> from PyQt5.QtSql import QSqlDatabase
>>> db = QSqlDatabase.database()
>>> db.tables()
['contacts', 'sqlite_sequence']

Now you can prepare an SQL query to insert sample data into the contacts table:

>>> # Prepare a query to insert sample data
>>> from PyQt5.QtSql import QSqlQuery

>>> insertDataQuery = QSqlQuery()
>>> insertDataQuery.prepare(
#	"""
#    INSERT INTO contacts (
#        name,
#        job,
#        email
#    )

#    VALUES (?, ?, ?)
#    """
# )
#True

