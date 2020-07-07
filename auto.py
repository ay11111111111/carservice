import sqlite3, os, json
from dict import dic
dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path+'/json_data/car-list.json') as f:
    car_list = json.load(f)

with open(dir_path+'/car-logos-dataset/car-logos.json') as f:
    car_logos = json.load(f)

try:
    sqliteConnection = sqlite3.connect('db.sqlite3')
    for car in car_list:

        brand_low = car['brand'].lower()
        img = '/logos/' + dic[brand_low]

        sqlite_insert_table_query = '''INSERT INTO garage_carbrand (name, logo)
                                        VALUES(?, ?);'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        brand = (car['brand'], img)
        cursor.execute(sqlite_insert_table_query, brand)
        sqliteConnection.commit()
        print("BRAND inserted")
        brand_id = cursor.lastrowid


        for model in car['models']:

            sqlite_insert_model_query = '''INSERT INTO garage_carmodel (name, brand_id)
                                            VALUES(?, ?);'''
            data_tuple = (model, brand_id,)
            cursor = sqliteConnection.cursor()
            cursor.execute(sqlite_insert_model_query, data_tuple)
            sqliteConnection.commit()


    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("sqlite connection is closed")
