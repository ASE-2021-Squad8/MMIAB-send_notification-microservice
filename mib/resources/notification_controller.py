def mib_resources_notification_send_email(body):  # noqa: E501
    """Send an email via celery

     # noqa: E501

    :param body: send an email according with request parameters
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = EmailBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
