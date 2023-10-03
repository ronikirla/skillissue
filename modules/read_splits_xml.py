import xml.etree.ElementTree as ET
from datetime import datetime as dt
import re
from modules.split import Split

class SplitsXML():
    DEFAULT_DT = dt.strptime("0:0:0.00", "%H:%M:%S.%f")
    
    def __init__(self, args):
        self.__args = args
        self.__tree = ET.parse(args.filename)

    def read_finished_runs(self):
        """Read finished run times from splits file into an array"""
        root = self.__tree.getroot()
        attempts = []
        missing = 0
        nof_attempts = 0
        for attempt in root.find("AttemptHistory").findall("Attempt"):
            nof_attempts += 1
            realtime = attempt.find("RealTime")
            if realtime != None:
                text = re.search("[^.]*...", realtime.text).group()
                t = dt.strptime(text, "%H:%M:%S.%f")
                attempts.append((t - self.DEFAULT_DT).total_seconds())
                continue
            missing += 1
            if not self.__args.drop_missing:
                started = dt.strptime(attempt.attrib["started"], "%m/%d/%Y %H:%M:%S")
                ended = dt.strptime(attempt.attrib["ended"], "%m/%d/%Y %H:%M:%S")
                attempt_time = ended - started
                if attempt_time.seconds > self.__args.remake_window:
                    attempts.append(float("inf"))
                else:
                    # Undo the added missing time in case run was shorter than remake_window
                    missing -= 1
        return Split(attempts, nof_attempts, missing)