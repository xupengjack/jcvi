"""
basic support for running library as script
"""

import sys
import logging
from optparse import OptionParser

from jcvi.utils.iter import flatten

class ActionDispatcher (object):

    def __init__(self, actions):

        self.actions = actions
        self.valid_actions, self.action_helps = zip(*actions)

    def print_help(self):
        help = "available actions:\n"
        for action, action_help in self.actions:
            help += "\t`%s`: %s\n" % (action, action_help)

        print >>sys.stderr, help
        sys.exit(1)

    def dispatch(self, globals):
        if len(sys.argv) == 1:
            self.print_help()
        
        action = sys.argv[1]

        if not action in self.valid_actions:
            print >>sys.stderr, "%s not a valid action" % action
            self.print_help()

        globals[action](sys.argv[2:])


def set_debug(instance, args):

    assert isinstance(instance, OptionParser), \
            "only OptionParser can add debug option"

    instance.add_option("--debug", dest="debug",
            default=False, action="store_true",
            help="set to debug level")

    opts, args = instance.parse_args(args)

    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)


def sh(cmd):
    """
    simple wrapper for system calls
    """
    from subprocess import call
    call(cmd, shell=True)
    logging.debug(cmd)
