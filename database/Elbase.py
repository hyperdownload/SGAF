import sqlite3
import hashlib
database_path = '.\database\escuela.db'

def create_database(path:str)->None:
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alumno (
        IdAlumno INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        IdTutor INTEGER NOT NULL,
        Nombre TEXT NOT NULL,
        Apellido TEXT NOT NULL,
        DNI INTEGER NOT NULL,
        FechaDeNacimiento DATE NOT NULL,
        Domicilio TEXT NOT NULL,
        Activo BOOLEAN NOT NULL,
        FechaCreacion DATETIME NOT NULL
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
        FechaCreacion INTEGER NOT NULL,
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
        IdMatricula INTEGER PRIMARY KEY AUTOINCREMENT,
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
        Email TEXT NOT NULL
    );
    ''')

    conn.commit()
    conn.close()

def register_user(user_name:str, password:str, email:str)->None:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT IdUsuario FROM Users WHERE email = ?', (email,))
    if cursor.fetchone() is not None:
        print("Error: ya existe un usuario con este email.")
        conn.close()
        return "Error: ya existe un usuario con este email."

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute('''
    INSERT INTO Users (NombreUser, Email, Password)
    VALUES (?, ?, ?)
    ''', (user_name, email, hashed_password))

    conn.commit()
    conn.close()

    return(f"Usuario {user_name} registrado.")

def get_property_user(x:str, y:str)->any:
    '''
        x = El elemento a seleccionar de la tabla Users
        y = El elemento condicional a obtener 
    '''
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(f'''
    SELECT {x} FROM Users WHERE Email = ?
    ''', (y,))
    dat = cursor.fetchone()
    conn.commit()
    conn.close()
    return dat[0]

if __name__ == '__main__':
    create_database(database_path)
    register_user('a','1','b@gmail.com')