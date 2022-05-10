from datetime import datetime
from os import path, makedirs, listdir, remove
import traceback


class Logger:

    def __init__(self):
        self._create_log_folder()
        self._delete_previous_logs()

    def report_start(self) -> None:
        """Reports the start of the program."""
        date_name = self._get_date_name()
        with open(f"logs/{date_name}_begin.txt", "w+") as log_file:
            log_file.write(f"Started at {self._today()}")

    def report_exception(self):
        """Reports an exception and its traceback."""
        date_name = self._get_date_name()
        with open(f"logs/{date_name}_error.txt", "w+") as log_file:
            log_file.write(traceback.format_exc())

    def report_end(self) -> None:
        """Reports the end of the program."""
        date_name = self._get_date_name()
        with open(f"logs/{date_name}_end.txt", "w+") as log_file:
            log_file.write(f"Ended at {self._today()}")

    def _delete_previous_logs(self):
        """Deletes the previous logs."""
        for file in listdir("logs"):
            file_path = path.join("logs", file)
            remove(file_path)

    def _create_log_folder(self):
        """Creates the logs folder if it doesn't exist."""
        if not path.exists("logs"):
            makedirs("logs")

    def _get_date_name(self):
        """Returns the date name for the log file."""
        return datetime.today().strftime('%m_%d_%Y')

    def _today(self) -> str:
        """Returns the current date."""
        return datetime.today().strftime('%b %d, %Y at %r')
