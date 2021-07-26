from pyvko.api_based import ApiBased
from pyvko.shared.mixins import Events, Groups


class EventsImplementation(ApiBased, Events):
    pass


class GroupsImplementation(ApiBased, Groups):
    pass
