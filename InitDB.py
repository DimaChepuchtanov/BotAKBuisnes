from getpass import getpass
from mysql.connector import connect, Error



def create_connection():
    m = connect(host="YEAR HOST",
                user="YEAR",
                password="YEAR",
                database="YEAR",)
    return m


if __name__ == "__main__":
    f = create_connection()
    cursor = f.cursor()
    cursor.execute("SELECT id FROM TABLE_NAME WHERE 	Tg_id = %s;",(222222,))