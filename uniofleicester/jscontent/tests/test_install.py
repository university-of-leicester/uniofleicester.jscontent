# -*- coding: utf8 -*-
from plone import api
import unittest2
from plone.testing.z2 import Browser
from zope.component import getMultiAdapter

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID
from plone.app.testing import login, setRoles
import transaction

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


class FunctionalTest(unittest2.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
