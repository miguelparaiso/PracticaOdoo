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
format_list = {
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
        'year':fields.date(string='Published'),
        'format':fields.selection(format_list, string='Format'),
        # 'format':fields.selection([('vinyl','Vinyl'),('cd','Cd'),('mp3','Mp3'),('mp4','Mp4')], string='Format'),
        'author_id':fields.many2many('discmanagement.author','disc_author','disc_id','author_id',string='Authors'),
        'song_id':fields.many2many('discmanagement.song','disc_song','disc_id','song_id',string='Songs'),
        'active': fields.boolean('Active', help="If the active field is set to False, it will allow you to hide the disc without removing it."),
    }
    _defaults = {
        'active': True,
        'format': 'cd',
    }

