from arche.security import PERM_MANAGE_SYSTEM
from arche.views.base import BaseView
from pyramid.view import view_config

from arche_hashlist.interfaces import IHashList
from arche_hashlist import _


@view_config(context=IHashList,
             permission=PERM_MANAGE_SYSTEM,
             renderer='arche_hashlist:templates/hashlist.pt')
class HashListView(BaseView):

    def __call__(self):
        return {}


@view_config(context=IHashList,
             name='work_on_hashing.json',
             renderer='json',
             permission=PERM_MANAGE_SYSTEM,)
class HashListWork(BaseView):

    def __call__(self):
        remaining = self.context.hash_plaintext(limit=100)
        if remaining:
            msg = self.request.localizer.translate(
                _("${num} remaining...", mapping={'num': remaining})
            )
        else:
            msg = self.request.localizer.translate(
                _("All done")
            )
        return {'remaining': remaining, 'msg': msg}


def includeme(config):
    config.scan(__name__)
