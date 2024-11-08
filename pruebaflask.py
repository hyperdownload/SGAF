from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import database.Elbase as base
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

@app.route('/', methods= ['GET','POST']) 
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        # nombre = base.get_user_property('NombreUser', email)
        print(hashlib.sha256(password.encode()).hexdigest() , base.get_user_property('Password', email))
        #OBVIAMENTE CAMBIAR LOGICA
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
    response = make_response(render_template("dashboard.html", email=session['user']))
    return no_cache(response)
    
@app.route("/Nuevo-alumno")
def new_student():
    return render_template("new-student.html")
    

@app.route('/submit', methods=['POST'])
def formulario():
    # data = request.form #con esta linea obtiene todos los datos

    student_data = {
        'nombre-alumno': request.form.get('nombre-alumno'),
        'apellido-alumno': request.form.get('apellido-alumno'),
        'dni-student': request.form.get('dni-student'),
        'dni-student-state': request.form.get('dni-student-state'),
        'cuil-student': request.form.get('cuil-student'),
        'fechaNacimiento': request.form.get('fechaNacimiento'),
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
        'transport': request.form.get('transport'),

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
        'tutor-vinculo': request.form.get('tutor-vinculo'),
        'nombre-tutoe': request.form.get('nombre-tutoe'),
        'apellido-tutor': request.form.get('apellido-tutor'),
        'tutor-dni': request.form.get('tutor-dni'),#Estado dni
        'dni-tutor': request.form.get('dni-tutor'),#dni
        'cpi-tutor': request.form.get('cpi-tutor'),
        'foreign_doc-tutor': request.form.get('foreign_doc-tutor'),
        'tutor-education': request.form.get('tutor-education'),
        'nivel-cursada': request.form.get('nivel-cursada'),
        'nivel-cursada-state': request.form.get('nivel-cursada-state'),
        'con-actividad': request.form.get('con-actividad'),
        'calle-tutor': request.form.get('calle-tutor'),
        'entre-calle-tutor': request.form.get('entre-calle-tutor'),
        'y-calle-tutor': request.form.get('y-calle-tutor'),
        'provincia-residencia-tutor': request.form.get('provincia-residencia-tutor'),
        'distrito-residencia-tutor': request.form.get('distrito-residencia-tutor'),
        'telefono-tutor': request.form.get('telefono-tutor'),

        'numero-calle-tutor': request.form.get('numero-calle-tutor'),
        'piso-domicilio-tutor': request.form.get('piso-domicilio-tutor'),
        'torre-domicilio-tutor': request.form.get('torre-domicilio-tutor'),
        'depto-domicilio-tutor': request.form.get('depto-domicilio-tutor'),
        'otrodato-domicilio-tutor': request.form.get('otrodato-domicilio-tutor'),
        'localidad-residencia-tutor': request.form.get('localidad-residencia-tutor'),
        'correo-tutor': request.form.get('correo-tutor'),
    }
    
    inscription_data = {
        'type_registration': request.form.get('type_registration'),
        'orientation': request.form.get('orientation'),
        'year_registration_fields': request.form.get('year_registration_fields'),
        'request_shift_fields': request.form.get('request_shift_fields'),
        'request_workday_fields': request.form.get('request_workday_fields'),
        'registration_conditiony_fields': request.form.get('registration_conditiony_fields'),
        'proyecto-inclusion': request.form.get('proyecto-inclusion'),
        'proyecto-inclusion-true': request.form.get('proyecto-inclusion-true'),
        'acompañante-externo': request.form.get('acompañante-externo'),
        'complementary_institution_cec': request.form.get('complementary_institution_cec'),
        'complementary_institution_cef': request.form.get('complementary_institution_cef'),
        'complementary_institution_eee': request.form.get('complementary_institution_eee'),
        'alimento-escolar': request.form.get('alimento-escolar'),  
    }

    legal_data = {
        'last_name_legals': request.form.get('last_name_legals'),
        'doc_type_legals': request.form.get('doc_type_legals'),
        'doc_number_legals': request.form.get('doc_number_legals'),
        'name_legals': request.form.get('name_legals'),
        'restriction_legal': request.form.get('restriction_legal'),

        'n_legajo_legals': request.form.get('n_legajo_legals'),
        'n_matriz_legal': request.form.get('n_matriz_legal'),
        'n_folio_legal': request.form.get('n_folio_legal'),

        'person_in_charge': request.form.get('person_in_charge'),
        'registration_date': request.form.get('registration_date'),
        'clarification': request.form.get('clarification'),
        'director_signature': request.form.get('director_signature'),
    }
    
    print(student_data,"\n",tutor_data,"\n",inscription_data,"\n",legal_data)
    return "Datos recibidos", 204

@app.route("/cursos")
def curso():
    # cursos = base.get_all_courses()  # Obtener la lista de cursos desde la base de datos
    a = base.get_total_cursos()
    nom=[]
    for n in range(a):

        curso = base.get_curso_property('Nombre', n+1)
        nom.append(curso)
    print(nom)
    return render_template("cursos.html", cursos=nom)
    
   # Obtener la lista de cursos de la base de datos

@app.route("/nuevoCurso")
def nuevoCurso():
    return render_template("nuevo-cursos.html")

@app.route("/Nuevo-curso-logica" , methods=['POST']) 
def nuevocursologica():
    # Aca se obtienen los datos zz
    nombre_curso = request.form.get("nombre-curso")
    orientation_options = request.form.get("orientation-options")
    turno_options = request.form.get("turno-options")
    # Crear el curso en la base de datos
    base.create_course(nombre_curso, turno_options, True, orientation_options)

    # Redirigir a la página de cursos después de crear el curso
    return redirect(url_for('curso'))

@app.route('/get-carta-template')
def get_carta_template():
    return render_template('/components/carta.html')
    
if __name__ == '__main__':
    app.run(debug=True)
