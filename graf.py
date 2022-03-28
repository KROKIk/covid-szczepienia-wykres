import matplotlib.axes
import numpy as np
import matplotlib.pyplot as plt
import pymysql
x = []
y = []

db = pymysql.connect(
  host="192.168.1.10",
  user="prod",
  password="wulcan123",
  database="covid-graph"
)

# Prepare the database
cursor = db.cursor()
cursor.execute("SELECT pelna_dawka, duda FROM gminy;")
rows = cursor.fetchall()

for element in rows[1:]:
  x.append(float(element[0].replace(",", ".")))
  y.append(float(element[1]))

x = np.array(x)
y = np.array(y)

matplotlib.pyplot.ylabel("% głosów na dude")
matplotlib.pyplot.xlabel("% w pełni zaszczepionych")

plt.xlim(0,100)
plt.ylim(0,100)


plt.plot(x, y, ".r", markersize=2)


plt.show()