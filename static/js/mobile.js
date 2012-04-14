/*
 * Event model. Grabs the instances from the REST API.
 */
Ext.define('Event', {
	extend: 'Ext.data.Model',
	config: {
		fields: ['id', 'title', 'start', 'duration', 'url'],
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
	id: 'EventStore',
	model: 'Event',
	sorters: 'start',
	grouper: function(record) {
		return record.get('start').hour;
	},
	autoLoad: true
});

Ext.application({
	name : 'RPGflock',

	launch : function() {
		Ext.create("Ext.tab.Panel", {
			fullscreen : true,
			tabBarPosition : 'bottom',

			items : [{
				title : 'Home',
				iconCls : 'home',
				cls : 'home',
				html : ['<img width="65%" src="http://staging.sencha.com/img/sencha.png" />', '<h1>Welcome to Sencha Touch</h1>', "<p>You're creating the Getting Started app. This demonstrates how ", "to use tabs, lists and forms to create a simple app</p>", '<h2>Sencha Touch 2</h2>'].join("")
			}, {
				xtype : 'list',
				title : 'Events',
				iconCls : 'star',
				displayField : 'title',
				items: [{
					width: Ext.os.deviceType == 'Phone' ? null : 300,
					height: Ext.os.deviceType == 'Phone' ? null : 500,
					xtype: 'list',
					store: 'EventStore',
					itemTpl: '<a href="{ url }" style="text-decoration: none;"><div style="font-weight: bold;">{ title }</div><div style="font-style: italic">{ start:date("g:i A") }, { duration } long</div></a>',
					grouped: true
				}]
			},
			//this is the new item
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
