# -*- coding: utf-8 -*-
"""Tests for enable_member action."""

from DateTime import DateTime
from niteoweb.ipn.core.interfaces import IIPN
from niteoweb.ipn.core.interfaces import IMemberEnabledEvent
from niteoweb.ipn.core.testing import IntegrationTestCase
from plone import api
from zope.component import eventtesting
from zope.component import queryAdapter
from zope.testing.loggingsupport import InstalledHandler

import mock


class TestEnableMember(IntegrationTestCase):
    """Test runtime flow through the enable_member() action."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.ipn = queryAdapter(self.portal, IIPN)
        self.log = InstalledHandler('niteoweb.ipn.core')
        eventtesting.setUp()

        # create a test product group and set it's validity
        api.group.create(groupname='1')
        group = api.group.get(groupname='1')
        group.setGroupProperties(mapping={'validity': 10})

    def tearDown(self):
        """Clean up after yourself."""
        self.log.clear()
        eventtesting.clearEvents()

    @mock.patch('niteoweb.ipn.core.ipn.DateTime')
    def test_create_member(self, DT):
        """Test creating a new member with enable_member() action."""
        DT.return_value = DateTime('2012/01/01')

        self.ipn.enable_member(
            email='new@email.com',
            product_id='1',
            trans_type='SALE',
            fullname='New Member',
            affiliate='aff@email.com'
        )

        # test member exists
        self.assertTrue(api.user.get(username='new@email.com'))

        # test member is in product group
        self.assertIn(
            'new@email.com',
            [user.id for user in api.user.get_users(groupname='1')]
        )

        # test member valid_to
        self.assertEqual(
            api.user.get(username='new@email.com').getProperty('valid_to'),
            DateTime('2012/01/11')
        )

        # test event emitted
        events = list(set(eventtesting.getEvents(IMemberEnabledEvent)))
        self.assertEquals(len(events), 1)
        self.assertEquals(events[0].username, 'new@email.com')

        # test member history
        self.assert_member_history(
            username='new@email.com',
            history=['2012/01/01 00:00:00|1|SALE|enable_member']
        )

        # test log output
        self.assertEqual(len(self.log.records), 4)
        self.assert_log_record(
            'INFO',
            "Creating a new member: new@email.com",
        )
        self.assert_log_record(
            'INFO',
            "Added member 'new@email.com' to product group '1'.",
        )
        self.assert_log_record(
            'INFO',
            "Member's (new@email.com) valid_to date set to 2012/01/11.",
        )
        self.assert_log_record(
            'INFO',
            "Enabled member 'new@email.com'.",
        )
