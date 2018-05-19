import json
import shutil
import tempfile
import uuid

from pyramid.response import Response
from pyramid.view import notfound_view_config
from pyramid.view import view_config

from .models import Image
from .utils import base64decode


MEDIA_DIR = 'media/'


class APIResponse(object):
    message = ''
    code = ''
    type = ''
    content = {}

    def __init__(self, message='', code=200, content='', type=''):
        self.message = message
        self.code = code
        self.content = content

    def __json__(self, request):
        return self.to_json(request)

    def to_json(self, request=None):
        json_resp = dict(message=self.message, code=self.code)
        json_resp.update(content=self.content)

        if request:
            request.response.status_code = self.code

        return json_resp

    json = property(to_json)

    def get_response(self):
        return Response(json.dumps(self.to_json()), status=201)


class NotFoundApiResponse(APIResponse):
    message = 'Path not found'
    code = 404


@notfound_view_config(renderer='json')
def notfound_view(request):
    response = NotFoundApiResponse()
    return response


def request_dispatch(request, dispatch_dict, **kwargs):
    if request.method in dispatch_dict.keys():
        view = dispatch_dict.get(request.method)
        return view(request, **kwargs)
    else:
        return APIResponse('Method not allowed', code=405)


def image_get(request, **kwargs):
    image = kwargs.get('obj')
    return APIResponse(code=200, content=image.to_json())


def image_put(request, **kwargs):
    image = kwargs.get('obj')

    file_content = request.json_body.get('image', '')
    image_file = base64decode(file_content)

    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(image_file)
    temp.close()

    image.update_image_matadata(temp.name)
    image.save(request.dbsession)

    return APIResponse('Updated', content=image.to_json())


def image_delete(request, **kwargs):
    image = kwargs.get('obj')
    request.dbsession.query(Image).filter_by(id=image.id).delete()
    return APIResponse('Deleted', content=image.to_json())


@view_config(route_name='image_detail', renderer='json')
def image_detail(request):
    image_id = request.matchdict.get('id')
    obj = request.dbsession.query(Image).filter_by(id=image_id).first()
    if obj:
        dispatch_dict = {
            'GET': image_get, 'PUT': image_put, 'DELETE': image_delete
        }
        return request_dispatch(request, dispatch_dict, obj=obj)
    else:
        return NotFoundApiResponse()


def imag_list_get(request, **kwargs):
    query = request.dbsession.query(Image)
    image_list = [obj.to_json() for obj in query]
    return APIResponse('Updated', content=image_list)


def image_list_post(request, **kwargs):
    file_content = request.json_body.get('image', None)
    image_file = base64decode(file_content)

    image = Image()

    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(image_file)
    temp.close()

    image.update_image_matadata(temp.name)

    media_dir = 'media'
    filename = '{}/{}.{}'.format(media_dir, uuid.uuid4().hex, image.extension)
    shutil.copy(temp.name, filename)

    image.save(request.dbsession)

    return APIResponse('Created', code=201, content=image.to_json())


@view_config(route_name='image_list', renderer='json')
def image_list(request):
    dispatch_dict = {'GET': imag_list_get, 'POST': image_list_post}
    return request_dispatch(request, dispatch_dict)
