"""Tests for Dummy Spinner."""

from niteoweb.ipn.core.interfaces import IIPN
from niteoweb.ipn.core.testing import IntegrationTestCase
from plone.app.testing import TEST_USER_ID
from zope.component import queryAdapter
from zope.testing.loggingsupport import InstalledHandler

log = InstalledHandler('niteoweb.ipn.core')


class TestDisableMember(IntegrationTestCase):
    """Test runtime flow through the disable_member() action."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.ipn = queryAdapter(self.portal, IIPN)
        self.log = log

    def tearDown(self):
        """Clean up after yourself."""
        log.clear()

    def test_disable_member_default(self):
        """Test default execution of disable_member() action."""
        self.ipn.disable_member({
            'email': TEST_USER_ID,
            'product_id': '13',
            'transaction_type': 'CANCEL',
        })

        # test log output
        self.assertEqual(len(log.records), 3)
        self._assert_log_record(
            'INFO',
            "Adding member 'test_user_1_' to Disabled group.",
        )
        self._assert_log_record(
            'INFO',
            "Revoking member 'test_user_1_' the Member role.",
        )
        self._assert_log_record(
            'INFO',
            "Disabled member 'test_user_1_'.",
        )
