import smtplib
import socket
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

class MailClient:
    def __init__(self):
        self.server_ip = "s1.ieslamar.org"
        self.ports = {
            "SMTP": 25,  # SMTP sin seguridad
            "SMTP-SUBMISSION": 587,  # SMTP autenticado sin SSL
            "IMAP": 143  # IMAP sin SSL
        }

    def check_smtp_connection(self, port):
        """Verifica si el servidor SMTP responde en el puerto especificado."""
        try:
            with socket.create_connection((self.server_ip, port), timeout=15):
                return True
        except (socket.timeout, ConnectionRefusedError):
            return False

    def send_email(self, sender_email, sender_password, recipient, subject, body):
        """Envía un correo utilizando SMTP en los puertos 587 o 25."""
        try:
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient
            message["Date"] = formatdate(localtime=True)
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain", "utf-8"))

            smtp_ports = [587, 25]  # Intenta primero 587, luego 25
            puerto_activo = None

            for smtp_port in smtp_ports:
                if self.check_smtp_connection(smtp_port):
                    puerto_activo = smtp_port
                    break  # Si encuentra un puerto disponible, lo usa

            if not puerto_activo:
                return "Error: No se pudo conectar con el servidor SMTP en los puertos (587, 25)."

            try:
                with smtplib.SMTP(self.server_ip, puerto_activo, timeout=15) as server:
                    if puerto_activo == 587:
                        server.starttls()  # Activa TLS si está en el puerto 587
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient, message.as_string())
                return f"Correo enviado correctamente a {recipient} usando el puerto {puerto_activo}"

            except smtplib.SMTPAuthenticationError:
                return "Error: Autenticación fallida. Verifica tu correo y contraseña."
            except smtplib.SMTPConnectError:
                return f"Error: No se pudo conectar al servidor en el puerto {puerto_activo}."
            except smtplib.SMTPException as e:
                return f"Error SMTP en el puerto {puerto_activo}: {str(e)}"

        except Exception as e:
            return f"Error inesperado al enviar el correo: {str(e)}"

    def fetch_emails(self, email_address, password):
        """Recibe correos utilizando IMAP sin SSL."""
        try:
            mail = imaplib.IMAP4(self.server_ip, self.ports["IMAP"])
            mail.login(email_address, password)
            mail.select("inbox")

            status, messages = mail.search(None, "ALL")
            email_ids = messages[0].split()
            emails = []

            for email_id in email_ids[-10:]:  # Obtener los últimos 10 correos
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = email.header.decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")
                        sender = msg.get("From")
                        emails.append((email_id, subject, sender))

            mail.logout()
            return emails
        except imaplib.IMAP4.error:
            return "Error: Fallo de autenticación en IMAP. Verifica tu correo y contraseña."
        except Exception as e:
            return f"Error al recibir los correos: {str(e)}"

    def delete_email(self, email_address, password, email_id):
        """Elimina un correo utilizando IMAP sin SSL."""
        try:
            mail = imaplib.IMAP4(self.server_ip, self.ports["IMAP"])
            mail.login(email_address, password)
            mail.select("inbox")

            mail.store(email_id, "+FLAGS", "\\Deleted")  # Marca el correo como eliminado
            mail.expunge()  # Borra permanentemente los correos marcados como eliminados
            mail.logout()

            return f"Correo con ID {email_id} eliminado correctamente."
        except imaplib.IMAP4.error:
            return "Error: Fallo de autenticación en IMAP. Verifica tu correo y contraseña."
        except Exception as e:
            return f"Error al eliminar el correo: {str(e)}"