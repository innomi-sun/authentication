import os
from flask import request

class Message():
    def __init__(self, root=None):
        if not root:
            root = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'i18n')
        assert os.path.isdir(root), '{} is not a directory.'.format(root)
        self.root = root

    def message(key):
        pass

    def template_text(self, filename):
        target = os.path.join(self.root, self.get_locale(), filename)
        assert os.path.isfile(target), '{} not exists.'.format(target)
        with open(target) as fp:
            text = ''.join(fp.readlines())
        return text

    def template(self, filename, **kwargs):
        text = self.template_text(filename)
        for arg in kwargs.items():
            text = text.replace('%' + arg[0] + '%', arg[1])
        return text

    def get_locale(self):
        return request.accept_languages.best_match(['en', 'zh', 'ja'])
