# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
"""
Main deferreds functions used in autonomie
"""
import colander
import calendar
import datetime
from deform import widget
from deform_bootstrap.widget import ChosenSingleWidget

from autonomie.models import user
from autonomie.models import company
from autonomie.models.task.invoice import get_invoice_years
from autonomie.views import render_api

from autonomie.views.forms import widgets as custom_widgets


MAIL_ERROR_MESSAGE = u"Veuillez entrer une adresse e-mail valide"


def get_users_options(roles=None):
    """
    Return the list of active users from the database formatted as choices:
        [(user_id, user_label)...]

    :param role: roles of the users we want
        default:  all
        values : ('contractor', 'manager', 'admin'))
    """
    if roles and not hasattr(roles, "__iter__"):
        roles = [roles]
    if roles:
        query = user.get_user_by_roles(roles)
    else:
        query = user.User.query()
    return [(unicode(u.id), render_api.format_account(u)) for u in query]


def get_deferred_user_choice(roles=None, widget_options=None):
    """
        Return a colander deferred for users selection options
    """
    widget_options = widget_options or {}
    default_option = widget_options.pop("default_option", None)
    @colander.deferred
    def user_select(node, kw):
        """
            Return a user select widget
        """
        choices = get_users_options(roles)
        if default_option:
            choices.insert(0, default_option)
        return ChosenSingleWidget(
            values=choices,
            **widget_options
            )
    return user_select


@colander.deferred
def deferred_autocomplete_widget(node, kw):
    """
        Dynamically assign a autocomplete single select widget
    """
    choices = kw.get('choices')
    if choices:
        wid = ChosenSingleWidget(values=choices)
    else:
        wid = widget.TextInputWidget()
    return wid


@colander.deferred
def deferred_today(node, kw):
    """
        return a deferred value for "today"
    """
    return datetime.date.today()


@colander.deferred
def deferred_now(node, kw):
    """
    Return a deferred datetime value for now
    """
    return datetime.datetime.now()


@colander.deferred
def deferred_current_user_id(node, kw):
    """
        Return a deferred for the current user
    """
    return kw['request'].user.id


def get_date_input(**kw):
    """
    Return a date input displaying a french user friendly format
    """
    date_input = custom_widgets.CustomDateInputWidget(**kw)
    return date_input


def get_datetime_input(**kw):
    """
    Return a datetime input displaying a french user friendly format
    """
    datetime_input = custom_widgets.CustomDateTimeInputWidget(**kw)
    return datetime_input


def user_node(roles=None, **kw):
    """
    Return a schema node for user selection
    roles: allow to restrict the selection to the given roles
        (to select between admin, contractor and manager)
    """
    widget_options = kw.pop('widget_options', {})
    return colander.SchemaNode(
            colander.Integer(),
            widget=get_deferred_user_choice(roles, widget_options),
            **kw
            )


def get_deferred_company_choices(widget_options):
    default_entry = widget_options.pop('default', None)
    @colander.deferred
    def deferred_company_choices(node, kw):
        """
        return a deferred company selection widget
        """
        values = [(comp.id, comp.name) for comp in company.Company.query()]
        if default_entry is not None:
            values.insert(0, default_entry)
        return ChosenSingleWidget(
            values=values,
            placeholder=u"Sélectionner une entreprise",
            **widget_options
            )
    return deferred_company_choices


def company_node(**kw):
    """
    Return a schema node for company selection

    """
    widget_options = kw.pop('widget_options', {})
    return colander.SchemaNode(
        colander.Integer(),
        widget=get_deferred_company_choices(widget_options),
        **kw
        )


def today_node(**kw):
    """
    Return a schema node for date selection, defaulted to today
    """
    if not "default" in kw:
        kw['default'] = deferred_today
    widget_options = kw.pop('widget_options', {})
    return colander.SchemaNode(
            colander.Date(),
            widget=get_date_input(**widget_options),
            **kw)


def now_node(**kw):
    """
    Return a schema node for time selection, defaulted to "now"
    """
    if not "default" in kw:
        kw['default'] = deferred_now
    return colander.SchemaNode(
        colander.DateTime(),
        widget=get_datetime_input(),
        **kw)


def come_from_node(**kw):
    """
    Return a form node for storing the come_from page url
    """
    if not "missing" in kw:
        kw["missing"] = ""
    return colander.SchemaNode(
            colander.String(),
            widget=widget.HiddenWidget(),
            **kw
            )


def textarea_node(**kw):
    """
    Return a node for storing Text objects
    """
    css_class = kw.pop('css_class', None) or 'span10'
    if kw.pop('richwidget', None):
        wid = widget.RichTextWidget(css_class=css_class, theme="advanced")
    else:
        wid = widget.TextAreaWidget(css_class=css_class)
    return colander.SchemaNode(
            colander.String(),
            widget=wid,
            **kw
            )


@colander.deferred
def default_year(node, kw):
    return datetime.date.today().year


def get_year_select_deferred(query_func):
    """
    return a deferred widget for year selection
    :param query_func: the query function returning a list of years
    """
    @colander.deferred
    def deferred_widget(node, kw):
        years = query_func()
        return widget.SelectWidget(values=zip(years, years),
                    css_class='input-small')
    return deferred_widget


def year_select_node(**kw):
    """
    Return a year select node with defaults and missing values
    """
    title = kw.pop('title', u"")
    query_func = kw.pop('query_func', get_invoice_years)
    return colander.SchemaNode(
        colander.Integer(),
        widget=get_year_select_deferred(query_func),
        default=default_year,
        missing=default_year,
        title=title,
        **kw
        )


@colander.deferred
def default_month(node, kw):
    return datetime.date.today().month


def get_month_options():
    return [(index, calendar.month_name[index].decode('utf8')) \
            for index in range(1, 13)]


def get_month_select_widget():
    """
    Return a select widget for month selection
    """
    options = get_month_options()
    return widget.SelectWidget(values=options,
                    css_class='input-small')


def month_select_node(**kw):
    """
    Return a select widget for month selection
    """
    title = kw.pop('title', u"")
    default = kw.pop('default', default_month)
    missing = kw.pop('missing', default_month)
    return colander.SchemaNode(
            colander.Integer(),
            widget=get_month_select_widget(),
            default=default,
            missing=missing,
            title=title,
            )


def mail_node(**kw):
    """
        Return a generic customized mail input field
    """
    title = kw.pop('title', None) or u"Adresse e-mail"
    return colander.SchemaNode(
        colander.String(),
        title=title,
        validator=colander.Email(MAIL_ERROR_MESSAGE),
        **kw)


