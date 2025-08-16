import cmd, sys
from abc import ABC, abstractmethod
import argparse
import threading

class Cmd(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _cmd_name(self):
        ...

    def __str__(self):
        return f"CMD: `{self._cmd_name()}`"

    @abstractmethod
    def _get_argparser(self):
        ...

    # @abstractmethod
    # def _get_help_string(self):
    #     ...

    def _parse_param(self, args):
        parser = self._get_argparser()
        try:
            parsed_args, unknow_args = parser.parse_known_args(args.split())
        except argparse.ArgumentError:
            print("Error, unable to parse args")

        if unknow_args != []:
            print(f"Arg(s) \'{' '.join(unknow_args)}\' does not exist")
            parser.print_help()

        if parsed_args.help:
            parser.print_help()

    def _get_default_argparser(self):
        parser = argparse.ArgumentParser(prog=self._cmd_name(), exit_on_error=False, add_help=False)

        parser.add_argument('--help', action='store_true')

        return parser
    

class CmdExit(Cmd):
    def __init__(self):
        super().__init__()

    def _cmd_name(self):
        return "exit"

    def _get_argparser(self):
        parser = self._get_default_argparser()
        parser.description = "Quit P2C"
        return(parser)
    
class CmdCreatePrj(Cmd):
    def __init__(self):
        super().__init__()

    def _cmd_name(self):
        return "create_prj"

    def _get_argparser(self):
        parser = self._get_default_argparser()
        parser.description = "Create a new P2C project"
        parser.add_argument("name", required=True)
        return(parser)
    
class CmdCreateNode(Cmd):
    def __init__(self):
        super().__init__()

    def _cmd_name(self):
        return "exit"

    def _get_argparser(self):
        parser = self._get_default_argparser()
        parser.description = "Quit P2C"
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
        cmd = CmdExit()
        cmd._parse_param(arg)
        return cmd

    # def do_loglevel(self, arg):
    #     cmd = CmdLoglevel()
    #     cmd._parse_param(arg)
    #     return cmd

    # Node commands
    def do_create_node(self, arg):
        'Create a node'

    def do_delete_node(self, arg):
        pass
    
    def do_edit_node(self, arg):
        pass

    def do_move_node(self, arg):
        pass

    # Link commands
    def do_link(self, arg):
        pass

    def do_unlink(self, arg):
        pass

    # List elements
    def do_lisl(self, arg):
        pass

    # Project management
    def do_open_prj(self, arg):
        pass

    def do_create_prj(self, arg):
        print("OMMGGGG")
        cmd = CmdCreateNode()
        cmd._parse_param(arg)
        return cmd

    def do_save_prj(self, arg):
        pass

    def postcmd(self, stop, line):
        if stop != None:
            self.queue.put(stop)
