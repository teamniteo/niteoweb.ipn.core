# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from niteoweb.ipn.core.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of niteoweb.ipn.core into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if niteoweb.ipn.core is installed in portal_quickinstaller."""
        self.assertTrue(
            self.installer.isProductInstalled('niteoweb.ipn.core'))

    def test_uninstall(self):
        """Test if niteoweb.ipn.core is cleanly uninstalled."""
        self.installer.uninstallProducts(['niteoweb.ipn.core'])
        self.assertFalse(
            self.installer.isProductInstalled('niteoweb.ipn.core'))
