import pandas as pd
import numpy as np
from main import login
from datetime import datetime, timedelta
from model.getResource import getResources

# start = datetime(2023, 5, 17, 0, 0, 0)
# end = datetime(2023, 5, 17, 23, 59, 59)
# # # unit = 26256679
# unit = 26258342

resources = getResources()
def getReport(unit, start, end):
    sdk = login()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 4,
        'reportObjectId': unit,
        'reportObjectSecId': 0,
        'reportObjectIdList': 0,
        'interval': {
            'from': int(start.timestamp()),
            'to': int(end.timestamp()),
            'flags': 0
        }
    }
    reports = sdk.report_exec_report(paramsExecReport)

    paramsSummary = {
        'tableIndex': 0,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][0]['rows']
    }
    rows = sdk.report_get_result_rows(paramsSummary)
    dataSummary = [r['c'] for r in rows]
    df_summary = pd.DataFrame(dataSummary)
    df_summary.rename(columns={0: 'distance', 1: 'avgSpeed', 2: 'maxSpeed', 3: 'engineTime', 4: 'parking', 5: 'consumed', 6: 'moveTime'}, inplace=True)
    df_summary['parking'] = df_summary['parking'].apply(lambda x: x.split(' ')[0]).astype(float)
    df_summary['engineTime'] = df_summary['engineTime'].apply(lambda x: x.split(' ')[0]).astype(float)
    df_summary['moveTime'] = df_summary['moveTime'].apply(lambda x: x.split(' ')[0]).astype(float)
    df_summary['distance'] = df_summary['distance'].apply(lambda x: x.split(' ')[0]).astype(float)
    df_summary['avgSpeed'] = df_summary['avgSpeed'].apply(lambda x: x.split(' ')[0]).astype(float)
    df_summary['consumed'] = df_summary['consumed'].apply(lambda x: x.split(' ')[0]).astype(float)
    df_summary['maxSpeed'] = df_summary['maxSpeed'].apply(lambda x: x['t'].split(' ')[0] if x != '0 km/h' else 0).astype(float)
    
    paramsSensor = {
        'tableIndex': 1,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][1]['rows']
    }
    rows = sdk.report_get_result_rows(paramsSensor)
    dataSensor = [r['c'] for r in rows]
    df_sensor = pd.DataFrame(dataSensor)
    df_sensor.rename(columns={0: 'fuelRalenti', 1: 'fuelOptimo', 2: 'fuelSobrecarga', 3: 'horasRalenti', 4: 'horasOptimo'}, inplace=True)
    df_sensor['fuelRalenti'] = df_sensor['fuelRalenti'].astype(float)
    df_sensor['fuelOptimo'] = df_sensor['fuelOptimo'].astype(float)
    df_sensor['fuelSobrecarga'] = df_sensor['fuelSobrecarga'].astype(float)
    df_sensor['horasRalenti'] = df_sensor['horasRalenti'].astype(float)
    df_sensor['horasOptimo'] = df_sensor['horasOptimo'].astype(float)
    df = pd.concat([df_summary, df_sensor], axis=1)

    paramsTracing = {
        'tableIndex': 2,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][2]['rows']
    }
    rowsTracing = sdk.report_get_result_rows(paramsTracing)
    headerTracing = reports['reportResult']['tables'][2]['header']
    dataTracing = [r['c'] for r in rowsTracing]
    df_tracing = pd.DataFrame(dataTracing, columns=headerTracing)
    df_tracing['Speed'] = df_tracing['Speed'].apply(lambda x: np.nan if x == "-----" else x.split(' ')[0]).astype(float)
    df_tracing['volTotalIngreso'] = df_tracing['volTotalIngreso'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['volTotalRetorno'] = df_tracing['volTotalRetorno'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['volDifTotalAbsolute'] = df_tracing['volDifTotalAbsolute'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['volDifTotalCus'] = df_tracing['volDifTotalCus'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['caudalIngreso'] = df_tracing['caudalIngreso'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['caudalRetorno'] = df_tracing['caudalRetorno'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['consumoCaudal'] = df_tracing['consumoCaudal'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['horasIngresoAbsolute'] = df_tracing['horasIngresoAbsolute'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['horasIngresoCus'] = df_tracing['horasIngresoCus'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['Voltaje.CanUp'] = df_tracing['Voltaje.CanUp'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['Nº de Err.CanUp'] = df_tracing['Nº de Err.CanUp'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['CANTD. INFOR. ACUM'] = df_tracing['CANTD. INFOR. ACUM'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['pitchAngle'] = df_tracing['pitchAngle'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['rollAngle'] = df_tracing['rollAngle'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['volFuelRalenti'] = df_tracing['volFuelRalenti'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['volFuelOptimo'] = df_tracing['volFuelOptimo'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['volFuelSobrecarga'] = df_tracing['volFuelSobrecarga'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['horasRalenti'] = df_tracing['horasRalenti'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['horasOptimo'] = df_tracing['horasOptimo'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing['Altitude'] = df_tracing['Altitude'].apply(lambda x: np.nan if x == "-----" else x).astype(float)
    df_tracing.interpolate(limit_direction='both', inplace=True)
    return df, df_tracing
# sdk.logout()
