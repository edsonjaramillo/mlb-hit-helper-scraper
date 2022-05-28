from datetime import datetime
from os import path, makedirs, listdir, remove
import traceback


class Logger:
    start: str = ""
    exception: str = "No Exceptions were raised."
    end: str = ""

    def __init__(self):
        self._create_log_folder()

    def report_start(self) -> None:
        """Reports the start of the program."""
        self.start = f"Started at {self._today()}"

    def report_exception(self):
        """Reports an exception and its traceback."""
        self.exception = traceback.format_exc()

    def report_end(self) -> None:
        """Reports the end of the program."""
        self.end = f"Ended at {self._today()}"

    def make_report(self) -> None:
        """Makes the report."""
        with open(f"logs/{self._get_date_name()}.txt", "w") as f:
            f.write(self.start + "\n")
            f.write(self.exception + "\n")
            f.write(self.end)

        print("Report created.")

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
