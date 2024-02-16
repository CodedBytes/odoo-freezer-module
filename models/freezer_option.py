# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class FomProducts(models.Model):
    _inherit = ['product.template']
    freezer_option = fields.Char(string='NewNameDisplayName', ondelete={'freezer': 'cascade'})

class FomSaleTreeView(models.Model):
    _inherit = ['sale.order.line']

    # inherit variables
    product_code = fields.Char(string='Product Code', ondelete={'code': 'cascade'})
    code_id = fields.Char(string='Cod. C4')
    order = fields.Many2one('sale.order', string='Ordem')

    # Automatically getting field information o tree from
    @api.onchange('product_id')
    def set_code(self):
        self.product_code = self.product_id.codigo
        self.code_id = self.product_id.comp_id
        

class FomSaleFormAndTreeView(models.Model):
    _inherit = ['sale.order']

    # inherit variables
    rz_social = fields.Char(string='Razão social', ondelete={'razao': 'cascade'})

    partner = fields.Many2one('res.partner', string='Parceiro')
    cnpj = fields.Char(string='CNPJ', compute="_get_cnpj")
    #social = fields.Char(string='reference', related='res.partner.legal_name')

    # Automatically getting field information 
    @api.onchange('partner_id')
    def set_code(self):
        self.rz_social = self.partner_id.legal_name

    @api.depends('partner_id')
    def _get_cnpj(self):
        for record in self:
            record.cnpj = record.partner_id.cnpj_cpf

class FomProductFormulary(models.Model):
    _inherit = ['product.template']

    # inherit variables
    codigo = fields.Char(string='Codigo Refrio', compute='_compute_codigo', inverse='_set_codigo')
    comp_id = fields.Char(string='Codigo CompuFour', compute='_compute_comp', inverse='_set_comp')

    def _set_codigo(self):
        variant_count = len(self.product_variant_ids)
        if variant_count == 1:
            self.product_variant_ids.codigo = self.codigo
        elif variant_count == 0:
            archived_variants = self.with_context(active_test=False).product_variant_ids
            if len(archived_variants) == 1:
                archived_variants.codigo = self.codigo


    @api.depends('product_variant_ids.codigo')
    def _compute_codigo(self):
        self.codigo = False
        for template in self:
            # TODO master: update product_variant_count depends and use it instead
            variant_count = len(template.product_variant_ids)
            if variant_count == 1:
                template.codigo = template.product_variant_ids.codigo
            elif variant_count == 0:
                archived_variants = template.with_context(active_test=False).product_variant_ids
                if len(archived_variants) == 1:
                    template.codigo = archived_variants.codigo


    def _set_comp(self):
        variant_count = len(self.product_variant_ids)
        if variant_count == 1:
            self.product_variant_ids.comp_id = self.comp_id
        elif variant_count == 0:
            archived_variants = self.with_context(active_test=False).product_variant_ids
            if len(archived_variants) == 1:
                archived_variants.comp_id = self.comp_id


    @api.depends('product_variant_ids.comp_id')
    def _compute_comp(self):
        self.comp_id = False
        for template in self:
            # TODO master: update product_variant_count depends and use it instead
            variant_count = len(template.product_variant_ids)
            if variant_count == 1:
                template.comp_id = template.product_variant_ids.comp_id
            elif variant_count == 0:
                archived_variants = template.with_context(active_test=False).product_variant_ids
                if len(archived_variants) == 1:
                    template.comp_id = archived_variants.comp_id
  


class FomProductAddField(models.Model):
    _inherit = ['product.product']

    # inherit variables
    codigo = fields.Char(string='Codigo Refrio')
    comp_id = fields.Char(string='Codigo CompuFour')
