class BaseOpulenceException(Exception):
    pass

class TaskTimeoutError(BaseOpulenceException):
    def __init__(self, value=None):
        self.value = value or ""

    def __str__(self):
        return "Celery task timeout: ({})".format(self.value)
