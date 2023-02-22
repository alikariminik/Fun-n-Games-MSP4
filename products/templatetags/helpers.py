from django import template

register = template.Library()


@register.simple_tag
def relative_url(value, field, value_one, field_one, urlencode=None):
    # Start building URL from two given fields
    url = '?{}={}&'.format(field, value)
    url += '{}={}'.format(field_one, value_one)
    if urlencode:
        querystring = urlencode.split('&')
        # Filter exisiting query string so direction and sort are no longer present
        querystring = [q for q in querystring if not (
            'sort' in q or 'direction' in q)]
        filtered_querystring = filter(
            lambda p: p.split('=')[0] != field, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url
