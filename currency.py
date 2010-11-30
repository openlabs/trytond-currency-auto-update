# -*- coding: UTF-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level
# of this repository contains the full copyright notices and license terms.
"Currency"
# pylint: disable-msg=E1101

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

    def get_services(self):
        """Get a list of available service
        Every service should be defined in a class method 
        which begins with _service_ For example:

        def _service_ecb(self, id=None, name_only=False):
            '''
            :param ids: IDs if being used for getting rate
            :param name_only: If true only the name, value pair
                of the service is returned
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
                     getattr(self, attribute)(None, True)
                    )
                )
        return services

    def update_all_currencies(self, _):
        """
        Update all the currencies
        """
        config_obj = self.pool.get('currency.update_config')

        ids = self.search([('auto_update', '=', True)])
        config = config_obj.browse(1)
        if not (config.service or config.base_currency):
            self.raise_user_error('config_absent')
        method = getattr(self, config.service)
        return method(ids, False)

    def _service_yahoo(self, ids=None, name_only=False):
        '''
        Return the rate of the currency from the service
        Alternately if name only, then return the name as a
        string

        :param id: ID if being used for getting rate
        :param name_only: If true only the name of service is returned
        '''
        if name_only:
            return 'Yahoo Finance'

        rate_obj = self.pool.get('currency.currency.rate')
        config_obj = self.pool.get('currency.update_config')
        config = config_obj.browse(1)

        for currency in self.browse(ids):
            url = 'http://download.finance.yahoo.com/d/quotes.csv?'
            params = {
                's': '%s%s=X' % (config.base_currency.code, currency.code),
                'f': 'sl1d1t1c1ohgv',
                'e': '.csv',
                }
            reader = urllib.urlopen(url, urllib.urlencode(params))
            data = reader.read().split(',')
            rate_obj.create({
                'currency': currency.id, 
                'rate': Decimal(data[1])
                    })
        return True

Currency()
