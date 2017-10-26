import SMTP
import mail
import console
from Constants import *
import os
import pickle


def connection_lost():
    import socket
    try:
        socket.gethostbyaddr("www.ya.ru")
    except Exception:
        return True
    return False


def view_traceback():
    import traceback
    import sys
    ex_type, ex, tb = sys.exc_info()
    traceback.print_tb(tb)
    del tb


def save_msg(options):
    assert isinstance(options, console.Options), "It is not options"
    with open('dump.pickle', 'wb') as f:
        pickle.dump(dict(options), f)


def print_options(options):
    assert isinstance(options, console.Options), "It is not options"
    result = """
    From: {sender}
    To: {to}
    Subject: {subject}

    {msg}

    Attachments: {attach}
    """
    print(
        result.format(
            sender=options.sender,
            to=options.recipients,
            subject=options.subject,
            msg=options.message,
            attach=options.attachments))


def send_msg_with_options(options):
    assert isinstance(options, console.Options), "It is not options"

    errors = {}
    if options.disable_logging:
        LOGGER.disable()
    else:
        LOGGER.enable()
    try:
        client = SMTP.SMTP((options.server, options.port),
                           encrypt=not options.disable_encryption)
        client.ehlo()
        if options.password is not None:
            client.auth(options.sender, options.password)
        if options.single:
            for recipient in options.recipients:
                _mail = mail.Mail(
                    options.sender,
                    [recipient],
                    options.subject,
                    options.message,
                    options.attachments)
                errors.update(
                    client.send_mesg(
                        options.sender,
                        [recipient],
                        str(_mail)))
        else:
            _mail = mail.Mail(
                options.sender,
                options.recipients,
                options.subject,
                options.message,
                options.attachments)
            errors = client.send_mesg(
                options.sender, options.recipients, str(_mail))
        for error in errors:
            error_str = "Wrong: %s - %s, %s" % (error,
                                                str(errors[error][0]),
                                                errors[error][1])
            print(error_str)
            LOGGER.register(log_level.ERROR, error_str)
        client.close()
        print("Message was send")
        LOGGER.register(log_level.INFO, "Message was send")

    except Exception as e:
        print("Error was occured:", e)
        if connection_lost():
            print("Connection lost. We save your message")
            save_msg(options)


def main():
    try:
        if os.path.exists('dump.pickle'):
            print("Exists not sent message")
            with open('dump.pickle', 'rb') as f:
                options = console.Options(pickle.load(f))
            print_options(options)
            if input("Do you want send message? (y/n)") == "y":
                send_msg_with_options(options)
            os.remove('dump.pickle')

        options = console.Console().parse_opt()
        send_msg_with_options(options)
    except Exception as e:
        print('Error was occured:')
        print(str(e))


if __name__ == "__main__":
    main()
