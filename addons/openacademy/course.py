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

class course(osv.Model):
    _name = "openacademy.course"
    
    _columns = {
                'name': fields.char(string="Title", size=64, required=True),
                'description': fields.text(string="Description"),
                
                # Campos relacionales
                # 'set null' reinicia responsible_id a undefined si el responsable es eliminado
                'responsible_id': fields.many2one('res.users', ondelete='set null',string='Responsible', select=True ),
                'session_ids': fields.one2many('openacademy.session','course_id', string="Sessions"),
                }

class Session(osv.Model):
    _name = "openacademy.session"
    
    def _get_taken_seats_percent(self, seats, attendee_list):
        # Prevenir que la división entre 0 de error
        try:
            # Se necesita al menos un número decimal para obtener un valor real
            return (100.0 * len(attendee_list)) / seats
        except ZeroDivisionError:
            return 0.0
        
    def _taken_seats_percent(self, cr, uid, ids, field, arg, context=None):
        # Calcular el porcentaje que se reserva
        result = {} 
        for session in self.browse(cr, uid, ids, context=context):
            result[session.id] = self._get_taken_seats_percent(session.seats, session.attendee_ids)
        return result
        
    
    _columns = {
                'name': fields.char(string="Name", size=256, required=True),
                'start_date': fields.date(string="Start date"),
                'duration': fields.float(string="Duration", digits=(6,2), help="Duration in days"),
                'seats': fields.integer(string="Number of seats"), 
                
                # Campos relacionales
                # 'cascade' destruye la sesión en caso de que course_id sea eliminado
                'instructor_id': fields.many2one('res.partner', string="Instructor"),
                # Ejercicio 3 domains 
                #'instructor_id': fields.many2one('res.partner', string="Instructor", domain=[('instructor','=',True),('category_id.name','ilike','Teacher')]),
                'course_id': fields.many2one('openacademy.course', ondelete='cascade', string="Course", required=True),
                'attendee_ids': fields.one2many('openacademy.attendee','session_id', string="Attendees"), 
                'taken_seats_percent': fields.function(_taken_seats_percent, type='float', string='Taken seats'),       
                }
    

class Attendee(osv.Model):
    _name = "openacademy.attendee"
    
    # _rec_name redefine el campo para llegar a ver el registro en otro objeto
    # En este caso, se imprimirá el nombre del partner como nombre del asistente
    
    _rec_name = 'partner_id'
    
    _columns = {         
                'partner_id': fields.many2one('res.partner', string="Partner"),
                'session_id': fields.many2one('openacademy.session', string="Session", required=True, ondelete='cascade'),               
                }
