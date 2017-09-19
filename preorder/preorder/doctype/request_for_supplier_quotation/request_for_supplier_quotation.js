// Copyright (c) 2017, ridhosribumi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Request for Supplier Quotation', {
	refresh: function(frm) {
	},
	refresh: function(frm, cdt, cdn) {
		if (frm.doc.docstatus == 1 && frm.doc.status == "Submitted") {
			//frm.add_custom_button(__('Set as Lost'), cur_frm.cscript['Declare Order Lost']);
			frm.add_custom_button(__("Send Email to Supplier"), function() {
				frappe.call({
					method: 'erpnext.buying.doctype.request_for_quotation.request_for_quotation.send_supplier_emails',
					freeze: true,
					args: {
						rfq_name: frm.doc.name
					},
					callback: function(r){
						frm.reload_doc();
					}
				});
			});
			//cur_frm.add_custom_button(__('Supplier Quotation'), cur_frm.cscript['Supplier Quotation'], __("Make"));
			//cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	},
	get_items: function(frm) {
		return frappe.call({
			method: "get_items",
			doc: frm.doc,
			callback: function(r, rt) {
				frm.refresh()
			}
		});
	},
});
cur_frm.cscript['Declare Order Lost'] = function(){
	var dialog = new frappe.ui.Dialog({
		title: "Set as Lost",
		fields: [
			{"fieldtype": "Text", "label": __("Reason for losing"), "fieldname": "reason",
				"reqd": 1 },
			{"fieldtype": "Button", "label": __("Update"), "fieldname": "update"},
		]
	});

	dialog.fields_dict.update.$input.click(function() {
		var args = dialog.get_values();
		if(!args) return;
		return cur_frm.call({
			method: "declare_order_lost",
			doc: cur_frm.doc,
			args: args.reason,
			callback: function(r) {
				if(r.exc) {
					frappe.msgprint(__("There were errors."));
					return;
				}
				dialog.hide();
				cur_frm.refresh();
			},
			btn: this
		})
	});
	dialog.show();
}
frappe.ui.form.on("Request for Supplier Quotation", {
	refresh: function() {
		if(cur_frm.doc.docstatus == 0 || cur_frm.doc.__islocal){
			cur_frm.add_custom_button(__("Inquiry"), function() {
				erpnext.utils.map_current_doc({
					method: "preorder.preorder.doctype.inquiry.inquiry.make_rfsq",
					source_doctype: "Inquiry",
					target: cur_frm,
					setters:  {
						company: cur_frm.doc.company || undefined,
					},
					get_query_filters: {
						docstatus: 1,
						status: ["!=", "Lost"],
					}
				})
			}, __("Get items from"));
		}
	},
});
cur_frm.cscript['Supplier Quotation'] = function() {
	frappe.model.open_mapped_doc({
		method: "preorder.preorder.doctype.request_for_supplier_quotation.request_for_supplier_quotation.make_supplier_quotation",
		frm: cur_frm
	})
}
cur_frm.set_query("inquiry", "inquiry_tbl",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: {
            'docstatus': 1,
						'status': ["!=", "Lost"]
        }
    }
});
frappe.ui.form.on("Request for Supplier Quotation", "supplier", function(frm, cdt, cdn) {
	    frappe.call({
	        method: "frappe.client.get",
	        args: {
	            doctype: "Supplier",
							filters:{
								name: cur_frm.doc.supplier
							}
	        },
	        callback: function (data) {
							frappe.model.set_value(cdt, cdn, "title", data.message.supplier_name);
					}
	    })
});
frappe.ui.form.on("Request for Supplier Quotation Inquiry", "inquiry", function(frm, cdt, cdn) {
    row = locals[cdt][cdn];
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Inquiry",
						name: row.inquiry
        },
        callback: function (data) {
					if(data.message.status != "Lost"){
            frappe.model.set_value(cdt, cdn, "transaction_date", data.message.transaction_date);
						frappe.model.set_value(cdt, cdn, "customer", data.message.customer);
						frappe.model.set_value(cdt, cdn, "customer_name", data.message.customer_name);
					}
				}
    })
});
/*
cur_frm.cscript.refresh_tbl = function( doc, cdt, cdn) {
	cur_frm.refresh_field("inquiry_tbl");
}
*/
frappe.ui.form.on("Request for Supplier Quotation", "refresh_tbl", function(frm) {
	frm.refresh_field("inquiry_tbl");
/*
	erpnext.utils.map_current_doc({
		method: "preorder.preorder.lemparan.get_items_selling_quotation",
		source_name: cur_frm.doc.name,
	});
	*/
})
