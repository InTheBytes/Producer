import pandas as pd
import random
import uuid
import datetime
import string
import re
import numpy as np
import bcrypt

N_ROLES = {'admin': 10, 'restaurant': 700, 'driver': 1800, 'customer': 8000}
N_RESTAURANTS = 800


def random_time(start, end):
    start_u = start.value // 10 ** 9
    end_u = end.value // 10 ** 9
    pd_time = pd.DatetimeIndex((10 ** 9 * np.random.randint(start_u, end_u, 1, dtype=np.int64)).view('M8[ns]'))[0]

    return pd_time.to_pydatetime()


def roles():
    role_out = []
    n = 1
    for role_name in N_ROLES:
        role_out.append({'role_id': n, 'name': role_name})
        n += 1
    return pd.DataFrame(role_out)


def make_user(role_id, first_name, last_name):
    user_id = uuid.uuid4()
    username = str(random.randint(10, 99)) + first_name + str(random.randint(10, 99))
    password = ''
    for i in range(random.randint(8, 16)):
        path = random.randint(0, 3)
        if path == 0:
            password += random.choice(string.ascii_lowercase)
        elif path == 1:
            password += random.choice(string.ascii_uppercase)
        elif path == 2:
            password += random.choice(string.digits)
        else:
            password += random.choice(string.punctuation)
    email = first_name + '.' + last_name + '@example.com'
    phone = random.randint(1000000000, 9999999999)
    active = 1
    return {'user_id': user_id,
            'user_role': role_id,
            'username': username,
            'password': password,
            'email': email,
            'phone': phone,
            'first_name': first_name,
            'last_name': last_name,
            'active': active}


def users():
    with open('data/first_names.txt', encoding='utf-8') as f:
        first_names = f.read().split('\n')
    with open('data/last_names.txt', encoding='utf-8') as f:
        last_names = f.read().split('\n')
    user_out = []
    role = 1
    for role_name in N_ROLES:
        for i in range(N_ROLES[role_name]):
            user_out.append(make_user(role, random.choice(first_names).title(), random.choice(last_names).title()))
        role += 1
    user_out = pd.DataFrame(user_out)
    user_out['password'] = user_out['password'].apply(lambda x: bcrypt.hashpw(x.encode('utf8'), bcrypt.gensalt()))
    return user_out


def make_confirmation(user_id, is_active):
    token_id = uuid.uuid4()
    confirmation_token = uuid.uuid4()
    created_date = random_time(pd.to_datetime('2021-01-01'), pd.to_datetime('2021-02-01'))
    return {'token_id': token_id,
            'user_id': user_id,
            'confirmation_token': confirmation_token,
            'created_date': created_date,
            'is_confirmed': is_active}


def confirmations(user_d):
    conf_out = []
    for user in user_d.iterrows():
        conf_out.append(make_confirmation(user[1]['user_id'], user[1]['active']))
    return pd.DataFrame(conf_out)


def make_driver(user_id):
    driver_id = uuid.uuid4()
    vehicle_id = uuid.uuid4()
    financial_id = uuid.uuid4()
    return {'driver_id': driver_id,
            'user_id': user_id,
            'vehicle_id': vehicle_id,
            'financial_id': financial_id,
            'status': 0}


def drivers(user_d):
    driver_out = []
    for user in user_d.iterrows():
        driver_out.append(make_driver(user[1]['user_id']))
    return pd.DataFrame(driver_out)


def make_payment(user_id, first_name, last_name):
    payment_id = uuid.uuid4()
    method = random.choice(['credit', 'stripe', 'debit'])
    nickname = 'main'
    expiration = random_time(pd.to_datetime('2022-01-01'), pd.to_datetime('2023-12-31'))
    account_num = str(random.randint(1000000000000000, 9999999999999999))
    code = str(random.randint(100, 999))
    return {'payment_id': payment_id,
            'user_id': user_id,
            'method': method,
            'nickname': nickname,
            'expiration': expiration,
            'account_num': account_num,
            'code': code,
            'holder_name': first_name + ' ' + last_name}


def payments(user_d):
    payment_out = []
    for user in user_d.iterrows():
        payment_out.append(make_payment(user[1]['user_id'], user[1]['first_name'], user[1]['last_name']))
    return pd.DataFrame(payment_out)


def make_restaurant(location_id, name):
    restaurant_id = uuid.uuid4()
    cuisine = random.choice(['Fast Food', 'Chicken', 'Burgers', 'Sandwiches', 'Desserts', 'Breakfast', 'Chinese',
                             'Italian', 'Mexican', 'Pizza', 'Soup', 'Seafood', 'Barbecue', 'Japanese'])
    name = re.sub(' +', ' ', name)
    return {'restaurant_id': restaurant_id,
            'location_id': location_id,
            'name': string.capwords(name, ' '),
            'cuisine': cuisine.title()}


