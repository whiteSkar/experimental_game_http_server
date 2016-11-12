from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from coconut.models import User

import json
import datetime

from enum import IntEnum


class ResponseStatus(IntEnum):
    SUCCESS = 1
    FAIL = 2
    INVALID_ARGUMENT = 3
    CREATE_USER = 4
    USER_WITH_SAME_DEVICE_ID_ALREADY_EXIST = 5
    USER_WITH_SAME_NAME_ALREADY_EXIST = 6

#TODO: use raise instead of status and msg I guess..?
@csrf_exempt
def create_user(request):
    args = get_post_args('user_name', 'device_id', request=request)
    user_name = args['user_name'].strip()
    device_id = args['device_id']
    ret_val = { 'status': ResponseStatus.FAIL }

    if user_name is None or not user_name:
        ret_val['status'] = ResponseStatus.INVALID_ARGUMENT
        ret_val['msg'] = 'user_name is not set'
    elif device_id is None or not device_id:
        ret_val['status'] = ResponseStatus.INVALID_ARGUMENT
        ret_val['msg'] = 'device_id is not set'
    else:
        users_with_device_id = User.objects.filter(device_id=device_id)
        users_with_user_name = User.objects.filter(user_name=user_name)
        if users_with_device_id.count() > 0:
            # probably another thread handled it already?
            ret_val['status'] = ResponseStatus.USER_WITH_SAME_DEVICE_ID_ALREADY_EXIST
            ret_val['user'] = users_with_device_id[0].user_name #TODO: return user view
        elif users_with_user_name.count() > 0:
            ret_val['status'] = ResponseStatus.USER_WITH_SAME_NAME_ALREADY_EXIST
            ret_val['msg'] = 'a user with the same user_name already exists.'
        else:
            #TODO: find out when to use timezone support and when to just use utc.
            now = datetime.datetime.now().replace(microsecond=0)
            user = User.objects.create(user_name=user_name, device_id=device_id, creation_date=now)
            ret_val['status'] = ResponseStatus.SUCCESS
            ret_val['user'] = user.user_name #TODO: return user view

    ret_val = json.dumps(ret_val)
    print(ret_val)
    return HttpResponse(ret_val)

@csrf_exempt
def authenticate_user(request):
    args = get_post_args('device_id', request=request)

    ret_val = { 'status': ResponseStatus.FAIL }
    device_id = args['device_id']
    if device_id is None or not device_id:
        ret_val['status'] = ResponseStatus.INVALID_ARGUMENT
        ret_val['msg'] = 'device_id is not set'
    else:
        users = User.objects.filter(device_id=device_id)
        if users.count() == 0:
            ret_val['status'] = ResponseStatus.CREATE_USER
        else:
            if users.count() > 1:
                print('[ERROR] - user with the same device_id exists more than one. THIS SHOULD NOT HAPPEN')

            user = users[0]
            ret_val['status'] = ResponseStatus.SUCCESS
            ret_val['user'] = user.user_name #TODO: return user view

    ret_val = json.dumps(ret_val)
    print(ret_val)
    return HttpResponse(ret_val)

def get_post_args(*args, request):
    arg_values = {}

    for arg in args:
        try:
            arg_value = request.POST[arg]
        except KeyError:
            arg_value = None

        arg_values[arg] = arg_value

    return arg_values
