from odoo import api, fields, models




class ProeqServer(models.Model):
    _name = 'proeq.server'
    _description = 'Server'

    # name, state, description, ip,

    name = fields.Char(string="Name",  required=True)
    state = fields.boolean(string="State", required = True,  readonly = True)
    description =  fields.Char(string="Description",  required=True)
    ip = fields.Char(string="Ip",  required=True)
    # Para analisar o state usa ping, caso esteja down usa wget para ter mais informações



