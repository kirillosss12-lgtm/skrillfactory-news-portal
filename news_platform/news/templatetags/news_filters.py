from django import template
import re

register = template.Library()

BAD_WORDS =[
    # Оскорбления и жаргон
    'редиска',
    'дурак',
    'идиот',
    'тупой',
    'лошара',
    'дебил',]

@register.filter(name='censor')
def censor(value):
    """
       Фильтр для цензурирования текста.
       Заменяет буквы в нежелательных словах на '*'
       """

    if not isinstance(value, str):
        return value

    text = value
    for word in BAD_WORDS:
        # Регулярное выражение для поиска слова целиком, игнорируя регистр
        # \b означает границу слова
        pattern = re.compile(re.escape(word), re.IGNORECASE)

        # Функция замены: оставляет первую букву, остальное заменяет на *
        def replace_with_stars(match):
            w = match.group(0)
            return w[0] + '*' * (len(w) - 1)

        text = pattern.sub(replace_with_stars, text)

    return text