from flask import Flask, render_template, request

app = Flask(__name__)


def calcular_promedio(notas):
    return sum(notas) / len(notas)


def determinar_estado(promedio, asistencia):
    return 'APROBADO' if promedio >= 40 and asistencia >= 75 else 'REPROBADO'


def obtener_nombre_mas_largo(nombres):
    return max(nombres, key=len)


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/ejercicio1', methods=['GET', 'POST'])
def ejercicio1():
    resultado = None
    error = None
    valores = {}
    if request.method == 'POST':
        valores = {campo: request.form.get(campo, '').strip()
                   for campo in ('nota1', 'nota2', 'nota3', 'asistencia')}
        try:
            notas = [float(valores[f'nota{i}']) for i in range(1, 4)]
            asistencia = float(valores['asistencia'])
            if not all(10 <= nota <= 70 for nota in notas):
                error = 'Las notas deben estar entre 10 y 70.'
            elif not 0 <= asistencia <= 100:
                error = 'La asistencia debe estar entre 0 y 100 %.'
            else:
                promedio = calcular_promedio(notas)
                resultado = {'promedio': round(promedio, 2),
                             'estado': determinar_estado(promedio, asistencia)}
        except ValueError:
            error = 'Ingresa valores numéricos en todos los campos.'
    return render_template('ejercicio1.html', resultado=resultado,
                           error=error, valores=valores)


@app.route('/ejercicio2', methods=['GET', 'POST'])
def ejercicio2():
    resultado = None
    error = None
    valores = {}
    if request.method == 'POST':
        valores = {f'nombre{i}': request.form.get(f'nombre{i}', '').strip()
                   for i in range(1, 4)}
        nombres = list(valores.values())
        if not all(nombres):
            error = 'Completa los tres nombres.'
        elif len({nombre.casefold() for nombre in nombres}) != 3:
            error = 'Ingresa tres nombres diferentes.'
        else:
            nombre = obtener_nombre_mas_largo(nombres)
            resultado = {'nombre': nombre, 'caracteres': len(nombre)}
    return render_template('ejercicio2.html', resultado=resultado,
                           error=error, valores=valores)


@app.route('/instrucciones')
def instrucciones():
    return render_template('instrucciones.html')


if __name__ == '__main__':
    app.run(debug=True)
