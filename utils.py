import requests
import psycopg2


def create_database(database_name, params):
    """Создание базы данных и таблиц для сохранения данных компаниях и их вакансиях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"DROP DATABASE IF EXISTS {database_name};")
    except:
        pass
    try:
        cur.execute(f"CREATE DATABASE {database_name};")
    except:
        pass

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE if exists logs;
            CREATE TABLE IF NOT EXISTS logs
            (tg_id varchar(100) not null,
            command varchar(50) not null,
            data_time varchar(50) not null,
            response text);
            """)

    conn.commit()
    conn.close()


def save_data_to_database(database_name, data_logs, params):
    """Сохранение данных о компаниях и их вакансиях в базу данных"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for log in data_logs:
            cur.execute("""
                            INSERT INTO logs (tg_id, command, data_time, response)
                            VALUES (%s, %s, %s, %s)
                            returning company_id;
                            """, (log['tg_id'], log['command'], log['data_time'], log['response']))

        conn.commit()
        conn.close()
