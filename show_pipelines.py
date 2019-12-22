import gitlab
import os
from datetime import datetime
from sty import fg, bg


def get_file_content(file_name):
    file = open(file_name)
    content = file.read()
    file.close()

    return content.rstrip()    # remove trailing newline


def get_project(project_id):
    token_file = os.getenv("HOME") + "/.local/etc/gitlab/python-gitlab"
    get_file_content(token_file)
    gl = gitlab.Gitlab("https://gitlab.com",
                       private_token=get_file_content(token_file))

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
        return fg(226)   # yellow
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


def get_pipelines(project):
    pipelines = project.pipelines.list()
    #print(pipelines[0])

    pipeline = project.pipelines.get(pipelines[0].id)
    jobs = pipeline.jobs.list()

    for job in jobs:
        if job.name == "inkscape:mac":

            commit_title = job.commit["title"];
            if len(commit_title) > 52:
                commit_title = commit_title[:49] + "..."

            commit_title = commit_title.ljust(52)
            stat="failed"
            print(get_status_color(stat) + get_datetime(job.created_at).strftime("%y%m%d-%H%M%S") + fg.rs, "·",
                  fg(248) + get_minutes_between(job.created_at, job.started_at) + fg.rs, "·",
                  fg(248) + get_minutes_between(job.started_at, job.finished_at) + fg.rs, " ",
                  fg(205) + job.commit["short_id"] + fg.rs, " ",
                  fg(33) + commit_title + fg.rs, " ",
                  fg.li_black + job.user["name"] + fg.rs,
                  sep="")
            #started_after = job.created_at



get_pipelines(get_project(3472737))

min=get_minutes_between("2019-12-22T10:59:32.621Z", "2019-12-22T11:59:32.621Z")
min=get_minutes_between("2019-12-22T10:59:32.621Z", "")


print(min)

