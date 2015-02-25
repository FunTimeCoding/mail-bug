import getpass
import imaplib
import email
import subprocess
import keyring
from email.parser import BytesHeaderParser
from python_utility.yaml_config import YamlConfig


class MailBug:
    def __init__(self):
        self.config = YamlConfig('~/.mail-bug.conf')

    @staticmethod
    def get_password_for_username(username):
        password = keyring.get_password('mail-bug', username)
        if password is not None:
            return password
        else:
            print('Password not yet stored in keyring.')
            return ''

    @staticmethod
    def save_password_for_username(username, password):
        print('Storing password in keyring.')
        keyring.set_password('mail-bug', username, password)

    @staticmethod
    def get_mail_text(message):
        maintype = message.get_content_maintype()
        if maintype == 'multipart':
            for part in message.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return message.get_payload()

    @staticmethod
    def parse_text(text):
        print('Text: ' + text)
        cmd = '/usr/local/bin/growlnotify -n mail-bug -m ' + text
        stat = subprocess.call(cmd, shell=True, executable='/bin/zsh')
        print('Stat: %d ' % stat)

    def run(self):
        name = self.config.get('username')
        if name == '':
            name = input('Username: ')
            self.config.set('username', name)
            self.config.save()

        password_loaded = False
        password = self.get_password_for_username(name)
        if password == '':
            password = getpass.getpass()
        else:
            password_loaded = True

        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(name, password)
            if not password_loaded:
                self.save_password_for_username(name, password)

            mail.select()
            result, data = mail.uid('search', None, 'ALL')
            elements = data[0].split()
            header_parser = BytesHeaderParser()
            # for element in elements:
            # result, data = mail.element('fetch', element, '(BODY[HEADER])')
            # msg = header_parser.parsestr(data[0][1])
            # print(msg['From'], msg['Date'], msg['Subject'])

            for element in elements:
                result, data = mail.uid('fetch', element, '(RFC822)')
                raw_mail = data[0][1]
                header = header_parser.parsebytes(raw_mail)
                message = email.message_from_bytes(raw_mail)
                # print('Message: ' + self.getMailText(message).strip() + "\n")

                if '#mb' in header['Subject']:
                    print('From: ' + header['From'])
                    print('Date: ' + header['Date'])
                    print('Subject: ' + header['Subject'])
                    text = self.get_mail_text(message).strip()
                    self.parse_text(text)
                    mail.uid('store', element, '+FLAGS', '\\Deleted')

            mail.expunge()
            mail.close()
            mail.logout()

        except Exception as e:
            print('Error: ' + format(e))

        return 0
