from __future__ import absolute_import

import copy
import inspect
import re
import traceback
import warnings
from base64 import b64decode
from distutils.util import strtobool

from django.conf import settings
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.six import string_types
from django.views.generic import View
from rpyc import BaseNetref

from flower.exceptions import HTTPError
from flower.options import options
from flower.utils import template
from ..utils import bugreport, prepend_url


class BaseHandler(View):
    template_engine = 'jinja2'

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.url_prefix = reverse("flower:main").rstrip(' / ')
        self.settings = options

    def render(self, template_name, context=None):
        if context is None:
            context = {}
        functions = inspect.getmembers(template, inspect.isfunction)
        assert not set(map(lambda x: x[0], functions)) & set(context.keys())
        context.update(functions)
        context.update({
            'url_prefix': self.url_prefix,
            'isinstance': isinstance
        })
        return render(self.request, template_name,
                      context=context,
                      using=self.template_engine)

    @staticmethod
    def json_default(o):
        warnings.warn("json dumps (%s)" % (o,), stacklevel=0)

    def write(self, data):
        # convert to local scope
        if isinstance(data, BaseNetref):
            data = copy.deepcopy(data)
        return JsonResponse(data, safe=False, json_dumps_params={
            'default': self.json_default
        })

    def write_error(self, status_code, **kwargs):
        if status_code in (404, 403):
            message = None
            if 'exc_info' in kwargs and kwargs['exc_info'][0] == Http404:
                message = kwargs['exc_info'][1].log_message
            response = self.render('flower/404.html', context={'message': message})
        elif status_code == 500:
            error_trace = ""
            for line in traceback.format_exception(*kwargs['exc_info']):
                error_trace += line

            response = self.render('error.html', context=dict(
                debug=self.settings.debug,
                status_code=status_code,
                error_trace=error_trace,
                bugreport=bugreport()
            ))
        elif status_code == 401:
            response = HttpResponse('Access denied', status=status_code)
            response['WWW-Authenticate'] = 'Basic realm="flower"'
        else:
            response = HttpResponse(status=status_code)
            if 'exc_info' in kwargs and kwargs['exc_info'][0] == Http404:
                message = kwargs['exc_info'][1].log_message
                response['Content-Type'] = 'text/plain'
                response.write(message)
        return response

    def get_current_user(self):
        # Basic Auth
        basic_auth = self.settings.basic_auth
        if basic_auth:
            auth_header = self.request.headers.get("Authorization", "")
            try:
                basic, credentials = auth_header.split()
                credentials = b64decode(credentials.encode()).decode()
                if basic != 'Basic' or credentials not in basic_auth:
                    raise HTTPError(401)
            except ValueError:
                raise HTTPError(401)

        # Google OpenID
        if not self.settings.auth:
            return True

        user = self.request.user
        username = getattr(user, settings.USERNAME_FIELD)
        if re.search(self.settings.auth, username):
            return user
        return None

    def get_argument(self, name, default=None, strip=True, type=None):
        arg = getattr(self.request, self.request.method).get(name, default)
        if isinstance(arg, string_types) and strip:
            arg = arg.strip()
        if type is not None:
            try:
                if type is bool:
                    arg = strtobool(str(arg))
                else:
                    arg = type(arg)
            except (ValueError, TypeError):
                if arg is None and default is None:
                    return arg
                raise Http404("Invalid argument '%s' of type '%s'" % (
                    arg, type.__name__))
        return arg

    @cached_property
    def capp(self):
        """return Celery application object"""
        return self.settings.app

    def reverse_url(self, *args):
        prefix = self.settings.url_prefix
        url = super(BaseHandler, self).reverse_url(*args)
        return prepend_url(url, prefix) if prefix else url
