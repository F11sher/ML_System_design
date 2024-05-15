import joblib
import pandas as pd

model = joblib.load('doc_model.pkl')

sick_names = {
    '0': ['Brain_stroke', 'Инсульт'],
    '1': ['COVID-19', 'COVID-19'],
    '2': ['Chikungunya', 'Чикунгунья'],
    '3': ['Dengue', 'Лихорадка Денге'],
    '4': ['Diphtheria', 'Дифтерия'],
    '5': ['Ebola', 'Вирус Эбола'],
    '6': ['Hepatitis', 'Гепатит'],
    '7': ['Japanese_encephalitis', 'Японский энцефалит'],
    '8': ['Liver_Cirrhosis', 'Цирроз печени'],
    '9': ['Lyme_disease', 'Болезнь Лайма'],
    '10': ['Malaria', 'Малярия'],
    '11': ['Measles', 'Корь'],
    '12': ['Meningitis', 'Менингит'],
    '13': ['Plague', 'Чума'],
    '14': ['Rift_Valley_fever', 'Вирус лихорадки Рифт-Вэлли'],
    '15': ['Rotavirus_infection', 'Ротавирусная инфекция'],
    '16': ['Tungiasis', 'Тунгиоз'],
    '17': ['West_Nile_fever', 'Вирус лихорадки Западного Нила'],
    '18': ['Yellow_Fever', 'Желтая лихорадка'],
    '19': ['Zika', 'Вирус Зика'],
}


async def get_predict(data):
    data = pd.DataFrame(data, index=[0])

    result = model.predict(data)

    return sick_names[str(int(result[0]))]
