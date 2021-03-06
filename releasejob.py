#!/usr/bin/env python3
# Job monitor for GitLab CI
# Licensed under MIT.
# https://github.com/dehesselle/gljobmon

import os
import datetime
from common import IniFile
import jobmon
import argparse
import errno


def get_ref():
    parser = argparse.ArgumentParser(description="get unreleased job_id")
    parser.add_argument('ref', metavar='ref', type=str, nargs='1',
                        help='git ref to select job_id from')
    args = parser.parse_args()
    return args.ref


class ReleaseLog(IniFile.IniFile):
    def __init__(self, filename=""):
        if os.path.exists(filename):
            IniFile.IniFile.__init__(self, filename)
        else:
            filename = os.getenv("HOME") + "/releases.log"
            if os.path.exists(filename):
                IniFile.IniFile.__init__(self, filename)
            else:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)


def main():
    if "PYCHARM_HOSTED" in os.environ:   # this is for testing only
        ref = "master"
    else:
        ref = get_ref()

    gitlab = IniFile.GitlabIni()
    releases = ReleaseLog()

    project = jobmon.get_project(gitlab.project_id, gitlab.server, gitlab.token)
    break_loop = False
    unreleased_job_found = False

    for pipeline in project.pipelines.list():
        for job in pipeline.jobs.list():
            if job.name == gitlab["jobmon"]["ci_job"] and pipeline.ref == ref:
                if job.status == "success":
                    if str(job.id) in releases:
                        break_loop = True
                        unreleased_job_found = False
                        break
                    else:
                        break_loop = True
                        unreleased_job_found = True
                        break
        if break_loop:
            break

    if unreleased_job_found:
        job_id = str(job.id)
        releases[job_id] = {}
        releases[job_id]["this_created"] = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        releases[job_id]["web_url"] = job.web_url
        releases[job_id]["created_at"] = job.created_at
        releases[job_id]["started_at"] = job.started_at
        releases[job_id]["finished_at"] = job.finished_at
        releases[job_id]["ref"] = pipeline.ref
        releases[job_id]["short_id"] = job.commit["short_id"]
        print(job_id)
    else:
        print(0)


if __name__ == '__main__':
    main()
