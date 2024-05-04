from django import template

register = template.Library()


@register.filter
def replace_commas(value):
    """Заменяет запятые на неразрывные пробелы."""
    if isinstance(value, str):
        return value.replace(',', '&nbsp;')
    return value
