from odoo import api, fields, models




class ProeqServer(models.Model):
    _name = 'proeq.server'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Server'

    # name, state, description, ip, type ( ODOO, VUE, DATABASE )

    name = fields.Char(string="Name",  required=True)
    state = fields.Selection([('on','On'), ('off','Off'),('problems','Problems')], string="State")
    # Para analisar o state usa ping, caso esteja down usa wget para ter mais informações
    description =  fields.Char(string="Description",  required=True)
    ip = fields.Char(string="Ip",  required=True)
    type = fields.Selection([('odoo','Odoo'), ('vue','Vue'),('database','DataBase'),('locust','Locust')], string="type")
    version = fields.Selection([('18.0', '18.0'), ('17.0', '17.0'), ('16.0', '16.0')],string="version")




