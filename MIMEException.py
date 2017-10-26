from Constants import *


class MIMEException(Exception):
    pass


class MIMEWrongInstance(MIMEException):
    @LOGGER.log(log_level.ERROR, "Wrong instance")
    def __init__(self, instance):
        self.instance = instance

    def __str__(self):
        return "Wrong instance, object must be " + str(self.instance)