def make_location(restaurant_d=None, address_d=None):
    location_id = uuid.uuid4()
    if restaurant_d is not None:
        full_address = list(restaurant_d['Location 1'])[0].split('\n')[0].split(' ')
        zip_code = list(restaurant_d['zipCode'])[0]
    else:
        full_address = list(address_d['address'])[0].split(' ')
        zip_code = list(address_d['zip_code'])[0]

    unit = full_address[-1]
    street = ' '.join(full_address[:-1])

    return {'location_id': location_id,
            'street': street.title(),
            'unit': unit.title(),
            'city': 'Baltimore',
            'state': 'MD',
            'zip_code': zip_code}


def locs_restaurants():
    restaurant_data = pd.read_csv('data/restaurants.csv')
    address_data = pd.read_csv('data/address_zipped.csv')
    location_out = []
    restaurant_out = []
    for i in range(N_ROLES['customer'] + N_RESTAURANTS):
        if i < N_ROLES['customer']:
            this_address = address_data.sample()
            location_out.append(make_location(address_d=this_address))
            address_data = address_data.drop(labels=this_address.index, axis=0)
        else:
            this_restaurant = restaurant_data.sample()
            this_location = make_location(restaurant_d=this_restaurant)
            location_out.append(this_location)
            restaurant_out.append(make_restaurant(this_location['location_id'], list(this_restaurant['name'])[0]))
            restaurant_data = restaurant_data.drop(labels=this_restaurant.index, axis=0)
    return pd.DataFrame(location_out), pd.DataFrame(restaurant_out)


def make_food(restaurant_id, food_d):
    food_id = uuid.uuid4()
    name = list(food_d['FOOD NAME'])[0]
    description = list(food_d['GROUP'])[0]

    if random.random() > 0.9:
        min_val = 20
        max_val = 50
    else:
        min_val = 2
        max_val = 20
    price = random.randint(min_val, max_val) - 0.01
    return {'food_id': food_id,
            'restaurant_id': restaurant_id,
            'name': name.title(),
            'price': price,
            'description': description.title()}


def food(restaurant_d):
    food_names = pd.read_csv('data/food.csv')
    food_out = []
    for restaurant in restaurant_d.iterrows():
        for i in range(random.randint(18, 50)):
            this_food = food_names.sample()
            food_out.append(make_food(restaurant[1]['restaurant_id'], this_food))
    return pd.DataFrame(food_out)


def make_manager(user_id, restaurant_id):
    return {'user_id': user_id,
            'restaurant_id': restaurant_id}


def managers(user_d, restaurant_d):
    manager_out = []
    for user in user_d.iterrows():
        restaurant = restaurant_d.sample()
        manager_out.append(make_manager(user[1]['user_id'], list(restaurant['restaurant_id'])[0]))
    return pd.DataFrame(manager_out)


def make_order(start_time, user_id, restaurant_id, location_id):
    order_id = uuid.uuid4()
    window_start = start_time + datetime.timedelta(minutes=random.randint(35, 60))
    window_end = window_start + datetime.timedelta(minutes=20)
    return {'order_id': order_id,
            'user_id': user_id,
            'restaurant_id': restaurant_id,
            'destination_id': location_id,
            'status': 4,
            'window_start': window_start,
            'window_end': window_end,
            'special_instructions': 'none'}


def make_delivery(driver_id, order_id, start_time):
    delivery_id = uuid.uuid4()
    r_0 = random.randint(5, 15)
    r_1 = random.randint(r_0 + 10, r_0 + 25)
    r_2 = random.randint(r_1 + 10, r_1 + 35)
    return {'delivery_id': delivery_id,
            'order_id': order_id,
            'driver_id': driver_id,
            'start_time': start_time + datetime.timedelta(minutes=r_0),
            'pickup_time': start_time + datetime.timedelta(minutes=r_1),
            'deliver_time': start_time + datetime.timedelta(minutes=r_2)}


def make_order_food(order_id, food_id):
    arr = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6]
    return {'order_id': order_id,
            'food_id': food_id,
            'quantity': random.choice(arr)}


def order_food(order_id, food_d):
    of_out = []
    price = 0
    arr = [2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7,
           7, 7, 7, 8, 8, 8, 9, 9, 10]
    for i in range(random.choice(arr)):
        this_food = food_d.sample()
        this_of = make_order_food(order_id, list(this_food['food_id'])[0])
        food_d = food_d.drop(index=this_food.index, axis=0)
        price += list(this_food['price'])[0] * this_of['quantity']
        of_out.append(this_of)
    return of_out, round(price, 2)


