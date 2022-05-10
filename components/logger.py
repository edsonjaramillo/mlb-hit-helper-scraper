from datetime import datetime
from os import name, path, makedirs
import traceback


class Logger:

    def report_start(self) -> None:
        """Reports the start of the program."""
        self._create_log_folder()
        date_name = self._get_date_name()
        with open(f"logs/{date_name}_begin.txt", "w+") as log_file:
            log_file.write(f"Started at {datetime.today()}")

    def report_exception(self, exception: Exception):
        """Reports an exception and its traceback."""
        self._create_log_folder()
        date_name = self._get_date_name()
        with open(f"logs/{date_name}_error.txt", "w+") as log_file:
            log_file.write(traceback.format_exc())

    def _create_log_folder(self):
        """Creates the logs folder if it doesn't exist."""
        if not path.exists("logs"):
            makedirs("logs")

    def _get_date_name(self):
        """Returns the date name for the log file."""
        if name == "nt":
            return datetime.today().strftime('%m_%d_%Y')
        else:
            return datetime.today().strftime('%m_%d_%Y')
