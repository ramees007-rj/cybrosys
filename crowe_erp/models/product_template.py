from odoo import fields, models, tools, api


class InheritProductTemplate(models.Model):
    _inherit = 'product.template'

    purchase_ok = fields.Boolean('Can be Purchased', default=False)
    detailed_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service')], string='Product Type', default='service',
        required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.')
    list_price = fields.Float(
        'Sales Price', default=0.0,
        digits='Product Price',
        help="Price at which the product is sold to customers.",
    )
    service_tracking = fields.Selection(
        selection=[
            ('no', 'Nothing'),
            ('task_global_project', 'Task'),
            ('task_in_project', 'Project & Task'),
            ('project_only', 'Project'),
        ],
        string="Create on Order", default="task_in_project", readonly=True,
        help="On Sales order confirmation, this product can generate a project and/or task. \
            From those, you can track the service you are selling.\n \
            'In sale order\'s project': Will use the sale order\'s configured project if defined or fallback to \
            creating a new project based on the selected template.")
