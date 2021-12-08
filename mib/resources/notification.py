import os
import smtplib
from smtplib import *
from email.message import EmailMessage
import socket
from collections import namedtuple
from logging import getLogger
import connexion
from flask import jsonify

EmailConfig = namedtuple("EmailConfig", ["server", "port", "email", "password"])
DefaultEmailConfig = EmailConfig(
    os.environ.get("SMTP_SERVER", "localhost"),
    int(os.environ.get("MAIL_PORT", "1025")),
    os.environ.get("MAIL_NOREPLY_ADDRESS", "noreply@mmiab.localhost"),
    os.environ.get("MAIL_SERVER_PASSWORD", ""),
)

def send_email():  # noqa: E501
    """Send an email

    :rtype: None
    """

    config = DefaultEmailConfig
    if connexion.request.is_json:
        body = connexion.request.get_json()
        try:
            with smtplib.SMTP(config.server, config.port, timeout=10) as server:
                if config.password != "":
                    server.starttls()
                    server.login(config.email, config.password)

                if "sender" not in body or body["sender"] == "":
                    return jsonify({"message": "invalid sender"}), 400

                if "recipient" not in body or body["recipient"] == "":
                    return jsonify({"message": "invalid recipient"}), 400

                if "body" not in body or body["body"] == "":
                    return jsonify({"message": "invalid email body"}), 400

                mail = EmailMessage()
                mail["Subject"] = "MMIAB - Message from " + body["sender"]
                mail.set_content(body["body"])
                server.sendmail(config.email, body["recipient"], mail.as_string())
        except Exception as e:  # pragma: no cover
            return jsonify({"message": "failure with SMTP"}), 500
    else:  # pragma: no cover
        return jsonify({"message": "endpoint requires json arguments"}), 400

    return jsonify({"message": "success"})

