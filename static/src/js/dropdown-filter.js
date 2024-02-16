odoo.define('fom.resourcetype.dropdown_filter', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var DropdownFilter = Widget.extend({
        events: {
            'click .dropdown-toggle': '_toggleDropdown',
            'click .dropdown-item': '_selectItem',
        },

        start: function () {
            this.$el.addClass('dropdown-filter');
            this.$('.dropdown-toggle').append('<span class="fa fa-caret-down"></span>');
            return this._super.apply(this, arguments);
        },

        _toggleDropdown: function () {
            this.$el.toggleClass('open');
        },

        _selectItem: function (ev) {
            var value = $(ev.currentTarget).data('value');
            this.trigger_up('facet_selected', { id: value });
        },
    });

    core.form_widget_registry.add('selection_tree', DropdownFilter);

    return DropdownFilter;
});