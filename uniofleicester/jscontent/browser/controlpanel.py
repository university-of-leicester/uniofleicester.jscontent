from zope.component import getUtility

from plone import api
from Products.Five import BrowserView
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.registry.interfaces import IRegistry

from uniofleicester.jscontent.interfaces import IAllowedSectionsSchema
from plone.z3cform import layout
from z3c.form import form


class AllowedSectionsForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IAllowedSectionsSchema


AllowedSectionsView = layout.wrap_form(AllowedSectionsForm, ControlPanelFormWrapper)
AllowedSectionsView.label = u"Allowed sections for tabbed and accordion views"


class JSAllowedView(BrowserView):

    def __call__(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IAllowedSectionsSchema)

        portal_path = api.portal.get().getPhysicalPath()
        context_path = self.context.getPhysicalPath()

        path = ('', ) + context_path[len(portal_path):]

        url = '/'.join(path) if len(path) > 1 else '/'

        return any([url.startswith(x) for x in settings.section])
