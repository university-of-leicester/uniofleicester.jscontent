from zope.interface import Interface
from zope import schema


class IAllowedSectionsSchema(Interface):

    section = schema.List(title=u"Allowed sections",
                          value_type=schema.TextLine())
