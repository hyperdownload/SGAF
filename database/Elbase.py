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

    # Tabla Alumno
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alumno (
        IdAlumno INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        IdTutor INTEGER NOT NULL,
        Nombre TEXT NOT NULL,
        Apellido TEXT NOT NULL,
        DNI INTEGER,
        EstadoDNI TEXT CHECK(EstadoDNI IN ('Argentino', 'Extranjero', 'En proceso')),
        CUIL INTEGER,
        FechaDeNacimiento DATE NOT NULL,
        Genero TEXT,
        Nacionalidad TEXT,
        ProvinciaNacimiento TEXT,
        DistritoNacimiento TEXT,
        LocalidadNacimiento TEXT,
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
        TelefonoCelular INTEGER,
        OtroDatoResidencia TEXT,
        CPI BOOLEAN,
        DocumentoExtranjero TEXT,
        Aborigen BOOLEAN,
        LenguaIndigena BOOLEAN,
        OtraLenguaHogar BOOLEAN,
        Transporte TEXT,
        Activo BOOLEAN NOT NULL,
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
                   
        Desmayos BOOLEAN,
        DolorPecho BOOLEAN,
        Mareo BOOLEAN,
        MayorCansancio BOOLEAN,
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
        Diabetes BOOLEAN,
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
        NombreEscuelaProcedencia TEXT

                   
        FOREIGN KEY (IdTutor) REFERENCES Tutor(IdTutor)
    );
    ''')

    # Tabla Tutor
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Tutor (
        IdTutor INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL,
        Apellido TEXT NOT NULL,
        DNI INTEGER NOT NULL,
        EstadoDNI TEXT CHECK(EstadoDNI IN ('Argentino', 'Extranjero', 'En proceso')),
        CUIL INTEGER,
        CorreoElectronico TEXT,
        Telefono INTEGER NOT NULL,
        TelefonoCelular INTEGER,
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
        Completado BOOLEAN,
        Actividad TEXT,
        Parentezco TEXT NOT NULL,
        CPI BOOLEAN,                     
        AsistenciaEducativa BOOLEAN,     
        CondicionActividad TEXT          
    );
    ''')

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
        AsistenteExterno BOOLEAN,      
        EscuelaContraturno BOOLEAN,     
        MaestriaInclusiva BOOLEAN,     
        FOREIGN KEY (IdAlumno) REFERENCES Alumno(IdAlumno)
    );
    ''')

    # Tabla Legal
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Legal (
        IdLegal INTEGER PRIMARY KEY AUTOINCREMENT,
        IdAlumno INTEGER NOT NULL,
        ApellidoLegal TEXT,
        TipoDocumentoLegal TEXT,
        NumeroDocumentoLegal INTEGER,
        NombreLegal TEXT,
        Restriccion TEXT,
        NumLegajo INTEGER,
        NumMatriz INTEGER,
        NumFolio INTEGER,
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
        AsistenteExterno BOOLEAN,
        EscuelaContraturno BOOLEAN,
        MaestriaInclusiva BOOLEAN,
        FOREIGN KEY (IdAlumno) REFERENCES Alumno(IdAlumno)
    );
    ''')

    conn.commit()
    conn.close()

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
    Registra a un nuevo alumno y su tutor en la base de datos, incluyendo los datos adicionales de tutor.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('SELECT IdTutor FROM Tutor WHERE DNI = ?', (tutor_data["dni"],))
    if tutor := cursor.fetchone():
        id_tutor = tutor[0]
    else:
        cursor.execute('''
        INSERT INTO Tutor (Nombre, Apellido, DNI, EstadoDNI, CUIL, CorreoElectronico, Telefono, TelefonoCelular, Calle, NumeroCalle, Piso, Torre, Depto, EntreCalle1, EntreCalle2, Provincia, Distrito, Localidad, NivelEducacionMaximo, Completado, Actividad, Parentezco, CPI, AsistenciaEducativa, CondicionActividad)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tutor_data["nombre"], tutor_data["apellido"], tutor_data["dni"], tutor_data["estado_dni"], tutor_data.get("cuil"), tutor_data.get("correo"), tutor_data["telefono"], tutor_data.get("telefono_celular"), tutor_data["calle"], tutor_data["numero_calle"], tutor_data.get("piso"), tutor_data.get("torre"), tutor_data.get("depto"), tutor_data.get("entre_calle_1"), tutor_data.get("entre_calle_2"), tutor_data["provincia"], tutor_data["distrito"], tutor_data["localidad"], tutor_data.get("nivel_educacion_maximo"), tutor_data.get("completado"), tutor_data.get("actividad"), tutor_data["parentezco"], tutor_data.get("cpi"), tutor_data.get("asistencia_educativa"), tutor_data.get("condicion_actividad")))
        id_tutor = cursor.lastrowid

    cursor.execute('SELECT IdAlumno FROM Alumno WHERE DNI = ?', (student_data["dni"],))
    if cursor.fetchone() is not None:
        conn.close()
        return "Error: ya existe un alumno con este DNI."

    cursor.execute('''
    INSERT INTO Alumno (IdTutor, Nombre, Apellido, DNI, EstadoDNI, CUIL, FechaDeNacimiento, Genero, Nacionalidad, ProvinciaNacimiento, DistritoNacimiento, LocalidadNacimiento, CalleResidencia, NumeroCalleResidencia, PisoResidencia, TorreResidencia, DeptoResidencia, EntreCalle1, EntreCalle2, ProvinciaResidencia, DistritoResidencia, LocalidadResidencia, Telefono, TelefonoCelular, OtroDatoResidencia, CPI, DocumentoExtranjero, Aborigen, LenguaIndigena, OtraLenguaHogar, Transporte, Activo, FechaCreacion, Hermanos, Lenguaje, PercibeAUH, PercibeProgresar, AsistenciaSalasMaternal, Asma, Cardiaco, Diabetes, Presion, Convulsiones, Quemaduras, Alergias, Oncohematologica, FaltaOrgano, Inmunodeficiencia, Fracturas, ProblemaVision, TraumatismoCraneal, ProblemaPie, Desmayos, DolorPecho, Mareo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id_tutor, student_data["nombre"], student_data["apellido"], student_data["dni"], student_data["estado_dni"], student_data.get("cuil"), student_data["fecha_nacimiento"], student_data.get("genero"), student_data.get("nacionalidad"), student_data.get("provincia_nacimiento"), student_data.get("distrito_nacimiento"), student_data.get("localidad_nacimiento"), student_data.get("calle_residencia"), student_data.get("numero_calle_residencia"), student_data.get("piso_residencia"), student_data.get("torre_residencia"), student_data.get("depto_residencia"), student_data.get("entre_calle_1"), student_data.get("entre_calle_2"), student_data.get("provincia_residencia"), student_data.get("distrito_residencia"), student_data.get("localidad_residencia"), student_data.get("telefono"), student_data.get("telefono_celular"), student_data.get("otro_dato_residencia"), student_data.get("cpi"), student_data.get("documento_extranjero"), student_data.get("aborigen"), student_data.get("lengua_indigena"), student_data.get("otra_lengua_hogar"), student_data.get("transporte"), student_data.get("activo"), student_data.get("hermanos"), student_data.get("lenguaje"), student_data.get("percibe_auh"), student_data.get("percibe_progresar"), student_data.get("asistencia_salas_maternal"), student_data.get("asma"), student_data.get("cardiaco"), student_data.get("diabetes"), student_data.get("presion"), student_data.get("convulsiones"), student_data.get("quemaduras"), student_data.get("alergias"), student_data.get("oncohematologica"), student_data.get("falta_organo"), student_data.get("inmunodeficiencia"), student_data.get("fracturas"), student_data.get("problema_vision"), student_data.get("traumatismo_craneal"), student_data.get("problema_pie"), student_data.get("desmayos"), student_data.get("dolor_pecho"), student_data.get("mareo")))

    conn.commit()
    conn.close()
    return f"Alumno {student_data['nombre']} {student_data['apellido']} registrado exitosamente."

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
    cursor.execute('''
    INSERT INTO Inscripcion (IdAlumno, TipoInscripcion, Orientacion, Anio, Turno, Jornada, CondicionInscripcion, Inclusivo, AsistenteExterno, EscuelaContraturno, MaestriaInclusiva)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (inscription_data["id_alumno"], inscription_data["tipo_inscripcion"], inscription_data.get("orientacion"), inscription_data.get("anio"), inscription_data.get("turno"), inscription_data.get("jornada"), inscription_data.get("condicion_inscripcion"), inscription_data.get("inclusivo"), inscription_data.get("asistente_externo"), inscription_data.get("escuela_contraturno"), inscription_data.get("maestria_inclusiva")))

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

if __name__ == '__main__':
    create_database(database_path)

    print(register_user('Sex', '1', 'b@gmail.com', 'Admin'))