def make_transaction(payment_id, order_id, subtotal, start_time):
    transaction_id = uuid.uuid4()
    tax = round(subtotal * 0.015, 2)
    fee = random.choice([1.99, 2.99, 3.99, 4.99])
    discount = 0
    tip_percentage = random.choice([0, 0.05, 0.1, 0.15, 0.2, 0.25])
    tip = round(subtotal * tip_percentage, 2)
    total = subtotal + tax + fee - discount + tip
    return {'transaction_id': transaction_id,
            'payment_id': payment_id,
            'order_id': order_id,
            'subtotal': subtotal,
            'tax': tax,
            'fee': fee,
            'discount': discount,
            'tip': tip,
            'total': round(total, 2),
            'payment_time': start_time}


# Creates orders, transactions, deliveries
# Given customer user, driver user, restaurant, customer location, customer payment, and food data
# Currently creates one order per user
def order_trans_delivery(customer_d, driver_d, restaurant_d, location_d, payment_d, food_d):
    transaction_out = []
    delivery_out = []
    order_out = []
    order_food_out = []
    for user in customer_d.iterrows():
        # Creates an order
        # Uses random restaurants, user locations
        payment_time = random_time(pd.to_datetime('2021-01-01'), pd.to_datetime('2021-06-02'))
        u_id = user[1]['user_id']
        r_id = list(restaurant_d.sample()['restaurant_id'])[0]
        this_location = location_d.sample()
        l_id = list(this_location['location_id'])[0]
        location_d = location_d.drop(labels=this_location.index, axis=0)
        this_order = make_order(payment_time, u_id, r_id, l_id)
        order_out.append(this_order)
        o_id = this_order['order_id']

        # Creates a delivery with a random driver
        d_id = list(driver_d.sample()['driver_id'])[0]
        this_delivery = make_delivery(d_id, o_id, payment_time)
        delivery_out.append(this_delivery)

        # Creates the cart for this order, with random food based upon the restaurant
        this_food_d = food_d[food_d['restaurant_id'] == r_id]
        this_order_food, subtotal = order_food(o_id, this_food_d)
        order_food_out += this_order_food

        # Creates the transaction with the user's payment information, subtotal based upon food cart
        p_id = list(payment_d[payment_d['user_id'] == u_id]['payment_id'])[0]
        this_transaction = make_transaction(p_id, o_id, subtotal, payment_time)
        transaction_out.append(this_transaction)

    order_out = pd.DataFrame(order_out)
    transaction_out = pd.DataFrame(transaction_out)
    delivery_out = pd.DataFrame(delivery_out)
    order_food_out = pd.DataFrame(order_food_out)
    return order_out, transaction_out, delivery_out, order_food_out


def main():
    role_data = roles()
    user_data = users()
    driver_users = user_data[user_data['user_role'] == 3].reset_index(drop=True)
    manager_users = user_data[user_data['user_role'] == 2].reset_index(drop=True)
    customer_users = user_data[user_data['user_role'] == 4].reset_index(drop=True)

    confirmation_data = confirmations(user_data)
    driver_data = drivers(driver_users)
    driver_payments = payments(driver_users)
    customer_payments = payments(customer_users)

    location_data, restaurant_data = locs_restaurants()
    customer_locations = location_data[:N_ROLES['customer']]
    food_data = food(restaurant_data)
    manager_data = managers(manager_users, restaurant_data)

    order_data, transaction_data, delivery_data, order_food_data = order_trans_delivery(customer_users,
                                                                                        driver_data,
                                                                                        restaurant_data,
                                                                                        customer_locations,
                                                                                        customer_payments,
                                                                                        food_data)

    role_data.to_csv('csv/role_data.csv', index=False)
    user_data.to_csv('csv/user_data.csv', index=False)
    location_data.to_csv('csv/location_data.csv', index=False)
    pd.concat([driver_payments, customer_payments]).to_csv('csv/payment_data.csv', index=False)
    confirmation_data.to_csv('csv/confirmation_data.csv', index=False)
    driver_data.to_csv('csv/driver_data.csv', index=False)
    restaurant_data.to_csv('csv/restaurant_data.csv', index=False)
    food_data.to_csv('csv/food_data.csv', index=False)
    manager_data.to_csv('csv/manager_data.csv', index=False)
    order_data.to_csv('csv/order_data.csv', index=False)
    transaction_data.to_csv('csv/transaction_data.csv', index=False)
    delivery_data.to_csv('csv/delivery_data.csv', index=False)
    order_food_data.to_csv('csv/order_food_data.csv', index=False)


main()
user_data = pd.read_csv('csv/user_data.csv')
user_data['password'] = user_data['password'].apply(lambda x: x[2:-1])
user_data.to_csv('csv/new_user_data.csv', index=False)
