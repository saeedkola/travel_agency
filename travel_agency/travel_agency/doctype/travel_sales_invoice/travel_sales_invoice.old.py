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
		self.make_gl_entries()

	def make_gl_entries(self):
		gl_entries = []
		settings = frappe.get_single('Travel Settings')
		#customer gl entries
		gl_entries.append(
			self.get_gl_dict({
				"account": settings.debit_to,
				"party_type": "Customer",
				"party": self.customer,
				"against": settings.income_account,
				"debit": self.total_amount,
				"debit_in_account_currency": self.total_amount,
				"voucher_no": self.name,
				"voucher_type": self.doctype
			})
		)

		gl_entries.append(
			self.get_gl_dict({
				"account": settings.income_account,
				"against": self.customer,
				"credit": self.total_amount,
				"credit_in_account_currency": self.total_amount,
				"cost_center": settings.cost_center,
				"voucher_no": self.name,
				"voucher_type": self.doctype				
			})
		)

		for item in self.items:
			gl_entries.append(
				self.get_gl_dict({
					"account": settings.credit_to,
					"party_type": "Supplier",
					"party": item.supplier,
					"against": settings.cost_account,
					"credit": item.cost_amount,
					"credit_in_account_currency": item.cost_amount,
					"voucher_no": self.name,
					"voucher_type": self.doctype	
				})
			)
			gl_entries.append(
				self.get_gl_dict({
					"account": settings.cost_account,
					"against": item.supplier,
					"debit": item.cost_amount,
					"debit_in_account_currency": self.total_amount,
					"cost_center": settings.cost_center,
					"voucher_no": self.name,
					"voucher_type": self.doctype
				})
			)

		if self.is_paid_by_customer:
			for item in self.customer_payments:
				gl_entries.append(
					self.get_gl_dict({
						"account": item.payment_account,
						"against": self.customer,
						"debit": item.amount,
						"debit_in_account_currency": item.amount,
						"voucher_type": self.doctype,
						"voucher_no" : self.name
					})
				)

				gl_entries.append(
					self.get_gl_dict({
						"account": settings.debit_to,
						"party_type": "Customer",
						"party": self.customer,
						"against": item.payment_account,
						"credit": item.amount,
						"credit_in_account_currency": item.amount,
						"voucher_no": self.name,
						"voucher_type": self.doctype
					})
				)

		if self.is_paid_supplier:
			for item in self.supplier_payments:
				gl_entries.append(
					self.get_gl_dict({
						"account": item.payment_account,
						"against": item.supplier,
						"credit": item.amount,
						"credit_in_account_currency": item.amount,
						"voucher_type": self.doctype,
						"voucher_no" : self.name
					})
				)
				gl_entries.append(
					self.get_gl_dict({
						"account": settings.credit_to,
						"party_type": "Supplier",
						"party": item.supplier,
						"against": item.payment_account,
						"debit": item.amount,
						"debit_in_account_currency": item.amount,
						"voucher_no": self.name,
						"voucher_type": self.doctype
					})
				)

		from erpnext.accounts.general_ledger import make_gl_entries
		make_gl_entries(gl_entries, cancel=(self.docstatus == 2),
			update_outstanding="Yes", merge_entries=False)		
	def on_cancel(self):
		delete_gl_entries(voucher_type=self.doctype, voucher_no=self.name)


		
		
