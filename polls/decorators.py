from functools import wraps
from django.shortcuts import redirect
import logging
logger = logging.getLogger(__name__)

def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home/flotes/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func