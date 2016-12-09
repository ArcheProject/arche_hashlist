
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('arche_hashlist')


def includeme(config):
    config.include('.resources')
    config.include('.schemas')
    config.include('.views')
    config.include('.script')
