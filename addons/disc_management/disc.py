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
lista_formatos = {
    ('vinyl','Vinyl'),
    ('cd','Cd'),
    ('mp3','Mp3'),
    ('mp4','Mp4'),
}

class disc(osv.osv):
    _name = 'discmanagement.disc'
    _description = 'Discs'
    _columns = {
        'name': fields.char('Title', size=64, required=True, translate=True),
        'description': fields.text('Description', size=256, translate=True),
        'year':fields.integer(string='Year of publication'),
        'format':fields.selection(lista_formatos, string='Format'),
        'publish_date': fields.date('Publish date'),
        'authors_ids':fields.many2many('discmanagement.authors','disc_author','disc_id','author_id',string='Author Ids'),
        'songs_ids':fields.many2many('discmanagement.songs','disc_song','disc_id','song_id',string='Songs Ids'),
        'active': fields.boolean('Active', help="If the active field is set to False, it will allow you to hide the disc without removing it."),
    }

