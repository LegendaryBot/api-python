class WoWCharacter:

    def __init__(self, region, realm, name, guild=None, main_char_for_guild=None):
        if main_char_for_guild is None:
            main_char_for_guild = []
        if not isinstance(region, str):
            raise TypeError('Expected str parameter, received %s instead.' % region.__class__.__name__)
        if not isinstance(realm, str):
            raise TypeError('Expected str parameter, received %s instead.' % realm.__class__.__name__)
        if not isinstance(name, str):
            raise TypeError('Expected str parameter, received %s instead.' % name.__class__.__name__)
        if guild is not None and not isinstance(guild, str):
            raise TypeError('Expected str parameter, received %s instead.' % guild.__class__.__name__)

        self.region = region
        self.realm = realm
        self.name = name
        self.guild = guild
        self.main_char_for_guild = main_char_for_guild

    def __eq__(self, other):
        return (self.region, self.realm, self.name) == (other.region, other.realm, other.name)

    def __hash__(self):
        return hash((self.region, self.realm, self.name))

    def __repr__(self):
        return '({},{},{},{},{})'.format(self.region, self.realm, self.name, self.guild, self.main_char_for_guild)

    def __str__(self):
        return "Region=%s, Realm=%s, Name=%s, Guild=%s, main_char_for_guild=%s" % (self.region, self.realm, self.name, self.guild, self.main_char_for_guild)
