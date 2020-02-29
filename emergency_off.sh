#!/bin/bash

crontab -l | grep -v '* * * * * bash /home/donald/Desktop/TextParser2/run_emergency.sh >/dev/null 2>&1'  | crontab -

(crontab -l ; echo "* * * * * bash /home/donald/Desktop/TextParser2/run.sh >/dev/null 2>&1") | crontab -
