from fastapi import Request
from starlette.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )


class AppException(object):
    class Create(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Object creation failed
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)

    class Get(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Object not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class Delete(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Object deletion failed
            """
            status_code = 409
            AppExceptionCase.__init__(self, status_code, context)

    class Update(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Object update failed
            """
            status_code = 409
            AppExceptionCase.__init__(self, status_code, context)

    class RequiresAuth(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Object is not public and requires auth
            """
            status_code = 401
            AppExceptionCase.__init__(self, status_code, context)
