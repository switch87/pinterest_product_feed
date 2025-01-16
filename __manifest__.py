{
    'name': 'Pinterest Product Feed',
    'version': '15.0.1.0.0',
    'category': 'Website',
    'summary': 'Genereer een productfeed voor Pinterest Catalogs.',
    'author': 'Jouw Naam',
    'website': 'https://www.jouw-bedrijf.nl',
    'license': 'LGPL-3',
    'depends': ['website', 'sale', 'product_brand'],
    'data': [
        'security/ir.model.access.csv',
        'views/feed_config_view.xml',
    ],
    'installable': True,
    'application': False,
}
