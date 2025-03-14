import re
from rest_framework.exceptions import ValidationError


class LinkOnVideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        print(value)
        reg = re.compile('^(https?:\/\/)?([\w-]{1,32}\.[\w-]{1,32})[^\s@]*$')
        tmp_val = dict(value).get(self.field)
        if not value or value is None or not bool(reg.match(tmp_val)):
            raise ValidationError('Ссылка не корректна. Не корректный формат ссылки.')
        elif "youtube.com" not in tmp_val:
            raise ValidationError(f'Ссылка на видео разрешена только с сайта youtube.com.')

