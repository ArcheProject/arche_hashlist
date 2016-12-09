from arche.security import PERM_MANAGE_SYSTEM
from arche.views.base import BaseView
from pyramid.view import view_config

from arche_hashlist.interfaces import IHashList


@view_config(context=IHashList,
             permission=PERM_MANAGE_SYSTEM,
             renderer='arche_hashlist:templates/hashlist.pt')
class HashListView(BaseView):

    def __call__(self):
        return {}


def includeme(config):
    config.scan(__name__)
