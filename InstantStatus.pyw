import sys, os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

from DailyStatusWeb import main

main()