import getpass
import imaplib
import yaml
import email
import subprocess
from os.path import expanduser
from email.parser import BytesHeaderParser

try:
    import keyring

    keyring_available = True
except ImportError:
    print('Password will not be saved because keyring is not available.')
    keyring_available = False


class MailBug:
    configPath = ''

    def __init__(self):
        home = expanduser('~')
        self.configPath = home + '/.mail-bug.conf'

    def get_username(self):
        result = ''
        try:
            stream = open(self.configPath, 'r')
            config_tree = yaml.load(stream)
            result = config_tree['username']
            stream.close()
        except IOError:
            print('Config ' + self.configPath + ' not found.')

        return result

    def save_username(self, name):
        try:
            stream = open(self.configPath, 'w')
            stream.write('')
            data = {'username': name}
            stream.write(yaml.dump(data, default_flow_style=False))
            stream.close()
        except IOError as e:
            print('Error while saving ' + self.configPath + ': ' + e.strerror)

    @staticmethod
    def get_password_for_username(username):
        result = ''
        if keyring_available:
            password = keyring.get_password('mail-bug', username)
            if password is not None:
                result = password
            else:
                print('Password not yet stored in keyring.')

        return result

    @staticmethod
    def save_password_for_username(username, password):
        if keyring_available:
            print('Storing password in keyring.')
            password = keyring.set_password('mail-bug', username, password)

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
        print('Stat: ' + stat)

    def run(self):
        name = self.get_username()
        if name == '':
            name = input('Username: ')
            self.save_username(name)

        passwordWasLoaded = False
        password = self.get_password_for_username(name)
        if password == '':
            password = getpass.getpass()
        else:
            passwordWasLoaded = True

        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(name, password)
            if not passwordWasLoaded:
                self.save_password_for_username(name, password)
        except Exception as e:
            print('Error: ' + e.message)

        try:
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
            print('Error: ' + e.message)

        return 0
