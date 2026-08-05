"""
Global Dashboard State
"""

from datetime import datetime


class DashboardState:

    def __init__(self):
        self.reset()

    # =====================================================
    # RESET
    # =====================================================

    def set_report(self, report):

        self.report = report
        
    #================================================
    
    def reset(self):

        self.target = ""
        self.profile = "FULL"
        self.report = "Not Generated"

        self.start_time = datetime.now()
        self.started = self.start_time.strftime("%H:%M:%S")
        self.elapsed = "00:00:00"

        self.progress = 0
        self.finished = False

        self.current_stage = "Idle"

        self.pipeline = [

            {"name": "Recon", "status": "pending"},

            {"name": "Enumeration", "status": "pending"},

            {"name": "Fingerprinting", "status": "pending"},

            {"name": "Vulnerability Detection", "status": "pending"},

            {"name": "CVE Mapping", "status": "pending"},

            {"name": "Risk Analysis", "status": "pending"},

            {"name": "Report", "status": "pending"},
        ]

        self.findings = {

            "Open Ports": 0,

            "Technologies": 0,

            "CVEs": 0,

            "Secrets": 0,

            "Directories": 0,

        }

        self.services = []

        self.events = []

        self.threat = {

            "Critical": 0,

            "High": 0,

            "Medium": 0,

            "Low": 0,

        }

    # =====================================================
    # TIMER
    # =====================================================

    def update_elapsed(self):

        self.elapsed = str(
            datetime.now() - self.start_time
        ).split(".")[0]

    # =====================================================
    # PROGRESS
    # =====================================================

    def set_progress(self, value):

        self.progress = max(
            0,
            min(100, int(value))
        )

    # =====================================================
    # PIPELINE
    # =====================================================

    def set_stage_running(self, stage):

        self.current_stage = stage

        for item in self.pipeline:

            if item["name"] == stage:

                item["status"] = "running"
                break

    def complete_stage(self, stage):

        self.current_stage = stage

        for item in self.pipeline:

            if item["name"] == stage:

                item["status"] = "done"
                break

    # =====================================================
    # EVENTS
    # =====================================================

    def add_event(self, message):

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.events.append(
            f"[{timestamp}] {message}"
        )

        self.events = self.events[-8:]

    # =====================================================
    # SERVICES
    # =====================================================

    def add_service(self, service):

        if service not in self.services:

            self.services.append(service)

    # =====================================================
    # FINDINGS
    # =====================================================

    def set_finding(self, key, value):

        self.findings[key] = value

    # =====================================================
    # THREATS
    # =====================================================

    def set_threat(self, level, value):

        if level in self.threat:

            self.threat[level] = value

    # =====================================================
    # FINISH
    # =====================================================

    def finish(self):

        self.progress = 100

        self.finished = True

        self.current_stage = "Completed"


state = DashboardState()