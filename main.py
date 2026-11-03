#1. Importar librerias para establecer conexion con DB y obtener variables de entorno
import os
import psycopg

#2. Definir variable para ruta DB

url = os.getenv("DATABASE_URL")

personajes = [
    ('Tony Stark', 'Dead', 'Human', 'Superhero', 'Male', 'Earth', 'Earth'),
    ('Steve Rogers', 'Alive', 'Human', 'Super soldier', 'Male', 'Earth', 'Earth'),
    ('Thor', 'Alive', 'Asgardian', 'God of Thunder', 'Male', 'Asgard', 'New Asgard'),
    ('Natasha Romanoff', 'Dead', 'Human', 'Spy', 'Female', 'Earth', 'Earth'),
    ('Bruce Banner', 'Alive', 'Human', 'Scientist', 'Male', 'Earth', 'Earth'),
    ('Clint Barton', 'Alive', 'Human', 'Archer', 'Male', 'Earth', 'Earth'),
    ('Wanda Maximoff', 'Alive', 'Human', 'Enhanced', 'Female', 'Sokovia', 'Earth'),
    ('Peter Parker', 'Alive', 'Human', 'Superhero', 'Male', 'Earth', 'Earth'),
    ('Doctor Strange', 'Alive', 'Human', 'Sorcerer', 'Male', 'Earth', 'Kamar-Taj'),
]


#3. Conexión con tabla + primera acción (execute) de crear tabla
try: 
    with psycopg.connect(url) as connection:
        with connection.cursor() as cur:
            #1. Crear tabla
            cur.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    status VARCHAR(100),
                    species VARCHAR(100),
                    type VARCHAR(100),
                    gender VARCHAR(100),
                    origin_name VARCHAR(100),
                    location_name VARCHAR(100),
                    created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP)
            """)

            #2. Sentencia SQL con 7 marcadores %s para insertar datos masivamente
            insert_query = """
                INSERT INTO characters (name, status, species, type, gender, origin_name, location_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            #3. Ejecución masiva de datos
            cur.executemany(insert_query, personajes)

            print(f"Se insertaron {len(personajes)} personajes correctamente.")

            #4. Ver datos de la tabla (dentro del mismo cursor)
            cur.execute("SELECT * FROM characters;")
            filas = cur.fetchall()

            for fila in filas:
                print(fila) 

            #5. Uso de fetchone() - Ejemplo: Buscar únicamente a Tony Stark
            cur.execute("SELECT * FROM characters WHERE name = %s;", ('Tony Stark',))
            personaje = cur.fetchone()

            # Devuelve UNA sola tupla (o None si no existe):
            # (1, 'Tony Stark', 'Dead', 'Human', 'Superhero', 'Male', 'Earth', 'Earth', ...)
            print(f"Personaje encontrado: {personaje[1]}")

            #6. Uso de fetchmany
            cur.execute("SELECT * FROM characters;")

            # Trae un bloque con los primeros 3 registros
            lote_1 = cur.fetchmany(3)  # Devuelve una lista con 3 tuplas

            # Si vuelves a llamar a fetchmany en la siguiente línea, trae los siguientes 3
            lote_2 = cur.fetchmany(3)  # Devuelve una lista con los siguientes 3 registros

except Exception as e:
  print(f"Error al insertar los datos: {e}")

