// Copyright (c) 2018, Element Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Travel Settings', {
	refresh: function(frm) {

	},
	onload: function(frm){
		frm.set_query("income_account",function(){
			return {
				"filters":{
					"account_type":"Income Account",
					"is_group":0
				}
			}
		});
		frm.set_query("debit_to",function(){
			return {
				"filters":{
					"account_type":"Receivable"
				}
			}
		});
		frm.set_query("cost_center",function(){
			return {
				"filters":{
					"is_group": 0
				}
			}
		});
		frm.set_query("credit_to",function(){
			return {
				"filters":{
					"account_type":"Payable",
					"is_group":0
				}
			}
		});
		frm.set_query("cost_account",function(){
			return {
				"filters":{
					"account_type":"Cost of Goods Sold"
				}
			}
		});
	}
});
