# swifttrack

Here are the example how to set the task

# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command

m = minute
h = hours
dom = day of month
mon = month
dow = day of the week

This command will is set to execute every minute so change it to your time needs.

1. crontab -e

2. * * * * * cd ~/Desktop/swiftrack && ~/Desktop/swiftrack/venv/bin/python ~/Desktop/swiftrack/swifttrack/manage.py generate_payroll
