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

class song(osv.osv):
    _name = 'discmanagement.song'
    _description = 'Songs'
    _columns = {
        'name': fields.char('Title', size=64, required=True, translate=True),
        'author_id':fields.many2one('discmanagement.author',ondelete='set null',string='Author who sings this song'),
        'disc_id':fields.many2many('discmanagement.disc','disc_song','song_id','disc_id',string='Disc where this song is'),
        'track_time': fields.float('Track time'),
        'active': fields.boolean('Active', help="If the active field is set to False, it will allow you to hide the song without removing it."),
    }
    _defaults = {
        'active': True,
    }
