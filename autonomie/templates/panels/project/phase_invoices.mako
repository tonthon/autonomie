<%doc>
    * Copyright (C) 2012-2016 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
       * TJEBBES Gaston <g.t@majerti.fr>

 This file is part of Autonomie : Progiciel de gestion de CAE.

    Autonomie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Autonomie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
</%doc>
<div class='header'>
    <h3 class='pull-left'>Factures, Avoirs</h3>
    % if api.has_permission('add_invoice'):
        <a
            class='btn btn-primary primary-action'
            href="${add_url}"
            ><span class='glyphicon glyphicon-plus-sign'></span>&nbsp;Créer une facture
        </a>
    % endif
</div>
% if invoices:
    <table class='table table-striped table-condensed'>
        <thead>
            <th></th>
            <th>Numéro</th>
            <th>Nom</th>
            <th class="hidden-xs">État</th>
            <th class='actions'>Actions</th>
        </thead>
    % for invoice in invoices:
    <tr>
        <td>
            % if getattr(invoice, 'estimation', None) or getattr(invoice, 'cancelinvoices', None) or getattr(invoice, 'invoice', None):
                <div
                    style="background-color:${invoice.color};\
                    width:10px;">
                    <br />
                </div>
            % endif
        </td>
        <% view_url = request.route_path('/%ss/{id}' % invoice.type_, id=invoice.id) %>
        <td
            class='rowlink'
            onclick="document.location='${view_url}'">
            ${invoice.official_number}
        </td>
        <td
            class='rowlink'
            onclick="document.location='${view_url}'">
            ${invoice.name}
        </td>
        <td
            class='rowlink hidden-xs'
            onclick="document.location='${view_url}'">
            % if api.status_icon(invoice):
                <i class='glyphicon glyphicon-${api.status_icon(invoice)}'></i>
            % endif
            ${api.format_status(invoice)}
        </td>
        <td class='actions'>
        ${request.layout_manager.render_panel('menu_dropdown', label="Actions", links=stream_actions(request, invoice))}
        </td>
    </tr>
    % endfor
    </table>
%else:
    <em>Aucune facture n'a été créée</em>
% endif
