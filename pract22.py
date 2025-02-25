import json
from abc import ABC, abstractmethod


def admin_interface():
    while True:
        print('Выберите ')
        print('1. Добавить новый товар')
        print('2. Удалить товар')
        print('3. Редактирование пользователя')
        print('4. Выход')
        while True:
            try:
                admin_choice = int(input('Ваш выбор: '))
                if admin_choice in [1, 2, 3, 4]:
                    break
                else:
                    print('Ошибка! Введите число от 1 до 4.')
            except ValueError:
                print('Ошибка! Введите число от 1 до 4.')

        if admin_choice == 1:
            add_product_to_store(store)
        elif admin_choice == 2:
            remove_product_from_store(store)
        elif admin_choice == 3:
            edit_user()
        elif admin_choice == 4:
            print('Всего доброго, admin!')
            break

# абстракция
class User(ABC):
    def __init__(self, username, password, role):
        self.__username = username
        self.__password = password
        self.__role = role

    def get_username(self):
        return self.__username


    def set_username(self, new_username):
        self.__username = new_username


    def get_password(self):
        return self.__password

    def set_password(self, new_password):
        self.__password = new_password

    def get_role(self):
        return self.__role


    @abstractmethod
    def show_interface(self):
        pass


class Admin(User):
    def show_interface(self):
        admin_interface()


class Customer(User):
    def __init__(self, username, password, role):
        super().__init__(username, password, role)
        self.__orders = []


    def get_orders(self):
        return self.__orders


    def add_order(self, order):
        self.__orders.append(order)

    def show_interface(self):
        customer_interface(self)


class Product:
    def __init__(self, name, quantity, price):
        self.__name = name
        self.__quantity = quantity
        self.__price = price


    def get_name(self):
        return self.__name


    def get_quantity(self):
        return self.__quantity


    def set_quantity(self, new_quantity):
        self.__quantity = new_quantity


    def get_price(self):
        return self.__price


