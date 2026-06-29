"""
Задания:
1. Дан список температурных изменений в течение дня (целые числа). Известно, что измеряющее устройство иногда сбоит
и записывает отсутствие температуры (значение None). Выведите среднюю температуру за наблюдаемый промежуток времени,
предварительно очистив список от неопределенных значений.
Гарантируется, что хотя бы одно определенное значение в списке есть.
2. Напишите функцию, которая принимает неограниченное количество числовых аргументов и возвращает
кортеж из двух списков: отрицательных значений (отсортирован по убыванию); неотрицательных значений
(отсортирован по возрастанию).
3. Составьте две функции для возведения числа в степень: один из вариантов реализуйте в рекурсивном стиле.
"""


# Задание 1
def calculate_average_temperature(temp_list):
    """
    Вычисляет среднюю температуру за наблюдаемый промежуток времени.
    Аргументы:
        temp_list (list): Список температур (целые числа и возможные None).
    Возвращает:
        float: Средняя температура с двумя знаками после запятой.
    Исключения:
        ValueError: Если в списке нет ни одного определенного значения.
    """
    cleaned = [temp for temp in temp_list if temp is not None]
    if not cleaned:
        raise ValueError("Список не содержит ни одного определенного значения температуры.")
    return round(sum(cleaned) / len(cleaned), 2)


def view_temperature():
    temperatures = [23, 25, None, 21, 24, None, 22, 26, None, 17]

    average = calculate_average_temperature(temperatures)
    print(f"\nСредняя температура за день: {average:.2f}°C")


# Задание 2
def sort_numbers(*args) -> tuple[[], []]:
    """
    Принимает неограниченное количество числовых аргументов и возвращает кортеж
    из двух списков: отрицательных значений (отсортирован по убыванию)
    и неотрицательных значений (отсортирован по возрастанию).
    Аргументы:
        *args: Произвольное количество числовых аргументов.
    Возвращает:
        tuple: Кортеж из двух списков:
            - первый список: отрицательные значения, отсортированные по убыванию
            - второй список: неотрицательные значения, отсортированные по возрастанию
    """
    negative_numbers = sorted([x for x in args if x < 0], reverse=True)
    non_negative_numbers = sorted([x for x in args if x >= 0])

    return negative_numbers, non_negative_numbers


def two_tuple_view():
    numbers = [5, -3, 0, -8, 12, -1, 7, -4, 3, 10, 12, 9, 1, -5, -9]

    negative, non_negative = sort_numbers(*numbers)

    print("\nОтрицательные значения (по убыванию):")
    print(negative)

    print("\nНеотрицательные значения (по возрастанию):")
    print(non_negative)

# Задание 3

def iterative_style(base, exponent):
    """
    Возводит число в степень итеративным способом.

    Аргументы:
        base: Основание степени.
        exponent: Показатель степени (неотрицательное целое число).
    Возвращает:
        float: Результат возведения в степень.
    Исключения:
        ValueError: Если показатель степени отрицательный.
    """
    if exponent < 0:
        raise ValueError("Показатель степени должен быть неотрицательным целым числом.")

    result = 1
    for _ in range(exponent):
        result *= base

    return result


def recursive_style(base, exponent):
    """
    Возводит число в степень рекурсивным способом.
    Аргументы:
        base: Основание степени.
        exponent: Показатель степени (неотрицательное целое число).
    Возвращает:
        float: Результат возведения в степень.
    Исключения:
        ValueError: Если показатель степени отрицательный.
    """
    if exponent < 0:
        raise ValueError("Показатель степени должен быть неотрицательным целым числом.")

    if exponent == 0:
        return 1
    # Рекурсивный случай
    else:
        return base * recursive_style(base, exponent - 1)


def view_exponent():
    test_cases = [
        (2, 10),
        (4, 6),
        (8, 9),
        (3.5, 3),
        (0, 5),
        (1, 100),
        (2.5, 4),
        (10, 0)
    ]

    print("Результаты возведения в степень:")
    print("=" * 50)

    for base, exponent in test_cases:
        print(f"{base} ^ {exponent}:")

        iterative_result = iterative_style(base, exponent)
        recursive_result = recursive_style(base, exponent)

        print(f"  Итеративный метод:      {iterative_result:.2f}")
        print(f"  Рекурсивный метод:      {recursive_result:.2f}")
        print()


if __name__ == "__main__":
    view_temperature()
    two_tuple_view()
    view_exponent()
