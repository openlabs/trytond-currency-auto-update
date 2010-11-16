# -*- coding: UTF-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level
# of this repository contains the full copyright notices and license terms.

{
    'name': 'Currency Auto Update',
    'version':'1.6.0.1',
    'author': 'Openlabs Technologies & Consulting (P) LTD',
    'email':'info@openlabs.co.in',
    'website': 'http://www.openlabs.co.in/',
    'description': '''Auto update of Currency

    The module fetches rates from the internet and updates the Tryton
    rates for currencies enabled to use the auto update.

    The currently available service programmed in the module are:

    1. Yahoo Finance

    DISCLAIMER: Rates and other information are supplied by independent 
    providers identified by Openlabs and maybe delayed. All information 
    provided "as is" for informational purposes only, not intended for 
    trading purposes or advice. Openlabs or any of independent providers 
    is liable for any informational errors, incompleteness, or delays, or 
    for any actions taken in reliance on information contained herein.
    
    By installing the module , you agree to the above terms and conditions.
    ''',
    'depends' : [
        'ir',
        'currency',
        ],
    'xml' : [
        'configuration.xml',
        'currency.xml'
        ],
    'translation': [
        ],

}
