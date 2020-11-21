from starlette.requests import Request


def db(request: Request):
    return request.app.extra['db']
