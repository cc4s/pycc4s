"""Functions to run cc4s."""
import shlex
from os.path import expandvars

from custodian import Custodian

from pycc4s.custodian.jobs import CC4SJob

_DEFAULT_HANDLERS = ()
_DEFAULT_VALIDATORS = ()


def run_cc4s(
    cc4s_cmd,
    handlers=_DEFAULT_HANDLERS,
    validators=_DEFAULT_VALIDATORS,
    max_errors=5,
    scratch_dir=None,
    cc4s_job_kwargs=None,
    custodian_kwargs=None,
):
    """Run cc4s."""
    cc4s_cmd = expandvars(cc4s_cmd)
    split_cc4s_cmd = shlex.split(cc4s_cmd)
    jobs = [CC4SJob(split_cc4s_cmd, **cc4s_job_kwargs)]

    c = Custodian(
        handlers,
        jobs,
        validators=validators,
        max_errors=max_errors,
        scratch_dir=scratch_dir,
        **custodian_kwargs,
    )
    c.run()
