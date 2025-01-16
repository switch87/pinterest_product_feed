import csv
import io
from odoo import http
from odoo.http import request, Response
from urllib.parse import quote

class PinterestProductFeedController(http.Controller):

    @http.route(['/pinterest_feed/<int:website_id>'], type='http', auth='public', website=True)
    def pinterest_product_feed(self, website_id, **kwargs):
        """
        CSV-feed voor Pinterest Catalogs.
        URL: /pinterest_feed/<website_id>?token=<je_token>
        """
        # 1. Ophalen van de feedconfig
        feed_config = request.env['pinterest.product.feed.config'].sudo().search([
            ('website_id', '=', website_id),
            ('active', '=', True),
        ], limit=1)

        if not feed_config:
            return "Geen actieve Pinterest-feedconfig gevonden voor deze website.", 404

        # 2. Token-check
        token = kwargs.get('token')
        if feed_config.feed_token and feed_config.feed_token != token:
            return "Ongeldige token of geen toegang tot deze feed.", 403

        # 3. Producten ophalen
        products = request.env['product.product'].sudo().search([
            ('sale_ok', '=', True),
            ('product_tmpl_id.website_published', '=', True),
            ('product_tmpl_id.website_id', '=', website_id)
        ])

        # 4. CSV genereren
        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Pinterest-velden (gebaseerd op je voorbeeld)
        header = [
            'id', 'item_group_id', 'title', 'description', 'link',
            'image_link', 'price', 'availability', 'condition',
            'additional_image_link', 'brand', 'size', 'custom_label_0'
        ]
        writer.writerow(header)

        for product in products:
            product_id = product.id
            item_group_id = product.product_tmpl_id.id
            title = product.product_tmpl_id.name
            description = product.product_tmpl_id.description_sale or ''
            link = f'{product.product_tmpl_id.website_id.domain}/shop/product/{product_id}'
            image_link = f'{product.product_tmpl_id.website_id.domain}/web/image/product.product/{product_id}/image_1920'
            price = f"{round(product.lst_price, 2):.2f} USD"
            availability = 'in stock' if product.qty_available > 0 else 'out of stock'
            condition = 'new'

            # Extra afbeeldingen ophalen
            additional_images = request.env['product.image'].sudo().search([
                ('product_tmpl_id', '=', product.product_tmpl_id.id)
            ])
            additional_image_link = ','.join([
                f'{product.product_tmpl_id.website_id.domain}/web/image/product.image/{img.id}/image_1920'
                for img in additional_images
            ])

            # Optionele velden
            brand = product.product_tmpl_id.product_brand_id.name if product.product_tmpl_id.product_brand_id else ''
            size = ', '.join([value.name for value in product.product_template_attribute_value_ids if value.attribute_id.name.lower() == 'size'])
            custom_label_0 = 'Bestseller'

            writer.writerow([
                product_id, item_group_id, title, description, link,
                image_link, price, availability, condition,
                additional_image_link, brand, size, custom_label_0
            ])

        csv_data = output.getvalue()
        output.close()

        return Response(
            csv_data,
            headers=[
                ('Content-Disposition', 'attachment; filename="pinterest_product_feed.csv"'),
                ('Content-Type', 'text/csv; charset=utf-8')
            ],
            status=200
        )
