# initialize
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")
django.setup()

from dvadmin.system.views.user import UsersInitSerializer
from dvadmin.system.views.menu import MenuInitSerializer
from dvadmin.utils.core_initialize import CoreInitialize
from dvadmin.system.views.role import RoleInitSerializer
from dvadmin.system.views.api_white_list import ApiWhiteListInitSerializer
from dvadmin.system.views.dept import DeptInitSerializer
from dvadmin.system.views.dictionary import DictionaryInitSerializer
from dvadmin.system.views.system_config import SystemConfigInitSerializer


class Initialize(CoreInitialize):
    def init_dept(self):
        """
        initialize department information
        """
        self.init_base(DeptInitSerializer, unique_fields=["name", "parent", "key"])

    def init_role(self):
        """
        initialize role information
        """
        self.init_base(RoleInitSerializer, unique_fields=["key"])

    def init_users(self):
        """
        initialize users information
        """
        self.init_base(UsersInitSerializer, unique_fields=["username"])

    def init_menu(self):
        """
        initialize menu information
        """
        self.init_base(
            MenuInitSerializer,
            unique_fields=["name", "web_path", "component", "component_name"],
        )

    def init_api_white_list(self):
        """ """
        self.init_base(
            ApiWhiteListInitSerializer,
            unique_fields=[
                "url",
                "method",
            ],
        )

    def init_dictionary(self):
        """ """
        self.init_base(
            DictionaryInitSerializer,
            unique_fields=[
                "value",
                "parent",
            ],
        )

    def init_system_config(self):
        """ """
        self.init_base(
            SystemConfigInitSerializer,
            unique_fields=[
                "key",
                "parent",
            ],
        )

    def run(self):
        self.init_dept()
        self.init_role()
        self.init_users()
        self.init_menu()
        self.init_api_white_list()
        self.init_dictionary()
        self.init_system_config()


if __name__ == "__main__":
    Initialize(app="dvadmin.system").run()
