import random as rnd


class Ship:
    def __init__(self):
        # представим корабль как набор модулей
        self.modules = []
        # длина корабля по умолчанию
        self.length = 0
        # позиция корабля по умолчанию
        self.x = 0
        self.y = 0
        # ориентация корабля по умолчанию
        self.orient = None

    def set_length(self, length):
        try:
            if 0 < length <= 3:
                self.length = length
            else:
                raise ValueError
        except ValueError:
            print('\nНеверная длина корабля!\n')

    def get_length(self):
        return self.length

    def set_orient(self, orient):
        try:
            if orient == 'h' or orient == 'v':
                self.orient = orient
            else:
                print('\nНеверно указана ориентация корабля!\n')
                raise ValueError
        except ValueError:
            pass

    def get_orient(self):
        return self.orient

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    # формируем корабль как список координат его модулей на игровом поле
    def set_modules(self):
        if self.get_length() > 1:
            if self.get_orient() == 'v':
                for i in range(0, self.length):
                    module = [self.x+i, self.y]
                    self.modules.append(module)
                return self.modules
            if self.get_orient() == 'h':
                for i in range(0, self.length):
                    module = [self.x, self.y+i]
                    self.modules.append(module)
                return self.modules
        else:
            module = [self.x, self.y]
            self.modules.append(module)
            return self.modules

    def get_modules(self):
        return self.modules


