from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response, g
from urllib.parse import quote
import database.Elbase as base
from flask import jsonify
import json
import hashlib

app = Flask(__name__)
app.secret_key = 'supersecretkey' #algo mucho muy importante para que funcione flash

def no_cache(response): #Borra la cache para no guardar las sesiones
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.errorhandler(405)
def page_not_found(e):
    return render_template('404.html'), 405

@app.before_request #Para el menu de los usuarios
def load_user_data():
    if 'user' in session:
        g.email = session['user']
        g.nombre = base.get_user_property('NombreUser', g.email)
    else:
        g.email = None
        g.nombre = None

@app.route('/', methods= ['GET','POST']) 
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if hashlib.sha256(password.encode()).hexdigest() == base.get_user_property('Password', email):
            session['user'] = email  
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos. Inténtalo de nuevo.')
    return render_template("login.html")
# --------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
# --------------------------------------------------
@app.route('/Recuperar-contraseña')
def forgot_password():
    return render_template("forgotPassword.html")
# --------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    cursos_data = base.get_total_cursos()
    print(cursos_data) 
    response = make_response(render_template("dashboard.html", total_cursos=cursos_data))
    return no_cache(response)

@app.route("/Nuevo-alumno")
def new_student():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("new-student.html")

def obtener_primer_numero(cadena): # obtiene el primer numero de un string, lo cree para obtener el año de los cursos
    for char in cadena:
        if char.isdigit():
            return int(char)
    return None

