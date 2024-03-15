import pandas as pd
from main import login
from datetime import datetime, timedelta
from model.getResource import getResources

start = datetime(2023, 10, 2, 0, 0, 0)
end = datetime(2023, 10, 2, 23, 59, 59)
unit = 26646581

def Datos(unit, start, end):
    sdk = login()
    resources = getResources()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 1,
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
    tables = reports['reportResult']['tables']

    i = 0
    rows = tables[i]['rows']
    paramsDiario = {
        'tableIndex': i,
        'indexFrom': 0,
        'indexTo': rows
    }
    data = sdk.report_get_result_rows(paramsDiario)
    dataDiario = [r['c'] for r in data]
    dfDiario = pd.DataFrame(dataDiario)
    headers = tables[i]['header']
    # replace header wth headers
    dfDiario.columns = headers
    dfDiario['Grouping'] = pd.to_datetime(dfDiario['Grouping'])
    dfDiario['EngineHours'] = dfDiario['EngineHours'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfDiario['Parkings'] = dfDiario['Parkings'].apply(lambda x: x.split(' ')[0]).astype(float)
    dfDiario['Consumed'] = dfDiario['Consumed'].apply(lambda x: x.split(' ')[0]).astype(float)

    i = 1
    paramSummary = {
        'tableIndex': i,
        'indexFrom': 0,
        'indexTo': rows
    }
    data = sdk.report_get_result_rows(paramSummary)
    dataSummary = [r['c'] for r in data]
    dfSummary = pd.DataFrame(dataSummary)
    headers = tables[i]['header']
    dfSummary.columns = headers
    dfSummary['EngineHours'] = dfSummary['EngineHours'].astype(float)
    dfSummary['Consumed'] = dfSummary['Consumed'].apply(lambda x: x.split(' ')[0]).astype(float)

    return dfDiario, dfSummary
# sdk.logout()
# df = reportByHour(unit, start, end)