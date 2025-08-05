from odoo import models, fields

class IdeaCategory(models.Model):
    _name = 'idea.category'
    _description = 'Idea Category'

    name = fields.Char(string="Category Name", required=True)
    responsible_ids = fields.Many2many(
        'res.partner',
        'idea_category_responsible_partner_rel',
        'category_id',
        'partner_id',
        string="Responsible Members"
    )
