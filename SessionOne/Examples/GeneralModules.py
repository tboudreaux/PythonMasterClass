# This will likely not run on your local machine as there are some non default conda modules -- installation
#   instructions for all are at the bottom of the file

try:        # Import error handling, more advanced usage can be done with scripted pip commands
    import numpy as np
    from tqdm import tqdm       # must be installed
    import os
    import shutil
    import argparse
    import random as r
    import sys
    from colorama import Fore, Back, Style
    basic = False
except ImportError:
    # Standard Library (anaconda) Packages
    import numpy as np
    import os
    import shutil
    import argparse
    import random as r
    import sys
    from colorama import Fore, Back, Style
    basic = True


def os_show():

    """
    OS
        The os module allows for interaction with the file structure and for many tasks that would normally be
        carried out in the command line to be scripts in python

        I will focus on UNIX os commands however they are relatively similar in windows
    """

    print Fore.RED + '###############' + Fore.RESET     # demo of colors in terminal (ANSI)
    print Fore.GREEN + 'Bottom Up:' + Fore.RESET
    print Fore.CYAN

    # scan directories for files -- os.walk allows for scanning of arbitrarily deep trees
    for root, dirs, files in os.walk('..', topdown=False):  # bottom up walk with os.walk starting from most sub and up
        print 'In Directory: ', root
        print 'With the Subdirectories: ', dirs
        print 'with the files: ', files
    print Fore.RESET
    print Fore.RED + '###############' + Fore.RESET

    print Fore.GREEN + 'Top Down' + Fore.RESET
    print Fore.CYAN

    for root_2, dirs_2, files_2 in os.walk('..', topdown=True): # Top down os.walk, more traditional, good if you
                                                                #   Don't have prior knowledge of structure
        print 'In Directory: ', root_2
        print 'With the Subdirectories: ', dirs_2
        print 'with the files: ', files_2
    print Fore.RESET
    print Fore.RED + '###############' + Fore.RESET
    cont = False
    change = False

    # General Y/N menu
    while cont is False:
        make_change = raw_input('Would you like to duplicate the entire file structure of this session [y/n]: ')

        if make_change.upper()[0] == 'Y':
            cont = True
            change = True
        elif make_change.upper()[0] == 'N':
            cont = True
            change = False
        else:
            print 'Please enter either yes or no'

    # If user wants to copy the file structure
    if change is True:
        for root_3, dirs_3, files_3 in os.walk('..'):
            for dir in dirs_3:
                if os.path.isdir('../' + root_3 + '/' + dir):
                    shutil.rmtree('../' + root_3 + '/' + dir)     # If the folder already exists remove it
                print 'Makign Directory: ' + '../' + root_3 + '/' + dir
                os.mkdir('../' + root_3 + '/' + dir)      # Build the directory structure
            for file in files_3:
                if os.path.exists('../' + root_3 + '/' + file):
                    os.remove('../' + root_3 + '/' + file)     # if the file exists remove it
                print 'Copying File: ' + '../' + root_3 + '/' + file
                shutil.copy(root_3 + '/' + file, '../' + root_3 + '/' + file)     # move the files


def tqdm_show():
    """
    TQDM
        Easy progress bar tha doesnt slow down program nearly as much as print statements to
    """

    a = [r.randint(0, 9999999) for i in range(10000)]       # Generate some large semi random number array
    # print 'UNSORTED:', a

    # This is a intentionally slow sort algorithm than takes ~n^2 times to run in order to show tqdm
    # (essentially this is bubble sort but slightly slower)
    smallest = a[0]
    smallest_index = 0
    b = []
    print 'Sorting: '
    for k in tqdm(range(len(a))):       # Initialize tqdm with the iterator range
        for index, element in enumerate(a):
            if element < smallest:  # find the smallest element in a each run through
                smallest = element
                smallest_index = index
        b.append(smallest)  # add the smallest element to a new array
        a.pop(smallest_index)   # remove that element from a
        if len(a) > 0:  # grab the last element of a w/o getting an index error
            smallest = a[0]
            smallest_index = 0
    print 'Sorted!'
    # print 'SORTED:', b


def sys_show():
    # print sys.argv
    if sys.platform.upper() == 'WINDOWS':   # check what platform code is running on
        print 'You are on windows'
    elif sys.platform.upper() == 'DARWIN':
        print 'You are on a mac'
    elif 'LINUX' in sys.platform.upper():
        print 'you are on some distro of linux'

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Command Line arguments to pass into program')
    parser.add_argument('Module', metavar="Module to demonstrate use of", type=str, nargs=1,
                        help="User spesified which function to test in this program")
    parser.add_argument('-bac', action='store_true', help='set a univesal background color for all printed text')
    parser.add_argument('-n', metavar='number of runs', type=int, default=[1], nargs=1,
                        help="how many times to run selected function")
    args = parser.parse_args()

    if args.bac is True:
        print Back.LIGHTMAGENTA_EX

    for i in range(args.n[0]):
        if args.Module[0] == 'o':
            os_show()
        elif args.Module[0] == 't':
            if basic is False:
                tqdm_show()
            else:
                print 'Unable to run "tqdm" demo on this computer as necessary dependencies may not be installed'
        elif args.Module[0] == 's':
            sys_show()

    print Style.RESET_ALL


# Install tqdm
# "pip install tqdm"