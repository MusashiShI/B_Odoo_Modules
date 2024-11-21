from odoo import api, fields, models




class ProeqServer(models.Model):
    _name = 'proeq.server'
    _description = 'Server'

    # name, state, description, ip, type ( ODOO, VUE, DATABASE )

    name = fields.Char(string="Name",  required=True)
    state = fields.Boolean(string="State", readonly = True)
    # Para analisar o state usa ping, caso esteja down usa wget para ter mais informações
    description =  fields.Char(string="Description",  required=True)
    ip = fields.Char(string="Ip",  required=True)
    type = fields.Selection([('odoo','Odoo'), ('vue','Vue'),('database','DataBase')], string="type")




