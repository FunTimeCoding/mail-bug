import yaml
from os.path import expanduser, isfile


class YamlConfig:
    def __init__(self, path: str=''):
        self.settings = {}
        self.path = path

        if self.exists():
            self.path = expanduser(path)
            stream = open(self.path, 'r')
            elements = yaml.load_all(stream)
            for dictionary in elements:
                for key, value in dictionary.items():
                    self.settings[key] = value

            stream.close()

    def exists(self) -> bool:
        if isfile(self.path):
            return True
        return False

    def contains(self, key: str):
        if key in self.settings:
            return True

        return False

    def get(self, key: str) -> str:
        return self.settings.get(key, '')

    def set(self, key: str, value: str):
        self.settings[key] = value

    def remove(self, key: str) -> str:
        return self.settings.pop(key, None)

    def save(self):
        stream = open(self.path, 'w')
        stream.write(yaml.dump(self.settings, default_flow_style=False))
        stream.close()
