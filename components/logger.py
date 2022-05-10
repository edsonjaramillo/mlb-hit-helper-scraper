from datetime import datetime
from os import name, path, makedirs
import traceback


class Logger:

    def report_exception(self, exception: Exception):
        self._create_log_folder()
        date_name = self._get_date_name()
        with open(f"logs/{date_name}.txt", "w+") as log_file:
            log_file.write(traceback.format_exc())

    def _create_log_folder(self):
        if not path.exists("logs"):
            makedirs("logs")

    def _get_date_name(self):
        if name == "nt":
            return datetime.today().strftime('%m_%d_%Y').upper()
        else:
            return datetime.today().strftime('%m_%d_%Y').upper()
