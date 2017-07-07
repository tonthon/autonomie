# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Action objects
"""
from autonomie.exception import Forbidden


class Action(object):
    """
        a state object with a name, permission and a callback callbacktion
        :param name: The state name
        :param permission: The permission needed to set this state
        :param callback: A callback function to call on state process
        :param status_attr: The attribute storing the model's status
        :param userid_attr: The attribute storing the status person's id
    """
    def __init__(
        self,
        name,
        permission,
        callback=None,
        status_attr=None,
        userid_attr=None,
        **kwargs
    ):
        self.name = name
        if not hasattr(permission, "__iter__"):
            permission = [permission]
        self.permissions = permission
        self.callback = callback
        self.status_attr = status_attr
        self.userid_attr = userid_attr
        self.options = kwargs

    def allowed(self, context, request):
        """
        return True if this state assignement on context is allowed
        in the current request

        :param obj context: An object with acl
        :param obj request: The Pyramid request object
        :returns: True/False
        :rtype: bool
        """
        res = False
        for permission in self.permissions:
            if request.has_permission(permission, context):
                res = True
                break

        return res

    def __json__(self, request):
        result = dict(status=self.name)
        result.update(self.options)
        return result

    def process(self, model, request, user_id, **kw):
        """
        Process the action

        Set the model's status_attr if needed (status)
        Set the model's status user_id attribute if needed (status_person_id)

        Fire a callback if needed
        """
        if self.status_attr is not None:
            setattr(model, self.status_attr, self.name)
        if self.userid_attr:
            setattr(model, self.userid_attr, user_id)
        if self.callback:
            return self.callback(request, model, user_id=user_id, **kw)
        else:
            return model

    def __repr__(self):
        return (
            "< State %s allowed for %s (status_attr : %s, "
            "userid_attr : %s )>" % (
                self.name, self.permissions, self.status_attr, self.userid_attr
            )
        )


class ActionManager(object):
    def __init__(self):
        self.items = []

    def add(self, action):
        self.items.append(action)

    def get_allowed_actions(self, request, context=None):
        """
        Return the list of next available actions regarding the current user
        perm's

        """
        result = []
        context = context or request.context

        for action in self.items:
            if action.allowed(context, request):
                result.append(action)
        return result

    def process(self, action_name, context, request, **params):
        """
        Process a specific action

        :param str action_name: The name of the action
        :param obj context: The context to manage
        :param obj request: The current request object
        :param dict params: The params to pass to the callback
        """
        action = None
        for action in self.items:
            if action.name == action_name:
                break
        if action is None:
            raise Exception(u"Unknown action : %s" % action_name)

        elif not action.allowed(context, request):
            raise Forbidden(
                u"This action is not allowed for %s : %s" (
                    request.user_id,
                    action_name,
                )
            )
        return action.process(context, request, request.user_id, **params)


def get_status_actions(data_type):
    """
    Return a state machine handling the basic states

    :param str data_type: estimation/invoice/cancelinvoice

    :returns: A state machine that can be used to perform state changes
    :rtype: class:`autonomie.models.statemachine.StateMachine`
    """
    manager = ActionManager()
    for status, icon, label, title, css in (
        (
            'draft', '', u'Enregistrer en brouillon',
            'Enregistrer ce document comme brouillon', 'btn btn-default'
        ),
        (
            'wait', 'time', u"Demander la validation",
            u"Enregistrer ce document et en demander la validation",
            "btn btn-success btn-primary-action",
        ),
        (
            'invalid', 'trash', u"Invalider",
            u"Invalider ce document", "btn btn-danger",
        ),
        (
            'valid', "ok-sign", u"Valider",
            u"Valider ce document", "btn btn-success btn-primary-action",
        )
    ):
        manager.add(
            Action(
                status,
                '%s.%s' % (status, data_type),
                status_attr='status',
                userid_attr='status_person_id',
                icon=icon,
                label=label,
                title=title,
                css=css,
            )
        )
    return manager


DEFAULT_ACTION_MANAGER = {
    'estimation': get_status_actions('estimation'),
    'invoice': get_status_actions('invoice'),
    'cancelinvoice': get_status_actions('cancelinvoice'),
}