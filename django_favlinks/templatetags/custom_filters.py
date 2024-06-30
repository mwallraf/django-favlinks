# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()


def querydict_to_dict(query_dict):
    """
    Converts a QueryDict (for example, request.POST or request.GET) object to a dictionary.
    Unlike Django's QueryDict.dict() method, this function keeps lists that have two or
    more items as lists.
    """
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data


@register.filter
def get_list_as_string(value):
    q = querydict_to_dict(value).get("q") if value else None
    if q and isinstance(q, list):
        return ",".join(q)  # Convert list to string
    return q
