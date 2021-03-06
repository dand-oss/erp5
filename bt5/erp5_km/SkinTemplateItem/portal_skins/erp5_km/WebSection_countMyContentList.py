"""
  This scripts counts the documents belonging to a given Person.
  If it is called on a Person object, it counts the documents
  which belong to that person. If it is called on another type
  of object, it counts the document which belong to the current
  user.
"""
if context.getPortalType() == 'Person':
  # If context is a person, get the user
  user = context.Person_getUserId()
  if user is None:
    # no way to determine documents if we have no reference
    return [[0]]
  return context.ContributionTool_countMyContentList(user=user, **kw)
else:
  return context.ContributionTool_countMyContentList(**kw)
