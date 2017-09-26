frappe.ui.form.on("Sales Invoice", "get_items", function(frm) {
	erpnext.utils.map_current_doc({
		method: "preorder.preorder.lemparan.get_items_tampungan",
		source_name: cur_frm.doc.sales_order+"|"+cur_frm.doc.percentage_dp+"|"+cur_frm.doc.inquiry,
	});
})
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
});
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
var calculate_dp = function(frm) {
    var dp = frm.doc.percentage_dp;
    var diskon = 100 - dp;
    frm.set_value("additional_discount_percentage", diskon);
    frm.set_value("discount_1", diskon);
}
frappe.ui.form.on("Sales Invoice", "total", function(frm) {
    calculate_dp(frm);
})
frappe.ui.form.on("Sales Invoice", "percentage_dp", function(frm) {
    calculate_dp(frm);
})
frappe.ui.form.on("Sales Invoice", "validate", function(frm) {
    calculate_dp(frm);
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