@app.route('/submit', methods=['POST'])
def formulario():

    student_data = {
        'nombre': request.form.get('nombre-alumno'),
        'apellido': request.form.get('apellido-alumno'),
        'dni': request.form.get('dni-student'),
        'estado_dni': request.form.get('dni-student-state'),
        'cuil': request.form.get('cuil-student'),
        'fecha_nacimiento': request.form.get('fechaNacimiento'),
        'gender': request.form.get('gender'),
        'nacionalidad': request.form.get('lugar-nacimiento-check'),
        'provincia-nacimiento-alumno-check': request.form.get('provincia-nacimiento-alumno-check'), #Bs As o Otra
        'provincia-nacimiento-alumno': request.form.get('provincia-nacimiento-alumno'), #Otra provincia input no esta¿
        'distrito-alumno': request.form.get('distrito-alumno'),
        'localidad-alumno': request.form.get('localidad-alumno'),

        'otra-nacionalidad': request.form.get('Nacionalidad-alumno'), #no esta¿

        'calle-alumno': request.form.get('calle-alumno'),
        'numero-calle-alumno': request.form.get('numero-calle-alumno'),
        'piso-domicilio-alumno': request.form.get('piso-domicilio-alumno'),
        'torre-domicilio-alumno': request.form.get('torre-domicilio-alumno'),
        'depto-domicilio-alumno': request.form.get('depto-domicilio-alumno'),
        'entre-calle-alumno': request.form.get('entre-calle-alumno'),
        'y-calle-alumno': request.form.get('y-calle-alumno'),
        'provincia-residencia-alumno': request.form.get('provincia-residencia-alumno'),
        'distrito-residencia-alumno': request.form.get('distrito-residencia-alumno'),
        'localidad-residencia-alumno': request.form.get('localidad-residencia-alumno'),
        'telefono-alumno': request.form.get('telefono-alumno'),
        'telefono-celular-alumno': request.form.get('telefono-celular-alumno'),
        'otrodato-domicilio-alumno': request.form.get('otrodato-domicilio-alumno'),

        'cpi-student': request.form.get('cpi-student'),
        'foreign_doc': request.form.get('foreign_doc'),

        'aboriginal-descendant': request.form.get('aboriginal-descendant'),
        'other-language': request.form.get('other-language'),
        'language': request.form.get('language'),
        'transporte': request.form.get('transport'),

        'siblings': request.form.get('siblings'),
        'percibe-auh': request.form.get('percibe-auh'),
        'percibe-progresar': request.form.get('percibe-progresar'),
        'children': request.form.get('children'),
        'salas-maternales': request.form.get('salas-maternales'),

        'asma': request.form.get('asma'),
        'cardiacas': request.form.get('cardiacas'),
        'diabetes': request.form.get('diabetes'),
        'presion': request.form.get('presion'),
        'convulsiones': request.form.get('convulsiones'),
        'sanguineas': request.form.get('sanguineas'),
        'quemaduras': request.form.get('quemaduras'),
        'falta-organo': request.form.get('falta-organo'),
        'oncohematologica': request.form.get('oncohematologica'),
        'inmunodeficiencias': request.form.get('inmunodeficiencias'),
        'fracturas': request.form.get('fracturas'),
        'otro-problema': request.form.get('otro-problema'),
        'traumatismo-craneal': request.form.get('traumatismo-craneal'),
        'problema-piel': request.form.get('problema-piel'),

        'desmayos': request.form.get('desmayos'),
        'dolor-fuerte-en-el-pecho': request.form.get('dolor-fuerte-en-el-pecho'),
        'mareo': request.form.get('mareo'),
        'mayor-cansancio': request.form.get('mayor-cansancio'),
        'palpitaciones': request.form.get('palpitaciones'),
        'dificultad-respirar': request.form.get('dificultad-respirar'),

        'sala-comun': request.form.get('sala-comun'),
        'internacion-intensiva': request.form.get('internacion-intensiva'),
        'sala-comun-cuantas-veces': request.form.get('sala-comun-cuantas-veces'),
        'internacion-intensiva-cuantas-veces': request.form.get('internacion-intensiva-cuantas-veces'),
        'sala-comun-diagnostico': request.form.get('sala-comun-diagnostico'),
        'internacion-intensiva-diagnostico': request.form.get('internacion-intensiva-diagnostico'),

        'padece-alergia': request.form.get('padece-alergia'),
        'medicamentos': request.form.get('medicamentos'),
        'vacunas': request.form.get('vacunas'),
        'alimento': request.form.get('alimento'),
        'picadura-insectos': request.form.get('picadura-insectos'),
        'alergias-Estacionales': request.form.get('alergias-Estacionales'),
        'otras-alergias': request.form.get('otras-alergias'),

        'medicamentos-requirio-internacion': request.form.get('medicamentos-requirio-internacion'),
        'vacunas-requirio-internacion': request.form.get('vacunas-requirio-internacion'),
        'alimento-requirio-internacion': request.form.get('alimento-requirio-internacion'),
        'picadura-insectos-requirio-internacion': request.form.get('picadura-insectos-requirio-internacion'),
        'alergias-Estacionales-requirio-internacion': request.form.get('alergias-Estacionales-requirio-internacion'),
        'otras-alergias-requirio-internacion': request.form.get('otras-alergias-requirio-internacion'),


        'disminucion-auditiva': request.form.get('disminucion-auditiva'),
        'disminución-visual': request.form.get('disminución-visual'),
        'medicacion-habitual': request.form.get('medicacion-habitual'),
        'operacion': request.form.get('operacion'),

        'disminucion-auditiva-audifonos': request.form.get('disminucion-auditiva-audifonos'),
        'disminución-visual-lentes': request.form.get('disminución-visual-lentes'),

        'medicacion-habitual-tipo': request.form.get('medicacion-habitual-tipo'),
        'motivo-operacion': request.form.get('motivo-operacion'),

        'muerte-subita': request.form.get('muerte-subita'),
        'Diabetes': request.form.get('Diabetes'),
        'problemas-cardíacos': request.form.get('problemas-cardíacos'),

        'tos-cronica': request.form.get('tos-cronica'),
        'celiaquia': request.form.get('celiaquia'),

        'distrito-establecimiento': request.form.get('distrito-establecimiento'),
        'nombre-establecimiento': request.form.get('nombre-establecimiento'),
        'numero-establecimiento': request.form.get('numero-establecimiento'),

        'sector-gestion': request.form.get('sector-gestion'),
        'clave-provincial': request.form.get('clave-provincial'),
        'cue': request.form.get('cue'),
        'pais-establecimiento-procedencia': request.form.get('pais-establecimiento-procedencia'),
        'provincia-establecimiento-procedencia': request.form.get('provincia-establecimiento-procedencia'),
        'nivel-modalidad': request.form.get('nivel-modalidad'),
        'distrito-establecimiento-procedencia': request.form.get('distrito-establecimiento-procedencia'),
        'gestion-establecimiento-procedencia': request.form.get('gestion-establecimiento-procedencia'),
        'dependecia_establecimiento': request.form.get('dependecia_establecimiento'),
        'nombre-escuela-procedencia': request.form.get('nombre-escuela-procedencia'),
    }
    
    tutor_data = {
        'parentezco': request.form.get('tutor-vinculo'),
        'nombre': request.form.get('nombre-tutoe'),
        'apellido': request.form.get('apellido-tutor'),
        'dni': request.form.get('dni-tutor'),#dni
        'estado_dni': request.form.get('tutor-dni'),#Estado dni
        'correo': request.form.get('correo-tutor'),
        'telefono': request.form.get('telefono-tutor'),
        'calle': request.form.get('calle-tutor'),
        'numero_calle': request.form.get('numero-calle-tutor'),
        'piso': request.form.get('piso-domicilio-tutor'),
        'torre': request.form.get('torre-domicilio-tutor'),
        'depto': request.form.get('depto-domicilio-tutor'),
        'entre_calle_1': request.form.get('entre-calle-tutor'),
        'entre_calle_2': request.form.get('y-calle-tutor'),
        'provincia': request.form.get('provincia-residencia-tutor'),
        'distrito': request.form.get('distrito-residencia-tutor'),
        'localidad': request.form.get('localidad-residencia-tutor'),
        'nivel_educacion_maximo': request.form.get('nivel-cursada'),
        'completado': request.form.get('nivel-cursada-state'),
        'actividad': request.form.get('con-actividad'),
        'cpi': request.form.get('cpi-tutor'),
        
        'foreign_doc-tutor': request.form.get('foreign_doc-tutor'),
        'tutor-education': request.form.get('tutor-education'),
        'otrodato-domicilio-tutor': request.form.get('otrodato-domicilio-tutor'),
    }
    
    inscription_data = {
        "id_alumno": 1,
        'tipo_inscripcion': request.form.get('type_registration'),
        'orientacion': request.form.get('orientation'),
        'anio': request.form.get('year_registration_fields'),
        'turno': request.form.get('request_shift_fields'),
        'jornada': request.form.get('request_workday_fields'),
        'condicion_inscripcion': request.form.get('registration_conditiony_fields'),
        'inclusivo': request.form.get('proyecto-inclusion'),
        'asistente_externo': request.form.get('acompañante-externo'),
        'escuela_contraturno': request.form.get('proyecto-inclusion-true'),
        'escuela_contraturno_cec': request.form.get('complementary_institution_cec'),
        'escuela_contraturno_cef': request.form.get('complementary_institution_cef'),
        'escuela_contraturno_eee': request.form.get('complementary_institution_eee'),
        'alimento-escolar': request.form.get('alimento-escolar'),  
    }

    legal_data = {
        "id_alumno": 1,
        'apellido_legal': request.form.get('last_name_legals'),
        'tipo_documento_legal': request.form.get('doc_type_legals'),
        'numero_documento_legal': request.form.get('doc_number_legals'),
        'nombre_legal': request.form.get('name_legals'),
        'restriccion': request.form.get('restriction_legal'),

        'num_legajo': request.form.get('n_legajo_legals'),
        'num_matriz': request.form.get('n_matriz_legal'),
        'num_folio': request.form.get('n_folio_legal'),

        'firma_responsable': request.form.get('person_in_charge'),
        'fecha_inscripcion': request.form.get('registration_date'),
        'aclaracion': request.form.get('clarification'),
        'firma_directivo': request.form.get('director_signature'),
    }
    base.register_student_and_tutor(student_data, tutor_data)
    # base.register_legal_data(legal_data)
    base.register_inscription(inscription_data)

    orientacion= request.form.get('orientation')
    turno= request.form.get('request_shift_fields')
    anio = request.form.get('year_registration_fields')
    
    # cursos_data = base.get_total_cursos()
    student_id = base.obtain_max_id_student()

    print( student_id, anio, turno.lower(), orientacion.lower())
    result = base.enroll_student_in_course(student_id= student_id, year= anio, turno= turno.lower(), specialty= "Orientacion")
    print(result)

    return "Datos recibidos", 204

