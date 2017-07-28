// Copyright (c) 2017, ridhosribumi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inquiry', {
	refresh: function(frm) {

	}
});
cur_frm.set_query("contact_person",  function (frm) {
		return {
        filters: [
            ['customer', '=', cur_frm.doc.customerben]
        ]
		}
});
