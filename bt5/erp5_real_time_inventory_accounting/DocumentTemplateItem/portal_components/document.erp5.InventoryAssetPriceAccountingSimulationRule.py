# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2017 Nexedi SA and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street - Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################

from erp5.component.document.InvoiceTransactionSimulationRule import (InvoiceTransactionSimulationRule,
                                                                     InvoiceTransactionRuleMovementGenerator)

class InventoryAssetPriceAccountingRuleMovementGenerator(InvoiceTransactionRuleMovementGenerator):
  """
  """
  # CMF Type Definition
  meta_type = 'ERP5 Inventory Asset Price Accounting Simulation Rule'
  portal_type = 'Inventory Asset Price Accounting Simulation Rule'

  # XXX: Copy/paste from Products.ERP5.mixin.rule to support Transit use case
  def getGeneratedMovementList(self, movement_list=None, rounding=False):
    """
    Returns a list of movements generated by that rule.

    movement_list - optional IMovementList which can be passed explicitely

    rounding - boolean argument, which controls if rounding shall be applied on
               generated movements or not

    NOTE:
      - implement rounding appropriately (True or False seems
        simplistic)
    """
    # Default implementation below can be overriden by subclasses
    # however it should be generic enough not to be overriden
    # by most classes
    # Results will be appended to result
    result = []
    # Build a list of movement and business path
    input_movement_list = self._getInputMovementList(
                            movement_list=movement_list, rounding=rounding)
    for input_movement in input_movement_list:
      # Merge movement and business path properties (core implementation)
      # Lookup Business Process through composition (NOT UNION)
      business_process = input_movement.asComposedDocument()
      explanation = self._applied_rule # We use applied rule as local explanation
      trade_phase = self._getTradePhaseList(input_movement, business_process) # XXX-JPS not convenient to handle
      update_property_dict = self._getUpdatePropertyDict(input_movement)

      for movement in business_process.getTradePhaseMovementList(explanation, input_movement,
                                                                 trade_phase=trade_phase, delay_mode=None,
                                                                 update_property_dict=update_property_dict):
        # PATCH-BEGIN
        update_dict = {}
        if movement.getLedger() in ('stock/stock/entree',
                                    'stock/preparation/entree',
                                    'stock/transit/sortie',
                                    'stock/customs/entree'):
          update_dict['start_date'] = update_dict['stop_date'] = input_movement.getStopDate()
        elif movement.getLedger() in ('stock/stock/sortie',
                                      'stock/preparation/sortie',
                                      'stock/transit/entree'):
          update_dict['start_date'] = update_dict['stop_date'] = input_movement.getStartDate()
        movement._edit(**update_dict)

        input_movement.log("%r (input_movement=%r): ledger=%r, start_date=%r, stop_date=%r" %
                           (movement,
                            input_movement,
                            movement.getLedger(),
                            movement.getStartDate(),
                            movement.getStopDate()))
        # PATCH-END
        result.append(movement)

    # And return list of generated movements
    return result

  def _getInputMovementList(self, movement_list=None, rounding=False):
    simulation_movement = self._applied_rule.getParentValue()

    # No expand if price is not set (already checked in 'Test Method ID' on the Rule).
    # Price is automatically acquired from Supply if not set directly on PL Movement.
    quantity = simulation_movement.getPrice()
    if quantity is None:
      return []

    return [simulation_movement.asContext(quantity=quantity)]

  def _getUpdatePropertyDict(self, input_movement):
    update_property_dict = InvoiceTransactionRuleMovementGenerator._getUpdatePropertyDict(
      self,
      input_movement)

    if input_movement.getRootAppliedRule().getCausalityValue().getPortalType().startswith('Purchase'):
      update_property_dict['source_section'] = input_movement.getDestinationSection()

    return update_property_dict

class InventoryAssetPriceAccountingSimulationRule(InvoiceTransactionSimulationRule):
  def _getMovementGenerator(self, context):
    return InventoryAssetPriceAccountingRuleMovementGenerator(
      applied_rule=context, rule=self)
