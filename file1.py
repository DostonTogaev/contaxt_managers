import psycopg2

db_person = {
    'host': 'localhost',
    'database': 'n35',
    'user': 'postgres',
    'password': '102030',
    'port': 5432
}


class DbConnect:
    def __init__(self, db_person):
        self.db_params = db_person
        self.conn = psycopg2.connect(**self.db_person)

    def __enter__(self):
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class Person:
    def __init__(self,
                 id: int | None = None,
                 full_name: str | None = None,
                 age: int | None = None,
                 email: str | None = None):
        self.id = id
        self.full_name = full_name
        self.age = age
        self.email = email


class Datas:
    def __init__(self):
        self.connection = psycopg2.connect('db_person')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""create table if not exists person(
        id serial PRIMARY KEY,
        name varchar(100) not null,
        age integer not null,
        email varchar(100) not null

    ); """)

    def save(self):
        with DbConnect(db_person) as cur:
            insert_query = 'insert into person (name, age, email) values (%s,%s,%s);'
            insert_params = (self.name, self.age, self.email)
            cur.execute(insert_query, insert_params)
            print('INSERT 0 1')

    def get_person(self, id):
        self.cursor.execute("SELECT * FROM persons WHERE id=?", (id))
        person_data = self.cursor.fetchone()
        if person_data:
            return Person(*person_data)
        else:
            return None


with DbConnect as cursor:
    database = Datas()
    person1 = Person(1, "sarvar aliyev", 18, "sarvar@example.com")
    database.save(person1)
    person2 = Person(2, "Jonibek asqarov", 25, "jonibek@example.com")
    database.save(person2)
    person3 = Person(3, "asror boqayev", 25, "asror@gmail.com")
    database.save(person3)


    person_id = 1
    retrieved_person = database.get_person(person_id)
    if retrieved_person:
        print("Ma'lumotlar:", retrieved_person.id, retrieved_person.full_name, retrieved_person.age,
              retrieved_person.email)
    else:
        print("it is not found id")
