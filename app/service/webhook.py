import requests

from app.models import Certificate

def send_webhook(url: str, cert: Certificate):
    requests.post(url, data={
        "id": cert.id,
        "certificate_body": cert.certificate_body,
        "active": cert.active,
        "expires_at": cert.expires_at,
        "alias": cert.alias,
    })
