# http://pythonhosted.org/plone.app.discussion/howtos/howto_extend_the_comment_form.html
# Customized to add "title" rather than "website"

from persistent import Persistent

from z3c.form.field import Fields

from zope import interface
from zope import schema

from zope.annotation import factory
from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from plone.z3cform.fieldsets import extensible

from plone.app.discussion.browser.comments import CommentForm
from plone.app.discussion.comment import Comment


# Interface to define the fields we want to add to the comment form.
class ICommentExtenderFields(Interface):
    title = schema.TextLine(title=u"Title", required=False)


# Persistent class that implements the ICommentExtenderFields interface
@interface.implementer(ICommentExtenderFields)
class CommentExtenderFields(Persistent):
    adapts(Comment)
    title = u""

# CommentExtenderFields factory
CommentExtenderFactory = factory(CommentExtenderFields)


# Extending the comment form with the fields defined in the
# ICommentExtenderFields interface.
class CommentExtender(extensible.FormExtender):
    adapts(Interface, IDefaultBrowserLayer, CommentForm)

    fields = Fields(ICommentExtenderFields)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        # Add the fields defined in ICommentExtenderFields to the form.
        self.add(ICommentExtenderFields, prefix="")
        # Move the title field to the top of the comment form.
        self.move('title', before='text', prefix="")
