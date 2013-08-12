<%doc>
Template used to render a search form
</%doc>
<% from autonomie.views.forms.lists import ITEMS_PER_PAGE_OPTIONS %>
<form class='navbar-form offset1 pull-right form-search form-inline' id='${elem.id_}' method='GET'>
    <div class='pull-left'>
        <input type='text' name='search' class='input-medium search-query' value="${elem.defaults['search']}">
        % if elem.helptext:
            <span class="help-block">${elem.helptext}</span>
        %endif
    </div>
    <select name='items_per_page'>
        % for text, value in ITEMS_PER_PAGE_OPTIONS:
            % if int(value) == int(elem.defaults['items_per_page']):
                <option value="${value}" selected='true'>${text}</option>
            %else:
                <option value="${value}">${text}</option>
            %endif
        % endfor
    </select>
    <button type="submit" class="btn" class='vertical-align:bottom;'>${elem.submit_text}</button>
</form>