class Board:
    def __init__(self):
        self.width = 0
        self.height = 0

        # набор модулей кораблей игрока
        self.user_ships_modules = []

        # набор уничтоженных модулей кораблей игрока
        self.user_ships_modules_hit = []

        # набор попаданий игрока "мимо"
        self.user_dots_hit = []

        # аналогично для компьютера
        self.ai_ships_modules = []
        self.ai_ships_modules_hit = []
        self.ai_dots_hit = []

    def set_width(self, width):
        self.width = width + 1

    def get_width(self):
        return self.width

    def set_height(self, height):
        self.height = height + 1

    def get_height(self):
        return self.height

    # собираем модули всех кораблей в одном месте - формируем список целей
    def set_user_ship(self, ship):
        try:
            # перебираем модули отдельного корабля
            for i in range(len(ship)):
                # если модуль уже есть в списке (если корабли пересекаются)
                if ship[i] in self.user_ships_modules:
                    raise ValueError
                # если модули (корабли) стоят рядом
                elif ([ship[i][0]+1, ship[i][1]] in self.user_ships_modules) or ([ship[i][0]-1, ship[i][1]] in self.user_ships_modules) or ([ship[i][0], ship[i][1]+1] in self.user_ships_modules) or ([ship[i][0], ship[i][1]-1] in self.user_ships_modules):
                    raise ValueError
                # если модуль корабля выходит за границы поля
                elif ship[i][0] > self.get_width()-1 or ship[i][1] > self.get_height()-1 or ship[i][0] <= 0 or ship[i][1] <= 0:
                    raise ValueError
        except ValueError:
            print('\nНеверно размещен корабль!\n')
        # если все успешно - добавляем модули корабля в список целей
        else:
            self.user_ships_modules += ship

    # аналогично для компьютера
    def set_ai_ship(self, ship):
        try:
            for i in range(len(ship)):
                if ship[i] in self.ai_ships_modules:
                    raise ValueError
                elif ([ship[i][0]+1, ship[i][1]] in self.ai_ships_modules) or ([ship[i][0]-1, ship[i][1]] in self.ai_ships_modules) or ([ship[i][0], ship[i][1]+1] in self.ai_ships_modules) or ([ship[i][0], ship[i][1]-1] in self.ai_ships_modules):
                    raise ValueError
                elif ship[i][0] > self.get_width()-1 or ship[i][1] > self.get_height()-1 or ship[i][0] <= 0 or ship[i][1] <= 0:
                    raise ValueError
        except ValueError:
            pass
        else:
            self.ai_ships_modules += ship

    def get_user_ship(self):
        return self.user_ships_modules

    def get_user_ship_hit(self):
        return self.user_ships_modules_hit

    def get_user_dots_hit(self):
        return self.user_dots_hit

    def get_ai_ship(self):
        return self.ai_ships_modules

    def get_ai_ship_hit(self):
        return self.ai_ships_modules_hit

    def get_ai_dots_hit(self):
        return self.ai_dots_hit

    # формируем механику выстрела
    def ad_user_hit(self):
        user_hit_success = False
        print('Выстрел игрока')
        # пока не получится правильный выстрел
        while not user_hit_success:
            try:
                user_hit_pos = input('Введите координаты выстрела: ')
                if not user_hit_pos.isnumeric() or len(user_hit_pos) != 2:
                    print('\nНеправильно введены координаты!\n')
                    raise ValueError
                else:
                    x = int(user_hit_pos[0])
                    y = int(user_hit_pos[1])
                    user_hit = [x, y]
                    # проверяем, не стреляли ли уже в это поле
                    if user_hit in self.ai_ships_modules_hit or user_hit in self.user_dots_hit:
                        print('\nСюда уже стреляли!\n')
                        raise ValueError
                    # проверяем, не пальнули ли в молоко
                    elif user_hit[0] < 1 or user_hit[0] > self.get_width() - 1 or user_hit[1] < 1 or user_hit[1] > self.get_height() - 1:
                        print('\nВыстрел за пределы поля!\n')
                        raise ValueError
                    # формально правильный выстрел - проверяем на точность попадания
                    elif user_hit in self.ai_ships_modules:
                        self.ai_ships_modules.remove(user_hit)
                        self.ai_ships_modules_hit.append(user_hit)
                        print('Попадание!')
                        user_hit_success = True
                    # стрельнул правильно, но промазал
                    else:
                        self.user_dots_hit.append(user_hit)
                        print('Мимо!')
                        user_hit_success = True
            except ValueError:
                pass

    # аналогично для компьютера
    def ad_ai_hit(self):
        ai_hit_success = False
        print('\nВыстрел компьютера\n')
        while not ai_hit_success:
            try:
                x = rnd.randint(1, board.get_width()-1)
                y = rnd.randint(1, board.get_height()-1)
                ai_hit = [x, y]
                if ai_hit in self.user_ships_modules_hit or ai_hit in self.ai_dots_hit:
                    raise ValueError
                elif ai_hit in self.user_ships_modules:
                    self.user_ships_modules.remove(ai_hit)
                    self.user_ships_modules_hit.append(ai_hit)
                    print('Попадание!')
                    ai_hit_success = True
                else:
                    self.ai_dots_hit.append(ai_hit)
                    print('Мимо!')
                    ai_hit_success = True
            except ValueError:
                pass

    # формируем игровые поля из заготовки и списков кораблей и выстрелов
    def form_user_board(self):
        print('\nВаше поле')
        user_field = []
        # исходное поле
        for i in range(self.get_width()):
            dots = []
            for j in range(self.get_height()):
                dots += [0]
            user_field.append(dots)
        user_field[0][0] = ' '
        # разметка поля
        for i in range(1, self.get_width()):
            user_field[i][0] = i
        for j in range(1, self.get_height()):
            user_field[0][j] = j
        # расставляем корабли
        for i in range(len(self.get_user_ship())):
            a = self.get_user_ship()[i][0]
            b = self.get_user_ship()[i][1]
            user_field[a][b] = '■'
        # отмечаем пробитые модули кораблей
        for i in range(len(self.get_user_ship_hit())):
            a = self.get_user_ship_hit()[i][0]
            b = self.get_user_ship_hit()[i][1]
            user_field[a][b] = 'X'
        # отмечаем промахи
        for i in range(len(self.get_ai_dots_hit())):
            a = self.get_ai_dots_hit()[i][0]
            b = self.get_ai_dots_hit()[i][1]
            user_field[a][b] = 'T'
        # рисуем получившееся
        for i in range(self.get_width()):
            for j in range(self.get_height()):
                print(f'{user_field[i][j]} | ', end='')
            print(end='\n')
        print(end='\n')

    def form_ai_board(self):
        print('\nПоле компьютера')
        ai_field = []
        for i in range(self.get_width()):
            dots = []
            for j in range(self.get_height()):
                dots += [0]
            ai_field.append(dots)
        ai_field[0][0] = ' '
        for i in range(1, self.get_width()):
            ai_field[i][0] = i
        for j in range(1, self.get_height()):
            ai_field[0][j] = j
        for i in range(len(self.get_ai_ship_hit())):
            a = self.get_ai_ship_hit()[i][0]
            b = self.get_ai_ship_hit()[i][1]
            ai_field[a][b] = 'X'
        for i in range(len(self.get_user_dots_hit())):
            a = self.get_user_dots_hit()[i][0]
            b = self.get_user_dots_hit()[i][1]
            ai_field[a][b] = 'T'
        for i in range(self.get_width()):
            for j in range(self.get_height()):
                print(f'{ai_field[i][j]} | ', end='')
            print(end='\n')
        print(end='\n')

