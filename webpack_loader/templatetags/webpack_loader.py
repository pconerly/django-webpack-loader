import datetime
from django import template

from ..utils import get_bundle


register = template.Library()


def filter_by_extension(bundle, extension):
    for chunk in bundle:
        if chunk['name'].endswith('.{}'.format(extension)):
            yield chunk


def render_as_tags(bundle):
    tags = []
    for chunk in bundle:
        url = chunk.get('publicPath') or chunk['url']
        if chunk['name'].endswith('.js'):
            tags.append('<script type="text/javascript" src="{}"></script>'.format(url))
        elif chunk['name'].endswith('.css'):
            tags.append('<link type="text/css" href="{}" rel="stylesheet">'.format(url))
    return '\n'.join(tags)


@register.simple_tag
def render_bundle(bundle_name, extension=None):
    bundle = get_bundle(bundle_name)
    if extension:
        bundle = filter_by_extension(bundle, extension)
    return render_as_tags(bundle)
