# -*- coding: utf-8 -*-
"""
[Python 2.7 (Mayavi is not yet compatible with Python 3+)]
Created on Mon Feb 09 18:11:08 2015
@author: Ryan Stauffer
https://github.com/ryanpstauffer/market-vis

market-vis v0.01
Market Visualization Prototype
Main script
"""

from datetime import datetime
from timeit import default_timer as timer
import pandas as pd
import argparse

from quotes import buildDailyPriceData, buildDummyData, createIndexedPricing
from visualization import visualizePrices, animateGIF

def main(mode="test", start="20150101", end="20160101", verbose=True):
    programStart = timer()
        
    #Select Dates  
    startDate = datetime.strptime(start, "%Y%m%d")
    endDate = datetime.strptime(end, "%Y%m%d")
    
    #Get data for S&P500 Constituents
    SP500Constituents = pd.read_csv("SP500_constituents.csv")
    
    if mode == "live":
        #Use for online stock price building, pulling from Google Finance API
        print("Pulling Data from Google Finance API")
        SP500StockPrices = buildDailyPriceData(SP500Constituents["Symbol"], startDate, endDate)
    
    else:
        #Use for offline testing (built from existing .csv file)
        print("Using Test Data from .csv")
        SP500StockPrices = buildDummyData()
    
    dataPullEnd = timer()
    
    SP500IndexedPrices = createIndexedPricing(SP500StockPrices, 100)
    
    calcEnd = timer() #Doesn't include visualization in timer
    
    visualizePrices(SP500IndexedPrices)
    visEnd = timer()
    
    if verbose:
        print("Data Pull Time: {0} sec".format(dataPullEnd - programStart))
        print("Calculation Time: {0} sec".format(calcEnd - dataPullEnd))
        print("Visualization Time: {0} sec".format(visEnd - calcEnd))
        print("Total Time: {0} sec".format(visEnd - programStart))
    
    #animateGIF('../images/prototype_animation.gif', SP500IndexedPrices)
    
    print('End')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Market Visualization Tool")
    parser.add_argument("mode", metavar="mode", choices=["live", "test"], default="test",
                        help="Running mode: live (online downloads) | test (offline test data)")
    parser.add_argument("startDate", nargs='?', type=str, default="20150101",
                        help="Start date of the live data pull (YYYYMMDD)")
    parser.add_argument("endDate", nargs='?', type=str, default="20160101",
                        help="End date of the live data pull (YYYYMMDD)")  
    parser.add_argument("-v", "--verbose", action="store_true", 
                        help="Includes time printouts during runtime")
#    group = parser.add_mutually_exclusive_group()
#    group.add_argument("-l", "--live", action="store_true",
#                       help="Runs live and downloads data from Google Finance API")
#    group.add_argument("-t", "--test", action="store_true",
#                       help="[Default] Runs in test mode, using existing data from .csv")
    args = parser.parse_args()
    main(args.mode, args.startDate, args.endDate, args.verbose)
#    if args.live:
#        print(args.live)
#        print("live", args.startDate, args.endDate)   
##        main("live", args.startDate, args.endDate)   
#    else:
#        print(args.live)
#        print("test")
##        main("test")  
    
