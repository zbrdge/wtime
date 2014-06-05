#!/usr/bin/env python
'''
 wtime-based timesheet/invoice generation
 puts a markdown timesheet in /tmp/invoice.md,
 embeds all time data in the file in an HTML comment
'''

from datetime import datetime
import string 
import importlib, sys

# Using importlib now, we specify which client configuration
# file to use, using a simple naming convention:
if sys.argv[1]:
    from importlib.import_module("wts_config_"+sys.argv[1]) import *

if __name__ == "__main__":

    md = open("/tmp/invoice.md", "w")

    mdtpl = "Contracting Services<br />{START} to {FINISH}"
    mdtpl += """
===========================================================

{IMAGE}

__{FULLNAME}__<br />
{ADDRESS_L1}<br />
{ADDRESS_L2}<br />
{ADDRESS_L3}

Client: {CLIENT}
---------------------
* Project: {PROJECT}
* Services: {SERVICES}
* Invoice #: {INVOICE_NUM}

Details
-------
* Hours Billed: {TOTAL}
* Rate: {RATE}
* Total Due: {FINAL}

Payment Options
---------------
* PayPal Invoice: {PAYPAL}
* Check or Money Order made payable to Zachary A. Breckenridge
  via mail at the address listed above.

***

Work Notes
==========

{WORKLOG}

<!---
{HARD_DATA_TIME_CONTENTS}

{HARD_DATA_DESC_CONTENTS}
!--->
"""

    # get a total of all hours worked and print a table
    wtime = open(config["{HARD_DATA_TIME}"], "r")
    wlog  = open(config["{HARD_DATA_DESC}"], "r")

    '''
       seconds = {
          'DD/MM/YY' : { [starttime, endtime], [starttime, endtime]...
       }
    '''
    seconds = {}
    day_order = []

    for line in wtime.readlines():
       times  = line.split(" ")
       dmy    = datetime.fromtimestamp(int(times[0]))
       dstr   = dmy.strftime("%m-%d-%Y")

       try:
         day_order.index(dstr)
       except:
         day_order.append(dstr)
         seconds[dstr] = []

       seconds[dstr].append(times)

    # read entire 'desc' file as a list
    desc = [] 
    for line in wlog.readlines():
       l = line.split(" ", 1)
       l[1] = l[1].replace("\n", "")
       desc.append(l)
  
    worklog = "" 
    total = 0.0
    for day in day_order:
       daytot = 0.0
       worklog += "### Activities on "+day+":\n" # +(13+len(day))*'='+"\n"

       for act in desc:
          d = datetime.fromtimestamp(int(act[0])).strftime("%m-%d-%Y")
          if d == day:
            worklog += "* " + act[1] + " -- " + \
	        datetime.fromtimestamp(int(act[0])).strftime("%I:%M %p")+"\n"
          

       for times in seconds[day]:
         daytot += (int(times[1]) - int(times[0]))
         

       tstr = "Total Hours for "+day
       worklog += "\n" + tstr + ": " + "{0:.2f}".format(daytot/60.0/60.0)+"\n\n"

       total += daytot

    rate = float(config['{RATE}'])
    total = total/60.0/60.0
    final = "{0:.2f}".format(total*rate)
    total = "{0:.2f}".format(total)

    worklog += "---\n" + "Total Hours Worked: "+total

    mdtpl = string.replace(mdtpl, "{START}", day_order[0])
    mdtpl = string.replace(mdtpl, "{FINISH}", day_order[len(day_order)-1])
    mdtpl = string.replace(mdtpl, "{TOTAL}", total)
    mdtpl = string.replace(mdtpl, "{FINAL}", final)
    mdtpl = string.replace(mdtpl, "{WORKLOG}", worklog)

    # embed the data files in the resulting markdown for reference
    wtime.seek(0)
    wlog.seek(0)
    config["{HARD_DATA_TIME_CONTENTS}"] = ""
    config["{HARD_DATA_DESC_CONTENTS}"] = ""

    for line in wtime.readlines():
      config["{HARD_DATA_TIME_CONTENTS}"] += line
    for line in wlog.readlines():
      config["{HARD_DATA_DESC_CONTENTS}"] += line

    # finish replacing values in template
    for name, val in config.items():
        mdtpl = string.replace(mdtpl, name, val)

    md.write(mdtpl)
    md.close()
    wtime.close()
    wlog.close()