print('М О Р С К О Й   Б О Й\n')
print('Правила игры:')
print('Вы задаете параметры поля, на котором хотите играть (высоту и ширину).\nПо умолчанию вам необходимо расположить на поле 6 кораблей:\n- один 3-палубный\n- два 2-палубных\n- четыре 1-палубных\nДля много палубных кораблей вы выбираете позицию начала корабля\nи его направление (вертикальное или горизонтальное).\nВы не можете расположить корабль встык к другому.\nПосле размещения кораблей вы производите выстрелы, вводя его координаты\n(строку и столбец): например, 43 - выстрел по клетке в четвертой строке во втором столбце.\nРезультатом выстрела могут быть промах (Т) и ранение корабля (Х).\nПобеждает тот игрок, кто раньше уничтожит все корабли противника.\n')

board = Board()
w = int(input('Введите ширину поля: '))
board.set_width(w)
h = int(input('Введите высоту поля: '))
board.set_height(h)

print('\nПоле сражения:')
field = []
for i in range(board.get_width()):
    dots = []
    for j in range(board.get_height()):
        dots += [0]
    field.append(dots)
field[0][0] = ' '
for i in range(1, board.get_width()):
    field[i][0] = i
for j in range(1, board.get_height()):
    field[0][j] = j
for i in range(board.get_width()):
    for j in range(board.get_height()):
        print(f'{field[i][j]} | ', end='')
    print(end='\n')
print(end='\n')

# расставляем корабли игрока
while len(board.get_user_ship()) < 3:
    try:
        print('Разместите 3-палубный корабль')
        pos = input('Введите позицию начала корабля: ')
        if not pos.isnumeric() or len(pos) != 2:
            print('\nНеправильно введены координаты!\n')
            raise ValueError
        else:
            user_ship_3 = Ship()
            user_ship_3.set_length(3)
            x = int(pos[0])
            y = int(pos[1])
            user_ship_3.set_pos(x, y)
        user_ship_3.set_orient(input('Введите расположение корабля - вертикально (v) или горизонтально (h): '))
    except ValueError:
        pass
    else:
        user_ship_3.set_modules()
        board.set_user_ship(user_ship_3.get_modules())
        board.form_user_board()

while len(board.get_user_ship()) < 5:
    try:
        print('Разместите первый 2-палубный корабль')
        pos = input('Введите позицию начала корабля: ')
        if not pos.isnumeric() or len(pos) != 2:
            print('\nНеправильно введены координаты!\n')
            raise ValueError
        else:
            user_ship_2_1 = Ship()
            user_ship_2_1.set_length(2)
            x = int(pos[0])
            y = int(pos[1])
            user_ship_2_1.set_pos(x, y)
        user_ship_2_1.set_orient(input('Введите расположение корабля - вертикально (v) или горизонтально (h): '))
    except ValueError:
        pass
    else:
        user_ship_2_1.set_modules()
        board.set_user_ship(user_ship_2_1.get_modules())
        board.form_user_board()

