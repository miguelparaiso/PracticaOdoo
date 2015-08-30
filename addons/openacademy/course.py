
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
from datetime import datetime, timedelta

class course(osv.Model):
    _name = "openacademy.course"
    
    # Esta función me permite duplicar un curso
    
    def copy(self, cr, uid, id, default, context=None):
        course = self.browse(cr, uid, id, context=context)
        new_name = "Copy of %s" % course.name
        # =like es el operador LIKE original de SQL
        others_count = self.search(cr, uid, [('name','=like', new_name+'%')],count=True, context=context)
        
        if others_count > 0:
            new_name = "%s (%s)" % (new_name, others_count+1)
        default['name'] = new_name
        return super(Course, self).copy(cr, uid, id , default, context=context)
    
    
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
    
    def onchange_taken_seats(self, cr, uid, ids, seats, attendee_ids):
        attendee_records = self.resolve_o2m_commands_to_record_dicts(cr, uid, 'attendee_ids', attendee_ids, ['id'])
        res = {
               'value' : {'taken_seats_percent' : self._get_taken_seats_percent(seats, attendee_records)}
               }
        if seats < 0:
            res['warning'] = {
                'title' : "Warning: problems",
                'message': "You cannot have negative number of seats",
                              }
        elif seats < len(attendee_ids):
            res['warning'] = {
                'title' : "Warning: problems",
                'message': "You need more seats for this session " ,                 
                              }
        return res
        
    def _check_instructor_not_in_attendees(self, cr, uid, ids, context=None):
        for session in self.browse(cr, uid, ids, context):
            partners = [att.partner_id for att in session.attendee_ids]
            if session.instructor_id and session.instructor_id in partners:
                 return False
        return True
    
    def _determin_end_date(self, cr, uid, ids, field, arg, context=None):
        result = {}
        for session in self.browse(cr, uid, ids, context=context):
            if session.start_date and session.duration:
                # Get a datetime object from session.start_date
                start_date = datetime.strptime(session.start_date, "%Y-%m-%d")
                # Get a timedelta object from session.duration
                duration = timedelta(days=(session.duration - 1))
                # Calculate the end time
                end_date = start_date + duration
                # Render in format YYYY-MM-DD
                result[session.id] = end_date.strftime("%Y-%m-%d")
            else:
                # TIP: In case session.start_date exists but session.duration not end_date will be equal to start_date 
                result[session.id] = session.start_date
        return result
    
    # Beware that fnct_inv take a unique id and not a list of id
    
    def _set_end_date(self, cr, uid, id, field, value, arg, context=None):
        session = self.browse(cr, uid, id, context=context)
        if session.start_date and value:
            start_date = datetime.strptime(session.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(value[:10], "%Y-%m-%d")
            duration = end_date - start_date
            self.write(cr, uid, id, {'duration': (duration.days + 1)}, context=context)
            
    
    """ Creamos funciones para la vista Gantt """
    
    def _determin_hours_from_duration(self, cr, uid, ids, field, arg, context=None):
        
        result = {}
        sessions = self.browse(cr, uid, ids, context=context)
        for session in sessions:
            result[session.id] = (session.duration * 24 if session.duration else 0)  
        return result      
    
    def _set_hours(self, cr, uid, id, field, value, arg, context=None):
        if value:
            self.write(cr, uid, id, {'duration' : (value / 24)}, context=context )
            
    
          
    """ Creamos función para el cálculo de número de asistentes en la vista Gráfico"""
    
    def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
        res={}
        for session in self.browse(cr, uid, ids, context=context):
            res[session.id] = len(session.attendee_ids)
        return res
        
        
    _columns = {
                'name': fields.char(string="Name", size=256, required=True),
                'start_date': fields.date(string="Start date"),
                'duration': fields.float(string="Duration", digits=(6,2), help="Duration in days"),
                'seats': fields.integer(string="Number of seats"), 
                'color' : fields.integer('Color'),
                # Campo state para el workflow (flujo de trabajo)
                'state' : fields.selection([('draft','Draft'),('confirmed','Confirmed'),('done','Done')], string="State"),
                # Campos relacionales
                # 'cascade' destruye la sesión en caso de que course_id sea eliminado
                'instructor_id': fields.many2one('res.partner', string="Instructor"),
                # Ejercicio 3 domains 
               # 'instructor_id': fields.many2one('res.partner', string="Instructor", domain=[('instructor','=',True),('category_id.name','ilike','Teacher')],                
                'course_id': fields.many2one('openacademy.course', ondelete='cascade', string="Course", required=True),
                'attendee_ids': fields.one2many('openacademy.attendee','session_id', string="Attendees"), 
                'taken_seats_percent': fields.function(_taken_seats_percent, type='float', string='Taken seats'),
                'end_date' : fields.function(_determin_end_date, fnct_inv=_set_end_date, type='date', string="End Date" ),
                'hours' : fields.function(_determin_hours_from_duration, fnct_inv=_set_hours, type='float', string="Hours"),
                # Habilitamos el store = True que lo que hace es que se guarde el dato
                'attendee_count' : fields.function(_get_attendee_count, type='integer', string='Attendee Count', store=True),    
                }
    
    _constraints = [
        (_check_instructor_not_in_attendees,
         "The instructor can not be also an attendee!",
         ['instructor_id','attendee_ids']),
                    ]
    
    _defaults = {
                 'state' : 'draft',
                 }
    
    def action_draft(self, cr, uid, ids, context=None):
        # Cambia a estado borrador
        return self.write(cr, uid, ids, {'state' : 'draft'}, context=context)
    
    def action_confirm(self, cr, uid, ids, context=None):
        # Cambia a estado confirmado
        return self.write(cr, uid, ids, {'state' : 'confirmed'}, context=context)
    
    def action_done(self, cr, uid, ids, context=None):
        # Cambia el estado a realizado
        return self.write(cr, uid, ids, {'state' : 'done'}, context=context)
    
    

class Attendee(osv.Model):
    _name = "openacademy.attendee"
    
    # _rec_name redefine el campo para llegar a ver el registro en otro objeto
    # En este caso, se imprimirá el nombre del partner como nombre del asistente
    
    _rec_name = 'partner_id'
    
    _columns = {         
                'partner_id': fields.many2one('res.partner', string="Partner"),
                'session_id': fields.many2one('openacademy.session', string="Session", required=True, ondelete='cascade'),               
                }
