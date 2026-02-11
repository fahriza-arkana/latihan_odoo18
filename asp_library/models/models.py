# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class asp_library(models.Model):
#     _name = 'asp_library.asp_library'
#     _description = 'asp_library.asp_library'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

