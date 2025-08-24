from statemachine import State
from statemachine import StateMachine
from cli import Cmd, CmdProject

import logging

logger = logging.getLogger(__name__)

class FSMProjectManager(StateMachine):
    s_idle         = State(initial=True)
    s_create       = State()
    s_open_project = State()
    s_delete       = State()
    s_close        = State()
    s_unactive     = State()
    s_active       = State()
    s_edited   = State()
    s_save     = State()


    # t_idle = s_idle.to.itself()

    t_create      = s_idle.to(s_create)
    t_create_done = s_create.to(s_unactive)

    t_open      = s_idle.to(s_open_project)
    t_open_done = s_open_project.to(s_unactive)

    # t_unactive = s_unactive.to.itself()

    t_set_active   = s_unactive.to(s_active)
    t_set_unactive = s_active.to(s_unactive)

    # t_active = s_active.to.itself()

    t_edited   = s_active.to(s_edited)

    # t_edited = s_edited.to.itself()

    t_save      = s_edited.to(s_save)
    t_save_done = s_save.to(s_active)

    t_close      = s_unactive.to(s_close)
    t_close_done = s_close.to(s_idle)

    t_delete      = s_unactive.to(s_delete)
    t_delete_done = s_delete.to(s_idle)

    def on_enter_s_create(self):
        logger.debug("FSM: exec create state")

        # Do somethings

        self.send("t_create_done")

    def on_enter_s_open_project(self):
        logger.debug("FSM: exec open project state")

        # Do somethings

        self.send("t_open_done")

    def on_enter_s_delete(self):
        logger.debug("FSM: exec delete state")

        # Do somethings

        self.send("t_delete_done")

    def on_enter_s_close(self):
        logger.debug("FSM: exec close state")

        # Do somethings

        self.send("t_close_done")

    def on_enter_s_unactive(self):
        logger.debug("FSM: exec unactive state")

    def on_enter_s_active(self):
        logger.debug("FSM: exec active state")

    def on_enter_s_edited(self):
        logger.debug("FSM: exec edited state")

    def on_enter_s_save(self):
        logger.debug("FSM: exec save state")

        # Do somethings

        self.send("t_save_done")

    def send_cmd_event(self, event, cmd):
        self.cmd = cmd
        self.send(event)

    def is_active(self):
        if self.current_state == self.s_active or self.current_state == self.s_edited or self.current_state == self.s_save:
            return True
        return False