@app.route("/cursos")
def curso():
    if 'user' not in session:
        return redirect(url_for('login'))
    cursos_data = base.get_total_cursos()
    nom = []
    orient = [] 
    turno_list = []
    url = []
    for n in range(cursos_data):
        curso = base.get_curso_property('Nombre', n + 1)
        orientacion = base.get_curso_property('orientacion', n + 1)
        turno = base.get_curso_property('Turno', n + 1)
        curso_url = quote(curso.replace(" ", "-").lower())
        nom.append(curso)
        orient.append(orientacion)
        turno_list.append(turno)
        url.append(curso_url)
    return render_template("cursos.html", cursos=nom , orientacion= orient, turnos = turno_list, url= url) 

@app.route("/nuevoCurso")
def nuevoCurso():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("nuevo-cursos.html")

@app.route("/Nuevo-curso-logica" , methods=['POST']) 
def nuevocursologica():
    # Aca se obtienen los datos zz
    nombre_curso = request.form.get("nombre-curso")
    orientation_options = request.form.get("orientation-options")
    turno_options = request.form.get("turno-options")
    anio_curso = obtener_primer_numero(nombre_curso)
    # Crear el curso en la base de datos
    base.create_course(nombre_curso, turno_options, True, orientation_options, anio_curso)

    return redirect(url_for('curso'))

@app.route('/get-carta-template')
def get_carta_template():
    return render_template('/components/carta.html')

@app.route("/cursos/<int:curso_id>-<nombre_curso>")
def cursos_grilla(curso_id,nombre_curso):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    nombre_curso = nombre_curso.replace("-", " ")
    curso = base.get_curso_property('Nombre', curso_id)
    orientacion = base.get_curso_property('orientacion', curso_id)
    turno = base.get_curso_property('Turno', curso_id)
    
    # Pasa los datos del curso a la plantilla
    return render_template("plantillaListadoCursos.html", cursos=curso, orientacion=orientacion, turno=turno)

def run_server():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'
    
    return app

if __name__ == '__main__':
    app.run(debug=True)
