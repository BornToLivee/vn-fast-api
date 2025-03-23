import logging
import watchtower
import boto3

class CloudWatchLogger:
    def __init__(self, log_group: str, stream_name: str, region_name: str = "eu-north-1"):
        """
        Initialization of the logger for CloudWatch.

        :param log_group: Name of the log group in AWS CloudWatch.
        :param stream_name: Name of the log stream in CloudWatch.
        :param region_name: AWS region, default is "us-east-1".
        """
        self.log_group = log_group
        self.stream_name = stream_name
        self.region_name = region_name
        self.logger = logging.getLogger("cloudwatch_logger")

        self.session = boto3.Session(region_name=self.region_name)

        self.cloudwatch_handler = watchtower.CloudWatchLogHandler(
            log_group=self.log_group,
            stream_name=self.stream_name,
            boto3_client=self.session.client("logs",region_name=self.region_name)
        )

        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.cloudwatch_handler.setFormatter(formatter)

        self.logger.addHandler(self.cloudwatch_handler)

    def log(self, level: str, message: str):
        """
        Logging messages with a dynamic level.

        :param level: Logging level (e.g., "DEBUG", "INFO", "ERROR").
        :param message: Message to log.
        """
        log_level = getattr(self.logger, level.lower(), None)
        if log_level:
            log_level(message)
        else:
            self.logger.error(f"Unknown log level: {level}, message: {message}")

    def log_exception(self, message: str, exception: Exception):
        """Logging exceptions with stack trace."""
        self.logger.exception(f"{message}: {exception}")
    

logger = CloudWatchLogger(
    log_group="vn-fast-api-logs",
    stream_name="local-log-stream",
    region_name="eu-north-1"
)