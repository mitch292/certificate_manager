from typing import Generator, List, Optional
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from app import crud
from app.models import Certificate, User


class CertificateGenerator:
    user: User
    alias: str
    expiration_date: str
    private_key: Optional[bytes] = None
    certificate: Optional[bytes] = None
    def __init__(self, user: User, alias: str):
        self.user = user
        self.alias = alias
        # always default to a year, this could be an arg to the constructor later on.
        self.expiration_date = datetime.utcnow() + timedelta(days=365)

    def generate_private_key(self):
        if self.private_key:
            return self.private_key
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        self.private_key = key

        return key
    
    def generate_certificate(self):
        if self.certificate:
            return self.certificate

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
            x509.NameAttribute(NameOID.EMAIL_ADDRESS, f"{self.user.email}"),
            x509.NameAttribute(NameOID.GIVEN_NAME, f"{self.user.name}"),
        ])

        if self.private_key is None:
            self.generate_private_key()

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            self.expiration_date
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False,
        # Sign our certificate with our private key
        ).sign(self.private_key, hashes.SHA256())
        
        self.certificate = cert

        return self.certificate
    
    def get_certificate(self):
        if self.certificate:
            return self.certificate
        return self.generate_certificate()
    
    def get_private_key(self):
        if self.private_key:
            return self.private_key
        return self.generate_private_key()
    
    def to_dict(self):
        return {
            "private_key": self.get_private_key().private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
            ),
            "certificate_body": self.get_certificate().public_bytes(serialization.Encoding.PEM),
            "alias": self.alias,
            "expires_at": self.expiration_date,
            "active": True,
        }


class CertificateManager:
    certificate: Certificate
    db: Generator
    webhooks_to_notify: Optional[List[str]] = None
    def __init__(self, db: Generator, certificate: Certificate):
        self.certificate = certificate
        self.db = db

    def get_webhooks_to_notify(self):
        if self.webhooks_to_notify is None:
            self.webhooks_to_notify = crud.webhook.get_multi_by_certificate(self.db, certificate_id=self.certificate.id)
        return self.webhooks_to_notify