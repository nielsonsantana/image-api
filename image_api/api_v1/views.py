from pyramid.response import Response
from pyramid.view import view_config


def hello_world(request):
    return Response('Hello %(name)s!' % request.matchdict)


@view_config(route_name='image_detail', renderer='json')
def image_detail(request):
    return Response('Hello %(id)s!' % request.matchdict)


@view_config(route_name='image_list', renderer='json')
def image_list(request):
    return Response('Hello %(name)s!' % request.matchdict)
