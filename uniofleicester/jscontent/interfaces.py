from zope.interface import Interface
from zope import schema


class IAllowedSectionsSchema(Interface):

    section = schema.List(title=u"Allowed sections",
                          default=['/', ],
                          value_type=schema.TextLine())
