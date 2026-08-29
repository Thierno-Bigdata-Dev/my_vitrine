from django.shortcuts import render

from .models import CustomUser


def is_vendor(func, ):
    def wrapper(request, *args, **kwargs):
        user: CustomUser = request.user
        if user.user_type != 'vendor':
            return render(request, 'common/unauthorized.html')
        return func(request, *args, **kwargs)
    return wrapper

