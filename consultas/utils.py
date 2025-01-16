import pandas as pd
import locale

def getUsers():
    df = pd.read_excel('base.xlsx', sheet_name='Base Plataforma 15012024', skiprows=1)
    asociados = df.values.tolist()
    print(len(asociados))
    print(asociados[0])
    # for asociado in asociados:
    #     aso = Asociado(
    #         nombre=asociado[1],
    #         documento=asociado[0],
    #         state=asociado[25],
    #         descripcion=asociado[24],
    #         causa=asociado[26])
    #     print("se creo")
    #     aso.save()

def setValue(value):
    reverseValue = list(value[::-1])
    formatted_list = []
    for i, char in enumerate(reverseValue):
        if i > 0 and i % 3 == 0:
            formatted_list.append(".")
        formatted_list.append(char)
    
    return "".join(formatted_list[::-1])

if __name__ == '__main__':
    print(setValue("25000000"))