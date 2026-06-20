'''Задача. Счастливый билетик (Python)
Напишите программу, которая получала бы на входе шестизначный номер билета
и выводила, счастливый это билет или нет.
К примеру, билеты 666 666 и 252 135 — счастливые, а 123 456 — нет.
Решение задачи:'''

lucky_number = input("Введите шестизначный номер билета (123456): \n")
if len(lucky_number) > 6:
    print(f"Вы ввели больше 6 символов: {lucky_number}")
else:
    number1 = 0
    number2 = 0
    for i in lucky_number[0:3]:
        number1 += int(i)
    for i in lucky_number[3:]:
        number2 += int(i)
    if number1 == number2:
        print(f"Ваш билет счастливый): {lucky_number}")
    else:
        print(f"Вам не повезло(: {lucky_number}")
