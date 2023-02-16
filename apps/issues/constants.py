from collections import OrderedDict


class Type:
    TASK = 'task'
    BUG = 'bug'
    STORY = 'story'

    FieldStr = OrderedDict({
        TASK: 'Task',
        BUG: 'Bug',
        STORY: 'Story'
    })

    @classmethod
    def choices(cls):
        return cls.FieldStr.items()


class Status:
    PENDING = 'pending'
    MOVE_TO_DEVELOPMENT = 'move_to_development'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'

    FieldStr = OrderedDict({
        PENDING: 'Pending',
        MOVE_TO_DEVELOPMENT: 'Move_to_development',
        IN_PROGRESS: 'In_progress',
        DONE: 'Done'
    })

    @classmethod
    def choices(cls):
        return cls.FieldStr.items()


class Priority:
    HIGHEST = 'highest'
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'
    LOWEST = 'lowest'

    FieldStr = OrderedDict({
        HIGHEST: 'Highest',
        HIGH: 'High',
        MEDIUM: 'Medium',
        LOW: 'Low',
        LOWEST: 'Lowest'
    })

    @classmethod
    def choices(cls):
        return cls.FieldStr.items()