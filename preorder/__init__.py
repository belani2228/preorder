# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = '0.5.6'

#0.5.6:
#   - Custom script item
#0.5.5:
#   - Minor update ntah dimana
#0.5.4:
#   - Minor update Assembly
#0.5.3:
#   - Add engineer in inquiry
#0.5.2:
#   - Update Sales Order
#0.5.1:
#   - Add doctype: Quotation Assembly Item
#   - Make Product Bundle from Product Assembly
#0.5.0:
#   - Add doctype: Product Assembly
#   - Add doctype: Product Assembly Item
#   - Add doctype: Inqury All Item
#   - Update doctype: Inqury Item
#   - Cleaning up request_for_supplier_quotation.py
#0.4.11:
#   - Add projected_qty in Purchase Order
#0.4.10:
#   - Add Proforma Invoice No in Sales Order
#   - Update Laporan Pembalik HPP
#0.4.9:
#   - Tidak bisa save delivery note jika group customernya reseler yang blm lunas
#   - Update & fix laporan pembalik hpp
#   - update get ammount injournal entry
#0.4.8:
#   - Remove Get Items in Request for Supplier Quotation
#   - Fix & update in Request for Supplier Quotation
#0.4.7:
#   - Fix buying write off account in Item Settings js
#0.4.6:
#   - Minor update on sales invoice write off account
#0.4.5:
#   - Add Laporan Pembalik HPP
#   - Update Delivery Note utk membuat Journal Entry
#   - Update Journal Entry utk menampung Reversing Entry
#   - Update hooks.py
#0.4.4:
#   - Menghubungkan Item Settings dengan Quotation Item
#0.4.3:
#   - Write off account in sales invoice & purchase invoice now automatic when type_of_invoice: Retention or Non Project Payment
#   - Update doctype Item Settings
#   - Sales Order tidak bisa save jika masih ada item tampungan
#0.4.2:
#   - Add Urgency Level on Inquiry
#0.4.1:
#   - Minor fix in Purchase Invoice custom script
#0.4.0:
#   - Percentage should not be greater than 100 or less than 0 in Purchase Invoice
#   - Adjustment taxes and charges in Purchase Invoice if taxes is exist
#0.3.9:
#   - Add get items from sales order in purchase order
#   - Minor fix purchase invoice DP taxes
#0.3.8:
#   - Update Purchase Order, Purchase Receipt, Purchase Invoice custom script
#0.3.7:
#   - Update related document in inquiry
#   - Set null in sales invoice unnecessary field if type of invoice has change
#   - Partial down payment when type of invoice sales invoice is non project payment
#   - Add purchase.py for accommodate all documents related to purchase
#0.3.6:
#   - Add down payment partial in sales invoice
#0.3.5:
#   - Update fixture
#0.3.4:
#   - Fix sales invoice dp, progress payment, pelunasan & retensi
#0.3.3:
#   - Fixture
#0.3.2:
#   - Sales Invoice with DP, progress payment, pelunasan & retensi
#   - Sales Invoice, Button Addjust taxes jika tipe invoice retensi
#0.3.1:
#   - Sales Invoice: Tambah get_items ketika tipe invoice pilih Down Payment
#0.3.0:
#   - Add custom & fixture in app
#0.2.0:
#   - Tdk pakai supplier quotation lagi
#0.1.5:
#   - Minor fix Inquiry
#0.1.4:
#   - Minor fix ketika submit supplier quotation
#0.1.3:
#   - Add supplier name in inquiry, quotation & sales order
#0.1.2:
#   - Fix supplier quotation tidak bisa hapus jika sudah ada quotation
#0.1.1:
#   - Fix no copy for title in RfSQ when get item from Inquiry
#0.1.0:
#   - Pindah file custom.css ke files
#0.0.23:
#   - Update lemparan, get_items_selling_quotation
#0.0.22:
#   - Update lemparan, get_items_from_sales_order
#0.0.21:
#   - Update on_submit in RfSQ
#0.0.20:
#   - Add in hooks.py: on_submit Sales Order
#   - Add in hooks.py: on_submit Purchase Order
#   - Add in hooks.py: before_cancel Purchase Order
#   - Update lemparan, get_items_from_sales_order
#0.0.19:
#   - Update Inquiry & Inquiry Item
#0.0.18:
#   - Add status Completed in RfSQ, if Supplier Quotation submit
#0.0.17:
#   - Add Set as Lost in Request for Supplier Quotation
#   - Add request_for_supplier_quotation_list.js
#   - Update Request for Supplier Quotation
#0.0.16:
#   - Update operan.py
#0.0.15:
#   - Update lemparan.py get_items_selling_quotation
#   - Add 3 rate & 3 supplier in Quotation
#   - Update on_submit & before_cancel Supplier Quotation
#0.0.14:
#   - Update lemparan.py get_items_selling_quotation
#0.0.13:
#   - Add status di Inquiry
#0.0.12:
#   - Fixed get_items in Quotation
#0.0.11:
#   - Add ignore price list from RFSQ to Supplier Quotation
#   - Add Dashboard in Inquiry
#   - Fox get_items in Reqeust for Supplier Quotation
#0.0.10:
#   - Update filter inquiry di quotation, hanya Inquiry yg sudah ada Supplier Quotation saja yg akan tampil
#   - Update hooks.py on_submit Quotation
#   - Update hooks.py before_cancel Quotation
#   - Update hooks.py on_submit Supplier Quotation
#   - Update hooks.py before_cancel Supplier Quotation
#0.0.9:
#   - Add operan.py
#0.0.8:
#   - Update Request for Supplier Quotation
#   - Update Supplier Quotation
#0.0.7:
#   - Fixed Request for Supplier Quotation
#0.0.6:
#   - Update Request for Supplier Quotation
#0.0.5:
#   - Add Request for Supplier Quotation
#0.0.4:
#0.0.3:
#   - Update Inquiry
#0.0.2:
#   - Add Inquiry
