import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

years = [2000+i for i in range(24)]

salary = pd.read_csv("data/salary.csv")
petroleum_coke = salary.T[0][1:]
rubber_and_plastic = salary.T[1][1:]
fishing = salary.T[2][1:]


inflation_data = pd.read_csv("data/inflation.csv")
inflation = inflation_data[['Год', 'Всего']]
inf_years = inflation_data['Год'][1:25]
inf_total = inflation_data['Всего'][1:25]


def take_real_salary(year_salary, initial_year, finish_year):
  real = year_salary
  for year in range(finish_year, initial_year, -1):
    real /= 1.0 + inflation[inflation['Год'] == year].iloc[0]['Всего'] / 100
  return real

real_petroleum_coke = [salary['2000'][0]]
real_rubber_and_plastic = [salary['2000'][1]]
real_fishing = [salary['2000'][2]]

for i in range(2001, 2024):
  year_salary = salary[str(i)]

  real_petroleum_coke.append(take_real_salary(year_salary[0], 2000, i))
  real_rubber_and_plastic.append(take_real_salary(year_salary[1], 2000, i))
  real_fishing.append(take_real_salary(year_salary[2], 2000, i))

  prev_salary = year_salary

real_average_salary = []
for i in range(0, 24):
  real_average_salary.append((real_petroleum_coke[i]+real_rubber_and_plastic[i]+real_fishing[i])/3)

hpi = pd.read_csv("data/hpi_score.csv")

full_data_source={
  'Инфляция': [inflation[inflation['Год'] == i].iloc[0]['Всего'] for i in range(2006, 2021)],
  'Уровень счастья': [float(i) for i in hpi.iloc[0].array],
  'Заработная плата': [float(i) for i in real_average_salary[6:21]]
}

full_data = pd.DataFrame(full_data_source, columns=['Инфляция', 'Уровень счастья', 'Заработная плата'])

def show_salary():
  fig, ax = plt.subplots()
  fig.set_figheight(7)
  fig.set_figwidth(15)
  plt.plot(years, petroleum_coke, color='r', label='Производство кокса и нефтепродуктов')
  plt.plot(years, rubber_and_plastic, color='b', label='Производство резиновых и пластмассовых изделий')
  plt.plot(years, fishing, color='g', label='Рыболовство, рыбоводство')
  plt.xticks(np.arange(2000, 2024, 1.0))
  plt.yticks(np.arange(2000, 150000, 5000.0))
  plt.legend()
  plt.title('Все деятельности')
  plt.xlabel('Год')
  plt.ylabel('Зароботная плата')
  st.pyplot(fig)
  st.write("Для производства кокса и нефтепродуктов наблюдается рост заработной платы до 2017 года. После 2017 года плата снижается и начинает расти только после 2020.")
  st.write("Для производства резиновых и пластмассовых изделий рост заработной платы продолжается все года.")
  st.write("Для рыболовства, рыбоводства заработная плата активно растет на протяжении всех лет. После 2014 года и 2021 года заработная плата начинает расти более активно.")
  
def show_inflation():
  fig, ax = plt.subplots()
  fig.set_figheight(7)
  fig.set_figwidth(15)
  plt.plot(inf_years, inf_total)
  plt.xticks(np.arange(2000, 2024, 1.0))
  plt.title('График инфляции')
  plt.xlabel('Год')
  plt.ylabel('Инфляция')
  st.pyplot(fig)

def show_real_salory():
  fig, ax = plt.subplots()
  fig.set_figheight(7)
  fig.set_figwidth(15)
  plt.plot(years, real_petroleum_coke, color='r', label='Производство кокса и нефтепродуктов')
  plt.plot(years, real_rubber_and_plastic, color='b', label='Производство резиновых и пластмассовых изделий')
  plt.plot(years, real_fishing, color='g', label='Рыболовство, рыбоводство')
  plt.xticks(np.arange(2000, 2024, 1.0))
  plt.yticks(np.arange(2000, 22000, 1000.0))
  plt.legend()
  plt.title('Все деятельности с учетом инфляции')
  plt.xlabel('Год')
  plt.ylabel('Зароботная плата')
  st.pyplot(fig)
  st.write("Для производства кокса и нефтепродуктов рост заработной платы с учетом инфляции длился до 2017 года "
         +"с небольшой просадкой в 2014-2015 году. После 2017 года заработная плата уменьшается и начинает расти "
         +"только в 2022 году, не превышая максимальной.")
  st.write("Для производства резиновых и пластмассовых изделий заработная плата растет менее значительно с небольшой просадкой в 2013-2015гг.")
  st.write("Для рыболовства, рыбоводства заработная плата растет на всем временном промежутке с началом активного роста после 2014 года и небольшой просадкой в 2019-2022гг.")
  
def show_hpi():
  fig, ax = plt.subplots()
  fig.set_figheight(5)
  fig.set_figwidth(10)
  plt.plot([i for i in range(2006, 2021)], [float(i) for i in hpi.iloc[0].array])
  plt.xticks(np.arange(2006, 2021, 1.0))
  plt.yticks(np.arange(0, 110, 10.0))
  plt.title('Уровень счастья в России')
  plt.xlabel('Год')  
  st.pyplot(fig)

def show_all_correlation():
  fig, ax = plt.subplots()
  sns.heatmap(full_data.corr(), ax=ax)
  st.write(fig)
  st.write("Наблюдается корреляция реальной заработной платы и уровня счастья")

def show_main_page():
  st.title("Проект: анализ зарплат в России")

  st.text("Заработные платы взяты с 2000 года по 2023")
  st.write('Для анализа были выраны 3 экономические деятельности:\n'
          +'1) производство кокса и нефтепродуктов;\n'
          +'2) производство резиновых и пластмассовых изделий;\n'
          +'3) рыболовство, рыбоводство.')
  st.table(salary)
  show_salary()
  st.header("Заработные платы с учетом инфляции")
  show_inflation()
  show_real_salory()
  st.header("Уровень счастья в России")
  show_hpi()
  show_all_correlation()


if __name__ == "__main__":
    show_main_page()