from odoo import fields, models

class PinterestProductFeedConfig(models.Model):
    _name = 'pinterest.product.feed.config'
    _description = 'Pinterest Product Feed Config'

    name = fields.Char(string='Naam', required=True)
    website_id = fields.Many2one(
        'website', 
        string='Website', 
        required=True,
        help="Website waarvoor de feed geldt."
    )
    active = fields.Boolean(default=True, string='Actief')
    feed_token = fields.Char(
        string='Feed Token', 
        help="Token om de feed te beveiligen."
    )
