from lib.yaml_config import YamlConfig
from os import remove
from os.path import isfile


def test_set_get_remove():
    config = YamlConfig()

    # should be empty
    assert config.contains('my-key') == False
    assert config.get('my-key') == ''

    # should contain something
    config.set('my-key', 'my-value')
    assert config.contains('my-key') == True
    assert config.get('my-key') == 'my-value'

    # should remove something
    config.remove('my-key')
    assert config.contains('my-key') == False
    assert config.get('my-key') == ''


def test_save():
    file = '/tmp/example.yml'

    # file should not exist
    if isfile(file):
        remove(file)
    assert isfile(file) == False

    # file should be created on save
    config = YamlConfig(file)
    assert isfile(file) == False
    config.save()
    assert config.exists() == True
    assert isfile(file) == True

    # file should be gone
    remove(file)
    assert isfile(file) == False


def test_write_and_read():
    file = '/tmp/example.yml'

    # file should not exist
    if isfile(file):
        remove(file)
    assert isfile(file) == False

    # file should be created
    writing_config = YamlConfig(file)
    writing_config.set('my-key', 'my-value')
    writing_config.save()

    # file should contain something
    reading_config = YamlConfig(file)
    assert reading_config.get('my-key') == 'my-value'

    # file should be gone
    remove(file)
    assert isfile(file) == False
