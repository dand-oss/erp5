##############################################################################
#
# Copyright (c) 2010 Nexedi SARL and Contributors. All Rights Reserved.
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################

from AccessControl import ClassSecurityInfo
from Products.ERP5Type import Permissions, PropertySheet

from Products.ERP5.mixin.rule import RuleMixin
from Products.ERP5.mixin.movement_collection_updater import MovementCollectionUpdaterMixin
class AccountingTransactionRootSimulationRule(RuleMixin, MovementCollectionUpdaterMixin):
  """
  Accounting Transaction Root Simulation Rule is a root level rule for
  Accounting Transaction.
  """
  # CMF Type Definition
  meta_type = 'ERP5 Accounting Transaction Root Simulation Rule'
  portal_type = 'Accounting Transaction Root Simulation Rule'

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  def _getMovementGenerator(self, context):
    """
    Return the movement generator to use in the expand process
    """
    return AccountingTransactionRuleMovementGenerator(applied_rule=context,
                                                      rule=self)

  ## XXX: From here on, copy/paste from DeliveryRootSimulationRule to avoid a
  ##      dependency on erp5_trade. Is this Rule really actually used/useful?
  #
  # Default Properties
  property_sheets = (
    PropertySheet.Base,
    PropertySheet.XMLObject,
    PropertySheet.CategoryCore,
    PropertySheet.DublinCore,
    PropertySheet.Task,
    PropertySheet.Predicate,
    PropertySheet.Reference,
    PropertySheet.Version,
    PropertySheet.Rule
    )
  def _isProfitAndLossMovement(self, movement):
    # For a kind of trade rule, a profit and loss movement lacks source
    # or destination.
    return (movement.getSource() is None or movement.getDestination() is None)

from Products.ERP5.mixin.movement_generator import MovementGeneratorMixin
class AccountingTransactionRuleMovementGenerator(MovementGeneratorMixin):

  def _getPortalDeliveryMovementTypeList(self):
    return self._rule.getPortalObject().getPortalAccountingMovementTypeList()

  def _getInputMovementList(self, movement_list=None, rounding=None):
    """
    Input movement list comes from delivery

    XXX: Copy/paste from DeliveryRootSimulationRule to avoid a dependency on
         erp5_trade. Is this Rule really actually used/useful?
    """
    delivery = self._applied_rule.getDefaultCausalityValue()
    if delivery is None:
      return []
    else:
      result = []
      movement_kw = {}
      movement_type_list = self._getPortalDeliveryMovementTypeList()
      if movement_type_list:
        movement_kw["portal_type"] = movement_type_list
      for movement in delivery.getMovementList(**movement_kw):
        simulation_movement_list = movement.getDeliveryRelatedValueList()
        if not simulation_movement_list or self._applied_rule in (
            simulation_movement.getParentValue()
            for simulation_movement in simulation_movement_list):
          result.append(movement)
      return result
