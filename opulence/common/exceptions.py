class BaseOpulenceException(Exception):
    pass


class TaskTimeoutError(BaseOpulenceException):
    def __init__(self, value=None):
        self.value = value or ""

    def __str__(self):
        return f"Celery task timeout: ({self.value})"
