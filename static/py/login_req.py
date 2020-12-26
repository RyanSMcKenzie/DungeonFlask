from functools import wraps
from flask import request, redirect, url_for, session

def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('mainPage', next=request.url))
        return func(*args, **kwargs)

    return decorated