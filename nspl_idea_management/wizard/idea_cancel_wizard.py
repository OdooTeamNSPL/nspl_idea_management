from odoo import models, fields, api
from odoo.exceptions import UserError


class IdeaCancelWizard(models.TransientModel):
    _name = 'idea.cancel.wizard'
    _description = 'Cancel Idea Wizard'

    reason = fields.Text(string="Cancellation Reason", required=True)

    def action_cancel_idea(self):
        idea = self.env['idea.idea'].browse(self.env.context.get('active_id'))
        if idea.state in ['approved', 'cancelled']:
            raise UserError("You cannot cancel an approved or already cancelled idea.")

        idea.write({
            'state': 'cancelled',
            'cancellation_reason': self.reason,
        })

        template = self.env.ref('nspl_idea_management.email_template_idea_cancelled', raise_if_not_found=False)
        if template:
            template.send_mail(idea.id, force_send=True)
