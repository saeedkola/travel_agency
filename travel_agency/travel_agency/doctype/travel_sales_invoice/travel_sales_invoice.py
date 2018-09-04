# -*- coding: utf-8 -*-
# Copyright (c) 2018, Element Labs and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import money_in_words
from frappe.utils.csvutils import getlink
from erpnext.controllers.accounts_controller import AccountsController
from erpnext.accounts.general_ledger import delete_gl_entries

class TravelSalesInvoice(AccountsController):
	def validate(self):
		for item in self.items:
		    if not item.supplier:
		    	if self.supplier:
		    		item.supplier = self.supplier
		    	else:
		    		frappe.throw('Row number {0} is Blank. Default Supplier Not Set.'.format(item.idx))

		if self.is_paid_by_customer:
			if not self.customer_payments:
				frappe.throw('Customer Payments Table is Empty')

		if self.is_paid_supplier:
			if not self.supplier_payments:
				frappe.throw('Supplier Payments Table is Empty')

	def on_submit(self):
		gl_entries = []
		settings = frappe.get_single('Travel Settings')
		#customer gl entries
		gl_entries.append({	
			"account": settings.debit_to,
			"party": self.customer,
			"party_type": "Customer",
			"debit": self.total_amount,
			"debit_in_account_currency": self.total_amount
		})

		gl_entries.append({
			"account": settings.income_account,
			"credit": self.total_amount,
			"credit_in_account_currency": self.total_amount,
			"cost_center": settings.cost_center	
		})

		for item in self.items:
			gl_entries.append({
				"account": settings.credit_to,
				"party": item.supplier,
				"party_type": "Supplier",
				"credit": item.cost_amount,
				"credit_in_account_currency": item.cost_amount		
			})
			gl_entries.append({				
				"account": settings.cost_account,
				"debit": item.cost_amount,
				"debit_in_account_currency": item.cost_amount,
				"cost_center": settings.cost_center
			})

		if self.is_paid_by_customer:
			for item in self.customer_payments:
				gl_entries.append({
					"account": item.payment_account,						
					"debit": item.amount,
					"debit_in_account_currency": item.amount
				})
				
				gl_entries.append({
						"account": settings.debit_to,						
						"party": self.customer,
						"party_type": "Customer",				
						"credit": item.amount,
						"credit_in_account_currency": item.amount	
				})
				

		if self.is_paid_supplier:
			for item in self.supplier_payments:
				gl_entries.append({
					"account": item.payment_account,
					"credit": item.amount,
					"credit_in_account_currency": item.amount	
				})
				
				gl_entries.append({
					"account": settings.credit_to,
					"party": item.supplier,
					"party_type": "Supplier",
					"debit": item.amount,
					"debit_in_account_currency": item.amount
				})

		doc = frappe.get_doc({
			"doctype": "Journal Entry",
			"company": self.company,
			"posting_date": self.posting_date,
			"voucher_type": "Journal Entry",
			"accounts" : gl_entries,
			"docstatus": 1			
		})
		jv = doc.insert()
		self.journal_entry = jv.name
		self.save()

	def on_cancel(self):
		jv = frappe.get_doc("Journal Entry", self.journal_entry)
		jv.docstatus = 2
		jv.save()

		self.journal_entry = ""
		self.save()