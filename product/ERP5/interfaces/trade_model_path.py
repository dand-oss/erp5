# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009 Nexedi SA and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
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
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
"""
Products.ERP5.interfaces.trade_model_path
"""

from zope.interface import Interface

class ITradeModelPath(Interface):
  """Trade Model Path interface specification

  ITradeModelPath provides a method to calculate the completion
  date of existing movements based on business path properties.
  It also provides methods to determine whether all related simulation
  movements related to a given explanation are completed, partially
  completed or frozen. Finally, it provides a method to invoke
  delivery builders for all movements related to a given explanation.
  """

  def getExpectedQuantity(amount):
    """Returns the new quantity for the provided amount taking
    into account the efficiency or the quantity defined on the business path.
    This is used to implement payment conditions or splitting production
    over multiple path. The total of getExpectedQuantity for all business
    path which are applicable should never exceed the original quantity.
    The implementation of this validation is left to rules.
    """
