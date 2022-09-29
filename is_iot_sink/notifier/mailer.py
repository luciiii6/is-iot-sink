import os
import smtplib, ssl
from is_iot_sink.logger import LOG
from email.message import EmailMessage


class Mailer:
    def __init__(self) -> None:
        self.__port = os.getenv('SMTP_PORT')
        self.__smtp_server = os.getenv('SMTP_HOST')
        self.__sender = os.getenv('SMTP_SENDER')
        self.__password = os.getenv('SMTP_PASSWORD')
        
    def send_mail(self, receivers: list, log: str = '', collector_id: str = ''):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.__smtp_server, self.__port, context=context) as server:
            server.login(self.__sender, self.__password)
            for receiver in receivers:
                message = self.__prepare_message(log, collector_id, receiver)
                server.send_message(message)
                LOG.info(f'Email sent sucessfully to {receiver} !')

    def __prepare_message(self, log: str, collector_id: str, receiver):
        msg = EmailMessage()
        msg.set_content('There was a problem with your irrigation system! \n\nErrors: ' + log + f'on collector: {collector_id}')

        msg['Subject'] = 'Irrigation System Error'
        msg['From'] = self.__sender
        msg['To'] = receiver

        return msg