while len(board.get_user_ship()) < 7:
    try:
        print('Разместите второй 2-палубный корабль')
        pos = input('Введите позицию начала корабля: ')
        if not pos.isnumeric() or len(pos) != 2:
            print('\nНеправильно введены координаты!\n')
            raise ValueError
        else:
            user_ship_2_2 = Ship()
            user_ship_2_2.set_length(2)
            x = int(pos[0])
            y = int(pos[1])
            user_ship_2_2.set_pos(x, y)
        user_ship_2_2.set_orient(input('Введите расположение корабля - вертикально (v) или горизонтально (h): '))
    except ValueError:
        pass
    else:
        user_ship_2_2.set_modules()
        board.set_user_ship(user_ship_2_2.get_modules())
        board.form_user_board()

while len(board.get_user_ship()) < 8:
    try:
        print('Разместите первый 1-палубный корабль')
        pos = input('Введите позицию корабля: ')
        if not pos.isnumeric() or len(pos) != 2:
            print('\nНеправильно введены координаты!\n')
            raise ValueError
        else:
            user_ship_1_1 = Ship()
            user_ship_1_1.set_length(1)
            x = int(pos[0])
            y = int(pos[1])
            user_ship_1_1.set_pos(x, y)
    except ValueError:
        pass
    else:
        user_ship_1_1.set_modules()
        board.set_user_ship(user_ship_1_1.get_modules())
        board.form_user_board()

while len(board.get_user_ship()) < 9:
    try:
        print('Разместите второй 1-палубный корабль')
        pos = input('Введите позицию корабля: ')
        if not pos.isnumeric() or len(pos) != 2:
            print('\nНеправильно введены координаты!\n')
            raise ValueError
        else:
            user_ship_1_2 = Ship()
            user_ship_1_2.set_length(1)
            x = int(pos[0])
            y = int(pos[1])
            user_ship_1_2.set_pos(x, y)
    except ValueError:
        pass
    else:
        user_ship_1_2.set_modules()
        board.set_user_ship(user_ship_1_2.get_modules())
        board.form_user_board()

while len(board.get_user_ship()) < 10:
    try:
        print('Разместите третий 1-палубный корабль')
        pos = input('Введите позицию корабля: ')
        if not pos.isnumeric() or len(pos) != 2:
            print('\nНеправильно введены координаты!\n')
            raise ValueError
        else:
            user_ship_1_3 = Ship()
            user_ship_1_3.set_length(1)
            x = int(pos[0])
            y = int(pos[1])
            user_ship_1_3.set_pos(x, y)
    except ValueError:
        pass
    else:
        user_ship_1_3.set_modules()
        board.set_user_ship(user_ship_1_3.get_modules())
        board.form_user_board()

while len(board.get_user_ship()) < 11:
    try:
        print('Разместите четвертый 1-палубный корабль')
        pos = input('Введите позицию корабля: ')
        if not pos.isnumeric() or len(pos) != 2:
            print('\nНеправильно введены координаты!\n')
            raise ValueError
        else:
            user_ship_1_4 = Ship()
            user_ship_1_4.set_length(1)
            x = int(pos[0])
            y = int(pos[1])
            user_ship_1_4.set_pos(x, y)
    except ValueError:
        pass
    else:
        user_ship_1_4.set_modules()
        board.set_user_ship(user_ship_1_4.get_modules())
        board.form_user_board()

