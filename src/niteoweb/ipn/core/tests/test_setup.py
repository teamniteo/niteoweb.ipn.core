# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from niteoweb.ipn.core.testing import IntegrationTestCase
from Products.CMFCore.utils import getToolByName


class TestInstall(IntegrationTestCase):
    """Test installation of niteoweb.ipn.core into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_installed(self):
        """Test if niteoweb.ipn.core is installed in portal_quickinstaller."""
        self.failUnless(self.installer.isProductInstalled('niteoweb.ipn.core'))

    def test_uninstall(self):
        """Test if niteoweb.ipn.core is cleanly uninstalled."""
        self.installer.uninstallProducts(['niteoweb.ipn.core'])
        self.failIf(self.installer.isProductInstalled('niteoweb.ipn.core'))
