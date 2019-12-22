import gitlab
import os
from datetime import datetime, timedelta
import time
from sty import fg
import signal
import sys


def get_file_content(file_name):
    file = open(file_name)
    content = file.read()
    file.close()
    return content.rstrip()    # remove trailing newline


def get_project(project_id):
    token_file = os.getenv("HOME") + "/.local/etc/gitlab/python-gitlab"
    get_file_content(token_file)
    gl = gitlab.Gitlab("https://gitlab.com", private_token=get_file_content(token_file))
    return gl.projects.get(project_id)


def get_datetime(gitlab_timestamp):
    dt_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.strptime(gitlab_timestamp, dt_format)


def get_minutes_between(gitlab_timestamp1, gitlab_timestamp2):
    try:
        datetime1 = get_datetime(gitlab_timestamp1)
        datetime2 = get_datetime(gitlab_timestamp2)
        minutes = abs(int((datetime1 - datetime2).total_seconds() / 60))
        if minutes > 999:
            minutes = 999
        minutes = str(minutes).zfill(3)
    except ValueError:
        minutes = "..."
    return minutes


def get_status_color(status):
    if status == "pending":
        return fg(214)  # orange
    elif status == "created":
        return fg.rs
    elif status == "running":
        return fg(226)  # yellow
    elif status == "success":
        return fg.green
    elif status == "canceled":
        return fg(124)  # dark red
    elif status == "skipped":
        return fg.li_black
    elif status == "failed":
        return fg(196)  # light red
    else:
        return fg.rs


def get_fixed_str(text, length):
    if len(text) > length:
        text = text[:length-3] + "..."
    return text.ljust(length)

def print_jobs(project, job_name):
    for pipeline in project.pipelines.list():
        for job in pipeline.jobs.list():
            if job.name == job_name:   # only interested in specific job_name
                print(get_status_color(job.status)
                      + get_datetime(job.created_at).strftime("%y%m%d-%H%M%S")
                      + fg.rs, "·",
                      fg(248) + get_minutes_between(job.created_at, job.started_at) + fg.rs, "·",
                      fg(248) + get_minutes_between(job.started_at, job.finished_at) + fg.rs, " ",
                      fg(131) + get_fixed_str(pipeline.ref, 10) + fg.rs, " ",
                      fg(205) + job.commit["short_id"] + fg.rs, " ",
                      fg(33) + get_fixed_str(job.commit["title"], 52) + fg.rs, " ",
                      fg.li_black + job.user["name"] + fg.rs,
                      sep="")


def move_cursor(x, y):  # https://stackoverflow.com/a/54630943
    print("\033[%d;%dH" % (y, x))


def clear_screen():  # https://stackoverflow.com/a/2084521
    print(chr(27) + "[2J")


def handle_signal(signal, frame):
    sys.exit(0)


def main():
    seconds = 120
    signal.signal(signal.SIGINT, handle_signal)
    clear_screen()
    while True:
        move_cursor(1, 1)
        print(" now:", datetime.now().strftime("%Y.%m.%d %H:%M:%S"), "\n")
        print_jobs(get_project(3472737), "inkscape:mac")
        dt = datetime.now() + timedelta(seconds=seconds)
        print("\nnext:", dt.strftime("%Y.%m.%d %H:%M:%S"), "--- Ctrl+C to exit")
        time.sleep(60)


if __name__ == '__main__':
    main()
