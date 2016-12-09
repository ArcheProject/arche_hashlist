import colander
import deform

from arche_hashlist import _


class HashListSchema(colander.Schema):
    title = colander.SchemaNode(
        colander.String(),
        title = _("Title"),
    )
    description = colander.SchemaNode(
        colander.String(),
        title = _("Description"),
        missing="",
    )
    plaintext = colander.SchemaNode(
        colander.String(),
        title = _("Add new rows to process"),
        description = _("rows_to_plaintext_description",
                        default="Note: You won't be able to see what you added if you edit again. "
                        "If you entered something by mistake, you need to delete this "
                        "content and start over. The same line will never be added twice though."),
        missing="",
        widget=deform.widget.TextAreaWidget(rows=10),
    )


def includeme(config):
    config.add_schema('HashList', HashListSchema, ['add', 'edit'])
