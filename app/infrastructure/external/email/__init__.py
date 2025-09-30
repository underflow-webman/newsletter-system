"""Email infrastructure implementations."""

from .interfaces import IEmailProvider, IEmailTemplateEngine, IEmailValidator, IEmailScheduler
from .base import BaseEmailService
from .daou import DaouEmailSenderAdapter
from .smtp import SMTPEmailService
from .sendgrid import SendGridEmailService
from .template import Jinja2TemplateEngine, MakoTemplateEngine
from .validator import EmailValidator
from .scheduler import AsyncEmailScheduler

__all__ = [
    "IEmailProvider",
    "IEmailTemplateEngine",
    "IEmailValidator",
    "IEmailScheduler",
    "BaseEmailService",
    "DaouEmailSenderAdapter",
    "SMTPEmailService",
    "SendGridEmailService",
    "Jinja2TemplateEngine",
    "MakoTemplateEngine",
    "EmailValidator",
    "AsyncEmailScheduler",
]

