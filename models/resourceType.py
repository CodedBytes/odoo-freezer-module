# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

# Resource type Model
class FomResourceType(models.Model):
    _name='fom.resourcetype'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Resource Type Management Interface"

    # Name field
    name = fields.Char(string='Resource Code', required=True, copy=False, readonly=True, default=lambda self: _('New Resource Type'))

    # Generate unique identifier.
    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New Resource Type'):
            sequence = self.env['ir.sequence'].next_by_code('fom.resourcetype') or _('New Resource Type')
            vals['name'] = sequence
        res = super(FomResourceType, self).create(vals)
        return res
    
    # Code Field
    resource_type_name = fields.Char(string='Resorce Type Name', required=True)

    # Parent Category field
    resource_type_parent_category = fields.Many2one('fom.resourcetype', string="Parent Category", required=False)

    # Status field
    active = fields.Boolean(string='Active', default=True, tracking=True)

    # Note
    remark = fields.Char(string="Remark")

    # Created time field
    created_time = fields.Datetime(string='Created Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)

    # Parent Category Custom Name.
    def name_get(self):
        result = []
        for rec in self:
            value = '[' + rec.name + '] ' + rec.resource_type_name
            result.append((rec.id, value))
        return result