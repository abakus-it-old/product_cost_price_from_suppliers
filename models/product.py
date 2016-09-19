from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class product_template_with_cost_price_auto(models.Model):
    _inherit = ['product.template']

    cost_price_from_suppliers = fields.Boolean('Auto cost from suppliers', default=True)
    standard_price = fields.Float('Cost Price', compute='_compute_lowest_supplier_price')
    manual_cost_price = fields.Float('Manual cost price', default=0)

    @api.one
    @api.depends('cost_price_from_suppliers', 'seller_ids', 'manual_cost_price')
    def _compute_lowest_supplier_price(self):

        if self.cost_price_from_suppliers == True:
            # Get the lowest price for suppliers
            min_price = 0
            for supp in self.seller_ids:
                if (min_price == 0 and supp.price > 0) or (supp.state == 'sellable' and supp.price < min_price):
                    min_price = supp.price

            self.standard_price = min_price
            _logger.debug("PT : Price computed regarded supplier (%s)", self.standard_price)
        else:
            self.standard_price = self.manual_cost_price
            _logger.debug("PT : Price computed manually (%s)", self.standard_price)

        # Set the flag on the child products
        for variant in self.product_variant_ids:
            variant.write({'cost_price_from_suppliers': self.cost_price_from_suppliers, 'manual_cost_price': self.manual_cost_price, 'standard_price': self.standard_price})
#            variant.cost_price_from_suppliers = self.cost_price_from_suppliers
#            variant.manual_cost_price = self.manual_cost_price
            _logger.debug("\n\nPT : Variant (%s) computation: %s (price=%s)", variant, variant.cost_price_from_suppliers, variant.manual_cost_price)

class product_product_with_cost_price_auto(models.Model):
    _inherit = ['product.product']

    cost_price_from_suppliers = fields.Boolean('Auto cost from suppliers', default=True)
    #standard_price = fields.Float('Cost Price', compute='_compute_lowest_supplier_price')
    manual_cost_price = fields.Float('Manual cost price', default=0)

    @api.multi
    def open_product_template(self):
        if self.product_tmpl_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'product.product_template_only_form_view',
                'res_model': 'product.template',
                'res_id': self.product_tmpl_id.id ,
                'view_type': 'form',
                'view_mode': 'form',
                }

    """

    @api.depends('cost_price_from_suppliers', 'seller_ids', 'manual_cost_price')
    @api.onchange('cost_price_from_suppliers', 'seller_ids', 'manual_cost_price')
    def _compute_lowest_supplier_price(self):
        if self.cost_price_from_suppliers == True:            
            # Get the lowest price for suppliers
            min_price = 0
            for supp in self.seller_ids:
                if (min_price == 0 and supp.price > 0) or (supp.state == 'sellable' and supp.price < min_price):
                    min_price = supp.price

            self.standard_price = min_price
            _logger.debug("PP : Price computed regarded supplier (%s)", self.standard_price)
        else:
            self.standard_price = self.manual_cost_price
            _logger.debug("PP : Price computed manually (%s)", self.standard_price)

        # Set settings on the parent product
        self.product_tmpl_id.manual_cost_price =  self.manual_cost_price
        self.product_tmpl_id.cost_price_from_suppliers = self.cost_price_from_suppliers
        self.product_tmpl_id.standard_price = self.standard_price
        _logger.debug("\n\nPP : Price computation set on PT")
"""        
