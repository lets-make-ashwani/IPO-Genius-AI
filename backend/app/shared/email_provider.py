import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from abc import ABC, abstractmethod
from app.config.settings import settings

logger = logging.getLogger("app")

class BaseEmailProvider(ABC):
    """
    Abstract base email provider to support future integrations
    such as Resend, SendGrid, Amazon SES, or Postmark.
    """
    @abstractmethod
    def send_email(self, to_email: str, subject: str, body_text: str, body_html: str = None) -> bool:
        pass


class SMTPEmailProvider(BaseEmailProvider):
    """
    Real SMTP Email Provider using standard smtplib.
    Reads configuration from settings.
    """
    def send_email(self, to_email: str, subject: str, body_text: str, body_html: str = None) -> bool:
        if not settings.SMTP_HOST:
            logger.error("SMTP_HOST not configured. Cannot send SMTP email.")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = settings.SMTP_FROM
            msg["To"] = to_email

            part1 = MIMEText(body_text, "plain")
            msg.attach(part1)

            if body_html:
                part2 = MIMEText(body_html, "html")
                msg.attach(part2)

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.starttls()
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM, to_email, msg.as_string())
            
            logger.info(f"SMTP email successfully sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send SMTP email to {to_email}: {e}", exc_info=True)
            return False


class ConsoleEmailProvider(BaseEmailProvider):
    """
    Console/Stdout fallback provider for development and testing.
    Prints the email body to logs without making network calls.
    """
    def send_email(self, to_email: str, subject: str, body_text: str, body_html: str = None) -> bool:
        logger.info("============== [DEVELOPMENT CONSOLE EMAIL] ==============")
        logger.info(f"To: {to_email}")
        logger.info(f"Subject: {subject}")
        logger.info("-------------------- TEXT BODY --------------------")
        for line in body_text.splitlines():
            logger.info(line)
        logger.info("=========================================================")
        return True


# Factory to get the configured email provider
def get_email_provider() -> BaseEmailProvider:
    if settings.SMTP_HOST:
        return SMTPEmailProvider()
    return ConsoleEmailProvider()

email_provider = get_email_provider()
