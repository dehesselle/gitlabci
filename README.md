# little helpers for GitLab CI

This repository is a collection of little helpers and convenience functions using [python-gitlab](https://python-gitlab.readthedocs.io) to access GitLab's API. I'm doing this for myself and for a very specific use case, so don't expect these scripts to be all-rounders, they are not meant to be that.

## general prerequisites

All the Python scripts require at least the following package:

```bash
pip3 install python-gitlab   # GitLab API
```

### configuration file

All the scripts depend on a configuration file `$XDG_CONFIG_HOME/gitlabci.ini` for credentials:

```ini
[gitlab]
server = https://gitlab.com
project_id = 1234567
access_token = secret
```

- You can find the `project_id` in the top left corner of you project's overview page, directly below the title.
- You need to create a [personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) for `access_token`.

## Overview

### [jobmon](/docs/jobmon.md)

Print a self-updating status page about specific GitLab CI jobs in the terminal.

![jobmon1](/docs/jobmon1.png)

## License

[MIT](LICENSE)