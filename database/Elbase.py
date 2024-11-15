import sqlite3
import hashlib
import datetime

database_path = './database/escuela.db'

def create_database(path: str) -> None:
    """
    Crea la base de datos y las tablas necesarias para almacenar información sobre alumnos, tutores, inscripciones, datos legales y más.
    """
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Tabla Alumno completada
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alumno (
        IdAlumno INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        IdTutor INTEGER NOT NULL,
        Nombre TEXT NOT NULL,
        Apellido TEXT NOT NULL,
        DNI INTEGER,
        CUIL INTEGER NOT NULL,
        Lenguaje BOOLEAN DEFAULT 0,
        EstadoDNI TEXT ,
        FechaDeNacimiento DATE NOT NULL,
        Genero TEXT,
        Nacionalidad TEXT,
        ProvinciaNacimiento TEXT,
        DistritoNacimiento TEXT,
        LocalidadNacimiento TEXT,
        OtraNacionalidad TEXT,
        CalleResidencia TEXT,
        NumeroCalleResidencia INTEGER,
        PisoResidencia INTEGER,
        TorreResidencia TEXT,
        DeptoResidencia TEXT,
        EntreCalle1 TEXT,
        EntreCalle2 TEXT,
        ProvinciaResidencia TEXT,
        DistritoResidencia TEXT,
        LocalidadResidencia TEXT,
        Telefono INTEGER,
        Celular INTEGER,
        OtroDatoResidencia TEXT,
        CPI BOOLEAN,
        DocumentoExtranjero TEXT,
        Aborigen BOOLEAN,
        LenguaIndigena BOOLEAN,
        OtraLenguaHogar BOOLEAN,
        Transporte TEXT,
        Activo BOOLEAN DEFAULT 1,
        FechaCreacion DATETIME NOT NULL,
        -- Nuevos campos 
        Hermanos INTEGER,
        PercibeAUH BOOLEAN,
        PercibeProgresar BOOLEAN,
        Hijos BOOLEAN,
        AsistenciaSalasMaternal BOOLEAN,
        Asma BOOLEAN,
        Cardiaco BOOLEAN,
        Diabetes BOOLEAN,
        Presion BOOLEAN,
        Convulsiones BOOLEAN,
        Sanguineas BOOLEAN,
        Quemaduras BOOLEAN,
        FaltaOrgano BOOLEAN,
        Oncohematologica BOOLEAN,
        Inmunodeficiencia BOOLEAN,
        Fracturas BOOLEAN,
        OtroProblemaHuesos BOOLEAN,
        TraumatismoCraneal BOOLEAN,
        ProblemaPiel BOOLEAN,
        ProblemaVision BOOLEAN,    
        Desmayos BOOLEAN,
        DolorPecho BOOLEAN,
        Mareo BOOLEAN,
        MayorCansancio BOOLEAN,
        --Desde aqui faltan estos campos
        Palpitaciones BOOLEAN,
        DificultadRespirar BOOLEAN,       
        SalaComun BOOLEAN,
        InternacionIntesiva BOOLEAN,
        SalaComunVeces INTEGER,
        InternacionIntesivaVeces INTEGER,
        SalaComunDiagnostico TEXT,
        InternacionIntesivaDiagnostico TEXT,    
        
        Alergias BOOLEAN,
        Medicamentos BOOLEAN,
        Vacunas BOOLEAN,
        Alimento BOOLEAN,
        PicaduraInsectos BOOLEAN,
        AlergiasEstacionales BOOLEAN,
        OtrasAlergias BOOLEAN,
        MedicamentosRequirioInternacion BOOLEAN,
        VacunasRequirioInternacion BOOLEAN,
        AlimentoRequirioInternacion BOOLEAN,
        PicaduraInsectosRequirioInternacion BOOLEAN,
        AlergiasEstacionalesRequirioInternacion BOOLEAN,
        OtrasAlergiasRequirioInternacion BOOLEAN,
        DisminucionAuditiva BOOLEAN,
        DisminucionVisual BOOLEAN,
        MedicacionHabitual BOOLEAN,
        Operacion BOOLEAN,
        DisminucionAuditivaAudifonos BOOLEAN,
        DisminucionVisualLentes BOOLEAN, 
        MedicacionHabitualTipo TEXT,
        MotivoOperacion TEXT,      
        MuerteSubita BOOLEAN,
        ProblemasCardiacos BOOLEAN,
        TosCronica BOOLEAN,
        Celiaquia BOOLEAN,
        DistritoEstablecimiento TEXT,
        NombreEstablecimiento TEXT,
        NumeroEstablecimiento INTEGER,
        SectorGestion BOOLEAN,
        ClaveProvincial TEXT,
        CUE TEXT,
        PaisEstablecimientoProcedencia BOOLEAN,
        ProvinciaEstablecimientoProcedencia BOOLEAN,
        NivelModalidad TEXT,
        DistritoEstablecimientoProcedencia TEXT,
        GestionEstablecimientoProcedencia BOOLEAN,
        DependenciaEstablecimiento BOOLEAN,
        NombreEscuelaProcedencia TEXT,
        FOREIGN KEY (IdTutor) REFERENCES Tutor(IdTutor)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tutor (
        IdTutor INTEGER PRIMARY KEY AUTOINCREMENT,
        Parentezco TEXT NOT NULL,
        Nombre TEXT NOT NULL,
        Apellido TEXT NOT NULL,
        EstadoDNI TEXT NOT NULL,
        DNI INTEGER NOT NULL UNIQUE,
        CorreoElectronico TEXT,
        Telefono INTEGER NOT NULL,
        Calle TEXT NOT NULL,
        NumeroCalle INTEGER NOT NULL,
        Piso INTEGER,
        Torre TEXT,
        Depto TEXT,
        EntreCalle1 TEXT,
        EntreCalle2 TEXT,
        Provincia TEXT NOT NULL,
        Distrito TEXT NOT NULL,
        Localidad TEXT NOT NULL,
        NivelEducacionMaximo TEXT,
        NivelEducacionState TEXT,
        Actividad TEXT,
        CPI BOOLEAN,
        DocumentoExtranjero BOOLEAN,
        RecibioEducacion BOOLEAN,
        OtroDatoResidencia TEXT
        );
    ''')
    
    # Tabla Legal completada
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Legal (
        IdLegal INTEGER PRIMARY KEY AUTOINCREMENT,
        IdAlumno INTEGER NOT NULL,
        ApellidoLegal TEXT,
        TipoDocumentoLegal TEXT,
        NumeroDocumentoLegal INTEGER,
        NombreLegal TEXT,
        Restriccion TEXT,  -- Descripción de la restricción legal
        NumLegajo INTEGER,  -- Número de legajo del alumno
        NumMatriz INTEGER,  -- Número de matriz
        NumFolio INTEGER,   -- Número de folio
        FirmaResponsable TEXT,
        FechaInscripcion DATE,
        Aclaracion TEXT,
        FirmaDirectivo TEXT,
        FOREIGN KEY (IdAlumno) REFERENCES Alumno(IdAlumno)
    );
    ''')

    # Tabla Inscripcion
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Inscripcion (
        IdInscripcion INTEGER PRIMARY KEY AUTOINCREMENT,
        IdAlumno INTEGER NOT NULL,
        TipoInscripcion TEXT NOT NULL,
        Orientacion TEXT,
        Anio INTEGER,
        Turno TEXT,
        Jornada TEXT,
        CondicionInscripcion TEXT,
        Inclusivo BOOLEAN,
        EscuelaEspecial BOOLEAN,
        AsistenteExterno BOOLEAN,
        EscuelaContraturnoCEC BOOLEAN,
        EscuelaContraturnoCEF BOOLEAN,
        EscuelaContraturnoEEE BOOLEAN,
        AlimentoEscolar BOOLEAN,
        FOREIGN KEY (IdAlumno) REFERENCES Alumno(IdAlumno)
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
        Orientacion TEXT NOT NULL,
        Turno TEXT NOT NULL,
        Activo BOOLEAN NOT NULL,
        FechaCreacion DATETIME NOT NULL
    );
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AlumnoCurso (
        IdAlumno INTEGER NOT NULL,
        IdCurso INTEGER NOT NULL,
        PRIMARY KEY (IdAlumno, IdCurso),
        FOREIGN KEY (IdAlumno) REFERENCES Alumno(IdAlumno) ON DELETE CASCADE,
        FOREIGN KEY (IdCurso) REFERENCES Curso(IdCurso) ON DELETE CASCADE
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

def asign_course(student_id: int, course_id: int):
    """Asigna un curso a un estudiante en la base de datos.

    Esta función verifica si el curso y el alumno existen, y si el curso tiene menos de 30 alumnos
    antes de vincular a un estudiante con un curso específico.

    Args:
        student_id (int): El identificador único del estudiante.
        course_id (int): El identificador único del curso.

    Returns:
        str: Un mensaje que indica el éxito o fracaso de la asignación del curso.

    Raises:
        sqlite3.Error: Si hay un error durante la operación de la base de datos.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Curso WHERE IdCurso = ?', (course_id,))
        if cursor.fetchone() is None:
            conn.close()
            return "Error: El curso especificado no existe."

        cursor.execute('SELECT * FROM Alumno WHERE IdAlumno = ?', (student_id,))
        if cursor.fetchone() is None:
            conn.close()
            return "Error: El alumno especificado no existe."

        cursor.execute('SELECT COUNT(*) FROM AlumnoCurso WHERE IdCurso = ?', (course_id,))
        alumnos_en_curso = cursor.fetchone()[0]
        if alumnos_en_curso >= 30:
            conn.close()
            return "Error: El curso ha alcanzado el límite máximo de 30 alumnos."

        cursor.execute('SELECT * FROM AlumnoCurso WHERE IdAlumno = ? AND IdCurso = ?', (student_id, course_id))
        if cursor.fetchone() is not None:
            conn.close()
            return "Error: El alumno ya está asignado a este curso."

        cursor.execute('INSERT INTO AlumnoCurso (IdAlumno, IdCurso) VALUES (?,?)', (student_id, course_id))
        conn.commit()
        conn.close()
        return "Curso asignado correctamente."
    except sqlite3.Error as e:
        if conn:
            conn.close()
        return f"Error: {e}"

def get_course_with_least_students(course_ids: list) -> tuple:
    """
    Cuenta el número de alumnos en cada curso especificado y devuelve el ID del curso con menos alumnos.

    Args:
        course_ids (list): Una lista de IDs de cursos a verificar.

    Returns:
        tuple: Un tuple conteniendo el ID del curso con menos alumnos y el número de alumnos en ese curso.
               Si hay un error o no se encuentran cursos, devuelve (None, None).

    Raises:
        sqlite3.Error: Si hay un error durante la operación de la base de datos.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        course_ids_str = ','.join(map(str, course_ids))

        query = f"""
        SELECT IdCurso, COUNT(IdAlumno) as NumAlumnos
        FROM AlumnoCurso
        WHERE IdCurso IN ({course_ids_str})
        GROUP BY IdCurso
        ORDER BY NumAlumnos ASC
        LIMIT 1
        """

        cursor.execute(query)
        result = cursor.fetchone()

        conn.close()

        return result
    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return (None, None)

def obtain_course_details(course_id:int):
    """Recupera los detalles de un curso específico de la base de datos.

    Esta función consulta la tabla Curso para obtener información sobre un curso identificado por su ID único. Devuelve los detalles del curso si se encuentra, o un mensaje de error si el curso no existe.

    Args:
        course_id (int): El identificador único del curso.

    Returns:
        tuple o str: Una tupla que contiene los detalles del curso o un mensaje de error si el curso no existe.

    Raises:
        sqlite3.Error: Si hay un error durante la operación de la base de datos.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Curso WHERE IdCurso =?', (course_id,))
        course_data = cursor.fetchone()
        conn.close()
        return "Error: el curso no existe." if course_data is None else course_data
    except sqlite3.Error as e:
        conn.close()
        return f"Error: {e}"
    
def delete_student_of_course(student_id:int, course_id:int):
    """Elimina a un estudiante de un curso específico en la base de datos.

    Esta función borra la asociación entre un estudiante y un curso de la tabla AlumnoCurso. Asegura que el estudiante especificado sea eliminado del curso, gestionando cualquier error potencial durante la operación.

    Args:
        student_id (int): El identificador único del estudiante.
        course_id (int): El identificador único del curso.

    Returns:
        str: Un mensaje que indica el resultado de la operación de eliminación.

    Raises:
        sqlite3.Error: Si hay un error durante la operación de la base de datos.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM AlumnoCurso WHERE IdCurso=? AND IdAlumno=?',(course_id, student_id))
        conn.commit()
        conn.close()
        return "Alumno eliminado."
    except sqlite3.Error as e:
        return f"Error: {e}"

def enroll_student_in_course(student_id: int, year: int, turno: str, specialty: str) -> str:
    """
    Inscribe a un alumno en un curso, verificando condiciones de año, turno y especialidad.

    Args:
        student_id (int): El identificador único del estudiante.
        year (int): El año en el que se inscribe el curso.
        turno (str): El turno (mañana, tarde, noche) del curso.
        specialty (str): La especialidad del curso.

    Returns:
        str: Un mensaje que indica el éxito o fracaso de la inscripción.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Alumno WHERE IdAlumno = ?', (student_id,))
        if cursor.fetchone() is None:
            conn.close()
            return "Error: El alumno especificado no existe."

        cursor.execute(
            '''
            SELECT IdCurso FROM Curso 
            WHERE Orientacion = ? AND Turno = ? AND Activo = 1 AND strftime('%Y', FechaCreacion) = ?
            ''', (specialty, turno, str(year))
        )
        course = cursor.fetchone()
        if course is None:
            conn.close()
            return "Error: No se encontró un curso que cumpla con las condiciones especificadas."

        course_id = course[0]

        cursor.execute('SELECT COUNT(*) FROM AlumnoCurso WHERE IdCurso = ?', (course_id,))
        if cursor.fetchone()[0] >= 30:
            conn.close()
            return "Error: El curso ha alcanzado el límite máximo de 30 alumnos."

        cursor.execute('INSERT INTO AlumnoCurso (IdAlumno, IdCurso) VALUES (?, ?)', (student_id, course_id))
        conn.commit()
        conn.close()
        return "Alumno inscrito correctamente en el curso."
    except sqlite3.Error as e:
        if conn:
            conn.close()
        return f"Error en la inscripción: {e}"

def get_student_data(student_id: int) -> dict:
    """
    Obtiene los datos completos de un alumno desde la base de datos.

    Args:
        student_id (int): El identificador único del estudiante.

    Returns:
        dict: Un diccionario con los datos del alumno o un mensaje de error si no se encuentra el alumno.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Alumno WHERE IdAlumno = ?', (student_id,))
        student_data = cursor.fetchone()

        if student_data is None:
            conn.close()
            return {"Error": "El alumno especificado no existe."}

        column_names = [description[0] for description in cursor.description]
        conn.close()

        return dict(zip(column_names, student_data))
    except sqlite3.Error as e:
        if conn:
            conn.close()
        return {"Error": f"Error al obtener datos del alumno: {e}"}

# Funciones de registro de usuario
def register_user(user_name: str, password: str, email: str, rango: str) -> str:
    """
    Registra un usuario con sus datos en la base de datos.
    """
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

def register_student_and_tutor(student_data: dict, tutor_data: dict) -> str:
    """
    Registra a un nuevo alumno y su tutor en la base de datos, incluyendo los datos adicionales del tutor.
    """
    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT IdTutor FROM Tutor WHERE DNI = ?', (tutor_data["dni"],))
        tutor = cursor.fetchone()

        if tutor:
            id_tutor = tutor[0]
        else:
            print(tutor_data["estado_dni"])
            cursor.execute('''
                INSERT INTO Tutor (
                    Parentezco, Nombre, Apellido, EstadoDNI, DNI, CorreoElectronico, Telefono, Calle, NumeroCalle, Piso, Torre,
                    Depto, EntreCalle1, EntreCalle2, Provincia, Distrito, Localidad, NivelEducacionMaximo, NivelEducacionState,
                    Actividad, CPI, DocumentoExtranjero, RecibioEducacion, OtroDatoResidencia
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tutor_data["parentezco"], tutor_data["nombre"], tutor_data["apellido"], tutor_data["estado_dni"], tutor_data["dni"],
                tutor_data.get("correo"), tutor_data["telefono"], tutor_data["calle"], tutor_data["numero_calle"],
                tutor_data.get("piso"), tutor_data.get("torre"), tutor_data.get("depto"), tutor_data.get("entre_calle_1"),
                tutor_data.get("entre_calle_2"), tutor_data["provincia"], tutor_data["distrito"], tutor_data["localidad"],
                tutor_data.get("nivel_educacion_maximo"), tutor_data.get("completado"), tutor_data.get("actividad"),
                tutor_data.get("cpi"), tutor_data.get("foreign_doc-tutor"), tutor_data.get("tutor-education"),
                tutor_data.get("otrodato-domicilio-tutor")
            ))
            id_tutor = cursor.lastrowid 

        cursor.execute('SELECT IdAlumno FROM Alumno WHERE DNI = ?', (student_data["dni"],))
        if cursor.fetchone() is not None:
            return "Error: ya existe un alumno con este DNI."

        cursor.execute('''
        INSERT INTO Alumno (
            IdTutor, Nombre, Apellido, DNI, EstadoDNI, CUIL, FechaDeNacimiento, Genero, Nacionalidad, ProvinciaNacimiento, 
            DistritoNacimiento, LocalidadNacimiento, OtraNacionalidad, CalleResidencia, NumeroCalleResidencia, PisoResidencia, 
            TorreResidencia, DeptoResidencia, EntreCalle1, EntreCalle2, ProvinciaResidencia, DistritoResidencia, LocalidadResidencia, 
            Telefono, Celular, OtroDatoResidencia, CPI, DocumentoExtranjero, Aborigen,Lenguaje, LenguaIndigena, OtraLenguaHogar, Transporte, 
            Activo, FechaCreacion, Hermanos, PercibeAUH, PercibeProgresar, Hijos, AsistenciaSalasMaternal, Asma, Cardiaco, Diabetes, 
            Presion, Convulsiones, Sanguineas, Quemaduras, FaltaOrgano, Oncohematologica, Inmunodeficiencia, Fracturas, 
            ProblemaVision, TraumatismoCraneal, ProblemaPiel, Desmayos, DolorPecho, Mareo, 
            MayorCansancio, OtroProblemaHuesos,Palpitaciones,DificultadRespirar,SalaComun,InternacionIntesiva,SalaComunVeces,
            InternacionIntesivaVeces, SalaComunDiagnostico,InternacionIntesivaDiagnostico,Alergias,Medicamentos,Vacunas,Alimento,PicaduraInsectos,
            AlergiasEstacionales,OtrasAlergias,MedicamentosRequirioInternacion,VacunasRequirioInternacion,AlimentoRequirioInternacion,PicaduraInsectosRequirioInternacion,
            AlergiasEstacionalesRequirioInternacion,OtrasAlergiasRequirioInternacion,DisminucionAuditiva,DisminucionVisual,MedicacionHabitual,Operacion,
            DisminucionAuditivaAudifonos,DisminucionVisualLentes,MedicacionHabitualTipo,MotivoOperacion,MuerteSubita,ProblemasCardiacos,TosCronica,Celiaquia,
            DistritoEstablecimiento,NombreEstablecimiento,NumeroEstablecimiento,SectorGestion,ClaveProvincial,CUE,PaisEstablecimientoProcedencia,ProvinciaEstablecimientoProcedencia,
            NivelModalidad,DistritoEstablecimientoProcedencia,GestionEstablecimientoProcedencia,DependenciaEstablecimiento,NombreEscuelaProcedencia
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            id_tutor,
            student_data.get("nombre"),
            student_data.get("apellido"),
            student_data.get("dni"),
            student_data.get("estado_dni"),
            student_data.get("cuil"),
            student_data.get("fecha_nacimiento"),
            student_data.get("gender"),
            student_data.get("nacionalidad"),
            student_data.get("provincia-nacimiento-alumno-check"),
            student_data.get("distrito-alumno"),
            student_data.get("localidad-alumno"),
            student_data.get("otra-nacionalidad"),
            student_data.get("calle-alumno"),
            student_data.get("numero-calle-alumno"),
            student_data.get("piso-domicilio-alumno"),
            student_data.get("torre-domicilio-alumno"),
            student_data.get("depto-domicilio-alumno"),
            student_data.get("entre-calle-alumno"),
            student_data.get("y-calle-alumno"),
            student_data.get("provincia-residencia-alumno"),
            student_data.get("distrito-residencia-alumno"),
            student_data.get("localidad-residencia-alumno"),
            student_data.get("telefono-alumno"),
            student_data.get("telefono-celular-alumno"),
            student_data.get("otrodato-domicilio-alumno"),
            student_data.get("cpi-student"),
            student_data.get("foreign_doc"),
            student_data.get("aboriginal-descendant"),
            student_data.get("language"),
            student_data.get("other-language"),
            student_data.get("transporte"),
            student_data.get("siblings"),
            student_data.get("percibe-auh"),
            student_data.get("percibe-progresar"),
            student_data.get("children"),
            student_data.get("salas-maternales"),
            student_data.get("asma"),
            student_data.get("cardiacas"),
            student_data.get("diabetes"),
            student_data.get("presion"),
            student_data.get("convulsiones"),
            student_data.get("sanguineas"),
            student_data.get("quemaduras"),
            student_data.get("falta-organo"),
            student_data.get("oncohematologica"),
            student_data.get("inmunodeficiencias"),
            student_data.get("fracturas"),
            student_data.get("disminución-visual"),
            student_data.get("traumatismo-craneal"),
            student_data.get("problema-piel"),
            student_data.get("desmayos"),
            student_data.get("dolor-fuerte-en-el-pecho"),
            student_data.get("mareo"),
            student_data.get("mayor-cansancio"),
            
            student_data.get("otro-problema"),
            student_data.get("palpitaciones"),
            student_data.get("dificultad-respirar"),
            student_data.get("sala-comun"),
            student_data.get("internacion-intensiva"),
            student_data.get("sala-comun-cuantas-veces"),
            student_data.get('internacion-intensiva-cuantas-veces'),
            
            student_data.get('sala-comun-diagnostico'),
            student_data.get('internacion-intensiva-diagnostico'),
            student_data.get('padece-alergia'),
            student_data.get('medicamentos'),
            student_data.get('vacunas'),
            student_data.get('alimento'),
            student_data.get('picadura-insectos'),
            student_data.get('alergias-Estacionales'),
            student_data.get('otras-alergias'),
            student_data.get('medicamentos-requirio-internacion'),
            student_data.get('vacunas-requirio-internacion'),
            student_data.get('alimento-requirio-internacion'),
            student_data.get('picadura-insectos-requirio-internacion'),
            student_data.get('alergias-Estacionales-requirio-internacion'),
            student_data.get('otras-alergias-requirio-internacion'),
            student_data.get('disminucion-auditiva'),
            student_data.get('disminución-visual'),
            student_data.get('medicacion-habitual'),
            student_data.get('operacion'),
            student_data.get('disminucion-auditiva-audifonos'),
            student_data.get('disminución-visual-lentes'),
            student_data.get('medicacion-habitual-tipo'),
            student_data.get('motivo-operacion'),
            student_data.get('muerte-subita'),
            student_data.get('Diabetes'),
            student_data.get('problemas-cardíacos'),
            student_data.get('tos-cronica'),
            student_data.get('celiaquia'),
            student_data.get('distrito-establecimiento'),
            student_data.get('nombre-establecimiento'),
            student_data.get('numero-establecimiento'),
            student_data.get('sector-gestion'),
            student_data.get('clave-provincial'),
            student_data.get('cue'),
            student_data.get('pais-establecimiento-procedencia'),
            student_data.get('provincia-establecimiento-procedencia'),
            student_data.get('nivel-modalidad'),
            student_data.get('distrito-establecimiento-procedencia'),
            
            student_data.get('gestion-establecimiento-procedencia'),
            student_data.get('dependecia_establecimiento'),
            student_data.get('nombre-escuela-procedencia'),
        ))

        conn.commit()
        return f"Alumno {student_data['nombre']} {student_data['apellido']} registrado exitosamente."
    
    except sqlite3.Error as e:
        conn.rollback()  
        return f"Error en la base de datos: {e}"

    finally:
        conn.close()  

def register_legal_data(legal_data: dict) -> str:
    """
    Registra los datos legales asociados a un alumno en la tabla Legal.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Legal (IdAlumno, ApellidoLegal, TipoDocumentoLegal, NumeroDocumentoLegal, NombreLegal, Restriccion, NumLegajo, NumMatriz, NumFolio, FirmaResponsable, FechaInscripcion, Aclaracion, FirmaDirectivo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (legal_data["id_alumno"], legal_data["apellido_legal"], legal_data["tipo_documento_legal"], legal_data["numero_documento_legal"], legal_data["nombre_legal"], legal_data["restriccion"], legal_data["num_legajo"], legal_data["num_matriz"], legal_data["num_folio"], legal_data["firma_responsable"], legal_data["fecha_inscripcion"], legal_data["aclaracion"], legal_data["firma_directivo"]))

    conn.commit()
    conn.close()
    return "Datos legales registrados exitosamente."

def register_inscription(inscription_data: dict) -> str:
    """
    Registra los datos de inscripción de un alumno en la base de datos.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    # Ejecuta la inserción de datos en la tabla Inscripcion
    cursor.execute('''
    INSERT INTO Inscripcion (
        IdAlumno, TipoInscripcion, Orientacion, Anio, Turno, Jornada,
        CondicionInscripcion, Inclusivo, EscuelaEspecial, AsistenteExterno,
        EscuelaContraturnoCEC, EscuelaContraturnoCEF, EscuelaContraturnoEEE, AlimentoEscolar
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        inscription_data["id_alumno"],
        inscription_data["tipo_inscripcion"],
        inscription_data.get("orientacion"),
        inscription_data.get("anio"),
        inscription_data.get("turno"),
        inscription_data.get("jornada"),
        inscription_data.get("condicion_inscripcion"),
        bool(inscription_data.get("inclusivo", False)),
        bool(inscription_data.get("escuela_especial", False)),
        bool(inscription_data.get("asistente_externo", False)),
        bool(inscription_data.get("escuela_contraturno_cec", False)),
        bool(inscription_data.get("escuela_contraturno_cef", False)),
        bool(inscription_data.get("escuela_contraturno_eee", False)),
        bool(inscription_data.get("alimento_escolar", False))
    ))
    
    # Confirma y cierra la conexión
    conn.commit()
    conn.close()
    
    return "Inscripción registrada exitosamente."


def get_user_property(property_name: str, condition_value: str, condition_field: str = 'Email') -> any:
    """
    Obtiene una propiedad específica de un usuario basado en una condición.
    
    Args:
        property_name (str): El campo que se desea obtener (ejemplo: 'NombreUser', 'Email', 'IdRango').
        condition_value (str): El valor del campo condicional (ejemplo: un correo electrónico o un nombre de usuario).
        condition_field (str): El campo por el cual se va a filtrar (por defecto 'Email').
    
    Returns:
        any: El valor de la propiedad solicitada o un mensaje de error si no se encuentra.
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

def create_course(nombre: str, turno: str, activo: bool, orientacion: str) -> str:
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
        INSERT INTO Curso (Nombre, Turno, Activo, FechaCreacion, Orientacion)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
        ''', (nombre.lower(), turno.lower(), activo, orientacion))
        
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
        cursor.execute('SELECT IdCurso, Nombre, Turno, Activo, FechaCreacion, Orientacion FROM Curso')
        cursos = cursor.fetchall()
        return [{"IdCurso": row[0], "Nombre": row[1], "Turno": row[2], "Activo": row[3], "FechaCreacion": row[4], "Orientacion": row[5],} for row in cursos]

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        return []

    finally:
        conn.close()

def get_curso_property(property_name: str, condition_value: str, condition_field: str = 'IdCurso') -> any:
    """
    Obtiene una propiedad específica de un curso basado en una condición.

    Esta función busca en la tabla Curso de la base de datos y devuelve el valor
    de una propiedad específica para un curso que cumpla con la condición dada.

    Args:
        property_name (str): El nombre de la propiedad del curso que se desea obtener.
        condition_value (str): El valor de la condición para filtrar el curso.
        condition_field (str, optional): El campo de la tabla Curso que se usará
            para filtrar. Por defecto es 'IdCurso'.

    Returns:
        any: El valor de la propiedad solicitada si se encuentra el curso.
             Si no se encuentra el curso, devuelve un mensaje de error.
             En caso de error en la base de datos, devuelve un mensaje con la descripción del error.

    Raises:
        sqlite3.Error: Si ocurre un error al interactuar con la base de datos.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        cursor.execute(f'''
        SELECT {property_name} FROM Curso WHERE {condition_field} = ?
        ''', (condition_value,))
        result = cursor.fetchone()
        
        if result is not None:
            return result[0]
        else:
            return f"Error: no se encontró un curso con {condition_field} = {condition_value}"
    
    except sqlite3.Error as e:
        return f"Error en la base de datos: {e}"
    
    finally:
        conn.close()

def get_total_cursos() -> int:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        cursor.execute('''
        SELECT MAX(IdCurso) FROM Curso
        ''')
        result = cursor.fetchone()

        return int(result[0]) if result is not None else "Error:"
    except sqlite3.Error as e:
        return f"Error en la base de datos: {e}"

    finally:
        conn.close()

if __name__ == '__main__':
    create_database(database_path)

    print(register_user('Sex', '1', 'b@gmail.com', 'Admin'))
