
from image_api.api_v1.routes import routes as api_routes_v1
from image_api.core.routes import routes as core_routes


def includeme(config):
    config.include(core_routes)
    config.include(api_routes_v1, route_prefix='/api/v1')

    config.add_static_view('static', 'static', cache_max_age=3600)
