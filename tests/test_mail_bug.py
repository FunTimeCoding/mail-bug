from mail_bug.mail_bug import MailBug


def test_return_code():
    bug = MailBug([])
    assert bug.run() == 0
