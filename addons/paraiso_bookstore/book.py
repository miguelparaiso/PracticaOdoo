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

language_list = {
    ('spanish','Spanish'),
    ('english','English'),
}

state_list = {
    ('library','Library'),
    ('warehouse','Warehouse'),
    ('Rent','Rent'),
    ('sold','Sold'),
}

class book(osv.osv):
    _name = 'bookstore.book'
    _description = 'Books'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
        'edition_date':fields.date('Edition date'),
        'language':fields.selection(language_list, string='Language'),
        'isbn':fields.char('Isbn', size=64),
        'book':fields.boolean('Book'),
        'author_id':fields.many2one('bookstore.author',ondelete='set null',string='Author'),
        'ebook':fields.boolean('Ebook'),
        'pagenumber':fields.integer('Page number'),
        'editorial':fields.char('Editorial', size=64),
        'active': fields.boolean('Active', help="If the active field is set to False, it will allow you to hide the author without removing it."),
        'extra_information':fields.text('Extra information'),
        'state':fields.selection(state_list, string='State'),
    }

    _defaults = {
        'state': 'library',
    }

