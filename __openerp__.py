{
    'name': "Product Cost Price from suppliers auto",
    'version': '9.0.1.1',
    'depends': ['account'],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Sales',
    'description': 
    """
Auto sets the cost price on products from the supplier pricelists (takes the price for the first supplier, lowest sequence).

Or allow to set it manually

This module has been developed by Valentin THIRION @ AbAKUS it-solution.
    """,
    'data': [
        'views/product_template.xml',
    ],
}