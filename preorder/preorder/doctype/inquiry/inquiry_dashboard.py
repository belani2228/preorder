from frappe import _

def get_data():
	return {
		'fieldname': 'inquiry',
		'transactions': [
			{
				'label': _('Related Document'),
				'items': ['Request for Supplier Quotation', 'Supplier Quotation', 'Quotation']
			},
		]
    }
