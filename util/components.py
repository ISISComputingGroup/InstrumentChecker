import os
from util.configurations import ConfigurationUtils


class ComponentUtils(ConfigurationUtils):

    _BASE_COMPONENT = "_base"

    def get_configurations_directory(self):
        return os.path.join(self.config_repo_path, "configurations", "components")