from django import template

register =  template.Library()

@register.filter
def pluck(query_set, key):
    # extract list of values for key 'arg' from a list of dictionaries
    try:
        return [item.get(key) for item in query_set]
    except Exception:
        return[]