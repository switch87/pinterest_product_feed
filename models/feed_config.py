
from odoo import fields, models

class ProductFeedConfig(models.Model):
    _name = 'product.feed.config'
    _description = 'Product Feed Config'

    name = fields.Char(string='Name', required=True)
    feed_type = fields.Selection(
        [
            ('facebook', 'Facebook'),
            ('google', 'Google'),
            ('pinterest', 'Pinterest')
        ],
        string='Feed Type',
        required=True,
        help="The platform for which the product feed is configured."
    )
    website_id = fields.Many2one(
        'website',
        string='Website',
        required=True,
        help="Website for which the feed applies."
    )
    active = fields.Boolean(default=True, string='Active')
    feed_token = fields.Char(
        string='Feed Token',
        help="Token used to authenticate feed requests."
    )
    last_sync_date = fields.Datetime(
        string='Last Sync Date',
        help="The last date when the feed was synchronized."
    )
