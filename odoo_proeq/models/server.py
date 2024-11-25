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
    User {server_type}
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

    @api.model
    def create(self, vals):
        record = super(ProeqServer, self).create(vals)
        record._create_ssh_file()
        return record

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





def create_inventory_file(server_name, server_ip):
    """
    Função para criar um inventário temporário para o Ansible.
    """
    inventory_content = f"""
[all]
{server_ip} ansible_ssh_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_ed25519.pub
"""
    inventory_path = f"/tmp/{server_name}_inventory.ini"
    try:
        with open(inventory_path, 'w') as inventory_file:
            inventory_file.write(inventory_content)
        return inventory_path
    except Exception as e:
        _logger.error(f"Erro ao criar inventário para {server_name}: {e}")
        raise Exception(f"Erro ao criar inventário: {e}")

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

    @api.model
    def create(self, vals):
        record = super(ProeqServer_Saas, self).create(vals)
        record._run_ansible_playbook()
        return record

    def write(self, vals):
        result = super(ProeqServer_Saas, self).write(vals)
        if 'ip' in vals or 'name' in vals or 'type' in vals:
            self._run_ansible_playbook()
        return result

    def _run_ansible_playbook(self):
        for record in self:
            try:
                # Criação do inventário dinâmico
                inventory_path = create_inventory_file(record.name, record.ip)

                # Caminho do playbook
                playbook_path = '~/playbook.yml '  # Atualize para o caminho real

                # Comando do Ansible
                command = [
                    'ansible-playbook',
                    '-i', inventory_path,
                    playbook_path,
                    '--extra-vars',
                    f"server_name={record.name} server_ip={record.ip} server_type={record.type}"
                ]

                # Executa o playbook
                _logger.info(f"Executando playbook Ansible para o servidor: {record.name}")
                subprocess.run(command, check=True)

                # Atualiza o estado do servidor
                record.state = 'on'

                # Remove o inventário temporário
                os.remove(inventory_path)

            except subprocess.CalledProcessError as e:
                record.state = 'problems'
                _logger.error(f"Erro ao executar playbook Ansible para {record.name}: {e}")
                raise Exception(f"Erro ao executar playbook Ansible: {e}")
            except Exception as e:
                record.state = 'problems'
                _logger.error(f"Erro geral: {e}")
                raise Exception(f"Erro: {e}")
