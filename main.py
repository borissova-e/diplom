import function

if __name__ == '__main__':

    user_id = input('Введите свой id в vkontakte: ')
    user = function.to_find_user_in_base(user_id)
    if user is None:
        user_vk = function.to_find_user_in_vk(user_id)
        user = function.to_add_user(user_vk)

    sex_for_finding = input(f'Уточните, кого вы ищете: женщину (1) или мужчину (2)?')
    dating_users = function.to_find_dating_user(user, sex_for_finding)
    count_dating_user = 0
    for element in dating_users['response']['items']:
        if function.to_check_dating_user_in_base(user_id, element['id']) is None:
            link = ('https://vk.com/id'+str(element['id']))
            print(f'Для вас подобран пользователь {link}')
            photos = function.to_get_photos(element)
            top_photos = function.to_get_top_photos(photos, 3)
            for photo in top_photos:
                print(f"Ссылка на фото с количеством лайков {photo['like']} : {photo['link']}")
            while True:
                like_person = input('Вам нравится пользователь? (да/нет) ')
                if like_person == 'да':
                    date_user = function.to_add_dating_user(element, user.id)
                    function.to_add_photos(top_photos, date_user.id)
                    break
                elif like_person == 'нет':
                    function.to_add_dating_user_to_black_list(element, user.id)
                    break
                else:
                    print(f'Ответ непонятен.')
            while True:
                continue_question = input('Продолжить поиск? (да/нет) ')
                if continue_question == 'да' or continue_question == 'нет':
                    break
                else:
                    print(f'Ответ непонятен')
            if continue_question == 'нет':
                print(f'До свидания!')
                break
        count_dating_user += 1
        if count_dating_user == len(dating_users['response']['items']):
            print(f'Найденные пользователи закончились')
