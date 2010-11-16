# -*- coding: UTF-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level
# of this repository contains the full copyright notices and license terms.
"Currency"

import urllib
from decimal import Decimal

from trytond.model import ModelSQL, ModelView, fields


class Currency(ModelSQL, ModelView):
    'Currency'
    _name = 'currency.currency'

    auto_update = fields.Boolean('Auto Update')

    def __init__(self):
        super(Currency, self).__init__()
        self._error_messages.update({
            'config_absent': 'Configuration is absent'
            })
        self._rpc.update({
            'update_all_currencies': True
            })

    def get_services(self, cursor, user, context=None):
        """Get a list of available service
        Every service should be defined in a class method 
        which begins with _service_ For example:

        def _service_ecb(self, cursor, user, id=None, 
            name_only=False, context=None):
            '''
            :param cursor: Database Cursor
            :param user: Tryton user
            :param ids: IDs if being used for getting rate
            :param name_only: If true only the name, value pair
                of the service is returned
            :param context: Tryton Context
            '''
            if name_only:
                return ('_service_ecb', 'European Central Bank')
            # Here execute and save the rate
        """
        services = [ ]
        for attribute in dir(self):
            if attribute.startswith('_service_'):
                services.append(
                    (
                     attribute,
                     getattr(self, attribute)(
                        cursor, user, None, True, context
                        )
                        )
                    )
        return services

    def update_all_currencies(self, cursor, user, context=None):
        """
        Update all the currencies
        """
        config_obj = self.pool.get('currency.update_config')

        ids = self.search(
            cursor, user, [('auto_update', '=', True)], context=context)
        config = config_obj.browse(cursor, user , 1, context=context)
        if not (config.service or config.base_currency):
            self.raise_user_error(cursor, 'config_absent', context=context)
        method = getattr(self, config.service)
        return method(cursor, user, ids, False, context)

    def _service_yahoo(self, cursor, user,
            ids=None, name_only=False, context=None):
        '''
        Return the rate of the currency from the service
        Alternately if name only, then return the name as a
        string

        :param cursor: Database Cursor
        :param user: Tryton user
        :param id: ID if being used for getting rate
        :param name_only: If true only the name of service is returned
        :param context: Tryton Context
        '''
        if name_only:
            return 'Yahoo Finance'

        rate_obj = self.pool.get('currency.currency.rate')
        config_obj = self.pool.get('currency.update_config')
        config = config_obj.browse(cursor, user , 1, context)

        for currency in self.browse(cursor, user, ids, context):
            url = 'http://download.finance.yahoo.com/d/quotes.csv?'
            params = {
                's': '%s%s=X' % (config.base_currency.code, currency.code),
                'f': 'sl1d1t1c1ohgv',
                'e': '.csv',
                }
            reader = urllib.urlopen(url, urllib.urlencode(params))
            data = reader.read().split(',')
            rate_obj.create(cursor, user, {
                    'currency': currency.id,
                    'rate': Decimal(data[1])
                    }, context)
        return True

Currency()
