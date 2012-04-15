/*
 * Event model. Grabs the instances from the REST API.
 */
Ext.define('Event', {
	extend: 'Ext.data.Model',
	config: {
		fields: [
			'id',
			{name: 'title', type: 'string'},
			{name: 'start', type: 'date'},
			{name: 'duration', type: 'float'},
			{name: 'url', type: 'string'}
		],
		proxy: {
			type: 'rest',
			url: '/api/events/',
			format: '?format=json',
			reader: {
				type: 'json'
			}
		}
	}
});

Ext.create('Ext.data.Store', {
	id: 'ListStore',
	model: 'Event',
	sorters: 'start',
	grouper: {
		groupFn: function(record) {
			return Ext.Date.format(record.get('start'), "Y/m/d g:i A");
		},
		sortProperty: 'start'
	},
	autoLoad: true
});

var event_template = new Ext.XTemplate(
	"<div>",
	"<a href=/events/{ id } style='text-decoration: none;'>",
	"<div style='font-weight: bold;'>",
	"{ title }",
	"</div>",
	"<div style='font-style: italic;'>",
	"{ start:date(\"g:i A\") }, { duration } hours",
	"</div>",
	"</a>",
	"</div>"
);

Ext.application({
	name : 'RPGflock',
	
	launch : function() {
		Ext.create("Ext.tab.Panel", {
			fullscreen : true,
			tabBarPosition : 'bottom',
			items : [{
				xtype : 'list',
				title : 'Events',
				iconCls : 'star',
				displayField : 'title',
				items: [{
					width: Ext.os.deviceType == 'Phone' ? null : 300,
					height: Ext.os.deviceType == 'Phone' ? null : 500,
					xtype: 'list',
					store: 'ListStore',
					itemTpl: event_template,
					grouped: true
				}]
			},
			{
				title : 'Contact',
				iconCls : 'user',
				xtype : 'formpanel',
				url : 'contact.php',
				layout : 'vbox',

				items : [{
					xtype : 'fieldset',
					title : 'Contact Us',
					instructions : '(email address is optional)',
					items : [{
						xtype : 'textfield',
						label : 'Name'
					}, {
						xtype : 'emailfield',
						label : 'Email'
					}, {
						xtype : 'textareafield',
						label : 'Message'
					}]
				}, {
					xtype : 'button',
					text : 'Send',
					ui : 'confirm',
					handler : function() {
						this.up('formpanel').submit();
					}
				}]
			}]
		});
	}
});
