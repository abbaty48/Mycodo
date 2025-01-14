# coding=utf-8
import subprocess

from flask_babel import lazy_gettext
from mycodo.config_translations import TRANSLATIONS
from mycodo.config import INSTALL_DIRECTORY
from mycodo.databases.models import Actions
from mycodo.function_actions.base_function_action import AbstractFunctionAction
from mycodo.utils.database import db_retrieve_table_daemon

FUNCTION_ACTION_INFORMATION = {
    'name_unique': 'system_restart',
    'name': f"{TRANSLATIONS['system']['title']}: {lazy_gettext('Restart')}",
    'library': None,
    'manufacturer': 'Mycodo',

    'url_manufacturer': None,
    'url_datasheet': None,
    'url_product_purchase': None,
    'url_additional': None,

    'message': 'Restart the System',

    'usage': 'Executing <strong>self.run_action("{ACTION_ID}")</strong> will restart the system in 10 seconds.',

    'dependencies_module': [],

    'custom_options': [

    ]
}


class ActionModule(AbstractFunctionAction):
    """Function Action: System Restart"""
    def __init__(self, action_dev, testing=False):
        super(ActionModule, self).__init__(action_dev, testing=testing, name=__name__)

        self.none = None

        action = db_retrieve_table_daemon(
            Actions, unique_id=self.unique_id)
        self.setup_custom_options(
            FUNCTION_ACTION_INFORMATION['custom_options'], action)

        if not testing:
            self.setup_action()

    def setup_action(self):
        self.action_setup = True

    def run_action(self, message, dict_vars):
        message += " System restarting in 10 seconds."
        cmd = f'{INSTALL_DIRECTORY}/mycodo/scripts/mycodo_wrapper restart 2>&1'
        subprocess.Popen(cmd, shell=True)

        self.logger.debug(f"Message: {message}")

        return message

    def is_setup(self):
        return self.action_setup
