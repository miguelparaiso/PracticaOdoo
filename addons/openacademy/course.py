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

class course(osv.osv):
    _name = 'openacademy.course'
    _description = 'Courses of the academy'
    _columns = {
        'name': fields.char(string='Title', size=64, required=True, translate=True),
        'description': fields.text(string='Description', size=256, translate=True),

        # Campos relacionales
        # 'set_null' reinicia responsible_id a undefined si el responsable es eliminado
        'responsible_id': fields.many2one('res.users', ondelete='set null',string='Responsible', select=True),
        'sessions_ids': fields.one2many('openacademy.session', 'course_id', string='Sessions'),
    }
# course() # Para cerrar la clase (ya no es obligatorio)


class session(osv.osv):
    _name = 'openacademy.session'
    _description = 'Sessions of the course'
    _columns = {
        'name': fields.char(string='Title', size=64, required=True, translate=True),
        'start_date': fields.date(string='Start date'),
        'duration': fields.float(string='Duration', digits=(6, 2), help="Duration in days"),
        'seats': fields.integer(string='Seats'),

        # Campor relacionales
        # 'cascade' destruye la sesión en caso de que course_id sea eliminado
        'instructor_id': fields.many2one('res.partner',string='Instructor'),
        'course_id': fields.many2one('res.partner', ondelete='cascade', string='Course', required=True),
        'attendee_ids': fields.one2many('openacademy.attendee', 'session_id', string='Attendees')
    }


class attendee(osv.osv):
    _name = 'openacademy.attendee'

    # _rec_name redefine el campo para llegar a ver el registro en otro objeto
    # En este caso, se reinicia el nombre del partner como nombre del asistente
    _rec_name = 'partner_id'
    _description = 'Attendees of the session'
    _columns = {
        'name': fields.char(string='Title', size=64, translate=True),
        'partner_id': fields.many2one('res.partner',string='Partner'),
        'session_id': fields.many2one('openacademy.session', string='Session', required=True, ondelete='cascade'),
    }