from .views import index


def routes(config):
    config.add_route('index', '/')
    config.add_view(index, route_name='index')
