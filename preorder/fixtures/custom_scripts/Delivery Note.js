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
    frm.set_value("discount_1_amount", diskon1_amount);
    frm.set_value("amount_after_discount_1", amount_after1);
    frm.set_value("discount_2_amount", diskon2_amount);
    frm.set_value("amount_after_discount_2", amount_after2);
    frm.set_value("discount_3_amount", diskon3_amount);
    frm.set_value("amount_after_discount_3", amount_after3);
    frm.set_value("additional_discount_percentage", total_diskon);
    frm.set_value("total_discount_percentage", total_diskon);
    var aa = (total_diskon/100) * frm.doc.total;
    frm.set_value("total_discount_amount", aa);
}
frappe.ui.form.on("Delivery Note", "discount_1", function(frm) {
    calculate_multilevel_discount(frm);
})
frappe.ui.form.on("Delivery Note", "discount_2", function(frm) {
    calculate_multilevel_discount(frm);
})
frappe.ui.form.on("Delivery Note", "discount_3", function(frm) {
    calculate_multilevel_discount(frm);
})
frappe.ui.form.on("Delivery Note", "net_total", function(frm) {
    calculate_multilevel_discount(frm);
})
frappe.ui.form.on("Delivery Note", "validate", function(frm) {
    calculate_multilevel_discount(frm);
    beda_diskon_amount(frm);
})
var beda_diskon_amount = function(frm){
    var total_diskon_persen = frm.doc.total_discount_percentage;
    var total_diskon_amount = (total_diskon_persen/100) * frm.doc.total;
    if(total_diskon_amount != frm.doc.total_discount_amount){
	frm.set_value("total_discount_percentage", "0");
	frm.set_value("discount_amount", frm.doc.total_discount_amount);
    }
}
frappe.ui.form.on("Delivery Note", "total_discount_amount", function(frm) {
    beda_diskon_amount(frm);
})
