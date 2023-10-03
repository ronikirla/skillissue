import xml.etree.ElementTree as ET
from datetime import datetime as dt
import re
from modules.split import Split

class AttemptProgress():
    """Keeps track of the time sum and split idx of each attempt in order to know when the latest split was
    to know how soon after a split a reset occurred and which split it was on."""
    def __init__(self):
        self.accuml_time = 0 # Time at last finished split
        self.split_idx = -1 # Index of last finished split

class SplitsXML():
    DEFAULT_DT = dt.strptime("0:0:0.00", "%H:%M:%S.%f")

    def __init__(self, args):
        self.__args = args
        self.__tree = ET.parse(args.filename)

    def read_finished_runs(self):
        """Read finished run times from splits file into a split object."""
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
            started = dt.strptime(attempt.attrib["started"], "%m/%d/%Y %H:%M:%S")
            ended = dt.strptime(attempt.attrib["ended"], "%m/%d/%Y %H:%M:%S")
            attempt_time = ended - started
            if attempt_time.seconds > self.__args.remake_window:
                missing += 1
                if not self.__args.drop_missing:
                    attempts.append(float("inf"))
        return Split(attempts, nof_attempts, missing)
    
    def read_all_splits(self):
        """Read all splits individually from splits file into an array of split objects."""
        splits = []
        root = self.__tree.getroot()
        attempt_progresses = {}
        for split_idx, segment in enumerate(root.find("Segments").findall("Segment")):
            attempts = []
            missing = 0
            nof_attempts = 0
            name = f"{split_idx + 1}. {segment.find('Name').text}"
            for attempt in root.find("AttemptHistory").findall("Attempt"):
                nof_attempts += 1
                attempt_id = attempt.attrib["id"]
                if not attempt_id in attempt_progresses:
                    attempt_progresses[attempt_id] = AttemptProgress()
                attempt_progress = attempt_progresses[attempt_id]
                time = segment.find("SegmentHistory").find(f".//Time[@id='{attempt_id}']")
                if time == None:
                    # If this time is missing and the previous one was present then count it as a reset.
                    if attempt_progress.split_idx == split_idx - 1:
                        started = dt.strptime(attempt.attrib["started"], "%m/%d/%Y %H:%M:%S")
                        ended = dt.strptime(attempt.attrib["ended"], "%m/%d/%Y %H:%M:%S")
                        attempt_time = ended - started
                        split_time = attempt_time.seconds - attempt_progress.accuml_time
                        if split_time > self.__args.remake_window:
                            missing += 1
                            if not self.__args.drop_missing:
                                attempts.append(float("inf"))
                    continue
                realtime = time.find("RealTime")
                if realtime != None:
                    text = re.search("[^.]*...", realtime.text).group()
                    t = dt.strptime(text, "%H:%M:%S.%f")
                    seconds = (t - self.DEFAULT_DT).total_seconds()
                    attempts.append(seconds)
                    attempt_progress.accuml_time = seconds
                    attempt_progress.split_idx = split_idx

            splits.append(Split(attempts, nof_attempts, missing, name))
        
        return splits