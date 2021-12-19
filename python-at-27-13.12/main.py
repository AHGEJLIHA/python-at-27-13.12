import sqlite3
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np


# Функция очистки от HTML-разметки
def clean_html(field):
    return re.sub(r'\<[^>]*\>', '', str(field))


# Создание базы данных 'works_database'
con = sqlite3.connect('works_database')
cur = con.cursor()

# Создание таблицы works с 9 полями по works.csv, одно из которых техническое поле ID
cur.execute('CREATE TABLE works('
            '"ID" INTEGER PRIMARY KEY AUTOINCREMENT,'
            '"salary" INTEGER,'
            '"educationType" TEXT,'
            '"jobTitle" TEXT,'
            '"qualification" TEXT,'
            '"gender" TEXT,'
            '"dateModify" TEXT,'
            '"skills" TEXT,'
            '"otherInfo" TEXT)')

# Считываем файл 'works.csv', чистим от HTML-разметки и заполняем таблицу 'works'
df = pd.read_csv('works.csv')
df['skills'] = df['skills'].apply(clean_html)
df['otherInfo'] = df['otherInfo'].apply(clean_html)
df.to_sql('works', con, if_exists='append', index=False)

weight_file_without_index = os.path.getsize('works_database')
cur.execute('CREATE INDEX salary_id ON works(salary);')
weight_file_with_index = os.path.getsize('works_database')
print('Объём файла изменился на ', abs(weight_file_with_index - weight_file_without_index))

# Вывод количества записей
cur.execute('SELECT COUNT(*) FROM works')
print('Количество записей: ', cur.fetchall()[0][0])

# Вывод количества мужчин и женщин
cur.execute('SELECT gender, COUNT(*) FROM works group by gender')
print('Количество полей с неуказанным полом, с женским полом и мужским полом: ', cur.fetchall())

# Количество записей с заполненными skills
cur.execute('SELECT COUNT(*) FROM works where skills not null')
print('Количество записей с заполненными skills: ', cur.fetchall()[0][0])

# Записи с заполненными skills
cur.execute('SELECT skills FROM works where skills not null')
# print('Записи с заполненными skills: ', cur.fetchall())

# Зарплата тех, у кого в skills указан Python
cur.execute('SELECT salary FROM works where skills LIKE "%Python%"')
# print('Зарплата тех, у кого в skills указан Python: ', cur.fetchall())

# Подсчет зарплаты мужчин и женщин
cur.execute('SELECT salary FROM works where gender = "Мужской"')
men_salary = [t[0] for t in cur.fetchall()]
# print('Зарплаты мужчин: ', men_salary)
cur.execute('SELECT salary FROM works where gender = "Женский"')
women_salary = [t[0] for t in cur.fetchall()]
# print('Зарплаты женщин: ', women_salary)

#Построение перцентили
percentiles = range(10, 91, 10)
women_percentiles = np.percentile(women_salary, percentiles, interpolation='lower')
men_percentiles = np.percentile(men_salary, percentiles, interpolation='lower')
for idx, v in enumerate(percentiles):
    print(f"до {men_percentiles[idx]} получают {percentiles[idx]}% мужчин")
    print(f"до {women_percentiles[idx]} получают {percentiles[idx]}% женщин")

# Графики распределения по з/п мужчин и женщин
figure(figsize=(10, 6))
plt.xlabel("Salary")
plt.ylabel("Percentiles")

plt.plot(women_percentiles, percentiles, 'red')
plt.plot(men_percentiles, percentiles, 'blue')
plt.legend(["Женщины", "Мужчины"])
plt.show()
