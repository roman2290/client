import psycopg2
import pprint

conn = psycopg2.connect(database="client", user="postgres")
with conn.cursor() as cur:
    cur.execute ("""
        DROP TABLE client, contact CASCADE
    """)

    # 1 Функция, создающая структуру БД (таблицы).
    def create_db(cur):
        cur.execute(""" 
            CREATE TABLE if not exists client ( 
            id_client SERIAL PRIMARY KEY,
            first_name VARCHAR (40) UNIQUE,
            last_name VARCHAR (40) UNIQUE,
            email VARCHAR (40) UNIQUE
    );   
    """)

        cur.execute("""   
            CREATE TABLE if not exists contact (
            id_contact SERIAL PRIMARY KEY,
            Phone VARCHAR (40) NOT NULL,
            a_id_client INTEGER REFERENCES client(id_client)
    );
    """)

# 2 Функция, позволяющая добавить нового клиента.
    def client_add(cur, id_client, first_name=None, last_name=None, email=None, phone=None):
        cur.execute(""" 
            INSERT INTO client (id_client, first_name, last_name, email) VALUES (%s, %s, %s, %s);
            """, (id_client, first_name, last_name, email))

# 3 Функция, позволяющая добавить телефон для существующего клиента.
    def phone_add(cur, id_contact, phone, a_id_client):
        cur.execute("""
            INSERT INTO contact VALUES (%s, %s, %s);
            """, (id_contact, phone, a_id_client))
        return id_contact

# 4 Функция, позволяющая изменить данные о клиенте.
    def change_client(cur, id_client, first_name=None, last_name=None, email=None):
        cur.execute ("""SELECT * FROM client
            WHERE id_client = %s """, (id_client,))
        info = cur.fetchall()
        if first_name is None:
            first_name = info[1]
        if last_name is None:
            last_name = info[2]
        if email is None:
            email = info[3]
        cur.execute("""
            UPDATE client
            SET first_name = %s, last_name = %s, email = %s
            WHERE id_client = %s
        """, ( first_name, last_name, email, id_client))
        return id_client

# 5 Функция, позволяющая удалить телефон для существующего клиента.
    def phone_delete(cur, phone: str) -> int:
        cur.execute(""" DELETE FROM contact WHERE phone = %s       
    """, (phone,))
        return phone

# # 6 Функция, позволяющая удалить существующего клиента.
    def client_delete(cur, id_client):
        cur.execute("""
            DELETE FROM client
            WHERE id_client = %s
        """, (id_client,))
        cur.execute("""
            DELETE FROM contact
            WHERE id_contact = %s
       """, (id_client,))
        return id_client

# # 7 Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
    def client_find(cur, first_name=None, last_name=None, email=None, phone=None ):    
        cur.execute("""
            SELECT first_name, last_name, email
            FROM client 
            WHERE first_name LIKE first_name AND last_name LIKE last_name 
            AND email LIKE email
        """,  first_name)
        cur.execute("""
            SELECT c.first_name, c.last_name, c.email, p.phone FROM client c
            JOIN contact p ON p.a_id_client = c.id_client
            WHERE c.first_name LIKE first_name AND c.last_name LIKE last_name
            AND c.email LIKE email AND p.phone like phone
        """, (phone))
        return cur.fetchall()[1]
        


    if __name__ == '__main__':

# 1 Функция, создающая структуру БД (таблицы).
        print('Таблицы созданы')
        create = create_db(cur)

# 2 Функция, позволяющая добавить нового клиента.
        print ('Создан новый клиент', client_add (cur, 1, 'Тони', 'Старк', 'ts@yandex.ru')),
        print ('Создан новый клиент', client_add (cur, 2, 'Стив', 'Роджерс', 'cr@yandex.ru')),
        print ('Создан новый клиент', client_add (cur, 3, 'Ник', 'Фбюри', 'nf@yandex.ru')),

# 3 Функция, позволяющая добавить телефон для существующего клиента.
        print ('Телефон добавлен для Тони', phone_add (cur, 1, '89557774523', 1))
        print ('Создан новый клиент', phone_add (cur, 2, '89997776594', 2))
        print ('Создан новый клиент', phone_add (cur, 3, '89997776593', 3))

# 4 Функция, позволяющая изменить данные о клиенте.
        print ('Данные клиента изменены', change_client (cur, 1, 'Николас', 'Фьюри', 'ff@yandex.ru'))
        print("Данные изменены")
        cur.execute("""
            SELECT a.id_client, a.first_name, a.last_name, a.email, s.phone FROM client a
            JOIN contact s ON s.a_id_client = a.id_client
            ORDER by a.id_client
            """)
        print(cur.fetchone())
# 5 Функция, позволяющая удалить телефон для существующего клиента.
        print("Телефон удалён: ",
        phone_delete(cur, '89997776593'))
        cur.execute("""
           SELECT a.first_name, a.last_name, a.email, s.phone FROM client a
           JOIN contact s ON s.a_id_client = a.id_client
           ORDER by s.phone
           """)
        print(cur.fetchall())

# 6 Функция, позволяющая удалить существующего клиента.
        print("CLIENT DELET ",
              client_delete(cur, 0))
        cur.execute("""
            SELECT a.id_client, a.first_name, a.last_name, a.email, s.phone FROM client a
            JOIN contact s ON s.id_contact = a.id_client
            ORDER by a.id_client
    """)
        print(cur.fetchall())

# # 7 Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
        pprint.pprint('Найден клиент по имени:')
        pprint.pprint(client_find(cur, 'Тони'))
        pprint.pprint('Найденный клиент по Фамилии:') 
        pprint.pprint(client_find(cur,))
        pprint.pprint('Найденный клиент по email:') 
        pprint.pprint(client_find(cur,))
        pprint.pprint('Найденный клиент по телефону:')
        pprint.pprint(client_find(cur,))
        
conn.commit()
conn.close()
