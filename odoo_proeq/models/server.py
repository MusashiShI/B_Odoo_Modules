from odoo import models, fields, api
import subprocess
import os
import logging

_logger = logging.getLogger(__name__)


def create_ssh_file(server_name, server_ip, server_type):
    """
    Função para criar um arquivo SSH no diretório /bin.
    """
    ssh_content = f"""# SSH Configuration for {server_name}
Host {server_name}
    HostName {server_ip}
    User {user}
"""
    file_path = f"/bin/{server_name}_server_ssh"
    try:
        with open(file_path, 'w') as ssh_file:
            ssh_file.write(ssh_content)
        os.chmod(file_path, 0o700)  # Define permissões seguras
        return file_path
    except Exception as e:
        _logger.error(f"Erro ao criar arquivo SSH para {server_name}: {e}")
        raise Exception(f"Erro ao criar arquivo SSH: {e}")


class ProeqServer(models.Model):
    _name = 'proeq.server'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Server'

    name = fields.Char(string="Name", required=True)
    state = fields.Selection(
        [('on', 'On'), ('off', 'Off'), ('problems', 'Problems')],
        string="State",
        default='off'
    )
    description = fields.Char(string="Description", required=True)
    ip = fields.Char(string="Ip", required=True)
    type = fields.Selection(
        [('odoo', 'Odoo'), ('vue', 'Vue'), ('database', 'DataBase'), ('locust', 'Locust')],
        string="Type"
    )
    odoo_version = fields.Selection(
        [('18.0', '18.0'), ('17.0', '17.0'), ('16.0', '16.0')],
        string="Odoo Version"
    )
    ubuntu_version = fields.Selection(
        [('24.04', '24.04'), ('22.04', '22.04')],
        string="Ubuntu Version"
    )
    user = fields.Char(string="User", required=True, default='ubuntu')

    @api.model_create_multi
    def create(self, vals_list):
        # Este método agora pode lidar com criação em lote
        records = super(ProeqServer, self).create(vals_list)
        for record in records:
            record._create_ssh_file()
        return records

    def write(self, vals):
        result = super(ProeqServer, self).write(vals)
        if 'ip' in vals or 'name' in vals or 'type' in vals:
            self._create_ssh_file()
        return result

    def _create_ssh_file(self):
        for record in self:
            try:
                file_path = create_ssh_file(record.name, record.ip, record.type)
                record.message_post(body=f"Arquivo SSH gerado: {file_path}")
                record.state = 'on'
            except Exception as e:
                record.state = 'problems'
                _logger.error(f"Erro ao criar arquivo SSH para {record.name}: {e}")
                raise Exception(f"Erro ao criar arquivo SSH: {e}")




class ProeqServer_Saas(models.Model):
    _name = 'proeq.saas.server'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Saas Server'

    name = fields.Char(string="Name", required=True)
    state = fields.Selection(
        [('on', 'On'), ('off', 'Off'), ('problems', 'Problems')],
        string="State",
        default='off'
    )
    description = fields.Char(string="Description", required=True)
    ip = fields.Char(string="Ip", required=False)  # O IP será preenchido automaticamente
    type = fields.Selection(
        [('odoo', 'Odoo'), ('vue', 'Vue'), ('database', 'DataBase'), ('locust', 'Locust')],
        string="Type"
    )
    odoo_version = fields.Selection(
        [('18.0', '18.0'), ('17.0', '17.0'), ('16.0', '16.0')],
        string="Odoo Version"
    )
    ubuntu_version = fields.Selection(
        [('24.04', '24.04'), ('22.04', '22.04')],
        string="Ubuntu Version"
    )
    user = fields.Char(string="User", required=True, default='ubuntu')

    @api.model
    def create(self, vals):
        record = super(ProeqServer_Saas, self).create(vals)
        record._deploy_odoo_server()  # Chama a função que vai fazer o deploy do Odoo
        return record

    def write(self, vals):
        result = super(ProeqServer_Saas, self).write(vals)
        if 'name' in vals or 'odoo_version' in vals:
            self._deploy_odoo_server()  # Se houver alterações no nome ou versão do Odoo, faz o deploy novamente
        return result

    def _deploy_odoo_server(self):
        for record in self:
            try:
                # Cria o comando para execução do deploy Odoo
                odoo_version = record.odoo_version or '16.0'  # Pega a versão do Odoo ou 16.0 por padrão
                server_name = record.name
                enterprise_flag = '-e' if 'enter' in record.description.lower() else ''  # Verifica se é enterprise
                # Define o comando de deploy
                deploy_command = f"odoo-deploy {enterprise_flag} -v {odoo_version} {server_name}"

                # Imprime as variáveis para debug
                _logger.info(f"Comando de deploy gerado: {deploy_command}")

                # Simula a execução do comando para testes
                # Abaixo simula uma execução bem-sucedida sem chamar o subprocess
                _logger.info("Simulação do comando de deploy. Não executando o comando real.")

                # Em um teste real, você poderia descomentar esta linha para realmente executar:
                # subprocess.run(deploy_command, shell=True, check=True)

                # Atualiza o estado do servidor para 'on' se tudo ocorrer bem
                record.state = 'on'

            except subprocess.CalledProcessError as e:
                record.state = 'problems'
                _logger.error(f"Erro ao executar o deploy do Odoo para {record.name}: {e}")
                raise Exception(f"Erro ao executar o deploy do Odoo: {e}")
            except Exception as e:
                record.state = 'problems'
                _logger.error(f"Erro geral: {e}")
                raise Exception(f"Erro: {e}")
