import os
import smtplib
from email.message import EmailMessage
import socket
from collections import namedtuple
import connexion
from flask import jsonify

EmailConfig = namedtuple("EmailConfig", ["server", "port", "email", "password"])
DefaultEmailConfig = EmailConfig(
    os.environ.get("SMTP_SERVER", "localhost"),
    int(os.environ.get("MAIL_PORT", "1025")),
    os.environ.get("MAIL_NOREPLY_ADDRESS", "noreply@mmiab.localhost"),
    os.environ.get("MAIL_SERVER_PASSWORD", ""),
)

def mib_resources_notification_send_email(body):  # noqa: E501
    """Send an email

    :param body: send an email according with request parameters
    :type body: dict | bytes

    :rtype: None
    """

    config = DefaultEmailConfig()
    if connexion.request.is_json:
        body = connexion.request.get_json()
        try:
            with smtplib.SMTP(config.server, config.port, timeout=10) as server:
                if config.password != "":
                    server.starttls()
                    server.login(config.email, config.password)

                mail = EmailMessage()
                mail["Subject"] = "MMIAB - Message from " + body["sender"]
                mail.set_content(body["body"])

                server.sendmail(config.email, body["receiver"], mail.as_string())
        except socket.timeout as e:  # pragma: no cover
            print(str(e))
            raise e
    else:  # pragma: no cover
        return jsonify({"message": "endpoint requires json arguments"}), 400

    return jsonify({"message": "success"})

