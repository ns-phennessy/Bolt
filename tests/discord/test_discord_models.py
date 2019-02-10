import unittest
from bolt.discord.models.base import Model, Field, ListField
from bolt.discord.models.base import ModelMissingRequiredKeyError, ModelValidationError
from bolt.discord.models.user import User
from bolt.discord.models.embed import Embed
from bolt.discord.models.channel import Channel, ChannelType
from bolt.discord.models.guild import Guild

class TestDiscordModel(unittest.TestCase):
    def test_user(self):
        input = {
            "id": "80351110224678912",
            "username": "Nelly",
            "discriminator": "1337",
            "avatar": "8342729096ea3675442027381ff50dfe",
            "verified": True,
            "email": "nelly@discordapp.com",
            "flags": 64,
            "premium_type": 1
        }

        actual = User.marshal(input)

        self.assertEqual(actual.id, input['id'])
        self.assertEqual(actual.name, input['username'])
        self.assertEqual(actual.email, input['email'])

        serialized = actual.serialize()
        self.assertEqual(serialized['id'], input['id'])
        self.assertEqual(serialized['username'], input['username'])
        self.assertEqual(serialized['email'], input['email'])

    def test_embed(self):
        input = {
            "title": "Title",
            "description": "Description",
            "url": "https://discordapp.com",
            "color": 2710212,
            "timestamp": "2015-04-26T06:26:56.936000+00:00",
            "footer": {
                "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png",
                "text": "footer text"
            },
            "thumbnail": {
                "url": "https://cdn.discordapp.com/embed/avatars/0.png"
            },
            "image": {
                "url": "https://cdn.discordapp.com/embed/avatars/0.png"
            },
            "author": {
                "name": "author name",
                "url": "https://discordapp.com",
                "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png"
            },
            "fields": [
                {
                    "name": "Field 1",
                    "value": "Lorum Ipsum",
                },
                {
                    "name": "Field 2",
                    "value": "Lorum Ipsum",
                    "inline": True
                }
            ]
        }

        actual = Embed.marshal(input)

        self.assertEqual(actual.title, input['title'])
        self.assertEqual(actual.url, input['url'])
        self.assertEqual(actual.fields[1].name, input['fields'][1]['name'])

        serialized = actual.serialize()
        self.assertEqual(serialized['title'], input['title'])
        self.assertDictEqual(serialized['fields'][1], input['fields'][1])

    def test_embed_long_input(self):
        with self.assertRaises(ModelValidationError):
            Embed.marshal({"title": "t" * 512,})

        with self.assertRaises(ModelValidationError):
            Embed.marshal({"description": "t" * 4096,})

        with self.assertRaises(ModelValidationError):
            Embed.marshal({"fields": [{"name": "name", "value": "value"} for f in range(0,50)]})

    def test_channel_text(self):
        input = {
            "id": "41771983423143937",
            "guild_id": "41771983423143937",
            "name": "general",
            "type": 0,
            "position": 6,
            "permission_overwrites": [],
            "rate_limit_per_user": 2,
            "nsfw": True,
            "topic": "24/7 chat about how to gank Mike #2",
            "last_message_id": "155117677105512449",
            "parent_id": "399942396007890945"
        }

        actual = Channel.marshal(input)

        self.assertEqual(actual.id, input['id'])
        self.assertEqual(actual.name, input['name'])
        self.assertEqual(actual.last_message_id, input['last_message_id'])
        self.assertEqual(actual.type, ChannelType.GUILD_TEXT)

        serialized = actual.serialize()
        self.assertEqual(serialized['id'], input['id'])
        self.assertEqual(serialized['topic'], input['topic'])
        self.assertEqual(serialized['nsfw'], input['nsfw'])

    def test_channel_voice(self):
        input = {
            "id": "155101607195836416",
            "guild_id": "41771983423143937",
            "name": "ROCKET CHEESE",
            "type": 2,
            "nsfw": False,
            "position": 5,
            "permission_overwrites": [],
            "bitrate": 64000,
            "user_limit": 0,
            "parent_id": None
        }

        actual = Channel.marshal(input)

        self.assertEqual(actual.id, input['id'])
        self.assertEqual(actual.guild_id, input['guild_id'])
        self.assertEqual(actual.type, ChannelType.GUILD_VOICE)

        serialized = actual.serialize()
        self.assertEqual(serialized['id'], input['id'])
        self.assertEqual(serialized['nsfw'], input['nsfw'])

    def test_channel_dm(self):
        input = {
            "id": "319674150115610528",
            "last_message_id": "3343820033257021450",
            "type": 1,
            "recipients": [
                {
                    "username": "test",
                    "discriminator": "9999",
                    "id": "82198898841029460",
                    "avatar": "33ecab261d4681afa4d85a04691c4a01"
                }
            ]
        }
        actual = Channel.marshal(input)

        self.assertEqual(actual.id, input['id'])
        self.assertEqual(actual.last_message_id, input['last_message_id'])
        self.assertEqual(actual.type, ChannelType.DM)
        self.assertTrue(isinstance(actual.recipients[0], User))
        self.assertTrue(len(actual.recipients) == len(input['recipients']))

        serialized = actual.serialize()
        self.assertEqual(serialized['id'], input['id'])
        self.assertEqual(serialized['recipients'][0]['id'], input['recipients'][0]['id'])

    def test_channel_group_dm(self):
        input = {
            "name": "Some test channel",
            "icon": None,
            "recipients": [
                {
                    "username": "test",
                    "discriminator": "9999",
                    "id": "82198898841029460",
                    "avatar": "33ecab261d4681afa4d85a04691c4a01"
                },
                {
                    "username": "test2",
                    "discriminator": "9999",
                    "id": "82198810841029460",
                    "avatar": "33ecab261d4681afa4d85a10691c4a01"
                }
            ],
            "last_message_id": "3343820033257021450",
            "type": 3,
            "id": "319674150115710528",
            "owner_id": "82198810841029460"
        }
        actual = Channel.marshal(input)

        self.assertEqual(actual.id, input['id'])
        self.assertEqual(actual.last_message_id, input['last_message_id'])
        self.assertEqual(actual.type, ChannelType.GROUP_DM)
        self.assertTrue(isinstance(actual.recipients[0], User))
        self.assertTrue(len(actual.recipients) == len(input['recipients']))

        serialized = actual.serialize()
        self.assertEqual(serialized['id'], input['id'])
        self.assertEqual(serialized['recipients'][0]['id'], input['recipients'][0]['id'])

    def test_channel_category(self):
        input = {
            "permission_overwrites": [],
            "name": "Test",
            "parent_id": None,
            "nsfw": False,
            "position": 0,
            "guild_id": "290926798629997250",
            "type": 4,
            "id": "399942396007890945"
        }
        actual = Channel.marshal(input)

        self.assertEqual(actual.id, input['id'])
        self.assertEqual(actual.type, ChannelType.GUILD_CATEGORY)
        self.assertTrue(len(actual.recipients) == 0)

        serialized = actual.serialize()
        self.assertEqual(serialized['id'], input['id'])

    def test_guild_basic(self):
        input = {
            "id": "41771983423143937",
            "application_id": None,
            "name": "Discord Developers",
            "icon": "86e39f7ae3307e811784e2ffd11a7310",
            "splash": None,
            "owner_id": "80351110224678912",
            "region": "us-east",
            "afk_channel_id": "42072017402331136",
            "afk_timeout": 300,
            "embed_enabled": True,
            "embed_channel_id": "41771983444115456",
            "verification_level": 1,
            "default_message_notifications": 0,
            "explicit_content_filter": 0,
            "mfa_level": 0,
            "widget_enabled": False,
            "widget_channel_id": "41771983423143937",
            "roles": [],
            "emojis": [],
            "features": ["INVITE_SPLASH"],
            "unavailable": False
        }
        actual = Guild.marshal(input)
