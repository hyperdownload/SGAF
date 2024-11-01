import sqlite3
import hashlib
import datetime

database_path = './database/escuela.db'

def create_database(path: str) -> None:
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alumno (
        IdAlumno INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        IdTutor INTEGER NOT NULL,
        Nombre TEXT NOT NULL,
        Apellido TEXT NOT NULL,
        DNI INTEGER,
        CUIL INTEGER,
        FechaDeNacimiento DATE NOT NULL,
        Domicilio TEXT NOT NULL,
        Genero TEXT,
        Nacionalidad TEXT,
        ProvinciaNacimiento TEXT,
        Distrito TEXT,
        Localidad TEXT,
        Calle TEXT,
        NumeroCalle INTEGER,
        Piso INTEGER,
        Torre TEXT,
        Depto TEXT,
        Telefono INTEGER,
        TelefonoCelular INTEGER,
        Activo BOOLEAN NOT NULL,
        FechaCreacion DATETIME NOT NULL,
        FOREIGN KEY (IdTutor) REFERENCES Tutor(IdTutor)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tutor (
        IdTutor INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Apellido TEXT NOT NULL,
        DNI INTEGER NOT NULL,
        Telefono INTEGER NOT NULL,
        Parentezco TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS LibroMatriz (
        IdLibroMatriz INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        FechaCreacion DATETIME NOT NULL,
        IdCalificador INTEGER NOT NULL,
        FOREIGN KEY (IdCalificador) REFERENCES Calificador(IdCalificador)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Calificador (
        IdCalificador INTEGER PRIMARY KEY AUTOINCREMENT,
        Año INTEGER NOT NULL,
        IdAlumno INTEGER NOT NULL,
        IdCalificacionMateria INTEGER NOT NULL,
        FOREIGN KEY (IdAlumno) REFERENCES Alumno(IdAlumno),
        FOREIGN KEY (IdCalificacionMateria) REFERENCES Materia(IdCalificacionMateria)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Materia (
        IdCalificacionMateria INTEGER PRIMARY KEY AUTOINCREMENT,
        NombreMateria TEXT NOT NULL,
        CalificacionMateria INTEGER NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MatriculaEncabezado (
        IdMatricula INTEGER PRIMARY KEY AUTOINCREMENT,
        FechaMatricula DATETIME NOT NULL,
        IdAlumno INTEGER NOT NULL,
        IdCurso INTEGER NOT NULL,
        FOREIGN KEY (IdAlumno) REFERENCES Alumno(IdAlumno),
        FOREIGN KEY (IdCurso) REFERENCES Curso(IdCurso)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MatriculaDetalle (
        IdMatriculaDetalle INTEGER PRIMARY KEY AUTOINCREMENT,
        IdMatricula INTEGER NOT NULL,
        TipoMatricula TEXT NOT NULL,
        Analitico BOOLEAN NOT NULL,
        Calificador BOOLEAN NOT NULL,
        FOREIGN KEY (IdMatricula) REFERENCES MatriculaEncabezado(IdMatricula)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Curso (
        IdCurso INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Turno TEXT NOT NULL,
        Activo BOOLEAN NOT NULL,
        FechaCreacion DATETIME NOT NULL,
        IdOrientacion INTEGER NOT NULL,
        FOREIGN KEY (IdOrientacion) REFERENCES Orientacion(IdOrientacion)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orientacion (
        IdOrientacion INTEGER PRIMARY KEY AUTOINCREMENT,
        NombreOrientacion TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        IdUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
        NombreUser TEXT NOT NULL,
        Password TEXT NOT NULL,
        Email TEXT NOT NULL,
        IdRango INTEGER NOT NULL,
        FOREIGN KEY (IdRango) REFERENCES Rangos(IdRango)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rangos (
        IdRango INTEGER PRIMARY KEY AUTOINCREMENT,
        NombreRango TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    INSERT OR IGNORE INTO Rangos (IdRango, NombreRango)
    VALUES 
        (1, 'Admin'),
        (2, 'Preceptor');
    ''')

    conn.commit()
    conn.close()

def register_user(user_name: str, password: str, email: str, rango: str) -> str:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('SELECT IdUsuario FROM Users WHERE Email = ?', (email,))
    if cursor.fetchone() is not None:
        conn.close()
        return "Error: ya existe un usuario con este email."

    cursor.execute('SELECT IdRango FROM Rangos WHERE NombreRango = ?', (rango,))
    rango_data = cursor.fetchone()
    if rango_data is None:
        conn.close()
        return f"Error: el rango '{rango}' no existe."

    id_rango = rango_data[0]

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute('''
    INSERT INTO Users (NombreUser, Email, Password, IdRango)
    VALUES (?, ?, ?, ?)
    ''', (user_name, email, hashed_password, id_rango))

    conn.commit()
    conn.close()

    return f"Usuario {user_name} registrado con rango {rango}."

def get_user_property(property_name: str, condition_value: str, condition_field: str = 'Email') -> any:
    """
    Obtiene una propiedad especifica de un usuario basado en una condicion.

    :param property_name: El campo que se desea obtener (ejemplo: 'NombreUser', 'Email', 'IdRango').
    :param condition_value: El valor del campo condicional (ejemplo: un correo electronico o un nombre de usuario).
    :param condition_field: El campo por el cual se va a filtrar (por defecto 'Email').
    :return: El valor de la propiedad solicitada o un mensaje de error si no se encuentra.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        cursor.execute(f'''
        SELECT {property_name} FROM Users WHERE {condition_field} = ?
        ''', (condition_value,))
        result = cursor.fetchone()
        
        if result is not None:
            return result[0]
        else:
            return f"Error: no se encontró un usuario con {condition_field} = {condition_value}"
    
    except sqlite3.Error as e:
        return f"Error en la base de datos: {e}"
    
    finally:
        conn.close()

def register_student(nombre_alumno: str, apellido_alumno: str, dni_alumno: int, fecha_nacimiento: str,
                     domicilio: str, activo: bool, nombre_tutor: str, apellido_tutor: str, dni_tutor: int,
                     telefono_tutor: int, parentezco: str, cuil: int, genero: str, nacionalidad: str,
                     provincia_nacimiento: str, distrito: str, localidad: str, calle: str,
                     numero_calle: int, piso: int, torre: str, depto: str, telefono: int,
                     telefono_celular: int) -> str:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    try:
        # Verifica y registra el tutor si no existe
        cursor.execute('SELECT IdTutor FROM Tutor WHERE DNI = ?', (dni_tutor,))
        if tutor_data := cursor.fetchone():
            id_tutor = tutor_data[0]
        else:
            cursor.execute('''
            INSERT INTO Tutor (Nombre, Apellido, DNI, Telefono, Parentezco)
            VALUES (?, ?, ?, ?, ?)
            ''', (nombre_tutor, apellido_tutor, dni_tutor, telefono_tutor, parentezco))
            id_tutor = cursor.lastrowid

        # Verifica si el alumno ya existe para evitar duplicados
        cursor.execute('SELECT IdAlumno FROM Alumno WHERE DNI = ?', (dni_alumno,))
        if cursor.fetchone() is not None:
            return "Error: ya existe un alumno con este DNI."

        # Registra al alumno con los nuevos datos
        fecha_creacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
        INSERT INTO Alumno (
            IdTutor, Nombre, Apellido, DNI, CUIL, FechaDeNacimiento, Domicilio, Genero, Nacionalidad,
            ProvinciaNacimiento, Distrito, Localidad, Calle, NumeroCalle, Piso, Torre, Depto, Telefono,
            TelefonoCelular, Activo, FechaCreacion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id_tutor, nombre_alumno.lower(), apellido_alumno.lower(), dni_alumno, cuil, fecha_nacimiento, domicilio.lower(), genero.lower(),
              nacionalidad.lower(), provincia_nacimiento.lower(), distrito.lower(), localidad.lower(), calle.lower(), numero_calle, piso, torre.lower(),
              depto.lower(), telefono, telefono_celular, activo, fecha_creacion))

        conn.commit()
        return f"Alumno {nombre_alumno} {apellido_alumno} registrado exitosamente."

    except sqlite3.Error as e:
        return f"Error en la base de datos: {e}"

    finally:
        conn.close()

def create_course(nombre: str, turno: str, activo: bool, id_orientacion: int) -> str:
    '''
    Crea un nuevo curso en la base de datos si no existe uno con el mismo nombre y turno.

    Parametros:
    nombre (str): El nombre del curso.
    turno (str): El turno en el que se impartira el curso (por ejemplo, 'Mañana', 'Tarde').
    activo (bool): Estado de actividad del curso (True si esta activo, False si está inactivo).
    id_orientacion (int): El ID de la orientación asociada al curso.

    Retorna:
    str: Un mensaje indicando si el curso fue creado exitosamente o si ocurrio un error o duplicado.
    '''
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    try:
        #Verifica si el curso ya existe para evitar duplicados
        cursor.execute('SELECT IdCurso FROM Curso WHERE Nombre = ? AND Turno = ?', (nombre, turno))
        if cursor.fetchone() is not None:
            return "Error: ya existe un curso con este nombre y turno."

        #Registra el curso
        cursor.execute('''
        INSERT INTO Curso (Nombre, Turno, Activo, FechaCreacion, IdOrientacion)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
        ''', (nombre.lower(), turno.lower(), activo, id_orientacion))
        
        conn.commit()
        return f"Curso '{nombre}' en turno '{turno}' registrado exitosamente."

    except sqlite3.Error as e:
        return f"Error en la base de datos: {e}"

    finally:
        conn.close()

def get_all_courses() -> list:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT IdCurso, Nombre, Turno, Activo, FechaCreacion FROM Curso')
        cursos = cursor.fetchall()
        return [{"IdCurso": row[0], "Nombre": row[1], "Turno": row[2], "Activo": row[3], "FechaCreacion": row[4]} for row in cursos]

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return []

    finally:
        conn.close()
        
if __name__ == '__main__':
    create_database(database_path)
    print(register_user('Sex', '1', 'b@gmail.com', 'Admin'))
