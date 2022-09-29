import os
import smtplib, ssl
from is_iot_sink.logger import LOG


class Mailer:
    def __init__(self) -> None:
        self.__port = os.getenv('SMTP_PORT')
        self.__smtp_server = os.getenv('SMTP_HOST')
        self.__sender = os.getenv('SMTP_SENDER')
        self.__password = os.getenv('SMTP_PASSWORD')
        
    def send_mail(self, receivers: list, log: str = '', collectorId: str = ''):
        message = self.__prepare_message(self, log, collectorId)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.__smtp_server, self.__port, context=context) as server:
            server.login(self.__sender, self.__password)
            for receiver in receivers:
                server.sendmail(self.__sender, receiver, message)
                LOG.info(f'Email sent sucessfully to {receiver} !')
    
    def __prepare_message(self, log: str, collectorId: str):
        msg = f'There was a problem with your irigation system! \n Error: {log} on {collectorId}'
        return msg
