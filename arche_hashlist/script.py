from __future__ import unicode_literals

from repoze.catalog.query import Eq


def hash_plaintext(env, parsed_ns):
    root = env['root']
    request = env['request']
    query = Eq('type_name', 'HashList')
    docids = root.catalog.query(query)[1]
    for hashlist in request.resolve_docids(docids, perm=None):
        if hashlist.plaintext_rows:
            print("-- %r has %s unhashed. Working..." % (hashlist.title, len(hashlist.plaintext_rows)))
            while hashlist.plaintext_rows:
                print "%s remaining..." % hashlist.hash_plaintext()
            print "-- Done\n"

def includeme(config):
    config.add_script(
        hash_plaintext,
        name='hash_plaintext',
        title = 'Hash all plaintext rows in HashLists',
        can_commit = True,
    )
