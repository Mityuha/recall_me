from ..types import BACK_ARROW, DELETE_EVENT, AllEventsState  # noqa

# State = AllEventsState

# class ScreenStateMachine:
#     def __init__(self) -> None:
#         self.machine: Machine = Machine(
#             model=self,
#             states=AllEventsState,
#             initial=AllEventsState.NO_MESSAGE,
#         )

#     self.machine.add_transition("message_sent", State.NO_MESSAGE, State.CMD_ALL_EVENTS_SCREEN,)
#     self.machine.add_transition("cron_message_sent", State.NO_MESSAGE, State.CRON_ALL_EVENTS_SCREEN,)
#     self.machine.add_transition("")
