from urllib.parse import urlencode

import requests

from data_base import User, Session, DatingUser

OAUTH_URl = 'https://oauth.vk.com/authorize'
APP_ID = 7666552

OAUTH_PARAMS = {
    'client_id': APP_ID,
    'display': 'page',
    'scope': 'photos',
    'response_type': 'token',
    'v': 5.122
}

# print('?'.join(
#     (OAUTH_URl, urlencode(OAUTH_PARAMS))
# ))

TOKEN = ''


def to_find_user(id):
    response = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': TOKEN,
            'v': 5.122,
            'user_ids': id,
            'fields': 'sex, city, bdate'

        }
    )
    return response.json()

def to_add_user(id):
    current_user = to_find_user(id)
    # print(current_user)
    user = User(
        vk_id=id,
        first_name=current_user['response'][0]['first_name'],
        second_name=current_user['response'][0]['last_name'],
        gender=current_user['response'][0]['sex'],
        city=current_user['response'][0]['city']['title']
                        )
    session.add(user)
    session.commit()

    print('Пользователь добавлен в базу.')



def to_find_dating_user(age_from, age_to, city):
    response = requests.get(
        'https://api.vk.com/method/users.search',
        params={
            'access_token': TOKEN,
            'v': 5.122,
            'count': 1,
            'age_from': age_from,
            'age_to': age_to,
            'city': city,
            'has_photo': 1,
            'fields': 'relation, photo, sex, city, age'

        }
    )
    return (response.json())

def to_add_dating_user(dating_user_json, id):
    print(dating_user_json)
    dating_u = DatingUser(
        vk_id=dating_user_json['response']['items'][0]['id'],
        first_name=dating_user_json['response']['items'][0]['first_name'],
        second_name=dating_user_json['response']['items'][0]['last_name'],
        id_User=id
    )
    session.add(dating_u)
    session.commit()


if __name__ == '__main__':
    user_id = input('Введите свой id в vkontakte: ')
    session = Session()
    query = session.query(User).filter(User.vk_id == user_id).delete()
    if not query:
        to_add_user(user_id)

    age_from = int(input('Введите начала диапазона поиска по возрасту: '))
    age_to = int(input('Введите конец диапазона поиска по возрасту: '))
    session.query(User).filter(User.id == user_id).update(
        {"range_age": [age_from, age_to]})
    session.commit()

    dating_users = to_find_dating_user(age_from, age_to, session.query(User.city).filter(User.id == user_id))
    id = session.query(User.id).filter(User.id == user_id)
    print(id)
    to_add_dating_user(dating_users, id)


