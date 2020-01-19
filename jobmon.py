#!/usr/bin/env python3
# Job monitor for GitLab CI
# Licensed under MIT.
# https://github.com/dehesselle/gljobmon

import gitlab   # pip install python-gitlab
import os
from datetime import datetime, timedelta
import time
from sty import fg   # pip install sty
import signal
import sys
import argparse
from common import IniFile
from common.get_status_color import *
from common.get_fixed_string import *


def get_project(project_id: str, server: str, token: str):
    # Get a project by its ID. You'll find the ID on your project's details page
    # (https://gitlab.com/<user>/<project>) directly below the name.
    gl = gitlab.Gitlab(server, private_token=token)
    return gl.projects.get(project_id)


def get_datetime(gitlab_timestamp: str) -> datetime:
    # Convert timestamp as supplied by GitLab to a datetime object.
    dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.strptime(gitlab_timestamp, dt_format)


def get_minutes_between(gitlab_timestamp1: str, gitlab_timestamp2: str) -> str:
    # Calculate the absolute difference between two timestamp objects in minutes.
    try:
        datetime1 = get_datetime(gitlab_timestamp1)
        datetime2 = get_datetime(gitlab_timestamp2)
        minutes = abs(int((datetime1 - datetime2).total_seconds() / 60))
        if minutes > 999:
            minutes = 999
        minutes = str(minutes).zfill(3)
    except (ValueError, TypeError) as e:
        minutes = "..."
    return minutes


def print_jobs(project, job_name: str) -> None:
    line_count = 0
    # Print some details about every job matching 'job_name' of every pipeline.
    # By default, "every pipeline" are in fact  the last 18 pipelines.
    for pipeline in project.pipelines.list():
        for job in pipeline.jobs.list():
            if job.name == job_name:   # only interested in specific job_name
                line_count += 1
                if line_count <= 18:
                    print(get_status_color(job.status)
                          + get_datetime(job.created_at).strftime("%y%m%d-%H%M%S")
                          + fg.rs,
                          " ",
                          fg(248) + get_minutes_between(job.created_at, job.started_at) + "·"
                          + get_minutes_between(job.started_at, job.finished_at) + fg.rs, " ",
                          fg(131) + get_fixed_str(pipeline.ref, 10) + fg.rs, " ",
                          fg(205) + job.commit["short_id"] + fg.rs, " ",
                          fg(33) + get_fixed_str(job.commit["title"], 52) + fg.rs, " ",
                          fg.li_black + get_fixed_str(job.user["name"], 16) + fg.rs,
                          sep="")


def move_cursor(x, y):
    # Move cursor to specific position using ANSI control characters.
    # https://stackoverflow.com/a/54630943
    print("\033[%d;%dH" % (y, x))


def clear_screen():
    # Clear the terminal screen using ANSI control characters.
    # https://stackoverflow.com/a/2084521
    print(chr(27) + "[2J")


def handle_signal(signal, frame):
    # Exit gracefully.
    sys.exit(0)


def main():
    # - Install signal handler to catch SIGINT, because we're going to use an
    #   endless loop the user has to quit with Ctrl+C.
    # - Check if a configuration file has been specified on the commandline.
    #   - Yes: try to use it
    #   - No: use default path
    # - read settings from configuration file
    # - Enter endless loop and update screen every X seconds with data from
    #   GitLab.

    signal.signal(signal.SIGINT, handle_signal)

    parser = argparse.ArgumentParser(description="monitor CI jobs")
    parser.add_argument("-f", "--file", metavar="file")
    args = parser.parse_args()

    if args.file is None:
        gl = IniFile.GitlabIni()           # use default path
    else:
        gl = IniFile.GitlabIni(args.file)  # use custom path

    seconds = int(gl["jobmon"]["update"])

    clear_screen()
    while True:
        move_cursor(1, 1)
        dt_now = datetime.now()
        project = get_project(gl.project_id, gl.server, gl.token)
        print(("this: " + dt_now.strftime("%Y.%m.%d %H:%M:%S") + " --- "
              + fg(230) + gl["jobmon"]["ci_job"] + fg.rs + " on " + project.web_url).ljust(111))
        print("".ljust(111))  # empty line
        print_jobs(project, gl["jobmon"]["ci_job"])
        print("".ljust(111))  # empty line
        print(("next: " + (dt_now + timedelta(seconds=seconds)).strftime("%Y.%m.%d %H:%M:%S")
               + " --- Ctrl+C to exit").ljust(110))

        if "PYCHARM_HOSTED" in os.environ:
            break   # no endless loop when developing

        time.sleep(seconds)


if __name__ == '__main__':
    main()
