from unicodedata import category


def admin_interface():
    print('Выберите функционал (1, 2, 3, 4, 5, 6, 7)?')
    print('Добавить новый товар: 1')
    print('Удалить товар: 2')
    print('Редактировать товар: 3')
    print('Добавить нового пользователя: 4')
    print('Удалить пользователя: 5')
    print('Редактирование пользователя: 6')
    print('Просмотр заказов пользователей: 7')
    print('Выход: 8')
    try:
        admin_choice = int(input('Ваш выбор: '))
    except ValueError:
        print('Ошибка! Просьба указать номер вашего выбора (1, 2, 3, 4, 5, 6, 7, 8)?')
        admin_choice = input('Ваш выбор: ')

    while admin_choice not in [1, 2, 3, 4, 5, 6, 7, 8]:
        print('Ошибка! Просьба указать номер вашего выбора (1, 2, 3, 4, 5, 6, 7, 8)?')
        admin_choice = int(input('Ваш выбор: '))
    return admin_choice


def add_new_product(name_prod, quantity_prod, price_prod):
    # print(name_product, quantity_product, price)
    # print(dict_products[category_product])
    dict_products[category_product].append([name_prod, quantity_prod, price_prod])
    # показ товаров выбранной категории
    print(f'Успешно добавлена позиция в категорию товаров: {category_product}')
    for j in dict_products[category_product]:
        print(f'    Товар: {j[0]}, кол-во на складе, шт: {j[1]}, цена/шт., руб.: {j[2]}')

def user_find_product():
    user_find_prod_in_shop = False
    user_find = input('Введите наименование товара: ')
    # print(dict_products.items())
    for i in dict_products.items():
        for j in i[1]:
            if j[0] == user_find:
                # print(f'Найден товар: {j}')
                print(f'    Найден товар: {j[0]} в категории: {i[0]}, кол-во на складе, шт: {j[1]}, цена/шт., руб.: {j[2]}')
                user_find_prod_in_shop = True
    if not user_find_prod_in_shop:
        print('К сожалению данного товара в нашем магазине сейчас нет!')


def make_user_order():
    # заказ товаров пользователем
    if user_active['role'] == 'user':

        # пользовательский поиск товаров (по названию)
        if input('Вы хотите ввести сразу наименование товара для поиска (да / нет)? ').lower() == 'да':
            while True:
                user_find_product()
                if input('Вы хотите продолжить поиск по наименованию товара (да/нет)? ').lower() == 'нет':
                    break


        print('Выберите номер интересующей категории товаров:')
        count = 1
        for i in dict_products.keys():
            print(f'№{count} категория: {i}')
            count += 1

    user_choice = input('Номер категории товаров: ')
    list_categories = list(dict_products.keys())
    print(f'Вы выбрали категорию: {list_categories[int(user_choice) - 1]}')
    count_product = 1
    for i in dict_products[list_categories[int(user_choice) - 1]]:
        i.insert(0, count_product)
        print(f'    №{i[0]}: {i[1]}, кол-во на складе, шт: {i[2]}, цена/шт., руб.: {i[3]}')
        count_product += 1

    # фильтр по цене товара меньше 100 руб.
    my_filter_price = input('Вы хотите отобразить товары в данной категории дешевле 100 руб? (да / нет): ')
    if my_filter_price.lower() == 'да':
        result = filter(lambda price: price[3] < 100, dict_products[list_categories[int(user_choice) - 1]])
        result = list(result)  # превращаем объект filter в список
        if len(result) > 0:
            for j in result:
                print(f'    №{j[0]}: {j[1]}, кол-во на складе, шт: {j[2]}, цена/шт., руб.: {j[3]}')
        elif len(result) == 0:
            print('Товаров дешевле 100 руб. в данной категории нет!')

    order = input('Вы готовы сделать заказ? (да / нет): ')
    for k in dict_products[list_categories[int(user_choice) - 1]]:
        k.pop(0)
    number_product = None
    if order.lower() == 'да':
        number_product = int(input('Укажите номер товара: '))
        product_data = dict_products[list_categories[int(user_choice) - 1]][number_product - 1]
        count_this_product = product_data[1]

        # Обработка ввода данных (ошибка ValueError)
        while True:
            try:
                count_product = int(input('Укажите кол-во товаров / шт.: '))
                break
            except ValueError:
                print("Пожалуйста, введите целое положительное число.")

        while count_product > count_this_product:
            print('На складе нет такого кол-ва данного товара!')
            try:
                count_product = int(input('Укажите кол-во товаров / шт.: '))
                break
            except ValueError:
                print("Пожалуйста, введите целое положительное число.")
        product_data[1] -= count_product




        # user_choice - категория товара
        # dict_products - словарь продуктов
        user_order = [
            username,
            dict_products[list_categories[int(user_choice) - 1]][number_product - 1][0],
            count_product,
            count_product * dict_products[list_categories[int(user_choice) - 1]][number_product - 1][2]
        ]

        print('-----------------------')
        print('Данные по заказу:')
        print(f'Покупатель: {user_order[0]}')
        print(f'Товар: {user_order[1]}')
        print(f'шт: {user_order[2]}')
        print(f'Сумма заказа, руб.: {user_order[3]}')

        return user_order

    elif order.lower() == 'нет':
        print('Вы не сделали заказа, не выбрали ни один товар!')
        user_order = [username, None, None, None]
        return user_order

dict_products = {
    'игры': [
        ['товар 1', 10, 2000],
        ['товар 2', 5, 80],
        ['товар 3', 1, 50]
    ],
    'программы': [
        ['товар 4', 3, 500],
        ['товар 5', 6, 300],
        ['товар 6', 2, 100]
    ],
    'курсы': [
        ['товар 7', 25, 50],
        ['товар 8', 30, 30],
        ['товар 9', 20, 10]
    ]
}

