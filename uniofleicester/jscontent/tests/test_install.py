# -*- coding: utf8 -*-
from plone import api
import unittest2
from plone.testing.z2 import Browser
from zope.component import getMultiAdapter, getUtility

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID, TEST_USER_PASSWORD
from plone.app.testing import login, setRoles
import transaction

from plone.registry.interfaces import IRegistry
from uniofleicester.jscontent.tests.layer import FUNCTIONAL_TESTING
from uniofleicester.jscontent.tests.layer import INTEGRATION_TESTING


class IntegrationTest(unittest2.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def testSetup(self):
        # css registry
        css = api.portal.get_tool('portal_css')
        css_ids = css.getResourceIds()
        self.assertTrue('++resource++uniofleicester.jscontent/styles.css' in css_ids)

        # js registry
        js = api.portal.get_tool('portal_javascripts')
        js_ids = js.getResourceIds()
        self.assertTrue('++resource++uniofleicester.jscontent/jscontent.js' in js_ids)
        self.assertTrue('++resource++uniofleicester.jscontent/jquery.easytabs.min.js' in js_ids)

        # control panel
        cp = api.portal.get_tool('portal_controlpanel')
        actions = cp.listActions()
        a_ids = [x.id for x in actions]
        self.assertTrue('uniofleicester.jscontent.allowedsections' in a_ids)
        for act in actions:
            if act.id == 'uniofleicester.jscontent.allowedsections':
                self.assertEqual(act.category, 'Products')

        # configuration registry
        record = api.portal.get_registry_record(
            'uniofleicester.jscontent.interfaces.IAllowedSectionsSchema.section')

        self.assertEqual(record, [u'/', ])

    def testUninstall(self):
        qi = api.portal.get_tool('portal_quickinstaller')

        # the add-on should be installed
        installed = [x['id'] for x in qi.listInstalledProducts()]
        self.assertTrue('uniofleicester.jscontent' in installed)

        # so let's uninstall it
        qi.uninstallProducts(products=['uniofleicester.jscontent'])
        installed = [x['id'] for x in qi.listInstalledProducts()]
        self.assertFalse('uniofleicester.jscontent' in installed)

        # css registry
        css = api.portal.get_tool('portal_css')
        css_ids = css.getResourceIds()
        self.assertFalse('++resource++uniofleicester.jscontent/styles.css' in css_ids)

        # js registry
        js = api.portal.get_tool('portal_javascripts')
        js_ids = js.getResourceIds()
        self.assertFalse('++resource++uniofleicester.jscontent/jscontent.js' in js_ids)
        self.assertFalse('++resource++uniofleicester.jscontent/jquery.easytabs.min.js' in js_ids)

        # control panel
        cp = api.portal.get_tool('portal_controlpanel')
        actions = cp.listActions()
        a_ids = [x.id for x in actions]
        self.assertFalse('uniofleicester.jscontent.allowedsections' in a_ids)

        # configuration registry
        self.assertRaises(api.exc.InvalidParameterError,
                          api.portal.get_registry_record, 'uniofleicester.jscontent.interfaces.IAllowedSectionsSchema.section')


class FunctionalTest(unittest2.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_page(self):
        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        browser.open(self.portal.absolute_url())

        self.failUnless('resourceuniofleicester.jscontentjscontent' in browser.contents)

        from uniofleicester.jscontent.interfaces import IAllowedSectionsSchema
        registry = getUtility(IRegistry)

        settings = registry.forInterface(IAllowedSectionsSchema)

        settings.section = [u'/news/', ]
        transaction.commit()

        browser.open(self.portal.absolute_url())

        self.failIf('resourceuniofleicester.jscontentjscontent' in browser.contents)

    def test_controlpanel(self):
        setRoles(self.portal, TEST_USER_ID, ('Manager', ))
        transaction.commit()

        from uniofleicester.jscontent.interfaces import IAllowedSectionsSchema
        registry = getUtility(IRegistry)

        settings = registry.forInterface(IAllowedSectionsSchema)
        self.assertEqual(settings.section, ['/', ])

        browser = Browser(self.layer['app'])
        browser.handleErrors = False

        browser.open("{}/login".format(self.portal.absolute_url()))
        browser.getControl(name='__ac_name').value = TEST_USER_NAME
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()

        browser.open("{}/@@allowed-sections".format(self.portal.absolute_url()))
        browser.getControl(name='form.widgets.section').value = "/news\n/study"
        browser.getControl(name='form.buttons.save').click()

        self.assertEqual(settings.section, [u'/news', u'/study'])

    def test_jscontent(self):
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ('Manager', ))

        view = getMultiAdapter((self.portal, self.request), name="jscontent_allowed")
        self.assertTrue(view())

        from uniofleicester.jscontent.interfaces import IAllowedSectionsSchema
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IAllowedSectionsSchema)

        settings.section = [u'/news', u'/study']

        view = getMultiAdapter((self.portal, self.request), name="jscontent_allowed")
        self.assertFalse(view())

        news = api.content.create(self.portal, "Folder", "news", "News")
        events = api.content.create(self.portal, "Folder", "events", "Events")

        view = getMultiAdapter((news, self.request), name="jscontent_allowed")
        self.assertTrue(view())

        view = getMultiAdapter((events, self.request), name="jscontent_allowed")
        self.assertFalse(view())
