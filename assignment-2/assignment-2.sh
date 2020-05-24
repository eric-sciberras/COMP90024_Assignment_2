#!/bin/bash

. ./openrc.sh; ansible-playbook -i hosts --ask-become-pass assignment-2.yaml