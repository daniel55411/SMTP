from Constants import *


class SMTPException(Exception):
    pass


class SMTPConnectionError(SMTPException):
    @LOGGER.log(log_level.ERROR, "Connection failed")
    def __init__(self):
        pass

    def __str__(self):
        return "Connection was failed"


class SMTPInitSessionError(SMTPException):
    @LOGGER.log(log_level.ERROR, "Session error")
    def __init__(self, server):
        self.server = server

    def __str__(self):
        return "Session error, server: " + str(self.server)


class SMTPAuthError(SMTPException):
    @LOGGER.log(log_level.ERROR, "Authenfication is Failed")
    def __init__(self):
        pass

    def __str__(self):
        return "Auth error"


class SMTPAuthProtocolError(SMTPException):
    @LOGGER.log(log_level.ERROR,
                "Auth Protocols is not supported on this server")
    def __init__(self):
        pass

    def __str__(self):
        return "Auth Protocols is not supported on this server"


class SMTPMailSenderError(SMTPException):
    @LOGGER.log(log_level.ERROR, "Error of mail sender")
    def __init__(self):
        pass

    def __str__(self):
        return "Error with mail's senders"

class SMTPEndData(SMTPException):
    @LOGGER.log(log_level.ERROR, "Error in end DATA")
    def __init__(self):
        pass

    def __str__(self):
        return "Something wrong while end DATA"

class SMTPDataError(SMTPException):
    @LOGGER.log(log_level.ERROR, "Error while DATA")
    def __init__(self):
        pass

    def __str__(self):
        return "Error while command DATA"