#!/bin/bash
pip install $(pip list --outdated | awk '{ print $1 }') --upgrade