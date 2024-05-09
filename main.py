import os


EMPTY_CELL = "_"


def cls() -> None:
    """
    Функция очищает консоль
    :return: None
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def init_field(size: int, empty_cell: str = EMPTY_CELL) -> list[list]:
    """
    Функция создаёт и возвращает пустое поле для игры
    :param size: размер поля, int
    :param empty_cell: чем заполняется пустая ячейка, str
    :return: пустое поле в виде двумерного массива, list[list]

    """
    return [[empty_cell] * size for _ in range(size)]


def draw_field(field: list[list]) -> None:
    """
    Функция рисует два поля - в читаемом виде (с заполнением пустыми клетками EMPTY_CELL) и с заполнением индексами,
    на место которых можно вставить ход игрока
    :param field: Поле в виде двумерного массива, list[list]
    :return: None
    """
    size = len(field)

    for i in range(size):
        for j in range(size):
            print(f'{field[i][j]:>3}', end='')
        print()
    print()

    for i in range(size):
        for j in range(size):
            if field[i][j] == 'X' or field[i][j] == 'O':
                print(f'{field[i][j]:>3}', end='')
            else:
                print(f'{i * size + (j + 1):>3}', end='')
        print()
    print()


def player_move(player: str, field: list[list]) -> None:
    """
    Функция запрашивает ход игрока в виде числа на игровом поле и проверяет значение. Если всё в порядке, ставит
    символ текущего игрока на поле
    :param player: Символ текущего игрока, принимает значения 'X' или 'O', str
    :param field: Поле в виде двумерного массива, list[list]
    :return: None
    """
    size = len(field)
    coord_y = None  # Начальная инициализация переменных, чтобы Pycharm не ругался на её отсутствие
    coord_x = None

    print(f'Ход игрока "{player}"')

    while True:
        move = input("Введите ход (число на поле): ")
        if not move.isdigit():
            print("Необходимо ввести положительное целое число")
            continue
        move = int(move)
        coord_y = move // size
        if move > 0 and move % size == 0:
            coord_y -= 1
            coord_x = size - 1
        else:
            coord_x = move % size - 1
        if move <= 0 or move > size ** 2:
            print("Число выходит за указанный диапазон, повторите попытку")
            continue
        if field[coord_y][coord_x] == 'X' or field[coord_y][coord_x] == 'O':
            print("Позиция уже занята, повторите попытку")
            continue
        break

    field[coord_y][coord_x] = player


def is_win(player: str, field: list[list]) -> bool:
    """
    Функция определяет, произошла ли победа. Проверяется, есть ли в какой-либо строке, столбце или диагонали победная
    комбинация (до 5 символов в ряд, чтобы не играть бесконечно на большом игровом поле).
    :param player: Символ текущего игрока, принимает значения 'X' или 'O', str
    :param field: Поле в виде двумерного массива, list[list]
    :return: True если победа, False если победа ещё не произошла, bool
    """
    size = len(field)
    if size <= 5:
        win_line = player * size
    else:
        win_line = player * 5

    for y in range(size):  # Проверка строк
        line = ''.join([field[y][x] for x in range(size)])
        if win_line in line:
            return True

    for x in range(size):  # Проверка столбцов
        line = ''.join([field[y][x] for y in range(size)])
        if win_line in line:
            return True

    for i in range(size):  # Проверка верхней половины / диагонали
        line = ''.join([field[i - j][j] for j in range(i + 1)])
        if win_line in line:
            return True
    for i in range(size - 1, 0, -1):  # Проверка нижней половины / диагонали
        line = ''.join([field[(size - 1) - j][size - i + j] for j in range(i)])
        if win_line in line:
            return True

    for i in range(size):  # Проверка верхней половины \ диагонали
        line = ''.join([field[j][(size - 1) - i + j] for j in range(i + 1)])
        if win_line in line:
            return True
    for i in range(size - 1, 0, -1):  # Проверка нижней половины \ диагонали
        line = ''.join([field[size - i + j][j] for j in range(i)])
        if win_line in line:
            return True

    return False


def is_draw(field: list[list]) -> bool:
    """
    Функция проверяет, произошла ли ничья.
    :param field: Поле в виде двумерного массива, list[list]
    :return: True если ничья, False если ничья ещё не произошла, bool
    """
    size = len(field)

    for y in range(size):  # Проверка по строкам, остались ли символы EMPTY_CELL в поле
        for x in range(size):
            if field[y][x] == EMPTY_CELL:
                return False
    return True


def change_player(player: str) -> str:
    """
    Функция получает на вход символ текущего игрока и меняет его
    :param player: Символ текущего игрока, принимает значения 'X' или 'O', str
    :return: Возвращает изменённый на противоположный символ игрока, str
    """
    return 'O' if player == 'X' else 'X'


def game(player: str, size: int, x_o_wins: list[int]) -> None:
    """
    Функция запускает игру.
    Происходит начальная инициализация пустого поля. Затем оно рисуется 2 раза - с EMPTY_CELL и с индексами.
    Пока не произошла победа или ничья, запрашиваем ход текущего игрока и ставим на поле. Каждый раз после этого рисуем
    поле.
    Печатаем результат игры: победивший игрок или ничья. Печатаем текущий счёт игроков
    :param player: Символ текущего игрока, принимает значения 'X' или 'O', str
    :param size: Размер поля, которое необходимо создать для игры, int
    :param x_o_wins: Количество побед игроков 'X' и 'O' в виде списка, list[int]
    :return: None
    """
    field = init_field(size)
    draw_field(field)
    player = change_player(player)  # Меняем игрока, чтобы цикл ниже начал работу с правильного игрока (т.к. в теле
    # цикла тоже меняется игрок и проверяется, победил ли он)

    while not is_win(player, field) and not is_draw(field):
        player = change_player(player)
        player_move(player, field)
        draw_field(field)
    if not is_draw(field):
        print(f'Выиграл Игрок "{player}"')
        if player == 'X':
            x_o_wins[0] += 1
        else:
            x_o_wins[1] += 1
        print(f'''Количество побед игрока "X": {x_o_wins[0]}
Количество побед игрока "O": {x_o_wins[1]}''')
    else:
        print("Ничья")


def get_size_validate() -> int:
    """
    Функция запрашивает размер поля и проверяет введенное значение
    :return: Размер поля, int
    """
    while True:
        size = input("Введите размер поля (3-7): ")
        if not size.isdigit():
            print("Необходимо ввести положительное целое число")
            continue
        size = int(size)
        if size < 3 or size > 7:
            print("Число должно быть в диапазоне от 3 до 7")
            continue
        break
    return size


def get_player_validate() -> str:
    """
    Функция запрашивает номер игрока из предложенного меню и проверяет введенное значение
    :return: Выбранный символ игрока 'X' или 'O', str
    """
    while True:
        player = input('Выберите, кто будет ходить первым (1-"X", 2-"O"): ')
        player = player.strip()
        match player:
            case '1':
                return 'X'
            case '2':
                return 'O'
            case _:
                print("Необходимо ввести цифру 1 или 2")


def get_answer_validate() -> bool:
    """
    Функция спрашивает, хотим ли сыграть ещё и проверяет введенное значение
    :return: True если ответ "да", False если ответ "нет", bool
    """
    while True:
        answer = input('Хотите сыграть ещё раз? (да/нет): ')
        answer = answer.lower().strip()
        match answer:
            case 'да':
                return True
            case 'нет':
                return False
            case _:
                print("Ответ неверный, попробуйте ещё раз")


def get_new_game_validate(round_counter: int) -> bool:
    """
    Функция спрашивает, хотим начать новую игру или начать следующий раунд с ранее выбранными настройками размера поля.
    :param round_counter: Следующий раунд, если продолжить игру, int
    :return: True если начинаем новую игру, False если продолжаем игру и начинаем новый раунд, bool
    """
    while True:
        answer = input(f'''Начать новую игру или продолжить с текущими настройками?:
    1. Начать новую игру
    2. Начать раунд {round_counter} с текущими настройками: ''')
        answer = answer.strip()
        match answer:
            case '1':
                return True
            case '2':
                return False
            case _:
                print("Необходимо ввести цифру 1 или 2")


def app() -> None:
    """
    Запуск приложения игры крестики-нолики. Выдает меню игры, происходит начальная инициализация размера поля, текущего
    раунда, количества побед каждого игрока, переключателей начала новой игры для циклов, происходит выбор первого
    игрока для начала игры. Здесь же идут запросы о начале новой игры или нового раунда.
    :return: None
    """
    answer_switch = True
    new_game_switch = True
    round_counter = 1
    x_o_wins = [0, 0]
    player = None
    size = None

    while answer_switch:
        print("""*******************************************
