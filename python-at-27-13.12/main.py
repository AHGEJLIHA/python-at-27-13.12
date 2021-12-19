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

# Построение перцентили
percentiles = range(10, 91, 10)
women_percentiles = np.percentile(women_salary, percentiles, interpolation='lower')
men_percentiles = np.percentile(men_salary, percentiles, interpolation='lower')
for idx, v in enumerate(percentiles):
    print(f"до {men_percentiles[idx]} получают {percentiles[idx]}% мужчин")
    print(f"до {women_percentiles[idx]} получают {percentiles[idx]}% женщин")

# Графики перцентели
figure(figsize=(10, 6))
plt.xlabel("Salary")
plt.ylabel("Percentiles")

plt.plot(women_percentiles, percentiles, 'red')
plt.plot(men_percentiles, percentiles, 'blue')
plt.legend(["Женщины", "Мужчины"])
plt.show()

# График распределения по заработным платам у мужчин и женщин
salary_step = 10000
salary_limit = 160000
figure(figsize=(28, 7))
bins = int(salary_limit / salary_step)
xs = range(0, salary_limit, salary_step)
ys = [round(i * salary_step, 2) for i in [j * 1e-6 for j in range(0, 36, 5)]]

women_salary = np.array([s[0] for s in cur.execute("SELECT salary FROM works WHERE gender='Женский';")])
men_salary = np.array([s[0] for s in cur.execute("SELECT salary FROM works WHERE gender='Мужской';")])
women_data = women_salary[women_salary <= salary_limit]
men_data = men_salary[men_salary <= salary_limit]

plt.xticks(labels=xs, ticks=xs)
plt.yticks(labels=ys, ticks=ys)
plt.hist([men_data, women_data], bins, label=['Мужчины', 'Женщины'], density=True)
plt.legend(loc='upper right')
plt.title("График распределения заработной платы мужчин и женщин")
plt.ylabel("Распределение по долям")
plt.xlabel("Зарплата")
plt.show()

# График распределения по заработным платам у мужчин и женщин
stmt_for_higher_edu = "SELECT salary FROM works WHERE salary <= " + str(salary_limit) + " AND educationType = "
stmt_for_not_higher_edu = "SELECT salary FROM works WHERE salary <= " + str(salary_limit) + " AND NOT educationType = "
higher_edu = np.array([i[0] for i in cur.execute(stmt_for_higher_edu + "'Высшее';")])
not_higher_edu = np.array([i[0] for i in cur.execute(stmt_for_not_higher_edu + "'Высшее';")])

y_loc = [i * 1e-6 for i in range(0, 41, 5)]
ys = [round(i * salary_step, 2) for i in y_loc]
figure(figsize=(28, 7))
plt.xticks(ticks=xs, labels=xs, rotation=30)
plt.yticks(ticks=y_loc, labels=ys)
plt.hist([higher_edu, not_higher_edu], bins,
         label=['Высшее', 'Невысшее'], density=True)
plt.legend(loc='upper right')
plt.title("График распределения заработной платы по образованию")
plt.xlabel("Зарплата")
plt.ylabel("Распределение по долям")

plt.show()

# Домашнее задание
# Таблица для гендера
cur.execute('CREATE TABLE genders(ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            'gender_value TEXT)')
con.commit()

cur.execute('INSERT INTO genders(gender_value) SELECT DISTINCT gender '
            'FROM works WHERE gender IS NOT NULL')
con.commit()

cur.execute('ALTER TABLE works ADD COLUMN gender_id INTEGER REFERENCES genders(id)')
con.commit()

cur.execute('UPDATE works SET gender_id = (SELECT id FROM genders WHERE gender_value = works.gender)')
con.commit()

cur.execute('ALTER TABLE works DROP COLUMN gender')
con.commit()

# По гендеру
cur.execute('SELECT * FROM genders')
# print(cur.fetchall())
cur.execute('SELECT gender_value FROM genders,works WHERE genders.id = works.gender_id')
# print(cur.fetchall())


# Таблица для образования
cur.execute('create table education(id INTEGER PRIMARY KEY AUTOINCREMENT, edu_value TEXT)')
con.commit()

cur.execute('INSERT INTO education(edu_value) SELECT DISTINCT educationType '
            'FROM works WHERE educationType IS NOT NULL')
con.commit()

cur.execute('ALTER TABLE works ADD COLUMN educationType_id INTEGER REFERENCES education(id)')
con.commit()

cur.execute('UPDATE works SET educationType_id = (SELECT id FROM education '
            'WHERE edu_value = works.educationType)')
con.commit()

cur.execute('ALTER TABLE works DROP COLUMN educationType')
con.commit()

# По образованию
cur.execute('SELECT * FROM education')
# print(cursor.fetchall())
cur.execute('SELECT edu_value FROM education,works WHERE education.id = works.educationType_id')
# print(cursor.fetchall())
