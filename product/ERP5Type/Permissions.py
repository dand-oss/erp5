##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
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
ERP5Permissions holds ERP5 permissions in a central place in order
to ease the understanding of the ERP5 permission structure. Most
permissions are defined in Zope or in the CMF. Some permissions are specific
to ERP5, in particular content creation permisions (ex. Add Organisation, etc.)

A complete explanation of the Zope security architecture is available here:
http://dev.zope.org/Wikis/DevSite/Projects/DeclarativeSecurity/ZopeSecurityForDevelopers
"""

from Products.CMFCore.CMFCorePermissions import setDefaultRoles
from Products.CMFCore import CMFCorePermissions

# Default Zope Permissions
View = CMFCorePermissions.View
AccessContentsInformation = CMFCorePermissions.AccessContentsInformation
UndoChanges = CMFCorePermissions.UndoChanges
ChangePermissions = CMFCorePermissions.ChangePermissions
ViewManagementScreens = CMFCorePermissions.ViewManagementScreens
ManageProperties = CMFCorePermissions.ManageProperties
FTPAccess = CMFCorePermissions.FTPAccess

# Default CMF Core Permissions
ListFolderContents = CMFCorePermissions.ListFolderContents
ListUndoableChanges = CMFCorePermissions.ListUndoableChanges
AccessInactivePortalContent = CMFCorePermissions.AccessInactivePortalContent
ModifyCookieCrumblers = CMFCorePermissions.ModifyCookieCrumblers
ReplyToItem = CMFCorePermissions.ReplyToItem
ManagePortal = CMFCorePermissions.ManagePortal
ModifyPortalContent = CMFCorePermissions.ModifyPortalContent
#ManageProperties = CMFCorePermissions.ManageProperties
ListPortalMembers = CMFCorePermissions.ListPortalMembers
AddPortalFolders = CMFCorePermissions.AddPortalFolders
AddPortalContent = CMFCorePermissions.AddPortalContent
SetOwnPassword = CMFCorePermissions.SetOwnPassword
AddPortalMember = CMFCorePermissions.AddPortalMember
SetOwnProperties = CMFCorePermissions.SetOwnProperties

# Default CMF Workflow Permissions
RequestReview = CMFCorePermissions.RequestReview
ReviewPortalContent = CMFCorePermissions.ReviewPortalContent
AccessFuturePortalContent = CMFCorePermissions.AccessFuturePortalContent

# ERP5 addition: delete content. It is still unclear
# if this permission makes any sense since we may
# use instead workflows and publication dates. Also,
# this permission does not fit into the DC workflow framework
# since it applies to the content itself rather than to the
# container
DeletePortalContent = CMFCorePermissions.ModifyPortalContent

# ERP5 addition: default content translation permissions
# this comes from Base18
TranslateContent = 'Translate Content'
setDefaultRoles(TranslateContent, ('Manager', 'Owner', 'Member'))

# ERP5 additions: we define some content creations
# securities here. Each ERP5 Document will
# point to one of these securities through the
# add_permission attribute
#
# we define here the "setDefaultRoles" although
# it does not apply to most roles since roles are defines
# on a ERP5 per ERP5 user basis. Most ERP5 users will
# subclass ERP5 basic types and define their own roles
#
# Our default permissions are very restrictive ; only
# managers can add content
#
# most content permissions in ERP5 are managed through
# workflow, on a type per type basis. Content permissions should
# be defined at the level of the XMLObject (ie. a the level of a
# synchronizable piece of content). This means for example
# that subcontent of an Organisation object (ex. Telephone)
# can be modified if the Organisation itself can be modified.
#
# Whenever we need different permissions on content and subcontent,
# we should consider a new workflow since this means that the
# organisation process for the 2 types of documents is not the same.
# This is consistent with the ERP5 principle that content consistency
# verification (ie. checking that a content is complete / consistent)
# is implemented through standard DC workflow rather through some ad hoc
# content input system as it exists in other ERPs.
#
# To summarize, the steps in a wizzard are less powerful than steps
# in a DC workflow. So, let us keep it simple and use only one tool:
# DC workflow.
#
# Now, how do we decide which permissions ? Our principle is simple
#
# - make it simple : if users need finer permissions, they can subclass
#
# - what matters now is to make a difference between content stored in My Stuff
#   and content stored in one of ERP5 modules (this benefitting from
#   permissions definition at the module level)
#
# If we need to change this some day, the best approaches consists in
#
# - using the 5 classes (ie. Resource, Movement, etc.) as 5 permissions
#
# - using modules as permissions (ie. Trade, Engineering, Accounting, etc.)
#
# - using technical types / interfaces (ie. Entity, Coordinate, Predicate, etc.)

#AddERP5Content = 'Add ERP5 content'
#setDefaultRoles(AddERP5Content, ('Manager', ))
AddERP5Content = AddPortalContent # Since we put come CPS content in ERP5 documents, there is no rationale in having 2 permissions

# Source Code Management - this is the highest possible permission
ManageExtensions = "Manage extensions"

