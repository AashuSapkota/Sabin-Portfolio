from django.core.exceptions import PermissionDenied


def only_admin():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_admin == True:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrapper_func
    return decorator


def only_users():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_admin == False:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrapper_func
    return decorator

