import vk_api
import json
from Search_criteria import define_search_criteria
import Work_with_DataBase

def search_for_pretenders(vk, info):
    response_pretender = vk.users.search(
        fields='bdate,sex,city',
        age_from=info['age_from'], age_to=info['age_to'],
        sex=info['sex'], city=info['city']
    )
    cleaned_pretender_list = remove_private_profiles(response_pretender)
    return cleaned_pretender_list


def remove_private_profiles(info):
    cleaned_info = []
    for pretender in info['items']:
        if pretender['is_closed']==False:
            cleaned_info.append(pretender)
    return cleaned_info


def get_top_3_avatars(vk, info):
    pretender_list = []
    for pretender in info[0:10]:
        response_photos = vk.photos.get(owner_id=pretender['id'], album_id='profile', extended=1)
        list_to_sort = response_photos['items']
        photo_list = sorted(list_to_sort, key=lambda x: x['likes']['count'], reverse=True)
        pretender_photos = dict(id=pretender['id'], photos=[])
        for photo in photo_list[0:3]:
            pretender_photos['photos'].append(photo['sizes'][-1]['url'])
        pretender_list.append(pretender_photos)
    del info[0:10]
    return pretender_list


def main():
    # user_input_login = input('Для доступа к программе введите свой логин и пароль.\nЛогин (или номер телефона: ')
    # user_input_password = input('Пароль: ')
    scope = 'photos,groups'
    vk_session = vk_api.VkApi(login='89090680016', password='', api_version='5.101', scope=scope)
    # vk_session = vk.api.VkApi(login=user_input_login, password=user_input_password, api_version='5.101', scope=scope)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    user_input_user = input('Введите id или screen_name пользователя в ВК для поиска пары: ')
    pretender_list = search_for_pretenders(vk, define_search_criteria(vk, user_input_user))

    with open('ten_pretenders.json', 'w') as file:
        json.dump(get_top_3_avatars(vk, pretender_list), file, ensure_ascii=False, indent=2)
    Work_with_DataBase.create_models(user_input_user)

    while True:
        user_input_next_step = input('Введите n, чтобы продолжить поиск или q, чтобы выйти из программы: ')
        if user_input_next_step == 'n':
            if pretender_list:
                with open('ten_pretenders.json', 'w') as file:
                    json.dump(get_top_3_avatars(vk, pretender_list), file, ensure_ascii=False, indent=2)
                Work_with_DataBase.create_models(user_input_user)

            else:
                print('Подходящих людей больше не найдено')
        if user_input_next_step == 'q':
            break


if __name__ == '__main__':
    main()