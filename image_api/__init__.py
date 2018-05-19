
from pyramid.config import Configurator


def _main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.routes')
    config.include('.core')
    config.include('.api_v1')
    config.include('cornice')
    config.scan()
    return config.make_wsgi_app(), config


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    wsgi, _ = _main(global_config, **settings)
    return wsgi


def main_test(global_config, **settings):
    return _main(global_config, **settings)
