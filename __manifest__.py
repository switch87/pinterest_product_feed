
{
    'name': 'Snakebyte E-Commerce Product Feed',
    'version': '1.0',
    'summary': 'Unified management for Facebook, Google, and Pinterest product feeds',
    'author': 'Gert Pellin',
    'category': 'Website',
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'views/feed_config_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
