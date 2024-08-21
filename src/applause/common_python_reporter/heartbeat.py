"""A background service for submitting heartbeat messages to the Applause Automation API.

This service keeps an Applause test run alive by sending heartbeat messages to the Applause Automation API.
If the heartbeat messages are not sent within a certain time frame, the test run will be marked with an Error.

Typical usage example:
    auto_api = AutoApi(config)
    test_run_id = auto_api.start_test_run(TestRunCreateDto(tests=["test1", "test2"])).run_id
    heartbeat_service = HeartbeatService(auto_api, test_run_id)
    heartbeat_service.start()

    ...Perform Actions on the Test Run...

    # End the heartbeat service when finished
    heartbeat_service.stop()

    # Make sure to end to end the test run when finished
    auto_api.end_test_run(test_run_id)

"""

from .auto_api import AutoApi
from apscheduler.schedulers.background import BackgroundScheduler


class HeartbeatService:
    """A background service for submitting heartbeat messages to the Applause Automation API.

    Attributes
    ----------
        auto_api (AutoApi): An instance of the AutoApi class.
        test_run_id (int): The id of the test run.
        job (apscheduler.job.Job): The job for the heartbeat service.
        sleep_time (float): The time to sleep between heartbeat messages.
        scheduler (apscheduler.schedulers.background.BackgroundScheduler): The scheduler for the heartbeat service.

    """

    def __init__(self, auto_api: AutoApi, test_run_id: int, sleep_time: float = 5):
        """Initialize the HeartbeatService object.

        Args:
        ----
            auto_api (AutoApi): An instance of the AutoApi class.
            test_run_id (int): The id of the test run.
            sleep_time (float): The time to sleep between heartbeat messages.

        """
        self.auto_api = auto_api
        self.test_run_id = test_run_id
        self.job = None
        self.sleep_time = sleep_time
        self.scheduler = BackgroundScheduler()

    def start(self):
        """Start the heartbeat service.

        Raises
        ------
            Exception: If the heartbeat service is already running.

        """
        if self.job is not None:
            raise Exception("Heartbeat worker - Already running")
        self.job = self.scheduler.add_job(lambda: self.auto_api.send_sdk_heartbeat(self.test_run_id), "interval", seconds=self.sleep_time)
        self.scheduler.start()
        pass

    def stop(self):
        """Stop the heartbeat service.

        Raises
        ------
            Exception: If the heartbeat service is not running.

        """
        if self.job is None:
            raise Exception("Heartbeat worker - Not running")
        self.scheduler.shutdown()
        self.job = None
        pass
