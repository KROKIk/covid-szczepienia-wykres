import pymysql

f = open("prezydenckie.tsv", encoding="UTF-8")

# Connect to the mysql database
db = pymysql.connect(
  host="192.168.1.10",
  user="prod",
  password="wulcan123",
  database="covid-graph"
)

# Prepare the database
cursor = db.cursor()
cursor.execute("USE `covid-graph`")

for line in f:
    data = line.replace("\n", "").split("\t")
    print(data)
    cursor.execute(f"UPDATE gminy set frekwencja = \"{data[1]}\", duda = \"{data[2]}\", trzaskowski = \"{data[3]}\" where gmina = \"{data[0]}\"")

db.commit()