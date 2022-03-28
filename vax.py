from time import sleep
import pymysql
from selenium import webdriver

db = pymysql.connect(
  host="192.168.1.10",
  user="prod",
  password="wulcan123",
  database="covid-graph"
)

# Prepare the database
cursor = db.cursor()
cursor.execute("USE `covid-graph`")

driver = webdriver.Chrome(executable_path='C:\\Projects\\Python\\covid-graph\\chromedriver.exe')
url = "https://www.gov.pl/web/szczepienia-gmin/sprawdz-poziom-wyszczepienia-mieszkancow-gmin"

driver.get(url)
driver.maximize_window()
sleep(1)

limit = 50
for n in range(limit):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_partial_link_text("50").click()

    dane = str(driver.find_element_by_class_name("results-table").text)
    dane = dane[250:]
    dane = dane.replace("\n", "`").replace("Kliknij enter aby pokazać szczegóły wiersza [object Object]`", "").split("zobacz szczegóły`")

    for row in dane[:-1]:
        data = row[:-1].split("`")
        print(data)
        gmina = data[2][: data[2].find("(") - 1]
        cursor.execute(f"insert into gminy (wojewodztwo, powiat, gmina, pelna_dawka, przyrost, liczba_ludnosci, 1_dawka, 2_dawka) values ('{data[0]}', '{data[1]}', '{gmina}', '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}', '{data[7]}')")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    if n == limit - 1:
        break
    driver.find_element_by_id("js-pagination-page-next").click()
    sleep(0.5)
    
db.commit()
driver.quit()