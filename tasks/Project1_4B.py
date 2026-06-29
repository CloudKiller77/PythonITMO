"""
Загрузите данные из файла …\data\orderdata_sample.csv file. На основе столбцов “Quantity”, “Price” и “Freight”
создайте новый столбец “Total” (например, по формуле Quantity * Price + Freight).
Отобразите на экран выборочно (на ваше усмотрение) столбцы на основе условия (на ваше усмотрение).
Сохраните все данные в новый файл.
"""

import csv

filename = "D:\My_work\pythonITMO\data\orderdata_sample.csv"
newfile = "D:\My_work\pythonITMO\data\orderdata_new.csv"
rows = []

# Вычитывание из файла и сохранение в список
with open(filename, "r", encoding="utf-8") as fh:
    reader = csv.DictReader(fh)
    rows = list(reader)

# Формирование нового столбца и запись значений в новый файл
with open(newfile, "w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=["OrderID", "CustomerID", "ManagerID", "Quantity", "Price", "Freight",
                                            "OrderDate", "ShippedDate", "Total"], quoting=csv.QUOTE_ALL)
    writer.writeheader()
    reader = csv.DictReader(fh)
    for row in rows:
        print(row)
        total = float(row["Quantity"]) * float(row["Price"]) - float(row["Freight"])
        writer.writerow(dict(OrderID=row["OrderID"], CustomerID=row["CustomerID"], ManagerID=row["ManagerID"],
                             Quantity=row["Quantity"], Price=row["Price"], Freight=row["Freight"],
                             OrderDate=row["OrderDate"], ShippedDate=row["ShippedDate"], Total=total))
