#!/usr/bin/env python3
# get CI artifact download URLs by commit sha
# Licensed under MIT.
# https://github.com/dehesselle/gitlabci

import gitlab    # pip install python-gitlab
import IniFile
import argparse


def get_commit_sha() -> str:
    parser = argparse.ArgumentParser(description="get artifact URLs by commit sha")
    parser.add_argument("sha", metavar="sha", type=str, help="commit sha")
    args = parser.parse_args()
    return args.sha


def main() -> None:
    ini = IniFile.GitlabIni()   # use default path

    gl = gitlab.Gitlab(ini.server, private_token=ini.token)

    project = gl.projects.get(ini.project_id)
    commit = project.commits.get(get_commit_sha())

    print("------------------------------------------------------------------------")
    # print("project.name =", project.name)
    # print()
    print("commit.id             =", commit.id)
    print("commit.title          =", commit.title)
    print("commit.committer_name =", commit.committer_name)
    print("commit.committed_date =", commit.committed_date)
    print("------------------------------------------------------------------------")

    pipeline = project.pipelines.get(commit.last_pipeline["id"])

    for job in pipeline.jobs.list():
        print(job.name + ":", job.status)
        if job.status == "success":
            print(job.web_url + "/artifacts/download")
        else:
            print("n/a")


if __name__ == "__main__":
    main()
