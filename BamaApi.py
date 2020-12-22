import requests
import re
from bs4 import BeautifulSoup
import mysql.connector


def get_data(url):
    response = requests.get(url=url)
    # print(response.headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # find Details(Odometer, year, color):
    res = soup.find_all("div", attrs={"class": "clearfix web-milage-div"})
    details = list()
    for item in res:
        reg = re.sub(r"\s+", " ", item.text).strip()
        result = re.sub(r"صفر", "0", reg, 0, re.MULTILINE)
        regex = r"کارکرد (\d+\,*\d*) کیلومتر (\d+)\، (.+)"
        de = re.findall(regex, result)
        details.append(list(de[0]))
    for odo in details:
        odo[0] = re.sub(r",", "", odo[0], 0, re.MULTILINE)
    # find Price:
    res_p = soup.find_all("span", attrs={"itemprop": "price"})
    i = 0
    for item in res_p:
        reg = re.sub(r"در توضیحات", "0", item.text, 0, re.MULTILINE).strip()
        result = re.sub(r",", "", reg, 0, re.MULTILINE)
        details[i].append(result)
        i += 1
    print("Get Data Successfully!")
    return details


def writeToDB(details):
    # Connect to DataBase :
    myConnect = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='1234',
        database=''
    )
    myCursor = myConnect.cursor(buffered=True, dictionary=True)  # buffered=True, dictionary=True
    myCursor.execute("SHOW DATABASES;")
    db_list = list()
    for db in myCursor:
        db_list.append(db['Database'])

    if 'renault_db' not in db_list:
        print(True)
        myCursor.execute("CREATE DATABASE Renault_DB")
    myCursor.execute("USE Renault_DB;")

    myCursor.execute("SHOW TABLES;")
    tb_list = list()
    for tb in myCursor:
        tb_list.append(tb['Tables_in_renault_db'])
    if 'l90' not in tb_list:
        myquery_Create = "CREATE TABLE L90(Odometer INT, Year INT, Color VARCHAR(255), Price INT (20), id INT AUTO_INCREMENT PRIMARY KEY);"
        myCursor.execute(myquery_Create)

    myCursor.execute("DELETE FROM L90;")

    myquery_Insert = "INSERT INTO L90 (Odometer, Year, Color, Price) VALUES (%s, %s, %s, %s)"
    values = list()
    for item in details:
        values.append(tuple(item))
    myCursor.executemany(myquery_Insert, values)
    myConnect.commit()
    print("Write to DataBase Successfully!")
    myConnect.close()


if __name__ == '__main__':
    url = "https://bama.ir/car/renault/tondar90/all-trims?hasprice=true"
    data = get_data(url)
    writeToDB(data)

