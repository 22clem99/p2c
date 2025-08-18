import cmd, sys
from abc import ABC, abstractmethod
import argparse
import threading
import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class P2CArgparse(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        # self.exit(2, '%s: error: %s\n' % (self.prog, message))

class Cmd(ABC):
    subparser_name = 'subparser_name'

    def __init__(self, args):
        logger.debug(f"Command '{self}' is about to be run")
        super().__init__()
        self._parse_param(args)

    @abstractmethod
    def _cmd_name(self):
        ...

    def __str__(self):
        return self._cmd_name()

    @abstractmethod
    def _get_argparser(self):
        ...

    def _parse_param(self, args):
        parser = self._get_argparser()

        parsed_args, unknown_args = parser.parse_known_args(args.split())

        self.parsed_args = vars(parsed_args)
        self.unknown_args = unknown_args

        if self.unknown_args != []:
            logger.info(f"Arg(s) \'{' '.join(self.unknown_args)}\' does not exist")
            parser.print_help()

        self._post_parsing()

    @abstractmethod
    def _post_parsing(self):
        ...

    def _get_default_argparser(self):
        parser = P2CArgparse(prog=self._cmd_name(), exit_on_error=False, add_help=False)

        subparsers = parser.add_subparsers(help='subcommand help', required=True, dest=self.subparser_name)

        subparsers.add_parser('help', help='display this help')

        return parser, subparsers

class CmdExit(Cmd):
    def __init__(self, args):
        super().__init__(args)

    def _cmd_name(self):
        return "exit"

    def _get_argparser(self):
        parser = self._get_default_argparser()
        parser.description = "Quit P2C"
        return(parser)

    def _post_parsing(self):
        pass

class CmdProject(Cmd):
    def __init__(self, args):
        super().__init__(args)

    def _cmd_name(self):
        return "project"

    class SubCmdProject(StrEnum):
        CREATE      = "create"
        OPEN        = "open"
        SAVE        = "save"
        DELETE      = "delete"
        CLOSE       = "close"
        SETACTIVE   = "setactive"
        UNSETACTIVE = "unsetactive"
        UNKNOWN     = auto()

    def _get_argparser(self):
        parser, subparsers = self._get_default_argparser()
        parser.description = "P2C project manager"
        parser_create      = subparsers.add_parser('create', help='Create a P2C project')
        parser_create.add_argument('name')
        parser_open        = subparsers.add_parser('open', help='Open a P2C project')
        parser_open.add_argument('name')
        parser_save        = subparsers.add_parser('save', help='Save a P2C project')
        parser_save.add_argument('name')
        parser_delete      = subparsers.add_parser('delete', help='Delete a P2C project')
        parser_delete.add_argument('name')
        parser_close       = subparsers.add_parser('close', help='Close a P2C project')
        parser_close.add_argument('name')
        parser_setactive   = subparsers.add_parser('setactive', help='Set the P2C project as current')
        parser_setactive.add_argument('name')
        parser_unsetactive = subparsers.add_parser('unsetactive', help='Unset the P2C project as current')
        parser_unsetactive.add_argument('name')
        return(parser)

    def _post_parsing(self):
        logger.debug(f"Start post parsing for command {self}")

        self.subcmd = self.SubCmdProject(self.parsed_args[Cmd.subparser_name])

        if self.subcmd == self.SubCmdProject.UNKNOWN:
            logger.warning("The subcmd parsed is unknown")
        else:
            try:
                del self.parsed_args[Cmd.subparser_name]
            except KeyError:
                logger.error("Tried to remove the subcmd from the dict but can't")

class CmdNode(Cmd):
    def __init__(self, args):
        super().__init__(args)

    def _cmd_name(self):
        return "node"

    def _get_argparser(self):
        parser = self._get_default_argparser()
        parser.description = "Node command management"
        return(parser)

# class CmdLoglevel(Cmd):
#     def __init__(self):
#         super().__init__()

#     def _cmd_name(self):
#         return "exit"

#     def _get_argparser(self):
#         parser = self._get_default_argparser()

#         parser.description = "Quit P2C"

#         return(parser)

class P2CShell(cmd.Cmd):
    intro = 'Welcome to the P2C shell.   Type help or ? to list commands.\n'
    prompt = 'p2c$ '
    file = None

    def __init__(self, completekey = "tab", stdin = None, stdout = None, queue = None):
        super().__init__(completekey, stdin, stdout)
        self.queue = queue

    def do_exit(self, arg):
        'Command to exit P2C cli'
        return CmdExit(arg)

    def do_project(self, arg):
        'Command to manage P2C project'
        return CmdProject(arg)

    def do_node(self, arg):
        'Command to manage Node of a P2C project'
        return CmdNode(arg)

    # def do_loglevel(self, arg):
    #     cmd = CmdLoglevel()
    #     cmd._parse_param(arg)
    #     return cmd

    def postcmd(self, stop, line):
        logger.debug(f"postcmd for the line {line=} is about to be run")
        if stop != None:
            self.queue.put(stop)
