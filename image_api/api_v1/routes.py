from .views import hello_world


def routes(config):
    config.add_route('hello', '/hello/{name}')
    config.add_view(hello_world, route_name='hello')

    config.add_route('image_detail', '/image/{id}')
    config.add_route('image_list', '/image/')
