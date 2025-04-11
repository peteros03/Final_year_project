from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.decorators import user_passes_test, login_required

def gatekeeper_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        print("Checking if user is gatekeeper...")  # 👈 add this line
        if request.user.is_authenticated and request.user.role == 'gatekeeper':
            print("User is gatekeeper")  # 👈 add this too
            return view_func(request, *args, **kwargs)
        print("User is not gatekeeper")  # 👈 also this
        return redirect('gatekeeper_login')
    return _wrapped_view


def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("teacher_login")
        if hasattr(request.user, 'profile') and request.user.profile.role == 'teacher':
            return view_func(request, *args, **kwargs)
        return redirect("teacher_login")
    return wrapper

# def teacher_required(view_func):
#     decorated_view_func = login_required(user_passes_test(
#         lambda user: user.role == 'teacher',
#         login_url='/teacher/login/'
#     )(view_func))
#     return decorated_view_func
