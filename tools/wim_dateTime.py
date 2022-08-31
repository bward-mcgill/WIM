#! /usr/bin/env python3

import argparse
from datetime import datetime, timedelta

def printListTs(year_init, month_init, day_init, sec_init, ts, nts):
   list_ts=""
   start_day=datetime(year=int(year_init), month=int(month_init), day=int(day_init), second=int(sec_init))

   if nts <= 0:
      list_ts=str(start_day.year).zfill(4)+str(start_day.month).zfill(2)+str(start_day.day).zfill(2)+str(start_day.hour*3600).zfill(5)
   else:
      for i in range(nts):
         new_day=start_day+timedelta(seconds=sec_init+i*ts)
         if i == 0 :
            list_ts=list_ts+" "+str(new_day.year).zfill(4)+str(new_day.month).zfill(2)+str(new_day.day).zfill(2)+str(new_day.hour*3600).zfill(5)+" "+str(new_day.year).zfill(4)+str(new_day.month).zfill(2)+str(new_day.day).zfill(2)+str(new_day.hour*3600).zfill(5)
         else:
            list_ts=list_ts+" "+str(new_day.year).zfill(4)+str(new_day.month).zfill(2)+str(new_day.day).zfill(2)+str(new_day.hour*3600).zfill(5)   
   print(list_ts)

def printTsModel(yyyy, mm, dd, sssss, model):
   day=datetime(year=yyyy, month=mm, day=dd)
   dayTs=day+timedelta(seconds=sssss)
   if model == 'CICE':
      print(str(dayTs.year).zfill(4)+'-'+str(dayTs.month).zfill(2)+'-'+str(dayTs.day).zfill(2)+"-"+str(dayTs.hour*3600).zfill(5))
   elif model == 'WW3':
      print(str(dayTs.year).zfill(4)+str(dayTs.month).zfill(2)+str(dayTs.day).zfill(2)+'-'+str(dayTs.hour).zfill(2)+str(dayTs.minute).zfill(2)+str(dayTs.second).zfill(2))

def createListDateTime(init_dateTime, ts, ts_u, nts):
   list_ts=[]
   start_day=init_dateTime
   from dateutil.relativedelta import relativedelta

   for i in range(nts):
      if ts_u == 's':
          new_day=start_day+timedelta(seconds=i*ts)
      elif ts_u == 'h':
          new_day=start_day+timedelta(hours=i*ts)
      elif ts_u == 'd':
          new_day=start_day+timedelta(days=i*ts)
      elif ts_u == 'm':
          new_day=start_day+relativedelta(months=i*ts)
      elif ts_u == 'y':
          new_day=start_day+relativedelta(years=i*ts)
      list_ts.append(new_day)
   return list_ts

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    parserPrintListTs=subparsers.add_parser('printListTs', help="Print the list of timestep.")
    parserPrintListTs.add_argument("year_s", help="Enter a start year", type=int)
    parserPrintListTs.add_argument("month_s", help="Enter a start month", type=int)
    parserPrintListTs.add_argument("day_s", help="Enter a start day", type=int)
    parserPrintListTs.add_argument("sec_s", help="Enter a start sec", type=int)
    parserPrintListTs.add_argument("dt_coup", help="Enter coupling frequency", type=int)
    parserPrintListTs.add_argument("ndt", help="Enter number of coupling (it defines end date)", type=int)

    parserPrintTs=subparsers.add_parser("printTs", help="Print a single timestep") 
    parserPrintTs.add_argument("year", help="Enter the year", type=int)
    parserPrintTs.add_argument("month", help="Enter the month.", type=int)
    parserPrintTs.add_argument("day", help="Enter the day.", type=int)
    parserPrintTs.add_argument("sec", help="Enter the seconds.", type=int)
    parserPrintTs.add_argument("model", help="Enter the model for the format (CICE : yyyy-mm-dd-sssss, WW3: yyyymmddd-hhmmss)", choices=['CICE', 'WW3'])


    args=parser.parse_args()

    if args.cmd == 'printListTs':
        printListTs(args.year_s, args.month_s, args.day_s, args.sec_s, args.dt_coup, args.ndt)
    if args.cmd == 'printTs':
        printTsModel(args.year, args.month, args.day, args.sec, args.model)

if __name__ == "__main__":
    main()

