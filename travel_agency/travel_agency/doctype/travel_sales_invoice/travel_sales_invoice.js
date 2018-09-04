// Copyright (c) 2018, Element Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Travel Sales Invoice', {
	refresh: function(frm) {

	},
	onload: function(frm){		
		frm.set_query("payment_account", "customer_payments", function(doc, cdt, cdn) {
			return {
				"filters":{
						"account_type":["in", ["Bank", "Cash"]],
						"is_group":0
				}
			}
		});
		frm.set_query("payment_account", "supplier_payments", function(doc, cdt, cdn) {
			// console.log(suppliers);
			return {
				"filters":{
						"account_type":["in", ["Bank", "Cash"]],
						"is_group":0
				}
			}
		});
	},
	customer : function(){
		// var me = this;
		// if(this.frm.updating_party_details) return;

		// erpnext.utils.get_party_details(this.frm,
		// 	"erpnext.accounts.party.get_party_details", {
		// 		posting_date: this.frm.doc.posting_date,
		// 		party: this.frm.doc.customer,
		// 		party_type: "Customer",
		// 		account: this.frm.doc.debit_to,
		// 		price_list: this.frm.doc.selling_price_list,
		// 	}, function() {
		// 		me.apply_pricing_rule();
		// 	})
	},
	is_paid_by_customer: function(frm){
		if(frm.doc.is_paid_by_customer){
			var d = frappe.model.add_child(frm.doc, "Travel Invoice Payment", "customer_payments");
			d.amount = frm.doc.total_amount;
			refresh_field("customer_payments");
		}else{
			frm.clear_table("customer_payments");
		}
	},
	is_paid_supplier: function(frm){
		if(frm.doc.is_paid_supplier){
			var items = frm.doc.items;
			var data = [];
			for (var i = 0; i < items.length; i++) {
				if (items[i].supplier in data) {
					data[items[i].supplier] += items[i].cost_amount;
				}else{
					data[items[i].supplier] = items[i].cost_amount;
				}
			}
			for(var key in data){
				var d = frappe.model.add_child(frm.doc, "Travel Invoice Supplier Payment", "supplier_payments");
				d.supplier = key;
				d.amount = data[key];
			}
			refresh_field("supplier_payments");
		}else{
			frm.clear_table("supplier_payments");
		}
	},
	supplier: function(frm){
		set_table_defaults(frm);
	}


});

frappe.ui.form.on("Travel Sales Item", "qty", update_item_totals );
frappe.ui.form.on("Travel Sales Item", "cost_rate", update_item_totals );
frappe.ui.form.on("Travel Sales Item", "sales_rate", update_item_totals );
// frappe.ui.from.on("Travel Sales Item", "supplier", trigger_setquery);

frappe.ui.form.on('Travel Sales Item',{
	item_code: function(frm){
		// console.log(frm.doc);
	},
	items_add: function(frm,cdt,cdn){
		set_table_defaults(frm);
	},
	items_remove: function(frm,cdt,cdn){
		update_grand_totals(frm);
	}
});



function update_item_totals(frm,cdt,cdn){

	var child = locals[cdt][cdn];
	child.cost_amount = (child.cost_rate) * child.qty;
	child.sales_amount = (child.sales_rate) * child.qty;
	refresh_field("items");
	update_grand_totals(frm);

}

function update_grand_totals(frm){
	var total_cost = 0;
	var total_sales = 0;
	frm.doc.items.forEach(function(d) { 
		total_cost += d.cost_amount; 
		total_sales += d.sales_amount;
	});
	frm.set_value('total_cost',total_cost);
	frm.set_value('total_amount',total_sales);
	trigger_setquery(frm);
}

function trigger_setquery(frm,cdt,cdn){
	
	frm.set_query("supplier", "supplier_payments", function(doc, cdt, cdn) {
		// console.log(suppliers);
		var items = frm.doc.items;
		var suppliers = [];
		for (var i = 0; i < items.length; i++) {
			if (items[i].supplier) {
				suppliers.push(items[i].supplier);
			}		
		}
		return {
			"filters":{
					"name":["in", suppliers]
			}
		}
	});
}

function set_table_defaults(frm){
	var items = frm.doc.items;
	for (var i = 0; i < items.length; i++) {
		if(!items[i].supplier){
			if (frm.doc.supplier) {
				items[i].supplier = frm.doc.supplier;
				refresh_field("items");

			}
		}
	}
}
