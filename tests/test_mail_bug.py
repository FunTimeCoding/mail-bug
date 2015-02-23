from lib.mail_bug import MailBug


def test_return_code():
    mb = MailBug()
    assert mb.run() == 0
