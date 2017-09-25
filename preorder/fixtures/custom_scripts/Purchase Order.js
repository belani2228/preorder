frappe.ui.form.on("Purchase Order", "validate", function(frm) {
	$.each(frm.doc.items, function(i, d) {
		if(d.amount == '0'){
			msgprint("Item No."+d.idx+", amount still empty");
			validated = false;
		}
	})
})
