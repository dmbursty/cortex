# Common initialization for scripts
import os
import sys

# Allow omission of the initial 'cortex.' for all import statements
sys.path.append(sys.path[0] + "/cortex")
# Set timezone to eastern
os.environ['TZ'] = 'US/Eastern'
