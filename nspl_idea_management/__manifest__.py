{
    'name': 'Idea Management',
    'version': '19.0.1',
    'summary': 'Manage your POS users’ ideas efficiently',
    'description': """
    The Idea Management module enables users to propose ideas from the website, 
    while managers can evaluate, approve, or reject ideas based on feasibility.

    ✔ Users can submit ideas from the website  
    ✔ Admins or managers can approve or reject ideas  
    ✔ Notification emails are sent on approval/rejection  
    ✔ Rejected ideas include reasons for rejection  
    ✔ Automatically creates project tasks for approved ideas  
    ✔ Fully integrated with Odoo's mail and activity system  
    """,
    'category': 'Project',
    'sequence': 10,
    'author': 'Namah Softech Private Limited',
    'maintainer': 'Namah Softech Private Limited',
    'company': 'Namah Softech Private Limited',
    'website': 'https://www.namahsoftech.com',
    'support': 'support@namahsoftech.com',
    'price': 29.99,
    'currency': 'USD',
    'contributors': ['Shivani Solanki'],
    'license': 'AGPL-3',
    'depends': ['project', 'mail', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'data/idea_email_template.xml',
        'views/idea_category_view.xml',
        'views/idea_reject_wizard_view.xml',
        'views/idea_cancel_wizard_view.xml',
        'views/idea_view.xml',
        'views/idea_menu.xml',
    ],
    'images': ['static/description/img/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
