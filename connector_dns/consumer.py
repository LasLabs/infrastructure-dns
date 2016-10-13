# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .unit.export_synchronizer import export_record
from openerp.addons.connector.event import (on_record_write,
                                            on_record_create,
                                            )


import logging
_logger = logging.getLogger(__name__)


@on_record_write(model_names=['dns.record.bind',
                              'dns.zone.bind',
                              ])
@on_record_create(model_names=['dns.record.bind',
                               'dns.zone.bind',
                               ])
def delay_export(session, model_name, record_id, vals):
    """ Delay a job which export a binding record.
    (A binding record being a ``dns.record.bind``,
    ``dns.zone.bind``, ...)
    """
    if session.context.get('connector_no_export'):
        return
    fields = vals.keys()
    export_record.delay(session, model_name, record_id, fields=fields)


@on_record_write(model_names=['dns.record',
                              'dns.zone',
                              ])
def delay_export_all_bindings(session, model_name, record_id, vals):
    """ Delay a job which export all the bindings of a record.
    In this case, it is called on records of normal models and will delay
    the export for all the bindings.
    """
    if session.context.get('connector_no_export'):
        return
    record = session.env[model_name].browse(record_id)
    fields = vals.keys()
    for binding in record.dns_bind_ids:
        export_record.delay(session, binding._model._name, binding.id,
                            fields=fields)
