import pandas as pd
import os;
import matplotlib.pyplot as plt
from db import db

def GetDailyPollutionData(day, neighborhood):
    # Data Extraction
    statistics = db['CalidadAire']
    contaminants = db['Contaminantes']
    stations = db['Estaciones']

    station = stations.find_one({"Nom_barri": neighborhood}, {"_id": 0, "Estacio": 1})
    if not station:
        return None

    station_code = station.get("Estacio")
    statistics = statistics.find({"ESTACIO": station_code, "DIA": day})

    # Data Cleaning
    fieldsToRemove = ["_id", "CODI_PROVINCIA", "PROVINCIA", "CODI_MUNICIPI", "MUNICIPI", "V12"]
    statisticsDF = pd.DataFrame(list(statistics)).drop(columns=fieldsToRemove)
    statisticsDF["ESTACIO"] = neighborhood

    contaminantsDF = pd.DataFrame(contaminants.find())
    contaminantsDF.rename(columns={'Codi_Contaminant': 'CODI_CONTAMINANT'}, inplace=True)


    


    # Data Analysis
    statisticsDF = pd.merge(statisticsDF, contaminantsDF, on="CODI_CONTAMINANT").drop(columns=["_id"])

    return statisticsDF

def GetDataForTable(day, neighborhood):
    statisticsDF = GetDailyPollutionData(day, neighborhood)
    if statisticsDF is None:
        return []
    return statisticsDF.to_dict(orient='records')

def GetDailyPollutionGraph(day, neighborhood):
    statisticsDF = GetDailyPollutionData(day, neighborhood)
    if statisticsDF is None:
        return

    # Data visualization
    try:
        plt.style.use('seaborn-darkgrid')
    except OSError as e:
        print(f"Error loading style: {e}")
        plt.style.use('ggplot')  # Usar un estilo alternativo

    plt.plot(statisticsDF["Desc_Contaminant"], statisticsDF['H12'], marker='o', linestyle='-', color='b', label='Pollution Level (H12)')
    plt.xlabel('Contaminant Name')
    plt.ylabel('Pollution Level (H12)')
    plt.title(f'Pollution Level by Contaminant, {neighborhood}, {day}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.gcf().set_facecolor('none')

    path="../static/dataVisualization/graphic.png"

    if(os.path.exists(path)):
        if(os.path.exists(path)):
            os.remove(path)

    plt.savefig("./static/dataVisualization/graphic.png", bbox_inches='tight', dpi=300)
    plt.close()


