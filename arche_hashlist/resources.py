from BTrees.OOBTree import OOSet
from arche.api import Content
from arche.api import ContextACLMixin
from arche.api import LocalRolesMixin
import bcrypt

from arche_hashlist import _


class HashList(Content, ContextACLMixin, LocalRolesMixin):
    type_name = "HashList"
    type_title = _("HashList")
    type_description = _("Encrypted text-rows that can be matched to this document")
    add_permission = "Add %s" % type_name
    css_icon = "glyphicon glyphicon-lock"
    nav_visible = False
    listing_visible = False
    search_visible = False
    salt = None

    def __init__(self, **kw):
        self.salt = bcrypt.gensalt()
        self.hashset = OOSet()
        self.plaintext_rows = OOSet()
        super(HashList, self).__init__(**kw)

    def check(self, value):
        return bcrypt.hashpw(value, self.salt) in self.hashset

    def hash_plaintext(self, limit=100):
        while limit and len(self.plaintext_rows):
            row = self.plaintext_rows.pop()
            hashed = bcrypt.hashpw(row, self.salt)
            if hashed not in self.hashset:
                self.hashset.add(hashed)

    @property
    def plaintext(self):
        return ''
    @plaintext.setter
    def plaintext(self, value):
        for row in value.splitlines():
            row = row.strip()
            if row not in self.plaintext_rows:
                self.plaintext_rows.add(row)


def includeme(config):
    config.add_content_factory(HashList)
