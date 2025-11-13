from odoo import models, fields, api
from odoo.exceptions import UserError


class Idea(models.Model):
    _name = 'idea.idea'
    _description = 'User Idea'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Subject", required=True)
    idea_manager_id = fields.Many2one('res.users', string="Idea Manager")
    member_ids = fields.Many2many('res.users', 'idea_user_rel', 'idea_id', 'user_id', string="Other Members")
    suggested_by_id = fields.Many2one('res.users', string="Suggested By", default=lambda self: self.env.user)

    responsible_ids = fields.Many2many(
        'res.partner',
        'idea_responsible_partner_rel',
        'idea_id',
        'partner_id',
        string="Responsible Members"
    )
    created_by_id = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user, readonly=True)

    description = fields.Text(string="Description")

    category_id = fields.Many2one('idea.category', string="Category")
    project_id = fields.Many2one('project.project', string="Related Project")
    rating = fields.Selection([
        ('1', '★☆☆☆☆'), ('2', '★★☆☆☆'), ('3', '★★★☆☆'), ('4', '★★★★☆'), ('5', '★★★★★'),
    ], string="Rating")

    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ], string="Status", default='new', tracking=True)

    cancellation_reason = fields.Text(string="Cancellation Reason", readonly=True)
    rejection_reason = fields.Text(string="Rejection Reason", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['created_by_id'] = self.env.uid
        return super().create(vals_list)

    def action_request_confirmation(self):
        for rec in self:
            if rec.state != 'new':
                raise UserError("Only ideas in 'New' state can be requested for confirmation.")
            rec.state = 'confirmed'
            # Send email to Idea Manager
            template = self.env.ref('nspl_idea_management.email_template_idea_request_confirmation',
                                    raise_if_not_found=False)
            if template and rec.idea_manager_id:
                template.send_mail(rec.id, force_send=True)



    def action_approve(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError("Only confirmed ideas can be approved.")
            rec.state = 'approved'


            if rec.project_id:
                self.env['project.task'].create({
                    'name': f'Idea: {rec.name}',
                    'project_id': rec.project_id.id,
                    'user_ids': [(6, 0, rec.member_ids.ids)],
                    'description': rec.description or '',
                })

            # Send email
            template = self.env.ref('nspl_idea_management.email_template_idea_approved', raise_if_not_found=False)
            if template:
                template.send_mail(rec.id, force_send=True)
