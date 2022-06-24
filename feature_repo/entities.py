from tecton import Entity

user = Entity(
    name='user',
    join_keys=['user_id'],
    description='A user of the platform',
    owner='david@tecton.ai',
    tags={'release': 'production'}
)

movie = Entity(
    name='movie',
    join_keys=['movie_id'],
    description='A movie',
    owner='david@tecton.ai',
    tags={'release': 'production'}
)
