frappe.ui.form.on("Sales Invoice", {
	refresh: function() {
		cur_frm.add_custom_button(__("Inquiry"), function() {
			erpnext.utils.map_current_doc({
				method: "erpnext.selling.doctype.sales_order.sales_order.make_delivery_note",
				source_doctype: "Inquiry",
				target: cur_frm,
				setters: {
					customer: cur_frm.doc.customer || undefined,
				},
				get_query_filters: {
					docstatus: 1,
					company: cur_frm.doc.company,
				}
			})
		}, __("Get items from"));
	},
	refresh: function(frm){
		frm.events.set_total_delivery_note(frm);
		frm.events.set_total_related_invoice(frm);
	},
	validate: function(frm){
		frm.events.set_total_delivery_note(frm);
		frm.events.set_total_related_invoice(frm);
	},
	type_of_invoice: function(frm){
		if(frm.doc.type_of_invoice == "Pelunasan"){
			frm.clear_table("delivery");
			if(!frm.doc.inquiry) return;
			return frappe.call({
				method: 'preorder.preorder.lemparan.get_delivery_note',
				args: {
					inquiry: frm.doc.inquiry
				},
				callback: function(r, rt) {
					if(r.message) {
						$.each(r.message, function(i, d) {
							var c = frm.add_child("delivery");
							c.delivery_note = d.delivery_note;
							c.posting_date = d.posting_date;
							c.net_total = d.net_total;
						})
						frm.refresh_fields();
						frm.events.set_total_delivery_note(frm);
					}
				}
			})
		}else if(frm.doc.type_of_invoice == "Retensi"){
			frm.clear_table("related");
			if(!frm.doc.inquiry) return;
			return frappe.call({
				method: 'preorder.preorder.lemparan.get_sales_invoice',
				args: {
					inquiry: frm.doc.inquiry
				},
				callback: function(r, rt) {
					if(r.message) {
						$.each(r.message, function(i, d) {
							var c = frm.add_child("related");
							c.sales_invoice = d.sales_invoice;
							c.posting_date = d.posting_date;
							c.net_total = d.net_total;
						})
						frm.refresh_fields();
						frm.events.set_total_related_invoice(frm);
					}
				}
			})
		}
	},
	percentage_dp: function(frm){
		frm.events.set_total_delivery_note(frm);
	},
	set_total_delivery_note: function(frm) {
		var total_dn = 0.0;
		$.each(frm.doc.delivery, function(i, row) {
			total_dn += flt(row.net_total);
		})
		frm.set_value("total_delivery_note", Math.abs(total_dn));
	},
	set_total_related_invoice: function(frm) {
		var total_si = 0.0;
		$.each(frm.doc.related, function(i, row) {
			total_si += flt(row.net_total);
		})
		frm.set_value("total_related_invoices", Math.abs(total_si));
		frm.set_value("write_off_amount", Math.abs(total_si));
	},
	adjust_taxes_and_charges: function(frm, cdt, cdn) {
		var tbl = frm.doc.taxes || [];
		var i = tbl.length;
		while (i--) {
			if(frm.doc.taxes[i].charge_type != "Actual"){
				var selisih = flt(frm.doc.net_total) - flt(frm.doc.write_off_amount);
				var actual = (flt(frm.doc.taxes[i].tax_amount)/flt(frm.doc.net_total)) * selisih;
				frm.doc.taxes[i].tax_amount = Math.abs(actual);
				frm.doc.taxes[i].charge_type = "Actual";
				frm.refresh_field("taxes");
			}
		}
	},
});
frappe.ui.form.on("Sales Invoice", "get_items", function(frm) {
    if(frm.doc.type_of_invoice == "Down Payment"){
	erpnext.utils.map_current_doc({
	    method: "preorder.preorder.lemparan.get_items_tampungan",
	    source_name: "SO|"+cur_frm.doc.sales_order+"|"+cur_frm.doc.percentage_dp+"|"+cur_frm.doc.inquiry,
	});
    }else if(frm.doc.type_of_invoice == "Progress Payment"){
	erpnext.utils.map_current_doc({
	    method: "preorder.preorder.lemparan.get_items_tampungan",
	    source_name: "DN|"+cur_frm.doc.delivery_note+"|"+cur_frm.doc.percentage_dp+"|"+cur_frm.doc.inquiry,
	});
    }else if(frm.doc.type_of_invoice == "Pelunasan"){
	erpnext.utils.map_current_doc({
	    method: "preorder.preorder.lemparan.get_items_from_pelunasan",
	    source_name: frm.doc.total_delivery_note+"|"+cur_frm.doc.percentage_dp+"|"+cur_frm.doc.inquiry,
	});
    }
})
/*
var calculate_total_dn = function(frm) {
    var total_claim = frappe.utils.sum(
        (frm.doc.delivery || []).map(function(i) {
			return (i.net_total);
		})
    );
    frm.set_value("total_delivery_note", total_claim);
}
frappe.ui.form.on("Sales Invoice", "percentage_dp", function(frm) {
    calculate_total_dn(frm);
})
frappe.ui.form.on("Sales Invoice", "validate", function(frm) {
    calculate_total_dn(frm);
})
*/
cur_frm.set_query("sales_order",  function (frm) {
    return {
        filters: [
            ['docstatus', '=', '1'],
	    ['status', 'in', 'To Deliver and Bill, To Bill, To Deliver, Completed'],
	    ['customer', '=', cur_frm.doc.customer]
        ]
    }
});
frappe.ui.form.on("Sales Invoice", "sales_order", function(frm, cdt, cdn) {
	frappe.call({
		method: "frappe.client.get",
	        args: {
			doctype: "Sales Order",
			filters:{
				name: cur_frm.doc.sales_order
			}
	        },
	        callback: function (data) {
			frappe.model.set_value(cdt, cdn, "nominal_so", data.message.net_total);
		}
	})
});
frappe.ui.form.on("Sales Invoice", "validate", function(frm) {
    calculate_multilevel_discount(frm);
})
var calculate_multilevel_discount = function(frm) {
    var diskon1 = frm.doc.discount_1;
    var diskon2 = frm.doc.discount_2;
    var diskon3 = frm.doc.discount_3;
    var diskon1_amt = ((100 - diskon1)/100) * 100;
    var diskon2_amt = ((100 - diskon2)/100) * diskon1_amt;
    var diskon3_amt = ((100 - diskon3)/100) * diskon2_amt;
    var total_diskon = 100 - diskon3_amt;
    var diskon1_amount = (diskon1/100) * frm.doc.total;
    var amount_after1 = frm.doc.total - diskon1_amount;
    var diskon2_amount = (diskon2/100) * amount_after1;
    var amount_after2 = amount_after1 - diskon2_amount;
    var diskon3_amount = (diskon3/100) * amount_after2;
    var amount_after3 = amount_after2 - diskon3_amount;
    frm.set_value("additional_discount_percentage", total_diskon);
    frm.set_value("discount_1_amount", diskon1_amount);
    frm.set_value("amount_after_discount_1", amount_after1);
    frm.set_value("discount_2_amount", diskon2_amount);
    frm.set_value("amount_after_discount_2", amount_after2);
    frm.set_value("discount_3_amount", diskon3_amount);
    frm.set_value("amount_after_discount_3", amount_after3);
}
frappe.ui.form.on("Sales Invoice", "discount_1", function(frm) {
    calculate_multilevel_discount(frm);
})
frappe.ui.form.on("Sales Invoice", "discount_2", function(frm) {
    calculate_multilevel_discount(frm);
})
frappe.ui.form.on("Sales Invoice", "discount_3", function(frm) {
    calculate_multilevel_discount(frm);
})
frappe.ui.form.on("Sales Invoice", "net_total", function(frm) {
    calculate_multilevel_discount(frm);
})
