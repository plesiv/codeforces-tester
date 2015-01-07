# -*- coding: utf-8 -*-
"""This module provides the main functionality.
"""
import os
import sys
import textwrap

from hac import ExitStatus
from hac.config import DEFAULT_CONFIG_DIR, USER_CONFIG_DIR, CONFIG_FILENAME, \
    config_parser
from hac.cli import cli_parser


def dict_override(a, b):
    """Overriding dictionary values.

    Values in second dictionary override the values in the first one (except
    when relevant value in second dictionary is None).

    >>> dict_override({'a': 1,'b': 2}, {'a': 3,'b': None}) == {'a': 3,'b': 2}
    True

    >>> dict_override({'a': 3,'b': None}, {'a': 1,'b': 2}) == {'a': 1,'b': 2}
    True
    """
    res = {}
    for key in (set(a.keys()) | set(b.keys())):
        if (key in b) and (b[key] != None):
            res[key] = b[key]
        else:
            res[key] = a[key]
    return res


def main(args=sys.argv[1:]):
    """Execution flow of the main function:

    1) get configuration (priorities: default < local < cli)
    2) branch according to command (prep, show)
    """

    # Get default global configuration
    global_config_file = os.path.join(DEFAULT_CONFIG_DIR, CONFIG_FILENAME)
    env_global = config_parser.parse_args(['@' + global_config_file])

    # Get local configuration
    user_config_file = os.path.join(USER_CONFIG_DIR, CONFIG_FILENAME)
    if os.path.exists(user_config_file):
        env_user = config_parser.parse_args(['@' + user_config_file])

    # Show help and exit when no arguments given.
    if len(args) == 0:
        cli_parser.print_help()
        sys.exit(ExitStatus.ERROR)

    # Parse CLI arguments
    env_cli = cli_parser.parse_args(args=args)

    # Resolve configuration
    conf_user = dict_override(vars(env_global), vars(env_user))
    conf_all = dict_override(conf_user, vars(env_cli))

    # TODO #1 web page-information DS
    # TODO #2 web-parsing DS and processor
    # TODO #3 decipher which problems to fetch (URL, other)
    # TODO #4 show command
    # TODO #5 prep command
    import pprint; pp = pprint.PrettyPrinter(indent=4)
    print("USER"); pp.pprint(conf_user)
    print("ALL"); pp.pprint(conf_all)

    # TODO create whole directory structure for dir that doesn't exist
    # TODO resolve paths got from user (~ etc.)
    # TODO lang, runner; no multiples, no clears previous enables
