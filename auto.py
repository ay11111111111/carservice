import sqlite3, os, json
dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path+'/json_data/car-list.json') as f:
    car_list = json.load(f)

try:
    sqliteConnection = sqlite3.connect('db.sqlite3')
    for car in car_list:
        brand = (car['brand'],)
        print(brand)
        sqlite_insert_table_query = '''INSERT INTO garage_carbrand (name)
                                        VALUES(?);'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
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


#     # CAR_BRANDS = [(str(car["brand"]), str(car["brand"])) for car in car_list]
#     INSERT INTO artists (name) VALUES('Bud Powell');
