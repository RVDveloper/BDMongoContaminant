from flask import Flask, render_template, request
from analysis.PollutionAnalytics import GetDailyPollutionData, GetDataForTable, GetDailyPollutionGraph

app = Flask(__name__)

# Routes
@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/Datos", methods=['POST'])
def Datos():
    if request.method == 'POST':
        day = int(request.form['Day'])
        neighborhood = request.form['Neighbourhood']
        # GetDailyPollutionData(day, neighborhood)
        data = GetDataForTable(day, neighborhood)
        return render_template('tempo.html', day=day, neighborhood=neighborhood, data=data)
    

@app.route("/get_daily_pollution_data", methods=['POST'])
def get_daily_pollution_data():
    if request.method == 'POST':
        day = int(request.form['Day'])
        neighborhood = request.form['Neighbourhood']
        pollution_data = GetDailyPollutionGraph(day, neighborhood)
        
        
        barrios_imagenes = {
            'el Poblenou': '../static/img/poblenoutitulo.jpg',
            'Sants': '../static/img/sants.jpg',
            'la Nova Esquerra de l\'Eixample': '../static/img/eixample.jpg',
            'la Vila de Gracia': '../static/img/vilagracia.jpg',
            'Sant Pere, Santa Caterina i la Ribera': '../static/img/santpere.jpg',
            'Pedralbes': '../static/img/pedralbes.jpg',
            'Vallvidrera-el Tibidabo-les Planes': '../static/img/tibidabo.jpg',
            'la Vall d\'Hebron': '../static/img/vall-dhebron.jpg'
        }

        # Obtener la ruta de la imagen para el barrio seleccionado
        imagenbarrio = barrios_imagenes.get(neighborhood, 'default_image.png')


        return render_template('grafica.html', pollution_data=pollution_data,  day=day, neighborhood=neighborhood, imagenbarrio=imagenbarrio)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)








