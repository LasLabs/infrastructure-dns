# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api

class DNSBackend(models.Model):
    _inherit = 'dns.backend'

    @api.model
    def _select_version(self):
        """ It injects Amazon Route53 into backend types """
        res = super(DNSBackend, self)._select_version()
        return [('route53_boto3', 'Route53')] + res
