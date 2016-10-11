# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from openerp.addons.connector.unit.backend_adapter import CRUDAdapter
from openerp.addons.connector_dns.unit.backend_adapter import (DNSLocation,
                                                               DNSAdapter,
                                                               )

_logger = logging.getLogger(__name__)

try:
    import boto3
except ImportError:
    _logger.warning('Cannot Import boto3')


class Route53Location(DNSLocation):

    def __init__(self, access_key_id, access_key):
        self.uri = 'route53'
        self.login = access_key_id
        self.password = access_key
        self.client = boto3.client(
            self.uri,
            aws_access_key_id=self.login,
            aws_secret_access_key=self.password
        )


class Route53Adapter(DNSAdapter):
    """ External Records Adapter for Route53 """

    def __init__(self, environment):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.ConnectorEnvironment`
        """
        super(DNSAdapter, self).__init__(environment)
        self.DNS = Route53Location(
            self.backend_record.login,
            self.backend_record.password,
        )

    def _paginate_infinite(self, paginator, data_key, starting_token=''):
        """ It provides pagination more akin to the __iter__ protocol
        :param paginator: Paginator retrieved from
            ``self.DNS.client.get_paginator()``
        :param data_key: (str) Key that the data is returned under, such as
            ``HostedZones`` or ``ResourceRecordSets``
        :param starting_token: (str) A token to specify where to start
            paginating. This is the ``NextToken`` from a previous response.
        :yields: (dict) One recordset of data
        """
        paginate_config = {
            'PageSize': 10,
            'MaxSize': 100,
        }
        if starting_token:
            paginate_config['StartingToken'] = starting_token
        response_iterator = paginator.paginate(
            PaginationConfig=paginate_config,
        )
        for page in response_iterator:
            for item in page[data_key]:
                yield item
        try:
            if page['IsTruncated']:
                yield self._paginate_infinite(
                    paginator,
                    data_key,
                    page['NextToken'],
                )
        except KeyError:
            pass
