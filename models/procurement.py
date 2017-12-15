# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, api
import logging
_logger = logging.getLogger(__name__)


class ProcurementOrder(models.Model):
    _name = "procurement.order"
    _inherit = 'procurement.order'

    @api.multi
    def _get_matching_bom(self):
        """ Finds the bill of material for the product from procurement order. """
        bom = False
        if self.move_dest_id:
            procurements = self.search([
                                    ('move_ids', 'in', [self.move_dest_id.id])])
            if procurements:
                line = procurements[0].sale_line_id
                if line:
                    bom = line.bom_id
        if self.bom_id:
            return self.bom_id
        elif bom:
            return bom
        else:
            return self.env['mrp.bom'].with_context(
                company_id=self.company_id.id, force_company=self.company_id.id
            )._bom_find(product=self.product_id,
                picking_type=self.rule_id.picking_type_id)

