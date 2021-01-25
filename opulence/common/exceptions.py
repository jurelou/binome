class BaseOpulenceException(Exception):
    pass

# Collectors exceptions
class BaseCollectorException(BaseOpulenceException):
    pass

class InvalidCollectorDefinition(BaseCollectorException):
    pass

class CollectorRuntimeError(BaseCollectorException):
    pass

# Agents exceptions
class BaseAgentException(BaseOpulenceException):
    pass

class CollectorNotFound(BaseAgentException):
    pass

class CollectorDisabled(BaseAgentException):
    pass