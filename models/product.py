from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class product_template_with_cost_price_auto(models.Model):
    _inherit = ['product.template']

    cost_price_from_suppliers = fields.Boolean('Auto cost from suppliers', default=True)
    standard_price = fields.Float('Cost Price', compute='_compute_lowest_supplier_price')
    manual_cost_price = fields.Float('Manual cost price', default=0)

    @api.multi
    @api.onchange('cost_price_from_suppliers')
    def set_cost_method_on_childs(self):
        _logger.debug("Price computation changed (supplier = %s)", self.cost_price_from_suppliers)
        # Set the flag on the child products
        for variant in self.product_variant_ids:
            variant.cost_price_from_suppliers = self.cost_price_from_suppliers

    @api.one
    @api.depends('cost_price_from_suppliers')
    def _compute_lowest_supplier_price(self):
        if self.cost_price_from_suppliers == True:
            # Get the lowest price for suppliers
            min_price = 0
            for supp in self.seller_ids:
                if (min_price == 0 and supp.price > 0) or (supp.state == 'sellable' and supp.price < min_price):
                    min_price = supp.price

            self.standard_price = min_price
            _logger.debug("Price computed regarded supplier (%s)", self.standard_price)
        else:
            self.standard_price = self.manual_cost_price
            _logger.debug("Price computed manually (%s)", self.standard_price)

class product_product_with_cost_price_auto(models.Model):
    _inherit = ['product.product']

    cost_price_from_suppliers = fields.Boolean('Auto cost from suppliers', default=True)
    standard_price = fields.Float('Cost Price', compute='_compute_lowest_supplier_price')
    manual_cost_price = fields.Float('Manual cost price', default=0)

    @api.multi
    @api.onchange('cost_price_from_suppliers')
    def set_cost_method_on_parent(self):
        _logger.debug("Price computation changed (supplier = %s)", self.cost_price_from_suppliers)
        # Set the flag on the parent product
        self.product_tmpl_id.cost_price_from_suppliers = self.cost_price_from_suppliers

    @api.one
    @api.depends('cost_price_from_suppliers')
    def _compute_lowest_supplier_price(self):
        if self.cost_price_from_suppliers == True:
            
            # Get the lowest price for suppliers
            min_price = 0
            for supp in self.seller_ids:
                if (min_price == 0 and supp.price > 0) or (supp.state == 'sellable' and supp.price < min_price):
                    min_price = supp.price

            self.standard_price = min_price
            _logger.debug("Price computed regarde supplier (%s)", self.standard_price)
        else:
            self.standard_price = self.manual_cost_price
            _logger.debug("Price computed manually (%s)", self.standard_price)
