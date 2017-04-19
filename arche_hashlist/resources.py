from base64 import b64encode

import bcrypt
from BTrees.OOBTree import OOSet
from arche.api import Content
from arche.api import ContextACLMixin
from arche.api import LocalRolesMixin
from arche.security import PERM_DELETE
from arche.security import PERM_EDIT
from arche.security import PERM_MANAGE_SYSTEM
from arche.security import PERM_MANAGE_USERS
from arche.security import PERM_VIEW
from arche.security import ROLE_ADMIN
from zope.interface import implementer

from arche_hashlist import _
from arche_hashlist.interfaces import IHashList


@implementer(IHashList)
class HashList(Content, ContextACLMixin, LocalRolesMixin):
    type_name = "HashList"
    type_title = _("HashList")
    type_description = _("Encrypted text-rows that can be matched to this document")
    add_permission = PERM_MANAGE_SYSTEM
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
        if value in self.plaintext_rows:
            return True
        value = b64encode(value.encode('utf-8'))
        return bcrypt.hashpw(value, self.salt) in self.hashset

    def hash_plaintext(self, limit=100):
        rows = list(self.plaintext_rows)[:limit]
        for row in rows:
            hashed = bcrypt.hashpw(row, self.salt)
            if hashed not in self.hashset:
                self.hashset.add(hashed)
            self.plaintext_rows.remove(row)
        return len(self.plaintext_rows)

    def hash_and_remove_plaintext(self, limit=100):
        rows = list(self.plaintext_rows)[:limit]
        for row in rows:
            hashed = bcrypt.hashpw(row, self.salt)
            if hashed in self.hashset:
                self.hashset.remove(hashed)
            self.plaintext_rows.remove(row)
        return len(self.plaintext_rows)

    @property
    def plaintext(self):
        return ''
    @plaintext.setter
    def plaintext(self, value):
        for row in value.splitlines():
            row = row.strip()
            if row and row not in self.plaintext_rows:
                self.plaintext_rows.add(b64encode(row.encode('utf-8')))


def includeme(config):
    config.add_content_factory(HashList, addable_to=('Root', 'Folder'))
    hashlist_acl = config.registry.acl.new_acl('HashList')
    hashlist_acl.add(ROLE_ADMIN, [PERM_VIEW, PERM_EDIT, PERM_MANAGE_SYSTEM, PERM_MANAGE_USERS, PERM_DELETE])
