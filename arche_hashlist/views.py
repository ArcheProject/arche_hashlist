from arche.security import PERM_MANAGE_SYSTEM
from arche.views.base import BaseView
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults

from arche_hashlist.interfaces import IHashList
from arche_hashlist import _


@view_defaults(context=IHashList, permission=PERM_MANAGE_SYSTEM)
class HashListView(BaseView):

    @view_config(renderer='arche_hashlist:templates/hashlist.pt')
    def main_view(self):
        return {}

    @view_config(name='delete_plaintext')
    def delete_unprocessed(self):
        self.context.plaintext_rows.clear()
        self.flash_messages.add(_("Cleared unprocessed plaintext rows"))
        return HTTPFound(location=self.request.resource_url(self.context))


@view_config(context=IHashList,
             name='work_on_hashing.json',
             renderer='json',
             permission=PERM_MANAGE_SYSTEM,)
class HashListWork(BaseView):

    def __call__(self):
        if self.request.GET.get('remove', False):
            remaining = self.context.hash_and_remove_plaintext(limit=100)
        else:
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
