# Job monitor for GitLab CI

Print a self-updating status page about specific GitLab CI jobs in the terminal.

![foo](/monitor1.png)

There are 6 columns:

- ___job created___ column as timestamp in `%y%m%d-%H%M%S` format
  - orange for pending jobs
  - yellow for running jobs
  - green for successfully completed jobs
  - red for failed jobs
- ___combined "job started" and "job finished"___ column, each as 3-digit value in "minutes since job creation" and "minutes since job start" in `NNN·NNN` format
- ___git reference___ column, limited to 10 chars
- ___commit hash___ column, short form
- ___commit message___ column, first line only and limited to 52 chars
- ___author___ column, limited to 16 chars

And this is what it looks like with pending and running jobs.

![foo](/monitor2.png)

## Usage

### Prerequisites

- You need [python-gitlab](https://python-gitlab.readthedocs.io/en/stable/index.html) and [sty](https://sty.mewo.dev/index.html) packages.

  ```bash
  pip3 install python-gitlab   # GitLab API
  pip3 install sty             # ANSI control for terminal colors
  ```

- Terminal with support for ANSI control characters and 256 colors.

### Configuration

Create a file `$HOME/jobmon.ini` to configure:

```ini
[gitlab]
server = https://gitlab.com
project_id = 1234567
ci_job = someName
access_token = secret

[jobmon]
update = 120
```

### Three, two, one ... go

Run the script:

```bash
./jobmon.py
```

You can also use a custom file/path for your configuration:

```bash
./jobmon.py -f <your configuration file>
```

## Status

unfinished, work in progress

## License

[MIT](LICENSE)