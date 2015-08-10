# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-2015 Aselcis Consulting, S.L. (https://www.aselcis.com). All Rights Reserved
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

class author(osv.osv):
    _name = 'discmanagement.author'
    _description = 'Authors'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
        'disc_id':fields.many2many('discmanagement.disc','disc_author','author_id','disc_id',string='Discs'),
        'song_id':fields.one2many('discmanagement.song','author_id',string='Singing songs'),
        'active': fields.boolean('Active', help="If the active field is set to False, it will allow you to hide the author without removing it."),
    }

    def button_ok(self, cr, uid, ids, *args):
        print "Boton Ok pulsado..."
        return True

