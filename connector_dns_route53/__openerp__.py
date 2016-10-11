# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Route53 DNS connector',
    'description': 'Provides two-way syncronization with Amazon Route53',
    'version': '9.0.1.0.0',
    'category': 'Connector',
    'depends': [
        'connector_dns',
    ],
    'author': 'LasLabs, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://laslabs.com',
    'data': [
        'views/dns_backend.xml',
        'views/dns_record.xml',
        'views/dns_zone.xml',
        'views/dns_menu.xml',
        'views/connector_config_settings.xml',
        'data/dns_record_type.xml',
        'security/dns.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