# здесь формируем позиции кораблей компьютера
while len(board.get_ai_ship()) < 3:
    try:
        x = rnd.randint(1, board.get_width()-1)
        y = rnd.randint(1, board.get_height()-1)
        ai_ship_3 = Ship()
        orient = rnd.randint(1, 100)
        if orient % 2 == 1:
            ai_ship_3.set_orient('v')
        else:
            ai_ship_3.set_orient('h')
        ai_ship_3.set_length(3)
        ai_ship_3.set_pos(x, y)
    except ValueError:
        pass
    else:
        ai_ship_3.set_modules()
        board.set_ai_ship(ai_ship_3.get_modules())

while len(board.get_ai_ship()) < 5:
    try:
        x = rnd.randint(1, board.get_width()-1)
        y = rnd.randint(1, board.get_height()-1)
        ai_ship_2_1 = Ship()
        orient = rnd.randint(1, 100)
        if orient % 2 == 1:
            ai_ship_2_1.set_orient('v')
        else:
            ai_ship_2_1.set_orient('h')
        ai_ship_2_1.set_length(2)
        ai_ship_2_1.set_pos(x, y)
    except ValueError:
        pass
    else:
        ai_ship_2_1.set_modules()
        board.set_ai_ship(ai_ship_2_1.get_modules())

while len(board.get_ai_ship()) < 7:
    try:
        x = rnd.randint(1, board.get_width()-1)
        y = rnd.randint(1, board.get_height()-1)
        ai_ship_2_2 = Ship()
        orient = rnd.randint(1, 100)
        if orient % 2 == 1:
            ai_ship_2_2.set_orient('v')
        else:
            ai_ship_2_2.set_orient('h')
        ai_ship_2_2.set_length(2)
        ai_ship_2_2.set_pos(x, y)
    except ValueError:
        pass
    else:
        ai_ship_2_2.set_modules()
        board.set_ai_ship(ai_ship_2_2.get_modules())

while len(board.get_ai_ship()) < 8:
    try:
        x = rnd.randint(1, board.get_width()-1)
        y = rnd.randint(1, board.get_height()-1)
        ai_ship_1_1 = Ship()
        ai_ship_1_1.set_length(1)
        ai_ship_1_1.set_pos(x, y)
    except ValueError:
        pass
    else:
        ai_ship_1_1.set_modules()
        board.set_ai_ship(ai_ship_1_1.get_modules())

while len(board.get_ai_ship()) < 9:
    try:
        x = rnd.randint(1, board.get_width()-1)
        y = rnd.randint(1, board.get_height()-1)
        ai_ship_1_2 = Ship()
        ai_ship_1_2.set_length(1)
        ai_ship_1_2.set_pos(x, y)
    except ValueError:
        pass
    else:
        ai_ship_1_2.set_modules()
        board.set_ai_ship(ai_ship_1_2.get_modules())

while len(board.get_ai_ship()) < 10:
    try:
        x = rnd.randint(1, board.get_width()-1)
        y = rnd.randint(1, board.get_height()-1)
        ai_ship_1_3 = Ship()
        ai_ship_1_3.set_length(1)
        ai_ship_1_3.set_pos(x, y)
    except ValueError:
        pass
    else:
        ai_ship_1_3.set_modules()
        board.set_ai_ship(ai_ship_1_3.get_modules())

while len(board.get_ai_ship()) < 11:
    try:
        x = rnd.randint(1, board.get_width()-1)
        y = rnd.randint(1, board.get_height()-1)
        ai_ship_1_4 = Ship()
        ai_ship_1_4.set_length(1)
        ai_ship_1_4.set_pos(x, y)
    except ValueError:
        pass
    else:
        ai_ship_1_4.set_modules()
        board.set_ai_ship(ai_ship_1_4.get_modules())

print('\nНачинаем игру!\n')
# пока не закончатся модули кораблей у игрока или компьютера
while board.get_user_ship() != [] and board.get_ai_ship() != []:
    board.ad_user_hit()
    board.ad_ai_hit()
    board.form_user_board()
    board.form_ai_board()
if board.get_user_ship() == []:
    print('Победа компьютера!')
if board.get_ai_ship() == []:
    print('Победа игрока!')
