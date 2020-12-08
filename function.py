import requests

from data_base import User, Session, DatingUser, Photo

TOKEN = input('Token: ')

def to_find_user_in_base(id):
    session = Session()
    finded_user = session.query(User).filter(User.vk_id == id).first()
    return finded_user


def to_find_user_in_vk(id):
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


def to_add_user(new_user):
    session = Session()
    age_from = int(input('Введите начала диапазона поиска по возрасту: '))
    age_to = int(input('Введите конец диапазона поиска по возрасту: '))
    user = User(
        vk_id=new_user['response'][0]['id'],
        first_name=new_user['response'][0]['first_name'],
        second_name=new_user['response'][0]['last_name'],
        # age=new_user['response'][0]['bdate'],
        range_age=[age_from, age_to],
        gender=new_user['response'][0]['sex'],
        city=new_user['response'][0]['city']
    )
    session.add(user)
    session.commit()

    print('Пользователь добавлен в базу.')
    return user


def to_find_dating_user(user, sex):
    response = requests.get(
        'https://api.vk.com/method/users.search',
        params={
            'access_token': TOKEN,
            'v': 5.122,
            'count': 15,
            'sex': sex,
            'age_from': user.range_age.lower,
            'age_to': user.range_age.upper,
            'city': user.city['id'],
            'has_photo': 1,
            'fields': 'relation, sex, city, bdate'

        }
    )
    return response.json()

def to_check_dating_user_in_base(user_id, dating_user_id):
    session = Session()
    checked_user = session.query(DatingUser).filter(DatingUser.vk_id == dating_user_id and DatingUser.id_User == user_id).first()
    return checked_user


def to_add_dating_user(dating_user_json, id_user):
    session = Session()
    dating_u = DatingUser(
        vk_id=dating_user_json['id'],
        first_name=dating_user_json['first_name'],
        second_name=dating_user_json['last_name'],
        # age=dating_user_json['bdate'],
        id_User=id_user
    )
    session.add(dating_u)
    session.commit()
    print(f'Пользователь добавлен в базу')
    return dating_u

def to_add_dating_user_to_black_list(dating_user_json, id_user):
    session = Session()
    dating_u = DatingUser(
        vk_id=dating_user_json['id'],
        first_name=dating_user_json['first_name'],
        second_name=dating_user_json['last_name'],
        # age=dating_user_json['bdate'],
        id_User=id_user,
        black_list=True
    )
    session.add(dating_u)
    session.commit()
    print(f'Пользователь добавлен в черный список')



def to_get_photos(dating_users):
    response = requests.get(
        'https://api.vk.com/method/photos.get',
        params={
            'access_token': TOKEN,
            'v': 5.122,
            'owner_id': dating_users['id'],
            'album_id': 'profile',
            'extended': 1
        }
    )
    return response.json()

def to_get_top_photos(photo_json, top_number):
    top_list = []
    top_like = [0]
    for photo in photo_json['response']['items']:
        link = photo['sizes'][2]['url']
        like = photo['likes']['count']
        if like > min(top_like):
            top_list.append({'link': link, 'like': like, 'id': photo['owner_id']})
            top_like.append(like)
            if len(top_like) > top_number:
                if min(top_like) == 0:
                    pass
                else:
                    for element in top_list:
                        if element['like'] == min(top_like):
                            top_list.remove(element)
                            break
                top_like.remove(min(top_like))
    return top_list

def to_add_photos(list_photo, dating_user_id):
    session = Session()
    for element in list_photo:
        photos = Photo(
            link_photo=element['link'],
            count_likes=element['like'],
            id_DatingUser=dating_user_id
        )
        session.add(photos)
        session.commit()
    print(f'Фотографии добавлены в базу')
