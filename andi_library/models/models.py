# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class andi_library(models.Model):
#     _name = 'andi_library.andi_library'
#     _description = 'andi_library.andi_library'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

