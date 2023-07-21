from dotenv import load_dotenv
load_dotenv()
import os
import certifi
import pymysql.cursors

connection = pymysql.connect(host=os.getenv("PLANETSCALE_HOST"),
                             user=os.getenv("PLANETSCALE_USERNAME"),
                             password=os.getenv("PLANETSCALE_PASSWORD"),
                             database=os.getenv("PLANETSCALE_DATABASE"),
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit = True,
                             ssl_verify_identity = True,
                             ssl      = {
                             "ca": certifi.where()
                             })

with connection:
    with connection.cursor() as cursor:
        sql = "show tables"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
