# This will likely not run on your local machine as there are many non default conda modules -- installation
#   instructions for all are at the bottom of the function

import numpy as np
import pandas as pd
from tqdm import tqdm
import astropy
import scipy
import os
import argparse
import math
import random as r
import sys
from colorama import Fore, Back, Style


def os_show():

    """
    OS
        The os module allows for interaction with the file structure and for many tasks that would normally be
        carried out in the command line to be scripts in python

        I will focus on UNIX os commands however they are relatively similar in windows
    """

    print Fore.RED + '###############' + Style.RESET_ALL
    print Fore.GREEN + 'Bottom Up:' + Style.RESET_ALL
    print Fore.CYAN
    for root, dirs, files in os.walk('..', topdown=False):
        print 'In Directory: ', root
        print 'With the Subdirectories: ', dirs
        print 'with the files: ', files
    print Style.RESET_ALL
    print Fore.RED + '###############' + Style.RESET_ALL

    print Fore.GREEN + 'Top Down' + Style.RESET_ALL
    print Fore.CYAN
    for root_2, dirs_2, files_2 in os.walk('..', topdown=True):
        print 'In Directory: ', root_2
        print 'With the Subdirectories: ', dirs_2
        print 'with the files: ', files_2
    print Style.RESET_ALL
    print Fore.RED + '###############' + Style.RESET_ALL


def tqdm_show():
    """
    TQDM
        Easy progress bar tha doesnt slow down program nearly as much as print statements to
    """

    a = [r.randint(0, 9999999) for i in range(10000)]
    print 'UNSORTED:', a
    smallest = a[0]
    smallest_index = 0
    b = []
    for k in tqdm(range(len(a))):
        for index, element in enumerate(a):
            if element < smallest:
                smallest = element
                smallest_index = index
        b.append(smallest)
        a.pop(smallest_index)
        if len(a) > 0:
            smallest = a[0]
            smallest_index = 0
    print 'SORTED:', b


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Command Line arguments to pass into program')
    parser.add_argument('Module', matavar="Module to demonstrate use of", type=str, nargs=1,
                        help="User spesified which function to test in this program")
    parser.add_argument('-bac', action='store_true', help='set a univesal background color for all printed text')
    parser.add_argument('-n', metavar='number of runs', type=int, default=[1], nargs=1,
                        help="how many times to run selected function")
    args = parser.parse_args()

    if args.Module[0] == 'o':
        os_show()
    elif args.Module[0] == 't':
        tqdm_show()