# print(dict_products)

admin = {
    'username': 'admin',
    'password': '666',
    'role': 'administrator'
}

users = [
    {
        'username': 'user_1',
        'password': '111',
        'role': 'user'
    },
    {
        'username': 'user_2',
        'password': '222',
        'role': 'user'
    }
]

list_order = []  # список заказов пользователей
list_users = []
for i in users:
    list_users += [i['username']]

# print(list_users)

user_active = None
entrance = False
username = None
user_list_orders = []
while not entrance:
    print('Добро пожаловать в интернет-магазин!')
    print('Пожалуйста, авторизуйтесь.')
    username = input('Логин: ')
    password = input('Пароль: ')
    if username in list_users:
        for i in users:
            if username == i['username'] and password == i['password']:
                print(f'Добро пожаловать, {username} в наш интернет-магазин!')
                user_active = i
                entrance = True
                break
            elif username == i['username'] and password != i['password']:
                print(f'{username}, вы не прошли проверку!')

    elif username in admin['username'] and password == admin['password']:
        print(f'Добро пожаловать, {username}!')
        user_active = admin
        entrance = True
        break
    else:
        print(f'{username}, вы не прошли проверку!')

# print(user_active)
while True:
    if user_active['role'] == 'user':
        user_list_orders += [make_user_order()]
        next_order = input('Хотите сделать еще заказ (да/нет)? ')
        if next_order.lower() == 'нет':
            break
    elif user_active['role'] == 'administrator':
        break

if user_active['role'] == 'user':
    history_user_order = input('Вы хотите посмотреть список ваших заказов (да/нет)? ')
    if history_user_order.lower() == 'да':
        print('Список ваших заказов:')
        for i in user_list_orders:
            if i[1]:
                print('----------------------')
                # print(i)
                print('Данные по заказу:')
                print(f'Покупатель: {i[0]}')
                print(f'Товар: {i[1]}')
                print(f'шт: {i[2]}')
                print(f'Сумма заказа, руб.: {i[3]}')

    change_user_data = input('Может Вы хотите изменить свои учетные данные (да/нет)? ')

    if change_user_data.lower() == 'да':
        new_username = input('Введите новое имя пользователя: ')
        user_active['username'] = new_username
        new_password = input('Введите новый пароль пользователя: ')
        user_active['password'] = new_password
        print('Ваши новые учетные данные:')
        print(f'Логин: {user_active['username']}')
        print(f'Пароль: {user_active['password']}')
        print(f'Спасибо за покупки, {user_active['username']}! Ждем вас снова в нашем интернет-магазине!')

    elif change_user_data.lower() == 'нет':
        print(f'Спасибо за покупки, {user_active['username']}! Ждем вас снова в нашем интернет-магазине!')

elif user_active['role'] == 'administrator':
    while True:
        admin_choice = admin_interface()


        if  admin_choice == 1:
            while True:
                print('*********** Добавление товара **************')
                print('Сейчас на складе категории товаров / товары:')
                for i in dict_products:
                    print(i)
                    for j in dict_products[i]:
                        print(f'    Товар: {j[0]}, кол-во на складе, шт: {j[1]}, цена/шт., руб.: {j[2]}')

                # показ товаров выбранной категории
                category_product = input('Введите категорию товара: ').lower()
                print(f'Выбрана категория товаров: {category_product}')
                for j in dict_products[category_product]:
                        print(f'    Товар: {j[0]}, кол-во на складе, шт: {j[1]}, цена/шт., руб.: {j[2]}')

                # добавление товаров в выбранную категорию
                name_product = input('Введите наименование товара: ')
                quantity_product = input('Введите кол-во товара: ')
                price = input('Введите цену товара, руб.: ')

                add_new_product(name_product, quantity_product, price)
                print('************************')
                exit_choice_admin = input('Вы хотите продолжить добавлять товар на склад (да / нет)? ')
                if exit_choice_admin.lower() == 'нет':
                    break
        elif  admin_choice == 2:
            while True:
                print('*********** Удаление товара **************')
                print('Сейчас на складе категории товаров / товары:')
                for i in dict_products:
                    print(i)
                    for j in dict_products[i]:
                        print(f'    Товар: {j[0]}, кол-во на складе, шт: {j[1]}, цена/шт., руб.: {j[2]}')

                # показ товаров выбранной категории для дальнейшего удаления
                category_product = input('Введите категорию товара: ').lower()
                print(f'Выбрана категория товаров: {category_product}')
                count_product = 1
                for i in dict_products[category_product]:
                    i.insert(0, count_product)
                    print(f'    №{i[0]}: {i[1]}, кол-во на складе, шт: {i[2]}, цена/шт., руб.: {i[3]}')
                    count_product += 1

                # удаление товаров в выбранной категории
                number_delete_name_product = int(input('Введите номер удаляемого товара: '))
                # print(number_delete_name_product)

                # удаляем временную нумерацию продуктов из бд товаров
                for k in dict_products[category_product]:
                    k.pop(0)

                dict_products[category_product].pop(number_delete_name_product - 1)

                print('************************')
                print(f'Выбрана категория товаров: {category_product}')
                for i in dict_products[category_product]:
                    print(f'    Товар: {i[0]}, кол-во на складе, шт: {i[1]}, цена/шт., руб.: {i[2]}')

                print('************************')
                exit_choice_admin = input('Вы хотите продолжить удалять товар на складе (да / нет)? ')
                if exit_choice_admin.lower() == 'нет':
                    break
        elif admin_choice == 8:
            print('Всего доброго, admin!')
            break


