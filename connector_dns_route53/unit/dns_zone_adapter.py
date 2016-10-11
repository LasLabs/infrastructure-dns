# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from .backend_adapter import Route53Adapter

_logger = logging.getLogger(__name__)


class DNSZoneAdapter(Route53Adapter):
    _model_name = 'dns.zone'

    def read(self, id, attributes=None):
        """ Retrieves the delegation set for a hosted zone.

        Includes the four name servers assigned to the hosted zone.

        :param id: (str) ID of Zone in Route53
        :param attributes: (None) Not supported, all attributes provided
        :return: (dict) Hosted zone information. Syntax:
            {
                'HostedZone': {
                    'Id': 'string',
                    'Name': 'string',
                    'CallerReference': 'string',
                    'Config': {
                        'Comment': 'string',
                        'PrivateZone': True|False
                    },
                    'ResourceRecordSetCount': 123
                },
                'DelegationSet': {
                    'Id': 'string',
                    'CallerReference': 'string',
                    'NameServers': [
                        'string',
                    ]
                },
                'VPCs': [
                    {
                        'VPCRegion': 'us-east-1'|'us-west-1'|'us-west-2'|'eu-west-1'|'eu-central-1'|'ap-southeast-1'|'ap-southeast-2'|'ap-south-1'|'ap-northeast-1'|'ap-northeast-2'|'sa-east-1'|'cn-north-1',
                        'VPCId': 'string'
                    },
                ]
            }
        """
        return self.DNS.client.get_hosted_zone(Id=id)

    def search_read(self, filters):
        """ Return an iterator of hosted zones
        :param filters: (dict) Filters to search by. Valid keys:
            * None
        :returns: (iter) Iterator of recordsets from API
        """
        paginator = self.DNS.client.get_paginator(
            'list_hosted_zones',
        )
        return self._paginate_infinite(
            paginator, 'HostedZones',
        )

    def create(self, data):
        """ Creates a new public hosted zone

        Used to specify how the Domain Name System (DNS) routes traffic on the
        Internet for a domain, such as example.com, and its subdomains.

        Warning (@TODO:):
            Public hosted zones cannot be converted to a private hosted zone
            or vice versa.
            Instead, create a new hosted zone with the same name and create
            new resource record sets.

        :param data: Data to use for request. Syntax:
            {
                'Name: 'string',
                'VPC': {
                    'VPCRegion': 'us-east-1'|
                                 'us-west-1'|
                                 'us-west-2'|
                                 'eu-west-1'|
                                 'eu-central-1'|
                                 'ap-southeast-1'|
                                 'ap-southeast-2'|
                                 'ap-south-1'|
                                 'ap-northeast-1'|
                                 'ap-northeast-2'|
                                 'sa-east-1'|
                                 'cn-north-1',
                    'VPCId': 'string'
                },
                'CallerReference': 'string',
                'HostedZoneConfig': {
                    'Comment': 'string',
                    'PrivateZone': True|False
                },
                'DelegationSetId': 'string',
            }
        :returns: (dict) New record data from server. Syntax:
            {
                'HostedZone': {
                    'Id': 'string',
                    'Name': 'string',
                    'CallerReference': 'string',
                    'Config': {
                        'Comment': 'string',
                        'PrivateZone': True|False
                    },
                    'ResourceRecordSetCount': 123
                },
                'ChangeInfo': {
                    'Id': 'string',
                    'Status': 'PENDING'|'INSYNC',
                    'SubmittedAt': datetime(2015, 1, 1),
                    'Comment': 'string'
                },
                'DelegationSet': {
                    'Id': 'string',
                    'CallerReference': 'string',
                    'NameServers': [
                        'string',
                    ]
                },
                'VPC': {
                    'VPCRegion': 'us-east-1'|'us-west-1'|'us-west-2'|'eu-west-1'|'eu-central-1'|'ap-southeast-1'|'ap-southeast-2'|'ap-south-1'|'ap-northeast-1'|'ap-northeast-2'|'sa-east-1'|'cn-north-1',
                    'VPCId': 'string'
                },
                'Location': 'string'
            }
        """
        return self.DNS.client.create_hosted_zone(**data)

    def delete(self, zone_id):
        """ Delete a record on the external system
        :param zone_id: (str) ID of the Zone on Route53
        :return: (dict) Response syntax:
            {
                'ChangeInfo': {
                    'Id': 'string',
                    'Status': 'PENDING'|'INSYNC',
                    'SubmittedAt': datetime(2015, 1, 1),
                    'Comment': 'string'
                }
            }
        """
        return self.DNS.client.delete_hosted_zone(Id=zone_id)
