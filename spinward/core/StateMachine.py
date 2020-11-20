#   StateMachine.py

"""
State machine implementation.

Dispatches to event handler methods whose names
follow the naming convention:
    state_(currentState)_(event)
"""


class StateError(Exception):
    pass


class StateMachine(object):
    """
    State machine mixin class.

    This class dispatches state-affecting events to
    calls to class methods for easy processing.

    The central method is state_machine_event. Call this
    method with an event (string, EnumType constant, or ??).
    It will use the event and the object's currentState
    to look up the appropriate event handler.

    SUBCLASS RESPONSIBILITIES:

    Subclasses must implement _get_current_state:

        def _get_current_state(self)
            Return the current state, in whatever form it is
            normally used for the class.

    If the state is not stored as a string, the subclass
    must implement _get_state_string:

        def _get_state_string(self, state)
            Translate a state value into a string representation.
            If using EnumType for the state, this method can
            simply return <EnumTypeSubclass>[state]

    If the event is not a string, the subclass
    must implement _get_event_string:

        def _get_event_string(self, event)
            Translate an event value into a string representation.
            If using EnumType for the event, this method can
            simply return <EnumTypeSubclass>[event]

    In addition, subclasses must implement a handler for each
    state and event, with this signature:
        def state_[currentState]_[event](self, *args, **kwargs)
    [currentState] is a string representing the current state of the object.
    [event] is a string representing the event to be handled.

    The state transition function must return True if it
    changed the state or False if it did not.

    The state transition function is responsible for
    - pre-transition validation & processing
    - state transition
    - post-transition processing
    """

    def __init__(self, *args, **kwargs):
        # _errorEventHandler is optional
        self._errorEventHandler = None
        # cache event handlers to minimize lookup time
        self._eventHandlers = {}


    def _get_current_state(self):
        """
        Return the current state, in whatever form it is normally used for the class.
        """
        raise NotImplementedError()


    def _get_event_handler(self, event):
        """
        Attempt to locate and return the appropriate event handler
        for the current state and the event.

        If no handler is found, return None.
        """
        # Get current state
        fromState = self._get_current_state()
        handlerKey = (fromState, event)
        handler = self._eventHandlers.get(handlerKey, None)
        if not handler:
            # Locate and cache event handler

            # Convert state value to string
            fromStateStr = self._get_state_string(fromState)
            # Convert event value to string
            eventStr = self._get_event_string(event)
            # Locate event handler
            handlerName = 'state_%s_%s' % (fromStateStr, eventStr)
            handler = getattr(self, handlerName, None)
            if handler:
                self._eventHandlers[handlerKey] = handler
        # Done
        return handler


    def _allowed_events(self, eventsList):
        """
        Return list of valid state events for this object,
        given the current state of the object.
        Each event is returned as (value,string)

        @param eventsList:	List of state machine event values
                            (enumerated, string, whatever).
        """
        allowed = []
        for event in eventsList:
            if self._get_event_handler(event):
                allowed.append(event)
        allowed = [(event, self._get_state_string(event)) for event in allowed]
        return allowed


    def event_is_allowed(self, event):
        """
        Return True if the specified event is allowed in the current state,
        or False if it is not.
        """
        handler = self._get_event_handler(event)
        return (handler is not None)


    def state_machine_event(self, event, *args, **kwargs):
        """
        Attempt to locate and invoke the appropriate event handler
        for the current state and the event.

        To implement an automatic transition, an event handler
        can recursively invoke self.state_machine_event.
        """
        handler = self._get_event_handler(event)
        if not handler:
            # Convert state value to string
            fromStateStr = self._get_state_string(self._get_current_state())
            # Convert event value to string
            eventStr = self._get_event_string(event)
            # Locate event handler
            handlerName = 'state_%s_%s' % (fromStateStr, eventStr)
            if self._errorEventHandler:
                self._errorEventHandler(handlerName, event, *args, **kwargs)
            else:
                raise StateError('No state event handler %s' % handlerName)
        # Invoke state transition method
        handler(*args, **kwargs)


    def _get_state_string(self, state):
        """
        Default implementation: Simply coerce state to string.
        """
        return str(state)


    def _get_event_string(self, event):
        """
        Default implementation: Simply coerce event to string.
        """
        return str(event)


if __name__ == '__main__':

    from EnumType import EnumType

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


    tests = [ # startState, event, endState
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

    smt = SMTest()

    testCount = 0
    passCount = 0
    failCount = 0
    failures = []

    def failure(startState, evt, endState, endStateActual):
        global testCount, failCount
        testCount += 1
        failCount += 1
        startState = Status[startState]
        evt = Events[evt]
        endState = Status[endState]
        endStateActual = Status[endStateActual]
        failures.append('%s/%s -> %s [%s]' % (startState, evt, endState, endStateActual))

    def success(startState, evt, endState):
        global testCount, passCount
        testCount += 1
        passCount += 1

    def report():
        print('TEST RESULTS:')
        print('\tPass count: %4d  (%5.1f%%)' % (passCount, passCount * 100.0 / testCount))
        print('\tFail count: %4d  (%5.1f%%)' % (failCount, failCount * 100.0 / testCount))
        if failCount > 0:
            print('Failures:')
            print('\t' + '\n\t'.join(failures))
            print('FAIL')
        else:
            print('PASS')

    for startState, evt, endState in tests:
        try:
            # Set initial state directly
            smt.status = startState
            # Process event
            smt.state_machine_event(evt)
            # Check final state
            if smt._get_current_state() == endState:
                success(startState, evt, endState)
            else:
                failure(startState, evt, endState, smt._get_current_state())
        except StateError:
            if endState is None:
                success(startState, evt, endState)
            else:
                failure(startState, evt, endState, smt._get_current_state())

    report()
