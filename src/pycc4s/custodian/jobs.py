"""Jobs for cc4s."""
import subprocess

from custodian.custodian import Job

INPUT_FILE_NAME = "cc4s.in"
OUTPUT_FILE_NAME = "cc4s.out.yaml"
LOG_FILE_NAME = "cc4s.log"
STDOUT_FILE_NAME = "cc4s.stdout"
STDERR_FILE_NAME = "cc4s.stderr"


class CC4SJob(Job):
    """Basic job for cc4s."""

    def __init__(
        self,
        cc4s_cmd,
        input_file=INPUT_FILE_NAME,
        output_file=OUTPUT_FILE_NAME,
        log_file=LOG_FILE_NAME,
        stdout_file=STDOUT_FILE_NAME,
        stderr_file=STDERR_FILE_NAME,
        dryrun_nranks=None,
    ):
        """Construct custodian CC4SJob."""
        self.cc4s_cmd = cc4s_cmd
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file
        self.stdout_file = stdout_file
        self.stderr_file = stderr_file
        self.dryrun_nranks = dryrun_nranks

    def setup(self):
        """Initial setup for CC4SJob."""

    def run(self):
        """Perform the actual cc4s run."""
        cmd = list(self.cc4s_cmd)
        cmd.extend(["-i", self.input_file])
        cmd.extend(["-o", self.output_file])
        cmd.extend(["-l", self.log_file])
        if self.dryrun_nranks is not None:
            cmd.extend(["-d", self.dryrun_nranks])
        with open(self.stdout_file, "w") as f_std, open(
            self.stderr_file, "w", buffering=1
        ) as f_err:
            # use line buffering for stderr
            p = subprocess.Popen(cmd, stdout=f_std, stderr=f_err)
        return p

    def postprocess(self):
        """Post-processing of CC4SJob."""
