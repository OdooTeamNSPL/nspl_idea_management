from odoo import models, fields, api
from odoo.exceptions import UserError

class IdeaRejectWizard(models.TransientModel):
    _name = 'idea.reject.wizard'
    _description = 'Reject Idea Wizard'

    reason = fields.Text(string="Rejection Reason", required=True)

    def action_reject_idea(self):
        idea = self.env['idea.idea'].browse(self.env.context.get('active_id'))
        if idea.state not in ['pending', 'confirmed']:
            raise UserError("Only 'Pending' or 'Confirmed' ideas can be rejected.")

        idea.write({
            'state': 'rejected',
            'rejection_reason': self.reason,
        })

        template = self.env.ref('nspl_idea_management.email_template_idea_rejected', raise_if_not_found=False)
        if template:
            template.send_mail(idea.id, force_send=True)
