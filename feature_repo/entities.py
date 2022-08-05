from tecton import Entity

user = Entity(
    name='user',
    join_keys=['USER_ID'],
    description='A user of the platform',
    owner='david@tecton.ai',
    tags={'release': 'production'}
)

movie = Entity(
    name='movie',
    join_keys=['MOVIE_ID'],
    description='A movie',
    owner='david@tecton.ai',
    tags={'release': 'production'}
)