class Store:
    def __init__(self):
        self.__products = {}

    def get_products(self):
        return self.__products

    def add_product(self, category, product):
        if category in self.__products:
            self.__products[category].append(product)
        else:
            self.__products[category] = [product]
        self.save_data()

    def remove_product(self, category, product_name):
        if category in self.__products:
            self.__products[category] = [p for p in self.__products[category] if p.get_name() != product_name]
        self.save_data()

    def save_data(self):
        data = {
            'products': {
                category: [
                    {'name': product.get_name(), 'quantity': product.get_quantity(), 'price': product.get_price()}
                    for product in products
                ]
                for category, products in self.__products.items()
            }
        }
        with open('store_data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


    @staticmethod
    def load_data():
        try:
            with open('store_data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                store = Store()
                for category, products in data['products'].items():
                    store.__products[category] = [
                        Product(product['name'], product['quantity'], product['price'])
                        for product in products
                    ]
                return store
        except FileNotFoundError:

            return Store()



def add_product_to_store(store):
    print('*********** Добавление товара **************')
    print('Сейчас на складе категории товаров / товары:')
    for category, products in store.get_products().items():
        print(category)
        for product in products:
            print(f'    Товар: {product.get_name()}, кол-во на складе, шт: {product.get_quantity()}, цена/шт., руб.: {product.get_price()}')

    category = input('Введите категорию товара: ').lower()
    name = input('Введите наименование товара: ')
    while True:
        try:
            quantity = int(input('Введите кол-во товара: '))
            break
        except ValueError:
            print('Ошибка! Введите целое число для количества товара.')
    while True:
        try:
            price = float(input('Введите цену товара, руб.: '))
            break
        except ValueError:
            print('Ошибка! Введите число для цены товара.')

    new_product = Product(name, quantity, price)
    store.add_product(category, new_product)
    print(f'Товар "{name}" успешно добавлен в категорию "{category}".')

def remove_product_from_store(store):
    print('*********** Удаление товара **************')
    print('Сейчас на складе категории товаров / товары:')
    for category, products in store.get_products().items():
        print(category)
        for product in products:
            print(f'    Товар: {product.get_name()}, кол-во на складе, шт: {product.get_quantity()}, цена/шт., руб.: {product.get_price()}')

    category = input('Введите категорию товара: ').lower()
    name = input('Введите наименование товара для удаления: ')
    store.remove_product(category, name)
    print(f'Товар "{name}" успешно удален из категории "{category}".')

def edit_user():
    print('*********** Редактирование пользователя **************')
    username = input('Введите имя пользователя для редактирования: ')
    new_username = input('Введите новое имя пользователя: ')
    new_password = input('Введите новый пароль: ')
    # Здесь можно добавить логику для поиска и изменения пользователя в списке пользователей
    print(f'Пользователь "{username}" успешно изменен.')

def customer_interface(customer):
    while True:
        order = make_order(store)
        if order:
            customer.add_order(order)
        if input('Хотите сделать еще заказ (да/нет)? ').lower() == 'нет':
            break
    view_orders(customer)
    change_user_data(customer)

def make_order(store):
    print('Выберите номер интересующей категории товаров:')
    categories = list(store.get_products().keys())
    for i, category in enumerate(categories, 1):
        print(f'№{i} категория: {category}')

    while True:
        try:
            user_choice = int(input('Номер категории товаров: ')) - 1
            if 0 <= user_choice < len(categories):
                break
            else:
                print('Ошибка! Введите номер из списка.')
        except ValueError:
            print('Ошибка! Введите число.')

    selected_category = categories[user_choice]
    print(f'Вы выбрали категорию: {selected_category}')


    filter_choice = input('Вы хотите отобразить товары дешевле 100 руб? (да/нет): ').lower()
    products = store.get_products()[selected_category]
    if filter_choice == 'да':
        products = [p for p in products if p.get_price() < 100]

    for i, product in enumerate(products, 1):
        print(f'    №{i}: {product.get_name()}, кол-во на складе, шт: {product.get_quantity()}, цена/шт., руб.: {product.get_price()}')

    while True:
        try:
            product_choice = int(input('Укажите номер товара: ')) - 1
            if 0 <= product_choice < len(products):
                break
            else:
                print('Ошибка! Введите номер из списка.')
        except ValueError:
            print('Ошибка! Введите число.')

    selected_product = products[product_choice]

    while True:
        try:
            quantity = int(input('Укажите кол-во товаров / шт.: '))
            if quantity > selected_product.get_quantity():
                print('На складе нет такого кол-ва данного товара!')
            else:
                break
        except ValueError:
            print('Ошибка! Введите целое число.')

    selected_product.set_quantity(selected_product.get_quantity() - quantity)
    total_price = quantity * selected_product.get_price()


    store.save_data()

    order = {
        'customer': customer.get_username(),
        'product': selected_product.get_name(),
        'quantity': quantity,
        'total_price': total_price
    }

    print('-----------------------')
    print('Данные по заказу:')
    print(f'Покупатель: {order["customer"]}')
    print(f'Товар: {order["product"]}')
    print(f'шт: {order["quantity"]}')
    print(f'Сумма заказа, руб.: {order["total_price"]}')

    return order

def view_orders(customer):
    if input('Вы хотите посмотреть список ваших заказов (да/нет)? ').lower() == 'да':
        print('Список ваших заказов:')
        for order in customer.get_orders():
            if order:
                print('----------------------')
                print('Данные по заказу:')
                print(f'Покупатель: {order["customer"]}')
                print(f'Товар: {order["product"]}')
                print(f'шт: {order["quantity"]}')
                print(f'Сумма заказа, руб.: {order["total_price"]}')

def change_user_data(customer):
    if input('Хотите изменить свои учетные данные? (да/нет): ').lower() == 'да':
        new_username = input('Введите новое имя пользователя: ')
        new_password = input('Введите новый пароль: ')
        customer.set_username(new_username)
        customer.set_password(new_password)
        print('Ваши данные успешно изменены.')


store = Store.load_data()  # Загрузка данных при начале программы
admin = Admin('admin', '666', 'administrator')
customer = Customer('user_1', '111', 'user')


def authenticate(username, password):
    if username == admin.get_username() and password == admin.get_password():
        return admin
    elif username == customer.get_username() and password == customer.get_password():
        return customer
    else:
        return None

while True:
    username = input('Логин: ')
    password = input('Пароль: ')
    user = authenticate(username, password)
    if user:
        print(f'Добро пожаловать, {user.get_username()}!')
        user.show_interface()
        break
    else:
        print('Ошибка! Попробуйте снова.')