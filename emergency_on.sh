#!/bin/bash

(crontab -l ; echo "* * * * * bash /home/donald/Desktop/TextParser2/run_emergency.sh >/dev/null 2>&1") | crontab -


