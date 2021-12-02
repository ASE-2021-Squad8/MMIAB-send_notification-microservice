import unittest
import json
import base64
import responses

from datetime import datetime


class TestEmail(unittest.TestCase):
    def setUp(self):
        from mib import create_app

        self.app = create_app()
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()


    def test_send_notification_task(self):
        # will send the email to local smtp server
        message = {
                "sender": "otto@squad.com",
                "body": "email will be not sent",
                "TESTING": True,
        }
        
        # because recipient is not present
        reply = self.client.put(
            "/api/email", json=message, content_type="application/json"
        )
        assert reply.status_code == 400

        recipient_mail = "example@example.com"
        message = {
                "sender": "otto@squad.com",
                "recipient": recipient_mail,
        }
        reply = self.client.put(
            "/api/email", json=message, content_type="application/json"
        )
        assert reply.status_code == 400

        message = {
                "recipient": recipient_mail,
                "body": "not sending this",
        }
        reply = self.client.put(
            "/api/email", json=message, content_type="application/json"
        )
        assert reply.status_code == 400

        message = {
                "sender": "fantastic@email.com",
                "recipient": recipient_mail,
                "body": "sending this",
        }
        reply = self.client.put(
            "/api/email", json=message, content_type="application/json"
        )
        assert reply.status_code == 200

