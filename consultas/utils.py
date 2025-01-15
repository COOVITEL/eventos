import pandas as pd

def getUsers(num):
    df = pd.read_excel('obsequios.xlsx', sheet_name='Hoja1', skiprows=1)
    asociados = df.values.tolist()
    asociado = [v for v in asociados if v[0] == num]
    if len(asociado) == 0:
        return {'state': False}
    else:
        asociado = asociado[0]
        setAsociado = {
            'name': asociado[1] if asociado[1] else "",
            'document': asociado[0] if asociado[0] else "",
            'state': asociado[25] if asociado[25] else "",
            'description': asociado[24] if asociado[24] else "",
            'causa': asociado[26] if asociado[26] else ""
        }
        
        return {'state': True, 'asociado': setAsociado}
