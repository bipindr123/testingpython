import xlrd
import MySQLdb


# Establish a MySQL connection
database = MySQLdb.connect (host="localhost", user = "root", passwd = "", db = "mysqlPython")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

book = xlrd.open_workbook("./puthere/myfile.xlsx")
sheet = book.sheet_by_index(0)


# Create the INSERT INTO sql query
query = INSERT INTO agents (agent=) VALUES (%s)
query = INSERT INTO metrics (metric) VALUES (%s)
query = INSERT INTO months (month) VALUES (%s)

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet.nrows):
      agent      = sheet.cell().value

      # Assign values from each row
      values = ()

      # Execute sql Query
      cursor.execute(query, values)

# Close the cursor
cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()
