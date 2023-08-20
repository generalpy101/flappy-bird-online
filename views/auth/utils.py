from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Forbidden
        return view_func(*args, **kwargs)

    return decorated_view
