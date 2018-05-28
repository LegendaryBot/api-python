import boto3
import os
from botocore.exceptions import ClientError

from wow.wowcharacter import WoWCharacter

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE_DISCORD_USER"))


class DiscordUser:

    def __init__(self, user_id):
        if not isinstance(user_id, int):
            raise TypeError('Expected int parameter, received %s instead.' % user_id.__class__.__name__)
        self.user_id = user_id
        self.characters = []
        self.__initialize_characters()

    def has_character(self, region, realm, name):
        """Check if a discord user has a certain character. """
        return self.characters.__contains__(WoWCharacter(region, realm, name))

    def compare_characters(self, character_list, otherway=False):
        """Gives the characters that are not in the given list"""
        if otherway:
            return list(set(character_list) - set(self.characters))
        else:
            return list(set(self.characters) - set(character_list))

    def get_main_character_for_guild(self, guild_id):
        if not isinstance(guild_id, int):
            raise TypeError('Expected int parameter, received %s instead.' % guild_id.__class__.__name__)
        for character in self.characters:
            if guild_id in character.main_char_for_guild:
                return character

    def remove_character(self, character):
        if not isinstance(character, WoWCharacter):
            raise TypeError('Expected WoWCharacter parameter, received %s instead.' % character.__class__.__name__)
        self.characters.remove(character)

    def add_character(self, character):
        if not isinstance(character, WoWCharacter):
            raise TypeError('Expected WoWCharacter parameter, received %s instead.' % character.__class__.__name__)
        self.characters.append(character)

    def save(self):
        json_entry = {
            "characters": []
        }
        for character in self.characters:
            if character.guild is not None:
                json_entry['characters'].append({
                    "region": character.region,
                    "realm": character.realm,
                    "name": character.name,
                    "guild": character.guild,
                    "mainCharacterForGuild": character.main_char_for_guild
                })
            else:
                json_entry['characters'].append({
                    "region": character.region,
                    "realm": character.realm,
                    "name": character.name,
                    "mainCharacterForGuild": character.main_char_for_guild
                })
        table.put_item(
            Item={
                'id': self.user_id,
                'json': json_entry
            }
        )

    def __initialize_characters(self):
        """Initialize the list of characters of the user."""
        if not self.characters:
            try:
                response_entry = table.get_item(
                    Key={
                        'id': self.user_id
                    }
                )
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                if 'Item' in response_entry and 'json' in response_entry['Item'] and 'characters' in \
                        response_entry['Item'][
                            'json']:
                    json_entry = response_entry['Item']['json']['characters']
                    for character in json_entry:
                        if 'guild' in character and 'mainCharacterForGuild' in character:
                            self.characters.append(
                                WoWCharacter(character['region'], character['realm'], character['name'],
                                             character['guild'],
                                             character['mainCharacterForGuild']))
                        elif 'guild' in character and 'mainCharacterForGuild' not in character:
                            self.characters.append(
                                WoWCharacter(character['region'], character['realm'], character['name'],
                                             character['guild'],
                                             ))
                        elif 'guild' not in character and 'mainCharacterForGuild' in character:
                            self.characters.append(
                                WoWCharacter(character['region'], character['realm'], character['name'], None,
                                             character['mainCharacterForGuild']))
                        else:
                            self.characters.append(
                                WoWCharacter(character['region'], character['realm'], character['name']))
