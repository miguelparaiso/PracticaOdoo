
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

{
    "name": "Open Academy",
    "version": "1.0",
    "depends": ["base"],
    "author": "Juani",
    "category": "Test",
    "description": """
    Modulo Open Academy para gestionar cursos
    - cursos
    - sesiones
    - registro de asistentes
    """,
    'data': [
             'views/openacademy_view.xml',
             'views/partner.xml',
             #'security/groups.xml',
             #'security/ir.model.access.csv',
             'wizard/create_attendee_view.xml',
             ],
    'demo': [
             # Archivos que contienen datos demo
             ],
    'test': [
             # Archivos que contienen tests
             ],
    'installable': True,
    'auto_install': False,
#    'certificate': 'certificate',
}