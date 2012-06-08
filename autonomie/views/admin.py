# -*- coding: utf-8 -*-
# * File Name : admin.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Administration views
    - user account handling
    - company account handling
    - config database configuration
    - welcome message delivery
"""
import logging


from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from deform import Form
from deform import ValidationFailure

from autonomie.models.model import Config
from autonomie.views.forms import MainConfig
from autonomie.views.forms.admin import get_config_appstruct
from autonomie.views.forms.admin import merge_dbdatas
from .base import BaseView

log = logging.getLogger(__name__)

class AdminViews(BaseView):
    """
        Main class for admin views
    """
    @view_config(route_name='admin_index', renderer='admin/index.mako', permission='admin')
    def admin_index(self):
        """
            Index of the administration page
        """
        return dict(title=u"Administration du site")

    @view_config(route_name="admin_main", renderer="admin/main.mako", permission='admin')
    def admin_main(self):
        """
            Main parameters administration
        """
        schema = MainConfig()
        form = Form(schema, buttons=('submit',))
        if 'submit' in self.request.params:
            datas = self.request.params.items()
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, errform:
                html_form = errform.render()
            else:
                # Validation OK
                # la table config étant un stockage clé valeur
                # le merge_session_with_post ne peut être utilisé
                dbdatas = self.dbsession.query(Config).all()
                dbdatas = merge_dbdatas(dbdatas, appstruct)
                for data in dbdatas:
                    self.dbsession.merge(data)
                self.dbsession.flush()
                self.request.session.flash(
                        u"La configuration a bien été modifiée", queue='main')
                return HTTPFound(self.request.route_path("admin_main"))
        else:
            config_dict = self.request.config
            appstruct = get_config_appstruct(config_dict)
            html_form = form.render(appstruct)
        return dict(title=u"Configuration générale",
                    html_form=html_form)
