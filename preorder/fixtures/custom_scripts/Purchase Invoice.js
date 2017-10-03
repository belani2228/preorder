frappe.ui.form.on("Purchase Invoice", {
	refresh: function() {

	},
	refresh: function(frm){
		frm.events.set_total_purchase_receipt(frm);
		frm.events.set_total_related_invoice(frm);
	},
	validate: function(frm){
		frm.events.set_total_purchase_receipt(frm);
		frm.events.set_total_related_invoice(frm);
	},
	type_of_invoice: function(frm){
		if(frm.doc.type_of_invoice == "Pelunasan"){
			frm.clear_table("receipt");
//			if(!frm.doc.inquiry) return;
			return frappe.call({
				method: 'preorder.preorder.lemparan.get_delivery_note',
				args: {
					inquiry: frm.doc.inquiry
				},
				callback: function(r, rt) {
					if(r.message) {
						$.each(r.message, function(i, d) {
							var c = frm.add_child("receipt");
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
//			if(!frm.doc.inquiry) return;
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
	set_total_purchase_receipt: function(frm) {
		var total_dn = 0.0;
		$.each(frm.doc.receipt, function(i, row) {
			total_dn += flt(row.net_total);
		})
		frm.set_value("total_purchase_receipt", Math.abs(total_dn));
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
