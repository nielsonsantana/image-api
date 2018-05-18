import json
import base64

from cornice import Service
from cornice.resource import resource
from pyramid.response import Response
from pyramid.view import view_config

from .models import Image
from .utils import extract_metadata
from .utils import base64decode

# def hello_world(request):
#     return Response('Hello %(name)s!' % request.matchdict)

# print data.encode("base64")

MEDIA_DIR = 'media/'


class APIResponse(object):
    message = ''
    code = ''
    type = ''


def request_dispatch(request, dispatch_dict):
    if request.method in dispatch_dict.keys():
        view = dispatch_dict.get(request.method)
        return view(request)
    else:
        return Response('Method not allowed', status=405)


def image_get(request):
    pass


def image_put(request):
    pass


@view_config(route_name='image_detail', request_method='GET', renderer='json')
def image_detail(request):
    dispatch_dict = {'GET': image_get, 'PUT': image_put}
    if request.method in dispatch_dict.keys():
        view = dispatch_dict.get(request.method)
        view(request)
    else:
        return Response('Method not allowed', status=405)
    return Response('Hello %(id)s!' % request.matchdict)


def image_list_post(request):
    file = request.json_body.get('image', None)
    name = request.json_body.get('name', None)
    image = base64decode(file)

    f = open(MEDIA_DIR + name, 'wb+')
    f.write(image)
    f.close()

    return Response('created', status=201)


def imag_list_get(request):
    pass


@view_config(route_name='image_list', renderer='json')
def image_list(request):
    dispatch_dict = {'GET': imag_list_get, 'POST': image_list_post}
    return request_dispatch(request, dispatch_dict)

    # dbsession = request.dbsession
    # print('json_body', request.json_body)
    # image = request.json_body.get('image', None)
    # # a = '' + 1
    # if image:
    #     image_data = base64.b64decode(image)
    #     # Image()
    #     return Response('Hello %(name)s!' % request.matchdict)
    # else:
    #     return Response(db_err_msg, content_type='text/plain', status=500)

# images = Service(name='image', path='/images/{id}', description="Image registration")

# _USERS = {}


# @images.get()
# def get_images(request):
#     """Returns a list of all users."""
#     return {'users': list(_USERS)}


# @resource(collection_path='/image', path='/image/{id}')
# class ImageView(object):

#     def __init__(self, request):
#         self.request = request
#         self.dbsession = request.dbsession

#     def collection_get(self):

#         return {
#             'notes': [
#                 {'id': note.id, 'title': note.title, 'description': note.description,
#                  'create_at': note.create_at, 'create_by':
#                  note.create_by, 'priority': note.priority}

#                 for note in DBSession.query(Image)
#             ]
#         }

#     def get(self):
#         return "lksadslkdfn"
#         try:
#             return DBSession.query(Image).get(
#                 int(self.request.matchdict['id'])).to_json()
#         except Exception:
#             return {}

#     def collection_post(self):

#         note = self.request.json
#         DBSession.add(Note.from_json(note))

#     def put(self):
#         try:
#             obj = DBSession.query(Note).filter(Note.id == self.request.matchdict['id'])
#             obj.update(self.request.json)
#             return {
#                 'notes': [
#                     {'id': note.id, 'title': note.title, 'description': note.description,
#                      'create_at': note.create_at, 'create_by': note.create_by,
#                      'priority': note.priority}
#                     for note in DBSession.query(Note)
#                 ]
#             }
#         except Exception:
#             return {'result': 'No object found'}

#     def delete(self):
#         obj = DBSession.query(Note).filter(Note.id == self.request.matchdict['id']).first()
#         DBSession.delete(obj)

#         return {
#             'notes': [
#                 {'id': note.id, 'title': note.title, 'description': note.description,
#                  'create_at': note.create_at, 'create_by':
#                  note.create_by, 'priority': note.priority}

#                 for note in DBSession.query(Note)

#             ]
#         }
