import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname="weather",
                user="postgres",
                password="MJWhzCSaU",
                host="db",
                port=5432
            )
            conn.close()
            print("База данных готова!")
            break
        except OperationalError:
            print("Ожидание базы данных...")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db()