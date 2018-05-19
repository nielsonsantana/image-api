from pyramid.response import Response


def index(request):
    return Response('Working', content_type='text/plain', status=200)
