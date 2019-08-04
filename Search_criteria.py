def define_search_criteria(vk, user):
    user_input_age_from = input('Введите нижнюю границу возраста для подбора пары: ')
    user_input_age_to = input('Введите верхнюю границу возраста для подбора пары: ')
    response_info = vk.users.get(user_ids=user, fields='sex,city')
    checked_info = check_user_data(vk, response_info)

    match_info = dict(
        age_from=user_input_age_from,
        age_to=user_input_age_to,
        sex=checked_info[0]['sex'],
        city=checked_info[0]['city']['id']
    )

    return match_info


def check_user_data(vk, info):

    if info[0]['sex'] == 0:
        user_input_sex = input('Введите пол пользователя, для которого подбирается пара:')
    else:
        user_input_sex = info[0]['sex']
    info[0]['sex'] = 2 if user_input_sex == 1 else 1

    if 'city' not in info[0]:
        user_input_country = input('Введите двухбуквенный код страны в стандарте ISO 3166-1 alpha-2, в которой проживает пользователь, для которого подбирается пара: ')
        response_country = vk.database.getCountries(need_all=0, code=user_input_country)
        user_input_city = input('Введите город проживания пользователя, для которого подбирается пара: ')
        response_city = vk.database.getCities(country_id=response_country['items'][0]['id'], q=user_input_city, count=1)
        info[0]['city'] = response_city['items'][0]

    return info