from django import template
from django.conf import settings

# если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать и фильтры потеряются :(
register = template.Library()
# в шаблоне нужно будет прописывать следующий тег: {% load custom_filters %}.

'''
@register.filter(name='multiply') # регистрируем наш фильтр под именем multiply, чтоб django понимал, что это именно фильтр, а не простая функция
def multiply(value, arg): # первый аргумент здесь — это то значение, к которому надо применить фильтр, второй аргумент — это аргумент фильтра, т.е. примерно следующее будет в шаблоне value|multiply:arg
    return str(value) * arg # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон
'''


@register.filter(name='censored')
def censored(value):
    file_path = settings.BASE_DIR.joinpath(
        'newspaper/static/newspaper/russian_ban_words.txt')
    with open(file_path, 'r', encoding='utf8') as file:
        bad_words = file.readlines()
    text = value
    for word in bad_words:
        word = word.replace('\n', '')
        if word in text.lower():
            text = text.replace(word, '****')
    return text

@register.filter(name='multiply') # регистрируем наш фильтр под именем multiply, чтоб django понимал, что это именно фильтр, а не простая функция
def multiply(value, arg): # первый аргумент здесь — это то значение, к которому надо применить фильтр, второй аргумент — это аргумент фильтра, т.е. примерно следующее будет в шаблоне value|multiply:arg
    # return str(value) * arg # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон
    if isinstance(value, str) and isinstance(arg, int): # проверяем, что value -- это точно строка, а arg -- точно число, чтобы не возникло курьёзов
       return str(value) * arg
    else:
       raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}') # в случае, если кто-то неправильно воспользовался нашим тегом, выводим ошибку