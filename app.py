from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import re

app = Flask(__name__)
app.secret_key = 'Villomax'
datos = pd.read_excel("datospersonales.xlsx")

def search_nombre(patron):
    datos[['Clave', 'Nombre', 'Correo', 'Telefono']] = datos[['Clave', 'Nombre', 'Correo', 'Telefono']].fillna('')
    coincidence_nombre = datos[datos['Nombre'].str.contains(patron, na=False, flags=re.IGNORECASE, regex=True)]
    return coincidence_nombre[['Clave', 'Nombre', 'Correo', 'Telefono']]

def search_correo(patron):
    datos[['Clave', 'Nombre', 'Correo', 'Telefono']] = datos[['Clave', 'Nombre', 'Correo', 'Telefono']].fillna('')
    coincidence_correo = datos[datos['Correo'].str.contains(patron, na=False, flags=re.IGNORECASE, regex=True)]
    return coincidence_correo[['Clave', 'Nombre', 'Correo', 'Telefono']]

def verificar_credenciales(usuario, contrasena):
    return usuario == 'David' and contrasena == 'Pr!ncesa29'

@app.route('/')
def index():
    if 'usuario' in session:
        return render_template('Formulario.html')
    else:
        return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if verificar_credenciales(usuario, contrasena):
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            return render_template('index.html', mensaje='Usuario o contraseña incorrectos')
    return render_template('index.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/Lista', methods=['POST'])
def lista():
    opcion = request.form.get('opcion', '')  # Obtener la opción seleccionada (nombre o correo)
    patron = request.form.get('patron', '')  # Obtener el patrón de búsqueda
    
    if opcion == 'nombre':
        result = search_nombre(patron)
    elif opcion == 'correo':
        result = search_correo(patron)
    else:
        result = pd.DataFrame()  # Opción inválida

    if not result.empty:
        resultados = result.to_dict(orient='records')
    else:
        resultados = None
    return render_template('Formulario.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
