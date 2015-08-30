
# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc, Open Source Management Solution    
#    Copyright (C) 2004-2010 Juan Ignacio Ubeda (http://www.avanzosc.com). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp.osv import osv, fields

class Partner(osv.Model):
    """ Heredado de res.partner"""
    
    # la línea de arriba es la manera de Python para documentar tus objetos (como las clases)
    
    _inherit = 'res.partner'
    
    _columns = {
                # Acabamos de agregar una nueva columna en res.partner   
                'instructor' : fields.boolean(string="Instructor"),
                }
    
    _defaults = {
               'instructor' : False,
               }