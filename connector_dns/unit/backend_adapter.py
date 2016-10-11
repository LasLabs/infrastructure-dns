# -*- coding: utf-8 -*-
# Copyright 2015 Elico Corp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from openerp.addons.connector.unit.backend_adapter import CRUDAdapter

_logger = logging.getLogger(__name__)


class DNSLocation(object):

    def __init__(self, uri, login, password):
        self.uri = uri
        self.login = login
        self.password = password


class DNSAdapter(CRUDAdapter):
    """ External Records Adapter for DNS """

    def __init__(self, environment):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.ConnectorEnvironment`
        """
        super(DNSAdapter, self).__init__(environment)
        self.DNS = DNSLocation(
            self.backend_record.uri,
            self.backend_record.login,
            self.backend_record.password,
        )

    def search(self, filters=None):
        """ Search records according to some criterias
        and returns a list of ids """
        raise NotImplementedError

    def read(self, id, attributes=None):
        """ Returns the information of a record """
        raise NotImplementedError

    def search_read(self, filters=None):
        """ Search records according to some criterias
        and returns their information"""
        raise NotImplementedError

    def create(self, data):
        raise NotImplementedError

    def write(self, data):
        """ Update records on the external system """
        raise NotImplementedError

    def delete(self, data):
        """ Delete a record on the external system """
        raise NotImplementedError
