import cmd, sys
from abc import ABC, abstractmethod
import argparse
import threading
import logging
from enum import StrEnum, auto
import shlex

logger = logging.getLogger(__name__)


class P2CArgparse(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        self.error_triggered = True

class Cmd(ABC):
    subparser_name = 'subparser_name'

    def __init__(self, args):
        logger.debug(f"Command '{self}' is about to be run")
        super().__init__()
        self.skip_cmd = False
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

        try:
            parsed_args, unknown_args = parser.parse_known_args(shlex.split(args))
        except argparse.ArgumentError:
            parser.error_triggered = True
            self.skip_cmd = True
            logger.debug(f"Unable to parse command, do nothing of this cmd")
            return

        self.parsed_args = vars(parsed_args)
        self.unknown_args = unknown_args

        if self.unknown_args != []:
            logger.info(f"Arg(s) \'{' '.join(self.unknown_args)}\' does not exist")
            parser.print_help()
            self.skip_cmd = True

        if parser.error_triggered == True:
            self.skip_cmd = True
            return

        self._post_parsing()

    @abstractmethod
    def _post_parsing(self):
        ...

    def _get_default_argparser(self):
        parser = P2CArgparse(prog=self._cmd_name(), exit_on_error=False, add_help=False)

        parser.error_triggered = False

        subparsers = parser.add_subparsers(help='subcommand help', required=True, dest=self.subparser_name)

        subparsers.add_parser('help', help='display this help')

        return parser, subparsers

class CmdExit(Cmd):
    def __init__(self, args):
        super().__init__(args)

    def _cmd_name(self):
        return "exit"

    def _get_argparser(self):
        parser, subparser = self._get_default_argparser()
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
        LIST_       = "list"
        UNKNOWN     = auto()

    def _get_argparser(self):
        parser, subparsers = self._get_default_argparser()
        parser.description = "P2C project manager"
        parser_create      = subparsers.add_parser('create', help='Create a P2C project')
        parser_create.add_argument('name')
        parser_open        = subparsers.add_parser('open', help='Open a P2C project')
        parser_open.add_argument('uid')
        parser_save        = subparsers.add_parser('save', help='Save a P2C project')
        parser_save.add_argument('uid')
        parser_delete      = subparsers.add_parser('delete', help='Delete a P2C project')
        parser_delete.add_argument('uid')
        parser_close       = subparsers.add_parser('close', help='Close a P2C project')
        parser_close.add_argument('uid')
        parser_setactive   = subparsers.add_parser('setactive', help='Set the P2C project as current')
        parser_setactive.add_argument('uid')
        parser_unsetactive = subparsers.add_parser('unsetactive', help='Unset the P2C project as current')
        parser_unsetactive.add_argument('uid')
        parser_list        = subparsers.add_parser('list', help='List open P2C project in the current session')
        return(parser)

    def _post_parsing(self):
        logger.debug(f"Start post parsing for command {self}")
        if self.skip_cmd == False:
            self.subcmd = self.SubCmdProject(self.parsed_args[Cmd.subparser_name])

            if self.subcmd == self.SubCmdProject.UNKNOWN:
                logger.warning("The subcmd parsed is unknown")
            else:
                try:
                    del self.parsed_args[Cmd.subparser_name]
                except KeyError:
                    logger.error("Tried to remove the subcmd from the dict but can't")

            try:
                self.project_name = self.parsed_args["name"]
            except KeyError:
                pass
        else:
            logger.debug("Skip post parsing")

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

class CLIEvent:
    def __init__(self):
        pass

class CLIEventAskSave(CLIEvent):
    def __init__(self):
        pass

class CLIEventExit(CLIEvent):
    def __init__(self):
        super().__init__()

class CLIEventCmdSuccessful(CLIEvent):
    def __init__(self, message):
        super().__init__()
        self.message = message

class CLIEventCmdFailed(CLIEvent):
    def __init__(self):
        super().__init__()

class P2CShell(cmd.Cmd):
    intro = 'Welcome to the P2C shell.   Type help or ? to list commands.\n'
    prompt = 'p2c$ '
    file = None

    def __init__(self, completekey = "tab", stdin = None, stdout = None, queue_output = None, queue_input = None):
        super().__init__(completekey, stdin, stdout)
        self.queue_output = queue_output
        self.queue_input  = queue_input

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
            if stop.skip_cmd == False:
                # Send the command to the exexutor thread
                self.queue_output.put(stop)

                # Wait for a return event
                event = self.queue_input.get()

                if isinstance(event, CLIEventExit):
                    logger.info(f"A exit has been received by the CLI thread")
                    return True
                elif isinstance(event, CLIEventCmdSuccessful):
                    logger.debug(f"Return to CLI with a successful CMD")
                    print(event.message)
        else:
            logger.debug("The command can't be parsed or is skipped")
