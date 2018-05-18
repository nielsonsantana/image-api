from pyramid.response import Response
from pyramid.view import notfound_view_config
from pyramid.view import view_config


@notfound_view_config(renderer='../templates/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    return {}


def index(request):
    print("BRASIL")
    # try:
    #     query = request.dbsession.query(MyModel)
    #     one = query.filter(MyModel.name == 'one').first()
    # except DBAPIError:
    return Response('Working', content_type='text/plain', status=200)

my_view = index