*            Крестики-Нолики              *
*******************************************""")
        if new_game_switch:
            round_counter = 1
            x_o_wins = [0, 0]
            size = get_size_validate()
            print(f"Установлен размер поля {size}")
            player = get_player_validate()

        if round_counter > 1:
            player = change_player(player)  # Меняем игрока, чтобы игроки ходили по очереди в разных раундах

        print(f"""***               РАУНД {round_counter}               ***""")
        game(player, size, x_o_wins)
        answer_switch = get_answer_validate()
        round_counter += 1
        if answer_switch:
            new_game_switch = get_new_game_validate(round_counter)
        cls()
    print("Спасибо за игру!")


if __name__ == "__main__":
    app()


"""Первая версия is_win, потом сократил код, оставил только вторую часть"""
# size = len(field)
#
# if size <= 5:
#     for y in range(size):  # Проверка строк
#         win_sum_check = 0
#         for x in range(size):
#             if field[y][x] == player:
#                 win_sum_check += 1
#         if win_sum_check == size:
#             return True
#
#     for x in range(size):  # Проверка столбцов
#         win_sum_check = 0
#         for y in range(size):
#             if field[y][x] == player:
#                 win_sum_check += 1
#         if win_sum_check == size:
#             return True
#
#     win_sum_check = 0  # Проверка диагонали \
#     for i in range(size):
#         if field[i][i] == player:
#             win_sum_check += 1
#     if win_sum_check == size:
#         return True
#
#     win_sum_check = 0  # Проверка диагонали /
#     for i in range(size):
#         if field[i][(size - 1) - i] == player:
#             win_sum_check += 1
#     if win_sum_check == size:
#         return True
# else:
#     win_line = player * 5
#     for y in range(size):  # Проверка строк
#         line = ''.join([field[y][x] for x in range(size)])
#         if win_line in line:
#             return True
#
#     for x in range(size):  # Проверка столбцов
#         line = ''.join([field[y][x] for y in range(size)])
#         if win_line in line:
#             return True
#
#     for i in range(size):  # Проверка верхней половины / диагонали
#         line = ''.join([field[i - j][j] for j in range(i + 1)])
#         if win_line in line:
#             return True
#     for i in range(size - 1, 0, -1):  # Проверка нижней половины / диагонали
#         line = ''.join([field[(size - 1) - j][size - i + j] for j in range(i)])
#         if win_line in line:
#             return True
#
#     for i in range(size):  # Проверка верхней половины \ диагонали
#         line = ''.join([field[j][(size - 1) - i + j] for j in range(i + 1)])
#         if win_line in line:
#             return True
#     for i in range(size - 1, 0, -1):  # Проверка нижней половины \ диагонали
#         line = ''.join([field[size - i + j][j] for j in range(i)])
#         if win_line in line:
#             return True
#
# return False
