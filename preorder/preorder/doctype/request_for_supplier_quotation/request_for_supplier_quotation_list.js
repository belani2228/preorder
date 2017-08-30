frappe.listview_settings['Request for Supplier Quotation'] = {
	add_fields: ["supplier_name", "status",	"company"],
	get_indicator: function(doc) {
		if(doc.status==="Submitted") {
			return [__("Submitted"), "blue", "status,=,Submitted"];
		} else if(doc.status==="Completed") {
			return [__("Completed"), "green", "status,=,Completed"];
		} else if(doc.status==="Lost") {
			return [__("Lost"), "darkgrey", "status,=,Lost"];
		}
	}
};
