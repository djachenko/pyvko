from pyvko.api_based import ApiBased
from pyvko.shared.mixins.events import Events
from pyvko.shared.mixins.groups import Groups


class EventsImplementation(ApiBased, Events):
    pass


class GroupsImplementation(ApiBased, Groups):
    pass
