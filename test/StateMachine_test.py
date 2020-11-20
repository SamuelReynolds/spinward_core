import unittest

from spinward.core.EnumType import EnumType
from spinward.core.StateMachine import StateMachine, StateError

Status = EnumType('Unknown', 'A', 'B', 'C', 'D')
Events = EnumType('E1', 'E2', 'E3', 'autotransition_')


class SMTest(StateMachine):

    def __init__(self, *args, **kwargs):
        super(SMTest, self).__init__(*args, **kwargs)
        self.status = Status.Unknown

    def _get_current_state(self):
        """
        Return string representation of current state.
        """
        return self.status

    def _get_state_string(self, state):
        return Status[state]

    def _get_event_string(self, event):
        return Events[event]

    def state_Unknown_E1(self, *args, **kwargs):
        #  Unknown -> A
        self.status = Status.A

    def state_A_E1(self, *args, **kwargs):
        #  A -> A
        self.status = Status.A

    def state_A_E2(self, *args, **kwargs):
        #  A -> B
        self.status = Status.B

    def state_B_E2(self, *args, **kwargs):
        #  B -> C
        self.status = Status.C

    def state_B_E3(self, *args, **kwargs):
        #  B -> D
        self.status = Status.D

    def state_C_E1(self, *args, **kwargs):
        #  C -> A
        self.status = Status.A

    def state_D_E1(self, *args, **kwargs):
        #  D -> A
        self.status = Status.A


class TestStateMachine(unittest.TestCase):

    def setUp(self):
        self.smt = SMTest()

    # def test___init__(self):
    #     # state_machine = StateMachine(*args, **kwargs)
    #     assert False # TODO: implement your test here

    def test_event_is_allowed(self):
        tests = [   # startState, event, endState
                [Status.Unknown, Events.E1, True],
                [Status.Unknown, Events.E2, False],
                [Status.Unknown, Events.E3, False],
                [Status.Unknown, Events.autotransition_, False],
                [Status.A, Events.E1, True],
                [Status.A, Events.E2, True],
                [Status.A, Events.E3, False],
                [Status.A, Events.autotransition_, False],
                [Status.B, Events.E1, False],
                [Status.B, Events.E2, True],
                [Status.B, Events.E3, True],
                [Status.B, Events.autotransition_, False],
                [Status.C, Events.E1, True],
                [Status.C, Events.E2, False],
                [Status.C, Events.E3, False],
                [Status.C, Events.autotransition_, False],
                [Status.D, Events.E1, True],
                [Status.D, Events.E2, False],
                [Status.D, Events.E3, False],
                [Status.D, Events.autotransition_, False],
            ]
        for startState, evt, expect in tests:
            # Set initial state directly
            self.smt.status = startState
            # Process event
            self.assertEqual(expect, self.smt.event_is_allowed(evt))

    def test_state_machine_event(self):
        tests = [   # startState, event, endState
                [Status.Unknown, Events.E1, Status.A],
                [Status.Unknown, Events.E2, None],
                [Status.Unknown, Events.E3, None],
                [Status.A, Events.E1, Status.A],
                [Status.A, Events.E2, Status.B],
                [Status.A, Events.E3, None],
                [Status.B, Events.E1, None],
                [Status.B, Events.E2, Status.C],
                [Status.B, Events.E3, Status.D],
                [Status.C, Events.E1, Status.A],
                [Status.C, Events.E2, None],
                [Status.C, Events.E3, None],
                [Status.D, Events.E1, Status.A],
                [Status.D, Events.E2, None],
                [Status.D, Events.E3, None],
            ]
        for startState, evt, endState in tests:
            try:
                # Set initial state directly
                self.smt.status = startState
                # Process event
                self.smt.state_machine_event(evt)
                # Check final state
                self.assertEqual(self.smt._get_current_state(), endState)
            except StateError:
                self.failIf(endState is not None, '%s/%s -> %s [%s]'
                            % (startState, evt, endState, self.smt._get_current_state()))


if __name__ == '__main__':
    unittest.main()
