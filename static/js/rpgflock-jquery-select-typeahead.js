/*
 * This is a plugin to turn select tags into textinput tags with typeahead autocomplete.
 * 
 * It is not complete.
 * 
 * Use:
 *   $('select#some-id').selectahead(); // Returns jQuery objects of the select items, NOT the newly inserted text items.
 * 
 * Requirements:
 *   jQuery
 *   Bootstrap's bootstrap-typeahead.js
 * 
 * Notes:
 *   Will probably break on select items without an id attribute.
 *   Will behave weirdly if multiple option items in the select have the same inner HTML.
 *   Will behave weirdly if there's markup in the inner HTML of the option items.
 * 
 * Features:
 *   Creates a text input with typeahead sources from the select.
 *   Hides the select.
 * 
 * Todo:
 *   Keep the select set to the option matching the current text of the text input.
 *   Prepopulate the text input with the already-selected item from the select.
 *   Reject text that does not correspond with any item in the select.
 *   Figure out what "finished" means: blur, hit enter, what else?
 */
(function( $ ) {
	$.fn.selectahead = function(settings) {
		function parse_options(options) {
			var ret = [];
			$.each(options, function(i, option) {
				ret.push({
					value: $(option).val(),
					name: $(option).html()
				});
			});
			return ret;
		}
		function parse_options_names(options) {
			// Expects a list of option objects as provided by parse_options above.
			var ret = [];
			$.each(options, function(i, option) {
				ret.push(option.name);
			});
			return ret;
		}
		var settings = $.extend({
			//pass
		}, settings);
		return this.each(function() {
			var options = parse_options($(this).children('option'));
			var options_names = parse_options_names(options);
			var text_input = $('<input type="text" />');
			text_input.attr('id', $(this).attr('id') + "_typeahead");
			$(this).after(text_input);
			$(this).hide();
			settings.source = options_names;
			text_input.typeahead(settings); // This REQUIRES that bootstrap-typeahead.js be loaded.
			// TODO select the appropriate option in the hidden select when the field is "finished", whether by blur or by something else.
			// TODO prepopulate the text_input with the selected item.
		});
	};
})( jQuery );

// Test cases:
//  - Called on a non-select.
//  - Called on a select with non-option children.
//  - Called on a select that subsequently changes.
//  - Called on a select with well-behaved option children.