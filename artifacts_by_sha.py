#!/usr/bin/env python3
# get CI artifact download URLs by commit sha
# Licensed under MIT.
# https://github.com/dehesselle/gitlabci

import gitlab    # pip install python-gitlab
from natter import IniFile
from common import *
from sty import fg   # pip install sty
import argparse


def get_commit_sha() -> str:
    parser = argparse.ArgumentParser(description="get artifact URLs by commit sha")
    parser.add_argument("sha", metavar="sha", type=str, help="commit sha")
    args = parser.parse_args()
    return args.sha


def get_commit_id(commit) -> str:
    return fg(205) + commit.short_id + fg.rs + commit.id[len(commit.short_id):]


def main() -> None:
    ini = IniFile("gitlabci.ini")

    gl = gitlab.Gitlab(ini["gitlab"]["server"], private_token=ini["gitlab"]["access_token"])

    project = gl.projects.get(ini["gitlab"]["project_id"])
    commit = project.commits.get(get_commit_sha())

    print("-" * 88)
    # print("project.name =", project.name)
    # print()
    print("commit.id             =", get_commit_id(commit))
    print("commit.title          =", fg(33) + commit.title + fg.rs)
    print("commit.committer_name =", fg.da_grey + commit.committer_name + fg.rs)
    print("commit.committed_date =", commit.committed_date)
    print("-" * 88)

    pipeline = project.pipelines.get(commit.last_pipeline["id"])

    for job in pipeline.jobs.list():
        if job.status == "success":
            print(fg.green + to_fixed_len(job.name, 15) + fg.rs, job.web_url + "/artifacts/download")
        else:
            print(get_status_color(job.status) + to_fixed_len(job.name, 15) + fg.rs, job.status)


if __name__ == "__main__":
    main()
