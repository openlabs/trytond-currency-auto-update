# -*- coding: UTF-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level
# of this repository contains the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, ModelSingleton, fields
from trytond.pyson import Eval, Bool, Not

class Configuration(ModelSingleton, ModelSQL, ModelView):
    "Currency Update Configuration"
    _name = "currency.update_config"
    _description = __doc__

    service = fields.Selection(
        'get_services', 'Service', 
        )
    base_currency = fields.Many2One(
        'currency.currency', 'Base Currency',
        help="Currency against which the rates will be updated.",
        depends=['service'], states={
                'required': Bool(Eval('service')),
                'invisible': Not(Bool(Eval('service'))),
            }
        )


    def get_services(self, cursor, user, context=None):
        """Gets the services from currency.currency
        """
        currency_obj = self.pool.get('currency.currency')
        return currency_obj.get_services(cursor, user, context)

Configuration()

