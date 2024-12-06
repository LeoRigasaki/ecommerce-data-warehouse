import psycopg2
from configparser import ConfigParser

def config(filename='config/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in {filename}')
    return db

def get_connection():
    try:
        params = config()
        connection = psycopg2.connect(**params)
        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return None

def test_connection():
    conn = get_connection()
    if conn is not None:
        print("Connection successful!")
        conn.close()
    else:
        print("Connection failed!")

if __name__ == "__main__":
    test_connection()