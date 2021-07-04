#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: 2021 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: to be decided

set -e
python3 -m venv venv
venv/bin/pip3 install -r requirements.txt
#venv/bin/pip3 install -r natter/requirements.txt
