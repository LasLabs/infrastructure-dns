# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.connector_dns.backend import backend, dns

route53 = backend.Backend(parent=dns)
route53_boto3 = backend.Backend(parent=route53, version='boto-3')
