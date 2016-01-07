## preheat-tesla

Preheat-tesla can be used to preheat or defrost (higher temperature) your Tesla Model S. It will wake up your car, check the current temperature and start the climate control if you have more than the minimal range.

You can configure pushover to receive a pushmessage on your phone once the process has started. It will tell you the current outside temperature and your range.

## Requirements

Preheat-tesla requires `https://github.com/jstenback/pytesla`

## Installation

Use crontab to schedule preheat-tesla.py, for instance:

```50 7 * * 1,2,3,4,5 /usr/local/bin/preheat.py > /dev/null 2>&1```

This will run preheat-tesla on monday to friday and will start on 7:50 in the morning. 

## Scheduling

Always schedule preheat-tesla +/- 15 minutes before you enter your car because it will need that time if it's really cold and the high temperature defrost option starts.

If it's not that cold, preheat-tesla will wait and preheat to your standard temperature a few minutes before you leave.
