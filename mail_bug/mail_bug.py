import argparse
import getpass
import imaplib
import email
import subprocess
import keyring
from email.parser import BytesHeaderParser
from python_utility.yaml_config import YamlConfig


class MailBug:
    def __init__(self, arguments: list):
        args = self.parse_args(arguments)
        self.verbose = args.verbose
        self.command = args.command
        self.config = YamlConfig(args.config_file)

    @staticmethod
    def parse_args(arguments: list=None):
        description = 'Process mails automatically.'
        parser = argparse.ArgumentParser(description=description)

        parser.add_argument(
            '-v',
            '--verbose',
            help='Turn on some verbose messages.',
            action='store_true'
        )

        parser.add_argument(
            '-c',
            '--config_file',
            help='Config file.',
            default='~/.mail-bug.conf'
        )

        valid_commands = MailBug.get_valid_commands()
        parser.add_argument(
            'command',
            metavar='COMMAND',
            nargs='?',
            type=str,
            help='Command to run.',
            default=valid_commands[0],
            choices=valid_commands
        )

        return parser.parse_args(arguments)

    @staticmethod
    def get_mail_text(message):
        maintype = message.get_content_maintype()
        result = ''
        if maintype == 'multipart':
            for part in message.get_payload():
                if part.get_content_maintype() == 'text':
                    result = part.get_payload()
                    break
        elif maintype == 'text':
            result = message.get_payload()
        return result

    @staticmethod
    def parse_text(text):
        print('Text: ' + text)
        cmd = '/usr/local/bin/growlnotify -n mail-bug -m ' + text
        stat = subprocess.call(cmd, shell=True, executable='/bin/zsh')
        print('Stat: %d ' % stat)

    def run(self):
        try:
            if self.command == 'eat':
                result = self.eat_command()
            else:
                result = 0
        except KeyboardInterrupt:
            result = 1
            print('\nUser aborted.')

        return result

    def eat_command(self):
        username = self.config.get('username')
        if username == '':
            username = input('Username: ')
            self.config.set('username', username)
            self.config.save()

        app_name = 'mail-bug'
        password_loaded = False
        password = keyring.get_password(app_name, username)
        if password is None:
            password = getpass.getpass()
        else:
            password_loaded = True

        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(username, password)
        if not password_loaded:
            keyring.set_password(app_name, username, password)

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

        return 0

    @staticmethod
    def get_valid_commands():
        return ['help', 'eat']
