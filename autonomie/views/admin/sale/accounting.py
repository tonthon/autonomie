# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os

import logging

from autonomie.models.treasury import CustomInvoiceBookEntryModule
from autonomie.forms.admin import get_config_schema

from autonomie.views.admin.tools import (
    get_model_admin_view,
    BaseConfigView,
    BaseAdminIndexView,
)
from autonomie.views.admin.sale import (
    SALE_URL,
    SaleIndexView,
)


logger = logging.getLogger(__name__)
ACCOUNTING_URL = os.path.join(SALE_URL, 'accounting')
ACCOUNTING_CONFIG_URL = os.path.join(ACCOUNTING_URL, 'config')


BaseSaleAccountingCustomView = get_model_admin_view(
    CustomInvoiceBookEntryModule,
    r_path=ACCOUNTING_URL,
)


class SaleAccountingIndex(BaseAdminIndexView):
    title = u"Configuration comptable du module Vente"
    description = u"Configurer la génération des écritures de vente"
    route_name = ACCOUNTING_URL


class SaleAccountingConfigView(BaseConfigView):
    """
        Cae information configuration
    """
    title = u"Configuration des informations générales et des \
modules prédéfinis"
    description = u"Configuration du code journal et des modules prédéfinis \
(Export des factures, contribution à la CAE, RG Externe, RG Interne)"
    route_name = ACCOUNTING_CONFIG_URL

    validation_msg = u"Les informations ont bien été enregistrées"
    keys = (
        'code_journal',
        'numero_analytique',
        'compte_frais_annexes',
        'compte_cg_banque',
        'compte_rrr',
        'compte_cg_tva_rrr',
        'code_tva_rrr',
        'compte_cg_contribution',
        "contribution_cae",
        'compte_rg_interne',
        "taux_rg_interne",
        'compte_rg_externe',
        "taux_rg_client",
        'sage_facturation_not_used',
        "sage_contribution",
        'sage_rginterne',
        'sage_rgclient',
    )
    schema = get_config_schema(keys)
    info_message = u"""
Configurez les exports comptables de votre CAE.
Configurez les champs indispensables aux exports :\
    <ul>\
        <li>Code journal</li>\
        <li>Numéro analytique de la CAE</li>\
        <li>Compte banque de l'entrepreneur</li>\
    </ul>\
Configurez les champs relatifs aux frais et remises:\
    <ul>\
<li>Compte de frais annexes</li>\
<li>Compte RRR (Rabais, Remises et Ristournes)</li>\
    </ul>\
    Configurez et activez des modules de retenues optionnels :\
        <ul>\
    <li>Module de contribution à la CAE</li>\
    <li>Module RG Externe (spécifique bâtiment)</li>\
    <li>Module RG Interne (spécifique bâtiment)</li>\
    </ul>
    """


class SaleAccountingCustomView(BaseSaleAccountingCustomView):
    title = u"Modules de contribution personnalisés"
    description = u"Configurer des écritures personnalisées pour les exports \
de factures"

    widget_options = {
        'add_subitem_text_template': u"Ajouter un module de contribution \
personnalisé",
        "orderable": False,
    }

    def query_items(self):
        return self.factory.query().filter_by(active=True).all()


def add_routes(config):
    config.add_route(ACCOUNTING_URL, ACCOUNTING_URL)
    config.add_route(ACCOUNTING_CONFIG_URL, ACCOUNTING_CONFIG_URL)
    config.add_route(
        SaleAccountingCustomView.route_name,
        SaleAccountingCustomView.route_name,
    )


def includeme(config):
    add_routes(config)
    config.add_admin_view(SaleAccountingIndex, parent=SaleIndexView)
    config.add_admin_view(SaleAccountingConfigView, parent=SaleAccountingIndex)
    config.add_admin_view(SaleAccountingCustomView, parent=SaleAccountingIndex)
