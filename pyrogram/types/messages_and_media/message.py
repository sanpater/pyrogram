#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import logging
from datetime import datetime
from functools import partial
from typing import List, Match, Union, BinaryIO, Optional, Callable

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram import utils
from pyrogram.errors import ChannelPrivate, MessageIdsEmpty, PeerIdInvalid, ChannelForumMissing
from pyrogram.parser import utils as parser_utils, Parser
from ..object import Object
from ..update import Update

log = logging.getLogger(__name__)


class Str(str):
    def __init__(self, *args):
        super().__init__()

        self.entities: Optional[List["types.MessageEntity"]] = None

    def init(self, entities: list):
        self.entities = entities

        return self

    @property
    def markdown(self) -> str:
        return Parser.unparse(self, self.entities, False)

    @property
    def html(self) -> str:
        return Parser.unparse(self, self.entities, True)

    def __getitem__(self, item) -> str:
        return parser_utils.remove_surrogates(parser_utils.add_surrogates(self)[item])


class Message(Object, Update):
    """A message.

    Parameters:
        id (``int``):
            Unique message identifier inside this chat.

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            Sender, empty for messages sent to channels.

        sender_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Sender of the message, sent on behalf of a chat.
            The channel itself for channel messages.
            The supergroup itself for messages from anonymous group administrators.
            The linked channel for messages automatically forwarded to the discussion group.

        sender_boost_count (``int``, *optional*):
            If the sender of the message boosted the chat, the number of boosts added by the user.

        sender_business_bot (:obj:`~pyrogram.types.User`, *optional*):
            The bot that actually sent the message on behalf of the business account. Available only for outgoing messages sent on behalf of the connected business account.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the message was sent.

        chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Conversation the message belongs to.

        topic_message (``bool``, *optional*):
            True, if the message is sent to a forum topic.

        automatic_forward (``bool``, *optional*):
            True, if the message is a channel post that was automatically forwarded to the connected discussion group.

        from_offline (``bool``, *optional*):
            True, if the message was sent by an implicit action, for example, as an away or a greeting business message, or as a scheduled message.

        topic (:obj:`~pyrogram.types.ForumTopic`, *optional*):
            Topic the message belongs to.

        forward_from (:obj:`~pyrogram.types.User`, *optional*):
            For forwarded messages, sender of the original message.

        forward_sender_name (``str``, *optional*):
            For messages forwarded from users who have hidden their accounts, name of the user.

        forward_from_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            For messages forwarded from channels, information about the original channel. For messages forwarded from anonymous group administrators, information about the original supergroup.

        forward_from_message_id (``int``, *optional*):
            For messages forwarded from channels, identifier of the original message in the channel.

        forward_signature (``str``, *optional*):
            For messages forwarded from channels, signature of the post author if present.

        forward_date (:py:obj:`~datetime.datetime`, *optional*):
            For forwarded messages, date the original message was sent.

        message_thread_id (``int``, *optional*):
            Unique identifier of a message thread to which the message belongs.
            For supergroups only.

        effect_id (``int``, *optional*):
            Unique identifier of the message effect.
            For private chats only.

        reply_to_message_id (``int``, *optional*):
            The id of the message which this message directly replied to.

        reply_to_story_id (``int``, *optional*):
            The id of the story which this message directly replied to.

        reply_to_story_user_id (``int``, *optional*):
            The id of the story sender which this message directly replied to.

        reply_to_top_message_id (``int``, *optional*):
            The id of the first message which started this message thread.

        reply_to_message (:obj:`~pyrogram.types.Message`, *optional*):
            For replies, the original message. Note that the Message object in this field will not contain
            further reply_to_message fields even if it itself is a reply.

        reply_to_story (:obj:`~pyrogram.types.Story`, *optional*):
            For replies, the original story.

        mentioned (``bool``, *optional*):
            The message contains a mention.

        empty (``bool``, *optional*):
            The message is empty.
            A message can be empty in case it was deleted or you tried to retrieve a message that doesn't exist yet.

        service (:obj:`~pyrogram.enums.MessageServiceType`, *optional*):
            The message is a service message.
            This field will contain the enumeration type of the service message.
            You can use ``service = getattr(message, message.service.value)`` to access the service message.

        media (:obj:`~pyrogram.enums.MessageMediaType`, *optional*):
            The message is a media message.
            This field will contain the enumeration type of the media message.
            You can use ``media = getattr(message, message.media.value)`` to access the media message.

        paid_media (:obj:`~pyrogram.types.PaidMediaInfo`, *optional*):
            The message is a paid media message.

        show_caption_above_media (``bool``, *optional*):
            If True, caption must be shown above the message media.

        edit_date (:py:obj:`~datetime.datetime`, *optional*):
            Date the message was last edited.

        edit_hidden (``bool``, *optional*):
            The message shown as not modified.
            A message can be not modified in case it has received a reaction.

        media_group_id (``int``, *optional*):
            The unique identifier of a media message group this message belongs to.

        author_signature (``str``, *optional*):
            Signature of the post author for messages in channels, or the custom title of an anonymous group
            administrator.

        has_protected_content (``bool``, *optional*):
            True, if the message can't be forwarded.

        has_media_spoiler (``bool``, *optional*):
            True, if the message media is covered by a spoiler animation.

        text (``str``, *optional*):
            For text messages, the actual UTF-8 text of the message, 0-4096 characters.
            If the message contains entities (bold, italic, ...) you can access *text.markdown* or
            *text.html* to get the marked up message text. In case there is no entity, the fields
            will contain the same text as *text*.

        quote_text (``str``, *optional*):
            For quote messages, the actual UTF-8 text of the message, 0-4096 characters.
            If the quote contains entities (bold, italic, ...) you can access *text.markdown* or
            *text.html* to get the marked up message text. In case there is no entity, the fields
            will contain the same text as *text*.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear
            in the caption.

        quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For quote messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        audio (:obj:`~pyrogram.types.Audio`, *optional*):
            Message is an audio file, information about the file.

        document (:obj:`~pyrogram.types.Document`, *optional*):
            Message is a general file, information about the file.

        photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Message is a photo, information about the photo.

        sticker (:obj:`~pyrogram.types.Sticker`, *optional*):
            Message is a sticker, information about the sticker.

        animation (:obj:`~pyrogram.types.Animation`, *optional*):
            Message is an animation, information about the animation.

        game (:obj:`~pyrogram.types.Game`, *optional*):
            Message is a game, information about the game.

        giveaway (:obj:`~pyrogram.types.Giveaway`, *optional*):
            Message is a giveaway, information about the giveaway.

        invoice (:obj:`~pyrogram.types.Invoice`, *optional*):
            Message is a invoice, information about the invoice.
            `More about payments » <https://core.telegram.org/bots/api#payments>`_

        story (:obj:`~pyrogram.types.Story`, *optional*):
            Message is a story, information about the story.

        video (:obj:`~pyrogram.types.Video`, *optional*):
            Message is a video, information about the video.

        video_processing_pending (``bool``, *optional*):
            True, if the video is still processing.

        alternative_videos (List of :obj:`~pyrogram.types.Video`, *optional*):
            Alternative qualities of the video, if the message is a video.

        voice (:obj:`~pyrogram.types.Voice`, *optional*):
            Message is a voice message, information about the file.

        video_note (:obj:`~pyrogram.types.VideoNote`, *optional*):
            Message is a video note, information about the video message.

        caption (``str``, *optional*):
            Caption for the audio, document, photo, video or voice, 0-1024 characters.
            If the message contains caption entities (bold, italic, ...) you can access *caption.markdown* or
            *caption.html* to get the marked up caption text. In case there is no caption entity, the fields
            will contain the same text as *caption*.

        contact (:obj:`~pyrogram.types.Contact`, *optional*):
            Message is a shared contact, information about the contact.

        location (:obj:`~pyrogram.types.Location`, *optional*):
            Message is a shared location, information about the location.

        venue (:obj:`~pyrogram.types.Venue`, *optional*):
            Message is a venue, information about the venue.

        web_page (:obj:`~pyrogram.types.WebPage`, *optional*):
            Message was sent with a webpage preview.

        poll (:obj:`~pyrogram.types.Poll`, *optional*):
            Message is a native poll, information about the poll.

        dice (:obj:`~pyrogram.types.Dice`, *optional*):
            A dice containing a value that is randomly generated by Telegram.

        new_chat_members (List of :obj:`~pyrogram.types.User`, *optional*):
            New members that were added to the group or supergroup and information about them
            (the bot itself may be one of these members).

        left_chat_member (:obj:`~pyrogram.types.User`, *optional*):
            A member was removed from the group, information about them (this member may be the bot itself).

        chat_join_type (:obj:`~pyrogram.enums.ChatJoinType`, *optional*):
            This field will contain the enumeration type of how the user had joined the chat.

        new_chat_title (``str``, *optional*):
            A chat title was changed to this value.

        new_chat_photo (:obj:`~pyrogram.types.Photo`, *optional*):
            A chat photo was change to this value.

        delete_chat_photo (``bool``, *optional*):
            Service message: the chat photo was deleted.

        group_chat_created (``bool``, *optional*):
            Service message: the group has been created.

        supergroup_chat_created (``bool``, *optional*):
            Service message: the supergroup has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a
            supergroup when it is created. It can only be found in reply_to_message if someone replies to a very
            first message in a directly created supergroup.

        channel_chat_created (``bool``, *optional*):
            Service message: the channel has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a
            channel when it is created. It can only be found in reply_to_message if someone replies to a very
            first message in a channel.

        migrate_to_chat_id (``int``, *optional*):
            The group has been migrated to a supergroup with the specified identifier.
            This number may be greater than 32 bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float
            type are safe for storing this identifier.

        migrate_from_chat_id (``int``, *optional*):
            The supergroup has been migrated from a group with the specified identifier.
            This number may be greater than 32 bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float
            type are safe for storing this identifier.

        pinned_message (:obj:`~pyrogram.types.Message`, *optional*):
            Specified message was pinned.
            Note that the Message object in this field will not contain further reply_to_message fields even if it
            is itself a reply.

        game_high_score (:obj:`~pyrogram.types.GameHighScore`, *optional*):
            The game score for a user.
            The reply_to_message field will contain the game Message.

        views (``int``, *optional*):
            Channel post views.

        forwards (``int``, *optional*):
            Channel post forwards.

        via_bot (:obj:`~pyrogram.types.User`):
            The information of the bot that generated the message from an inline query of a user.

        outgoing (``bool``, *optional*):
            Whether the message is incoming or outgoing.
            Messages received from other chats are incoming (*outgoing* is False).
            Messages sent from yourself to other chats are outgoing (*outgoing* is True).
            An exception is made for your own personal chat; messages sent there will be incoming.

        quote (``bool``, *optional*):
            If True, message contains a quote.

        matches (List of regex Matches, *optional*):
            A list containing all `Match Objects <https://docs.python.org/3/library/re.html#match-objects>`_ that match
            the text of this message. Only applicable when using :obj:`Filters.regex <pyrogram.Filters.regex>`.

        command (List of ``str``, *optional*):
            A list containing the command and its arguments, if any.
            E.g.: "/start 1 2 3" would produce ["start", "1", "2", "3"].
            Only applicable when using :obj:`~pyrogram.filters.command`.

        forum_topic_created (:obj:`~pyrogram.types.ForumTopicCreated`, *optional*):
            Service message: forum topic created

        forum_topic_closed (:obj:`~pyrogram.types.ForumTopicClosed`, *optional*):
            Service message: forum topic closed

        forum_topic_reopened (:obj:`~pyrogram.types.ForumTopicReopened`, *optional*):
            Service message: forum topic reopened

        forum_topic_edited (:obj:`~pyrogram.types.ForumTopicEdited`, *optional*):
            Service message: forum topic edited

        general_topic_hidden (:obj:`~pyrogram.types.GeneralTopicHidden`, *optional*):
            Service message: forum general topic hidden

        general_topic_unhidden (:obj:`~pyrogram.types.GeneralTopicUnhidden`, *optional*):
            Service message: forum general topic unhidden

        video_chat_scheduled (:obj:`~pyrogram.types.VideoChatScheduled`, *optional*):
            Service message: voice chat scheduled.

        video_chat_started (:obj:`~pyrogram.types.VideoChatStarted`, *optional*):
            Service message: the voice chat started.

        video_chat_ended (:obj:`~pyrogram.types.VideoChatEnded`, *optional*):
            Service message: the voice chat has ended.

        video_chat_members_invited (:obj:`~pyrogram.types.VoiceChatParticipantsInvited`, *optional*):
            Service message: new members were invited to the voice chat.

        phone_call_started (:obj:`~pyrogram.types.PhoneCallStarted`, *optional*):
            Service message: phone call started.

        phone_call_ended (:obj:`~pyrogram.types.PhoneCallEnded`, *optional*):
            Service message: phone call ended.

        web_app_data (:obj:`~pyrogram.types.WebAppData`, *optional*):
            Service message: web app data sent to the bot.

        gift_code (:obj:`~pyrogram.types.GiftCode`, *optional*):
            Service message: gift code information.

        gift (:obj:`~pyrogram.types.Gift`, *optional*):
            Service message: star gift information.

        requested_chats (:obj:`~pyrogram.types.RequestedChats`, *optional*):
            Service message: requested chats information.

        successful_payment (:obj:`~pyrogram.types.SuccessfulPayment`, *optional*):
            Service message: successful payment.

        refunded_payment (:obj:`~pyrogram.types.RefundedPayment`, *optional*):
            Service message: refunded payment.

        giveaway_created (``bool``, *optional*):
            Service message: giveaway launched.

        giveaway_winners (:obj:`~pyrogram.types.GiveawayWinners`, *optional*):
            A giveaway with public winners was completed.

        giveaway_completed (:obj:`~pyrogram.types.GiveawayCompleted`, *optional*):
            Service message: a giveaway without public winners was completed.

        chat_ttl_period (``int``, *optional*):
            Service message: chat TTL period changed.

        boosts_applied (``int``, *optional*):
            Service message: how many boosts were applied.

        write_access_allowed (:obj:`~pyrogram.types.WriteAccessAllowed`, *optional*):
            Service message: the user allowed the bot to write messages after adding it to the attachment or side menu, launching a Web App from a link, or accepting an explicit request from a Web App sent by the method `requestWriteAccess <https://core.telegram.org/bots/webapps#initializing-mini-apps>`__

        connected_website (``str``, *optional*):
            The domain name of the website on which the user has logged in. `More about Telegram Login <https://core.telegram.org/widgets/login>`__

        contact_registered (:obj:`~pyrogram.types.ContactRegistered`, *optional*):
            Service message: contact registered in Telegram.

        screenshot_taken ((:obj:`~pyrogram.types.ScreenshotTaken`, *optional*):
            Service message: screenshot of a message in the chat has been taken.

        business_connection_id (``str``, *optional*):
            Unique identifier of the business connection from which the message was received.
            If non-empty, the message belongs to a chat of the corresponding business account that is independent from any potential bot chat which might share the same identifier.
            This update may at times be triggered by unavailable changes to message fields that are either unavailable or not actively used by the current bot.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
            Additional interface options. An object for an inline keyboard, custom reply keyboard,
            instructions to remove reply keyboard or to force a reply from the user.

        reactions (List of :obj:`~pyrogram.types.Reaction`):
            List of the reactions to this message.

        raw (:obj:`~pyrogram.raw.types.Message`, *optional*):
            The raw message object, as received from the Telegram API.

        link (``str``, *property*):
            Generate a link to this message, only for groups and channels.

        content (``str``, *property*):
            The text or caption content of the message.
    """

    # TODO: Add game missing field

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
        sender_boost_count: int = None,
        sender_business_bot: "types.User" = None,
        date: datetime = None,
        chat: "types.Chat" = None,
        topic_message: bool = None,
        automatic_forward: bool = None,
        from_offline: bool = None,
        show_caption_above_media: bool = None,
        quote: bool = None,
        topic: "types.ForumTopic" = None,
        forward_from: "types.User" = None,
        forward_sender_name: str = None,
        forward_from_chat: "types.Chat" = None,
        forward_from_message_id: int = None,
        forward_signature: str = None,
        forward_date: datetime = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        reply_to_story_id: int = None,
        reply_to_story_user_id: int = None,
        reply_to_top_message_id: int = None,
        reply_to_message: "Message" = None,
        reply_to_story: "types.Story" = None,
        mentioned: bool = None,
        empty: bool = None,
        service: "enums.MessageServiceType" = None,
        scheduled: bool = None,
        from_scheduled: bool = None,
        media: "enums.MessageMediaType" = None,
        paid_media: "types.PaidMediaInfo" = None,
        edit_date: datetime = None,
        edit_hidden: bool = None,
        media_group_id: int = None,
        author_signature: str = None,
        has_protected_content: bool = None,
        has_media_spoiler: bool = None,
        text: Str = None,
        quote_text: Str = None,
        entities: List["types.MessageEntity"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        quote_entities: List["types.MessageEntity"] = None,
        audio: "types.Audio" = None,
        document: "types.Document" = None,
        photo: "types.Photo" = None,
        sticker: "types.Sticker" = None,
        animation: "types.Animation" = None,
        game: "types.Game" = None,
        giveaway: "types.Giveaway" = None,
        giveaway_winners: "types.GiveawayWinners" = None,
        giveaway_completed: "types.GiveawayCompleted" = None,
        invoice: "types.Invoice" = None,
        story: "types.Story" = None,
        video: "types.Video" = None,
        video_processing_pending: bool = None,
        alternative_videos: List["types.Video"] = None,
        voice: "types.Voice" = None,
        video_note: "types.VideoNote" = None,
        caption: Str = None,
        contact: "types.Contact" = None,
        location: "types.Location" = None,
        venue: "types.Venue" = None,
        web_page: "types.WebPage" = None,
        poll: "types.Poll" = None,
        dice: "types.Dice" = None,
        new_chat_members: List["types.User"] = None,
        left_chat_member: "types.User" = None,
        chat_join_type: "enums.ChatJoinType" = None,
        new_chat_title: str = None,
        new_chat_photo: "types.Photo" = None,
        delete_chat_photo: bool = None,
        group_chat_created: bool = None,
        supergroup_chat_created: bool = None,
        channel_chat_created: bool = None,
        migrate_to_chat_id: int = None,
        migrate_from_chat_id: int = None,
        pinned_message: "Message" = None,
        game_high_score: int = None,
        views: int = None,
        forwards: int = None,
        via_bot: "types.User" = None,
        outgoing: bool = None,
        matches: List[Match] = None,
        command: List[str] = None,
        forum_topic_created: "types.ForumTopicCreated" = None,
        forum_topic_closed: "types.ForumTopicClosed" = None,
        forum_topic_reopened: "types.ForumTopicReopened" = None,
        forum_topic_edited: "types.ForumTopicEdited" = None,
        general_topic_hidden: "types.GeneralTopicHidden" = None,
        general_topic_unhidden: "types.GeneralTopicUnhidden" = None,
        video_chat_scheduled: "types.VideoChatScheduled" = None,
        video_chat_started: "types.VideoChatStarted" = None,
        video_chat_ended: "types.VideoChatEnded" = None,
        video_chat_members_invited: "types.VideoChatMembersInvited" = None,
        phone_call_started: "types.PhoneCallStarted" = None,
        phone_call_ended: "types.PhoneCallEnded" = None,
        web_app_data: "types.WebAppData" = None,
        gift_code: "types.GiftCode" = None,
        gift: "types.Gift" = None,
        requested_chats: "types.RequestedChats" = None,
        successful_payment: "types.SuccessfulPayment" = None,
        refunded_payment: "types.RefundedPayment" = None,
        giveaway_created: bool = None,
        chat_ttl_period: int = None,
        boosts_applied: int = None,
        write_access_allowed: "types.WriteAccessAllowed" = None,
        connected_website: str = None,
        contact_registered: "types.ContactRegistered" = None,
        screenshot_taken: "types.ScreenshotTaken" = None,
        business_connection_id: str = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reactions: List["types.Reaction"] = None,
        raw: "raw.types.Message" = None
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.sender_chat = sender_chat
        self.sender_boost_count = sender_boost_count
        self.sender_business_bot = sender_business_bot
        self.date = date
        self.chat = chat
        self.topic_message = topic_message
        self.automatic_forward = automatic_forward
        self.from_offline = from_offline
        self.show_caption_above_media = show_caption_above_media
        self.quote = quote
        self.topic = topic
        self.forward_from = forward_from
        self.forward_sender_name = forward_sender_name
        self.forward_from_chat = forward_from_chat
        self.forward_from_message_id = forward_from_message_id
        self.forward_signature = forward_signature
        self.forward_date = forward_date
        self.message_thread_id = message_thread_id
        self.effect_id = effect_id
        self.reply_to_message_id = reply_to_message_id
        self.reply_to_story_id = reply_to_story_id
        self.reply_to_story_user_id = reply_to_story_user_id
        self.reply_to_top_message_id = reply_to_top_message_id
        self.reply_to_message = reply_to_message
        self.reply_to_story = reply_to_story
        self.mentioned = mentioned
        self.empty = empty
        self.service = service
        self.scheduled = scheduled
        self.from_scheduled = from_scheduled
        self.media = media
        self.paid_media = paid_media
        self.edit_date = edit_date
        self.edit_hidden = edit_hidden
        self.media_group_id = media_group_id
        self.author_signature = author_signature
        self.has_protected_content = has_protected_content
        self.has_media_spoiler = has_media_spoiler
        self.text = text
        self.quote_text = quote_text
        self.entities = entities
        self.caption_entities = caption_entities
        self.quote_entities = quote_entities
        self.audio = audio
        self.document = document
        self.photo = photo
        self.sticker = sticker
        self.animation = animation
        self.game = game
        self.giveaway = giveaway
        self.giveaway_winners = giveaway_winners
        self.giveaway_completed = giveaway_completed
        self.invoice = invoice
        self.story = story
        self.video = video
        self.video_processing_pending = video_processing_pending
        self.alternative_videos = alternative_videos
        self.voice = voice
        self.video_note = video_note
        self.caption = caption
        self.contact = contact
        self.location = location
        self.venue = venue
        self.web_page = web_page
        self.poll = poll
        self.dice = dice
        self.new_chat_members = new_chat_members
        self.left_chat_member = left_chat_member
        self.chat_join_type = chat_join_type
        self.new_chat_title = new_chat_title
        self.new_chat_photo = new_chat_photo
        self.delete_chat_photo = delete_chat_photo
        self.group_chat_created = group_chat_created
        self.supergroup_chat_created = supergroup_chat_created
        self.channel_chat_created = channel_chat_created
        self.migrate_to_chat_id = migrate_to_chat_id
        self.migrate_from_chat_id = migrate_from_chat_id
        self.pinned_message = pinned_message
        self.game_high_score = game_high_score
        self.views = views
        self.forwards = forwards
        self.via_bot = via_bot
        self.outgoing = outgoing
        self.matches = matches
        self.command = command
        self.screenshot_taken = screenshot_taken
        self.business_connection_id = business_connection_id
        self.reply_markup = reply_markup
        self.forum_topic_created = forum_topic_created
        self.forum_topic_closed = forum_topic_closed
        self.forum_topic_reopened = forum_topic_reopened
        self.forum_topic_edited = forum_topic_edited
        self.general_topic_hidden = general_topic_hidden
        self.general_topic_unhidden = general_topic_unhidden
        self.video_chat_scheduled = video_chat_scheduled
        self.video_chat_started = video_chat_started
        self.video_chat_ended = video_chat_ended
        self.video_chat_members_invited = video_chat_members_invited
        self.phone_call_started = phone_call_started
        self.phone_call_ended = phone_call_ended
        self.web_app_data = web_app_data
        self.gift_code = gift_code
        self.gift = gift
        self.requested_chats = requested_chats
        self.successful_payment = successful_payment
        self.refunded_payment = refunded_payment
        self.giveaway_created = giveaway_created
        self.chat_ttl_period = chat_ttl_period
        self.boosts_applied = boosts_applied
        self.write_access_allowed = write_access_allowed
        self.connected_website = connected_website
        self.contact_registered = contact_registered
        self.reactions = reactions
        self.raw = raw

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        message: "raw.base.Message",
        users: dict,
        chats: dict,
        topics: dict = None,
        is_scheduled: bool = False,
        replies: int = 1,
        business_connection_id: str = None,
        raw_reply_to_message: "raw.base.Message" = None
    ):
        if isinstance(message, raw.types.MessageEmpty):
            return Message(
                id=message.id,
                empty=True,
                business_connection_id=business_connection_id,
                raw=message,
                client=client,
            )

        from_id = utils.get_raw_peer_id(message.from_id)
        peer_id = utils.get_raw_peer_id(message.peer_id)
        user_id = from_id or peer_id

        if isinstance(message.from_id, raw.types.PeerUser) and isinstance(message.peer_id, raw.types.PeerUser):
            if from_id not in users or peer_id not in users:
                try:
                    r = await client.invoke(
                        raw.functions.users.GetUsers(
                            id=[
                                await client.resolve_peer(from_id),
                                await client.resolve_peer(peer_id)
                            ]
                        )
                    )
                except PeerIdInvalid:
                    pass
                else:
                    users.update({i.id: i for i in r})

        if isinstance(message, raw.types.MessageService):
            message_thread_id = None
            action = message.action

            text = None
            new_chat_members = None
            left_chat_member = None
            new_chat_title = None
            delete_chat_photo = None
            migrate_to_chat_id = None
            migrate_from_chat_id = None
            group_chat_created = None
            channel_chat_created = None
            new_chat_photo = None
            forum_topic_created = None
            forum_topic_closed = None
            forum_topic_reopened = None
            forum_topic_edited = None
            general_topic_hidden = None
            general_topic_unhidden = None
            video_chat_scheduled = None
            video_chat_started = None
            video_chat_ended = None
            video_chat_members_invited = None
            phone_call_started = None
            phone_call_ended = None
            web_app_data = None
            gift_code = None
            giveaway_created = None
            requested_chats = None
            successful_payment = None
            refunded_payment = None
            chat_ttl_period = None
            boosts_applied = None
            gift = None
            giveaway_completed = None
            connected_website = None
            write_access_allowed = None
            screenshot_taken = None
            chat_join_type = None
            contact_registered = None

            service_type = None

            if isinstance(action, raw.types.MessageActionChatAddUser):
                new_chat_members = [types.User._parse(client, users[i]) for i in action.users]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
                chat_join_type = enums.ChatJoinType.BY_ADD
            elif isinstance(action, raw.types.MessageActionChatJoinedByLink):
                new_chat_members = [types.User._parse(client, users[utils.get_raw_peer_id(message.from_id)])]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
                chat_join_type = enums.ChatJoinType.BY_LINK
            elif isinstance(action, raw.types.MessageActionChatJoinedByRequest):
                new_chat_members = [types.User._parse(client, users[utils.get_raw_peer_id(message.from_id)])]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
                chat_join_type = enums.ChatJoinType.BY_REQUEST
            elif isinstance(action, raw.types.MessageActionChatDeleteUser):
                left_chat_member = types.User._parse(client, users[action.user_id])
                service_type = enums.MessageServiceType.LEFT_CHAT_MEMBERS
            elif isinstance(action, raw.types.MessageActionChatEditTitle):
                new_chat_title = action.title
                service_type = enums.MessageServiceType.NEW_CHAT_TITLE
            elif isinstance(action, raw.types.MessageActionChatDeletePhoto):
                delete_chat_photo = True
                service_type = enums.MessageServiceType.DELETE_CHAT_PHOTO
            elif isinstance(action, raw.types.MessageActionChatMigrateTo):
                migrate_to_chat_id = action.channel_id
                service_type = enums.MessageServiceType.MIGRATE_TO_CHAT_ID
            elif isinstance(action, raw.types.MessageActionChannelMigrateFrom):
                migrate_from_chat_id = action.chat_id
                service_type = enums.MessageServiceType.MIGRATE_FROM_CHAT_ID
            elif isinstance(action, raw.types.MessageActionChatCreate):
                group_chat_created = True
                service_type = enums.MessageServiceType.GROUP_CHAT_CREATED
            elif isinstance(action, raw.types.MessageActionChannelCreate):
                channel_chat_created = True
                service_type = enums.MessageServiceType.CHANNEL_CHAT_CREATED
            elif isinstance(action, raw.types.MessageActionChatEditPhoto):
                new_chat_photo = types.Photo._parse(client, action.photo)
                service_type = enums.MessageServiceType.NEW_CHAT_PHOTO
            elif isinstance(action, raw.types.MessageActionCustomAction):
                text = action.message
                service_type = enums.MessageServiceType.CUSTOM_ACTION
            elif isinstance(action, raw.types.MessageActionTopicCreate):
                forum_topic_created = types.ForumTopicCreated._parse(message)
                service_type = enums.MessageServiceType.FORUM_TOPIC_CREATED
            elif isinstance(action, raw.types.MessageActionTopicEdit):
                if action.title:
                    forum_topic_edited = types.ForumTopicEdited._parse(action)
                    service_type = enums.MessageServiceType.FORUM_TOPIC_EDITED
                elif action.hidden:
                    general_topic_hidden = types.GeneralTopicHidden()
                    service_type = enums.MessageServiceType.GENERAL_TOPIC_HIDDEN
                elif action.closed:
                    forum_topic_closed = types.ForumTopicClosed()
                    service_type = enums.MessageServiceType.FORUM_TOPIC_CLOSED
                else:
                    if hasattr(action, "hidden") and action.hidden:
                        general_topic_unhidden = types.GeneralTopicUnhidden()
                        service_type = enums.MessageServiceType.GENERAL_TOPIC_UNHIDDEN
                    else:
                        forum_topic_reopened = types.ForumTopicReopened()
                        service_type = enums.MessageServiceType.FORUM_TOPIC_REOPENED
            elif isinstance(action, raw.types.MessageActionGroupCallScheduled):
                video_chat_scheduled = types.VideoChatScheduled._parse(action)
                service_type = enums.MessageServiceType.VIDEO_CHAT_SCHEDULED
            elif isinstance(action, raw.types.MessageActionGroupCall):
                if action.duration:
                    video_chat_ended = types.VideoChatEnded._parse(action)
                    service_type = enums.MessageServiceType.VIDEO_CHAT_ENDED
                else:
                    video_chat_started = types.VideoChatStarted()
                    service_type = enums.MessageServiceType.VIDEO_CHAT_STARTED
            elif isinstance(action, raw.types.MessageActionInviteToGroupCall):
                video_chat_members_invited = types.VideoChatMembersInvited._parse(client, action, users)
                service_type = enums.MessageServiceType.VIDEO_CHAT_MEMBERS_INVITED
            elif isinstance(action, raw.types.MessageActionPhoneCall):
                if action.reason:
                    phone_call_ended = types.PhoneCallEnded._parse(action)
                    service_type = enums.MessageServiceType.PHONE_CALL_ENDED
                else:
                    phone_call_started = types.PhoneCallStarted._parse(action)
                    service_type = enums.MessageServiceType.PHONE_CALL_STARTED
            elif isinstance(action, raw.types.MessageActionWebViewDataSentMe):
                web_app_data = types.WebAppData._parse(action)
                service_type = enums.MessageServiceType.WEB_APP_DATA
            elif isinstance(action, raw.types.MessageActionGiveawayLaunch):
                giveaway_created = types.GiveawayCreated._parse(client, action)
                service_type = enums.MessageServiceType.GIVEAWAY_CREATED
            elif isinstance(action, raw.types.MessageActionGiveawayResults):
                service_type = enums.MessageServiceType.GIVEAWAY_COMPLETED
                giveaway_completed = await types.GiveawayCompleted._parse(
                    client,
                    action,
                    types.Chat._parse(client, message, users, chats, is_chat=True),
                    getattr(
                        getattr(
                            message,
                            "reply_to",
                            None
                        ),
                        "reply_to_msg_id",
                        None
                    )
                )
            elif isinstance(action, raw.types.MessageActionGiftCode):
                gift_code = types.GiftCode._parse(client, action, users, chats)
                service_type = enums.MessageServiceType.GIFT_CODE
            elif isinstance(action, (raw.types.MessageActionRequestedPeer, raw.types.MessageActionRequestedPeerSentMe)):
                requested_chats = types.RequestedChats._parse(client, action)
                service_type = enums.MessageServiceType.REQUESTED_CHAT
            elif isinstance(action, (raw.types.MessageActionPaymentSent, raw.types.MessageActionPaymentSentMe)):
                successful_payment = types.SuccessfulPayment._parse(action)
                service_type = enums.MessageServiceType.SUCCESSFUL_PAYMENT
            elif isinstance(action, raw.types.MessageActionPaymentRefunded):
                refunded_payment = types.RefundedPayment._parse(action)
                service_type = enums.MessageServiceType.REFUNDED_PAYMENT
            elif isinstance(action, raw.types.MessageActionSetMessagesTTL):
                chat_ttl_period = action.period
                service_type = enums.MessageServiceType.CHAT_TTL_CHANGED
            elif isinstance(action, raw.types.MessageActionBoostApply):
                boosts_applied = action.boosts
                service_type = enums.MessageServiceType.BOOST_APPLY
            elif isinstance(action, (raw.types.MessageActionStarGift, raw.types.MessageActionStarGiftUnique)):
                gift = await types.Gift._parse_action(client, message, users, chats)
                service_type = enums.MessageServiceType.GIFT
            elif isinstance(action, raw.types.MessageActionBotAllowed):
                connected_website = getattr(action, "domain", None)
                if connected_website:
                    service_type = enums.MessageServiceType.CONNECTED_WEBSITE
                else:
                    write_access_allowed = types.WriteAccessAllowed._parse(action)
                    service_type = enums.MessageServiceType.WRITE_ACCESS_ALLOWED
            elif isinstance(action, raw.types.MessageActionScreenshotTaken):
                service_type = enums.MessageServiceType.SCREENSHOT_TAKEN
                screenshot_taken = types.ScreenshotTaken()
            elif isinstance(action, raw.types.MessageActionContactSignUp):
                service_type = enums.MessageServiceType.CONTACT_REGISTERED
                contact_registered = types.ContactRegistered()

            from_user = types.User._parse(client, users.get(user_id, None))
            sender_chat = types.Chat._parse(client, message, users, chats, is_chat=False) if not from_user else None

            parsed_message = Message(
                id=message.id,
                message_thread_id=message_thread_id,
                date=utils.timestamp_to_datetime(message.date),
                chat=types.Chat._parse(client, message, users, chats, is_chat=True),
                from_user=from_user,
                sender_chat=sender_chat,
                service=service_type,
                text=text,
                new_chat_members=new_chat_members,
                left_chat_member=left_chat_member,
                new_chat_title=new_chat_title,
                new_chat_photo=new_chat_photo,
                delete_chat_photo=delete_chat_photo,
                migrate_to_chat_id=utils.get_channel_id(migrate_to_chat_id) if migrate_to_chat_id else None,
                migrate_from_chat_id=-migrate_from_chat_id if migrate_from_chat_id else None,
                group_chat_created=group_chat_created,
                channel_chat_created=channel_chat_created,
                forum_topic_created=forum_topic_created,
                forum_topic_closed=forum_topic_closed,
                forum_topic_reopened=forum_topic_reopened,
                forum_topic_edited=forum_topic_edited,
                general_topic_hidden=general_topic_hidden,
                general_topic_unhidden=general_topic_unhidden,
                video_chat_scheduled=video_chat_scheduled,
                video_chat_started=video_chat_started,
                video_chat_ended=video_chat_ended,
                video_chat_members_invited=video_chat_members_invited,
                phone_call_started=phone_call_started,
                phone_call_ended=phone_call_ended,
                web_app_data=web_app_data,
                giveaway_created=giveaway_created,
                giveaway_completed=giveaway_completed,
                gift_code=gift_code,
                gift=gift,
                requested_chats=requested_chats,
                successful_payment=successful_payment,
                refunded_payment=refunded_payment,
                chat_ttl_period=chat_ttl_period,
                boosts_applied=boosts_applied,
                chat_join_type=chat_join_type,
                business_connection_id=business_connection_id,
                connected_website=connected_website,
                write_access_allowed=write_access_allowed,
                contact_registered=contact_registered,
                screenshot_taken=screenshot_taken,
                raw=message,
                client=client
                # TODO: supergroup_chat_created
            )

            if isinstance(action, raw.types.MessageActionPinMessage):
                try:
                    parsed_message.pinned_message = await client.get_messages(
                        chat_id=parsed_message.chat.id,
                        pinned=True,
                        replies=0
                    )

                    parsed_message.service = enums.MessageServiceType.PINNED_MESSAGE
                except (MessageIdsEmpty, ChannelPrivate):
                    pass
            elif isinstance(action, raw.types.MessageActionGameScore):
                parsed_message.game_high_score = types.GameHighScore._parse_action(client, message, users)

                if message.reply_to and replies:
                    try:
                        parsed_message.reply_to_message = await client.get_messages(
                            chat_id=parsed_message.chat.id,
                            message_ids=message.id,
                            reply=True,
                            replies=0
                        )

                        parsed_message.service = enums.MessageServiceType.GAME_HIGH_SCORE
                    except (MessageIdsEmpty, ChannelPrivate):
                        pass

            client.message_cache[(parsed_message.chat.id, parsed_message.id)] = parsed_message

            if message.reply_to and message.reply_to.forum_topic:
                parsed_message.topic_message = True
                if message.reply_to.reply_to_top_id:
                    parsed_message.message_thread_id = message.reply_to.reply_to_top_id
                else:
                    parsed_message.message_thread_id = message.reply_to.reply_to_msg_id or 1

            return parsed_message

        if isinstance(message, raw.types.Message):
            message_thread_id = None
            entities = [types.MessageEntity._parse(client, entity, users) for entity in message.entities]
            entities = types.List(filter(lambda x: x is not None, entities))

            forward_from = None
            forward_sender_name = None
            forward_from_chat = None
            forward_from_message_id = None
            forward_signature = None
            forward_date = None

            forward_header = message.fwd_from  # type: raw.types.MessageFwdHeader

            if forward_header:
                forward_date = utils.timestamp_to_datetime(forward_header.date)

                if forward_header.from_id:
                    raw_peer_id = utils.get_raw_peer_id(forward_header.from_id)
                    peer_id = utils.get_peer_id(forward_header.from_id)

                    if peer_id > 0:
                        forward_from = types.User._parse(client, users[raw_peer_id])
                    else:
                        forward_from_chat = types.Chat._parse_channel_chat(client, chats[raw_peer_id])
                        forward_from_message_id = forward_header.channel_post
                        forward_signature = forward_header.post_author
                elif forward_header.from_name:
                    forward_sender_name = forward_header.from_name

            photo = None
            location = None
            contact = None
            venue = None
            game = None
            giveaway = None
            giveaway_winners = None
            invoice = None
            story = None
            audio = None
            voice = None
            animation = None
            video = None
            alternative_videos = []
            video_note = None
            sticker = None
            document = None
            web_page = None
            poll = None
            dice = None
            paid_media = None

            media = message.media
            media_type = None
            has_media_spoiler = None

            if media:
                if isinstance(media, raw.types.MessageMediaPhoto):
                    photo = types.Photo._parse(client, media.photo, media.ttl_seconds)
                    media_type = enums.MessageMediaType.PHOTO
                    has_media_spoiler = media.spoiler
                elif isinstance(media, raw.types.MessageMediaGeo):
                    location = types.Location._parse(client, media.geo)
                    media_type = enums.MessageMediaType.LOCATION
                elif isinstance(media, raw.types.MessageMediaContact):
                    contact = types.Contact._parse(client, media)
                    media_type = enums.MessageMediaType.CONTACT
                elif isinstance(media, raw.types.MessageMediaVenue):
                    venue = types.Venue._parse(client, media)
                    media_type = enums.MessageMediaType.VENUE
                elif isinstance(media, raw.types.MessageMediaGame):
                    game = types.Game._parse(client, message)
                    media_type = enums.MessageMediaType.GAME
                elif isinstance(media, raw.types.MessageMediaGiveaway):
                    giveaway = types.Giveaway._parse(client, media, chats)
                    media_type = enums.MessageMediaType.GIVEAWAY
                elif isinstance(media, raw.types.MessageMediaGiveawayResults):
                    giveaway_winners = await types.GiveawayWinners._parse(client, media, users, chats)
                    media_type = enums.MessageMediaType.GIVEAWAY_WINNERS
                elif isinstance(media, raw.types.MessageMediaInvoice):
                    invoice = types.Invoice._parse(client, media)
                    media_type = enums.MessageMediaType.INVOICE
                elif isinstance(media, raw.types.MessageMediaStory):
                    story = await types.Story._parse(client, media, users, chats, media.peer)
                    media_type = enums.MessageMediaType.STORY
                elif isinstance(media, raw.types.MessageMediaDocument):
                    doc = media.document

                    if isinstance(doc, raw.types.Document):
                        attributes = {type(i): i for i in doc.attributes}

                        file_name = getattr(
                            attributes.get(
                                raw.types.DocumentAttributeFilename, None
                            ), "file_name", None
                        )

                        if raw.types.DocumentAttributeAnimated in attributes:
                            video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
                            animation = types.Animation._parse(client, doc, video_attributes, file_name)
                            media_type = enums.MessageMediaType.ANIMATION
                            has_media_spoiler = media.spoiler
                        elif raw.types.DocumentAttributeSticker in attributes:
                            sticker = await types.Sticker._parse(client, doc, attributes)
                            media_type = enums.MessageMediaType.STICKER
                        elif raw.types.DocumentAttributeVideo in attributes:
                            video_attributes = attributes[raw.types.DocumentAttributeVideo]

                            if video_attributes.round_message:
                                video_note = types.VideoNote._parse(client, doc, video_attributes, media.ttl_seconds)
                                media_type = enums.MessageMediaType.VIDEO_NOTE
                            else:
                                video = types.Video._parse(client, doc, video_attributes, file_name, media.ttl_seconds, media.video_cover, media.video_timestamp)
                                media_type = enums.MessageMediaType.VIDEO
                                has_media_spoiler = media.spoiler

                                altdocs = media.alt_documents or []
                                for altdoc in altdocs:
                                    if isinstance(altdoc, raw.types.Document):
                                        altdoc_attributes = {type(i): i for i in altdoc.attributes}
                                        altdoc_file_name = getattr(
                                            altdoc_attributes.get(
                                                raw.types.DocumentAttributeFilename, None
                                            ), "file_name", None
                                        )

                                        altdoc_video_attribute = altdoc_attributes.get(raw.types.DocumentAttributeVideo, None)

                                        if altdoc_video_attribute:
                                            alternative_videos.append(
                                                types.Video._parse(client, altdoc, altdoc_video_attribute, altdoc_file_name)
                                            )
                        elif raw.types.DocumentAttributeAudio in attributes:
                            audio_attributes = attributes[raw.types.DocumentAttributeAudio]

                            if audio_attributes.voice:
                                voice = types.Voice._parse(client, doc, audio_attributes, media.ttl_seconds)
                                media_type = enums.MessageMediaType.VOICE
                            else:
                                audio = types.Audio._parse(client, doc, audio_attributes, file_name)
                                media_type = enums.MessageMediaType.AUDIO
                        else:
                            document = types.Document._parse(client, doc, file_name)
                            media_type = enums.MessageMediaType.DOCUMENT
                elif isinstance(media, raw.types.MessageMediaWebPage):
                    if isinstance(media.webpage, raw.types.WebPage):
                        web_page = types.WebPage._parse(
                            client,
                            media.webpage,
                            getattr(media, "force_large_media", None),
                            getattr(media, "force_small_media", None),
                            getattr(media, "manual", None),
                            getattr(media, "safe", None)
                        )
                        media_type = enums.MessageMediaType.WEB_PAGE
                    else:
                        media = None
                elif isinstance(media, raw.types.MessageMediaPoll):
                    poll = types.Poll._parse(client, media)
                    media_type = enums.MessageMediaType.POLL
                elif isinstance(media, raw.types.MessageMediaDice):
                    dice = types.Dice._parse(client, media)
                    media_type = enums.MessageMediaType.DICE
                elif isinstance(media, raw.types.MessageMediaPaidMedia):
                    paid_media = types.PaidMediaInfo._parse(client, media)
                    media_type = enums.MessageMediaType.PAID_MEDIA
                else:
                    media = None

            reply_markup = message.reply_markup

            if reply_markup:
                if isinstance(reply_markup, raw.types.ReplyKeyboardForceReply):
                    reply_markup = types.ForceReply.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyKeyboardMarkup):
                    reply_markup = types.ReplyKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyInlineMarkup):
                    reply_markup = types.InlineKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyKeyboardHide):
                    reply_markup = types.ReplyKeyboardRemove.read(reply_markup)
                else:
                    reply_markup = None

            from_user = types.User._parse(client, users.get(user_id, None))
            sender_chat = types.Chat._parse(client, message, users, chats, is_chat=False) if not from_user else None

            reactions = types.MessageReactions._parse(client, message.reactions)

            parsed_message = Message(
                id=message.id,
                message_thread_id=message_thread_id,
                effect_id=getattr(message, "effect", None),
                date=utils.timestamp_to_datetime(message.date),
                chat=types.Chat._parse(client, message, users, chats, is_chat=True),
                from_user=from_user,
                sender_chat=sender_chat,
                sender_business_bot=types.User._parse(
                    client,
                    users.get(getattr(message, "via_business_bot_id", None))
                ),
                text=(
                    Str(message.message).init(entities) or None
                    if media is None or web_page is not None
                    else None
                ),
                caption=(
                    Str(message.message).init(entities) or None
                    if media is not None and web_page is None
                    else None
                ),
                entities=(
                    entities or None
                    if media is None or web_page is not None
                    else None
                ),
                caption_entities=(
                    entities or None
                    if media is not None and web_page is None
                    else None
                ),
                author_signature=message.post_author,
                has_protected_content=message.noforwards,
                has_media_spoiler=has_media_spoiler,
                forward_from=forward_from,
                forward_sender_name=forward_sender_name,
                forward_from_chat=forward_from_chat,
                forward_from_message_id=forward_from_message_id,
                forward_signature=forward_signature,
                forward_date=forward_date,
                mentioned=message.mentioned,
                scheduled=is_scheduled,
                from_scheduled=message.from_scheduled,
                media=media_type,
                paid_media=paid_media,
                show_caption_above_media=getattr(message, "invert_media", None),
                edit_date=utils.timestamp_to_datetime(message.edit_date),
                edit_hidden=message.edit_hide,
                media_group_id=message.grouped_id,
                photo=photo,
                location=location,
                contact=contact,
                venue=venue,
                audio=audio,
                voice=voice,
                animation=animation,
                game=game,
                giveaway=giveaway,
                giveaway_winners=giveaway_winners,
                invoice=invoice,
                story=story,
                video=video,
                video_processing_pending=getattr(message, "video_processing_pending", None),
                alternative_videos=types.List(alternative_videos) if alternative_videos else None,
                video_note=video_note,
                sticker=sticker,
                document=document,
                web_page=web_page,
                poll=poll,
                dice=dice,
                views=message.views,
                forwards=message.forwards,
                sender_boost_count=getattr(message, "from_boosts_applied", None),
                via_bot=types.User._parse(client, users.get(message.via_bot_id, None)),
                outgoing=message.out,
                business_connection_id=business_connection_id,
                reply_markup=reply_markup,
                reactions=reactions,
                from_offline=getattr(message, "offline", None),
                raw=message,
                client=client
            )

            if any((isinstance(entity, raw.types.MessageEntityBlockquote) for entity in message.entities)):
                parsed_message.quote = True

            if (
                forward_header and
                forward_header.saved_from_peer and
                forward_header.saved_from_msg_id
            ):
                saved_from_peer_id = utils.get_raw_peer_id(forward_header.saved_from_peer)
                saved_from_peer_chat = chats.get(saved_from_peer_id)
                if (
                    isinstance(saved_from_peer_chat, raw.types.Channel) and
                    not saved_from_peer_chat.megagroup
                ):
                    parsed_message.automatic_forward = True

            if message.reply_to:
                if isinstance(message.reply_to, raw.types.MessageReplyHeader):
                    parsed_message.reply_to_message_id = getattr(message.reply_to, "reply_to_msg_id", None)
                    parsed_message.reply_to_top_message_id = getattr(message.reply_to, "reply_to_top_id", None)

                    if message.reply_to.forum_topic:
                        parsed_message.topic_message = True
                        if message.reply_to.reply_to_top_id:
                            parsed_message.message_thread_id = message.reply_to.reply_to_top_id
                        else:
                            parsed_message.message_thread_id = message.reply_to.reply_to_msg_id or 1

                        if topics:
                            parsed_message.topic = types.ForumTopic._parse(client, topics.get(parsed_message.message_thread_id), users=users, chats=chats)
                    elif message.reply_to.quote:
                        quote_entities = [types.MessageEntity._parse(client, entity, users) for entity in message.reply_to.quote_entities]
                        quote_entities = types.List(filter(lambda x: x is not None, quote_entities))

                        parsed_message.quote = message.reply_to.quote
                        parsed_message.quote_text = (
                            Str(message.reply_to.quote_text).init(quote_entities) or None
                            if media is None or web_page is not None
                            else None
                        )
                        parsed_message.quote_entities = (
                            quote_entities or None
                            if media is None or web_page is not None
                            else None
                        )
                elif isinstance(message.reply_to, raw.types.MessageReplyStoryHeader):
                    parsed_message.reply_to_story_id = message.reply_to.story_id
                    parsed_message.reply_to_story_user_id = utils.get_peer_id(message.reply_to.peer)

                if replies:
                    if raw_reply_to_message:
                        parsed_message.reply_to_message = await types.Message._parse(
                            client,
                            raw_reply_to_message,
                            users,
                            chats,
                            business_connection_id=business_connection_id,
                            replies=0
                        )
                    else:
                        if isinstance(message.reply_to, raw.types.MessageReplyHeader):
                            if message.reply_to.reply_to_peer_id:
                                key = (utils.get_peer_id(message.reply_to.reply_to_peer_id), message.reply_to.reply_to_msg_id)
                                reply_to_params = {"chat_id": key[0], 'message_ids': key[1]}
                            else:
                                key = (parsed_message.chat.id, parsed_message.reply_to_message_id)
                                reply_to_params = {'chat_id': key[0], 'message_ids': message.id, 'reply': True}

                            reply_to_message = client.message_cache[key]

                            if not reply_to_message:
                                try:
                                    reply_to_message = await client.get_messages(
                                        replies=replies - 1,
                                        **reply_to_params
                                    )
                                except (ChannelPrivate, MessageIdsEmpty):
                                    pass

                            parsed_message.reply_to_message = reply_to_message
                        elif isinstance(message.reply_to, raw.types.MessageReplyStoryHeader):
                            if client.me and not client.me.is_bot:
                                parsed_message.reply_to_story = await client.get_stories(
                                    utils.get_peer_id(message.reply_to.peer),
                                    message.reply_to.story_id
                                )

            if not parsed_message.topic and parsed_message.chat.is_forum and client.me and not client.me.is_bot:
                try:
                    parsed_message.topic = await client.get_forum_topics_by_id(
                        chat_id=parsed_message.chat.id,
                        topic_ids=parsed_message.message_thread_id or 1
                    )
                except (ChannelPrivate, ChannelForumMissing):
                    pass

            if not parsed_message.poll:  # Do not cache poll messages
                client.message_cache[(parsed_message.chat.id, parsed_message.id)] = parsed_message

            return parsed_message

    @property
    def link(self) -> str:
        if (
            self.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)
            and self.chat.username
        ):
            return f"https://t.me/{self.chat.username}/{self.id}"
        else:
            return f"https://t.me/c/{utils.get_channel_id(self.chat.id)}/{self.id}"

    @property
    def content(self) -> str:
        return self.text or self.caption or Str("").init([])

    async def get_media_group(self) -> List["types.Message"]:
        """Bound method *get_media_group* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.get_media_group(
                chat_id=message.chat.id,
                message_id=message.id
            )

        Example:
            .. code-block:: python

                await message.get_media_group()

        Returns:
            List of :obj:`~pyrogram.types.Message`: On success, a list of messages of the media group is returned.

        Raises:
            ValueError: In case the passed message id doesn't belong to a media group.
        """

        return await self._client.get_media_group(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def reply_text(
        self,
        text: str,
        quote: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        show_caption_above_media: bool = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup=None
    ) -> "Message":
        """Bound method *reply_text* of :obj:`~pyrogram.types.Message`.

        An alias exists as *reply*.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_message(
                chat_id=message.chat.id,
                text="hello",
                reply_to_message_id=message.id
            )

        Example:
            .. code-block:: python

                await message.reply_text("hello", quote=True)

        Parameters:
            text (``str``):
                Text of the message to be sent.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_message(
            chat_id=self.chat.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            show_caption_above_media=show_caption_above_media,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            schedule_date=schedule_date,
            protect_content=protect_content,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup
        )

    reply = reply_text

    async def reply_animation(
        self,
        animation: Union[str, BinaryIO],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        show_caption_above_media: bool = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Union[str, BinaryIO] = None,
        disable_notification: bool = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_animation* :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_animation(
                chat_id=message.chat.id,
                animation=animation
            )

        Example:
            .. code-block:: python

                await message.reply_animation(animation)

        Parameters:
            animation (``str``):
                Animation to send.
                Pass a file_id as string to send an animation that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an animation from the Internet, or
                pass a file path as string to upload a new animation that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Animation caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            has_spoiler (``bool``, *optional*):
                Pass True if the animation needs to be covered with a spoiler animation.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            duration (``int``, *optional*):
                Duration of sent animation in seconds.

            width (``int``, *optional*):
                Animation width.

            height (``int``, *optional*):
                Animation height.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the animation file sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_animation(
            chat_id=self.chat.id,
            animation=animation,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            show_caption_above_media=show_caption_above_media,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_audio(
        self,
        audio: Union[str, BinaryIO],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        duration: int = 0,
        performer: str = None,
        title: str = None,
        thumb: Union[str, BinaryIO] = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_audio* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_audio(
                chat_id=message.chat.id,
                audio=audio
            )

        Example:
            .. code-block:: python

                await message.reply_audio(audio)

        Parameters:
            audio (``str``):
                Audio file to send.
                Pass a file_id as string to send an audio file that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an audio file from the Internet, or
                pass a file path as string to upload a new audio file that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Audio caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            duration (``int``, *optional*):
                Duration of the audio in seconds.

            performer (``str``, *optional*):
                Performer.

            title (``str``, *optional*):
                Track name.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the music file album cover.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_audio(
            chat_id=self.chat.id,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumb,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_cached_media(
        self,
        file_id: str,
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_cached_media* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_cached_media(
                chat_id=message.chat.id,
                file_id=file_id
            )

        Example:
            .. code-block:: python

                await message.reply_cached_media(file_id)

        Parameters:
            file_id (``str``):
                Media to send.
                Pass a file_id as string to send a media that exists on the Telegram servers.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``bool``, *optional*):
                Media caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_cached_media(
            chat_id=self.chat.id,
            file_id=file_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup
        )

    async def reply_chat_action(
        self,
        action: "enums.ChatAction",
        business_connection_id: str = None
    ) -> bool:
        """Bound method *reply_chat_action* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            from pyrogram import enums

            await client.send_chat_action(
                chat_id=message.chat.id,
                action=enums.ChatAction.TYPING
            )

        Example:
            .. code-block:: python

                from pyrogram import enums

                await message.reply_chat_action(enums.ChatAction.TYPING)

        Parameters:
            action (:obj:`~pyrogram.enums.ChatAction`):
                Type of action to broadcast.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ValueError: In case the provided string is not a valid chat action.
        """
        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_chat_action(
            chat_id=self.chat.id,
            action=action,
            business_connection_id=business_connection_id
        )

    async def reply_contact(
        self,
        phone_number: str,
        first_name: str,
        quote: bool = None,
        last_name: str = "",
        vcard: str = "",
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        quote_entities: List["types.MessageEntity"] = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_contact* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_contact(
                chat_id=message.chat.id,
                phone_number=phone_number,
                first_name=first_name
            )

        Example:
            .. code-block:: python

                await message.reply_contact("+1-123-456-7890", "Name")

        Parameters:
            phone_number (``str``):
                Contact's phone number.

            first_name (``str``):
                Contact's first name.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            last_name (``str``, *optional*):
                Contact's last name.

            vcard (``str``, *optional*):
                Additional data about the contact in the form of a vCard, 0-2048 bytes

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_contact(
            chat_id=self.chat.id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup
        )

    async def reply_document(
        self,
        document: Union[str, BinaryIO],
        quote: bool = None,
        thumb: Union[str, BinaryIO] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        file_name: str = None,
        force_document: bool = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_document* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_document(
                chat_id=message.chat.id,
                document=document
            )

        Example:
            .. code-block:: python

                await message.reply_document(document)

        Parameters:
            document (``str``):
                File to send.
                Pass a file_id as string to send a file that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a file from the Internet, or
                pass a file path as string to upload a new file that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the file sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            caption (``str``, *optional*):
                Document caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            file_name (``str``, *optional*):
                File name of the document sent.
                Defaults to file's path basename.

            force_document (``bool``, *optional*):
                Pass True to force sending files as document. Useful for video files that need to be sent as
                document messages instead of video messages.
                Defaults to False.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_document(
            chat_id=self.chat.id,
            document=document,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            file_name=file_name,
            force_document=force_document,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            schedule_date=schedule_date,
            protect_content=protect_content,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_game(
        self,
        game_short_name: str,
        quote: bool = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_game* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_game(
                chat_id=message.chat.id,
                game_short_name="lumberjack"
            )

        Example:
            .. code-block:: python

                await message.reply_game("lumberjack")

        Parameters:
            game_short_name (``str``):
                Short name of the game, serves as the unique identifier for the game. Set up your games via Botfather.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An object for an inline keyboard. If empty, one ‘Play game_title’ button will be shown automatically.
                If not empty, the first button must launch the game.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        return await self._client.send_game(
            chat_id=self.chat.id,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup
        )

    async def reply_inline_bot_result(
        self,
        query_id: int,
        result_id: str,
        quote: bool = None,
        disable_notification: bool = None,
        message_thread_id: bool = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        quote_entities: List["types.MessageEntity"] = None
    ) -> "Message":
        """Bound method *reply_inline_bot_result* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_inline_bot_result(
                chat_id=message.chat.id,
                query_id=query_id,
                result_id=result_id
            )

        Example:
            .. code-block:: python

                await message.reply_inline_bot_result(query_id, result_id)

        Parameters:
            query_id (``int``):
                Unique identifier for the answered query.

            result_id (``str``):
                Unique identifier for the result that was chosen.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            reply_to_message_id (``bool``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

        Returns:
            On success, the sent Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        return await self._client.send_inline_bot_result(
            chat_id=self.chat.id,
            query_id=query_id,
            result_id=result_id,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities
        )

    async def reply_location(
        self,
        latitude: float,
        longitude: float,
        quote: bool = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_location* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_location(
                chat_id=message.chat.id,
                latitude=latitude,
                longitude=longitude
            )

        Example:
            .. code-block:: python

                await message.reply_location(latitude, longitude)

        Parameters:
            latitude (``float``):
                Latitude of the location.

            longitude (``float``):
                Longitude of the location.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            quote_text (``str``):
                Text of the quote to be sent.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_location(
            chat_id=self.chat.id,
            latitude=latitude,
            longitude=longitude,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup
        )

    async def reply_media_group(
        self,
        media: List[Union["types.InputMediaPhoto", "types.InputMediaVideo"]],
        quote: bool = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        quote_entities: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        business_connection_id: str = None
    ) -> List["types.Message"]:
        """Bound method *reply_media_group* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_media_group(
                chat_id=message.chat.id,
                media=list_of_media
            )

        Example:
            .. code-block:: python

                await message.reply_media_group(list_of_media)

        Parameters:
            media (``list``):
                A list containing either :obj:`~pyrogram.types.InputMediaPhoto` or
                :obj:`~pyrogram.types.InputMediaVideo` objects
                describing photos and videos to be sent, must include 2–10 items.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

        Returns:
            On success, a :obj:`~pyrogram.types.Messages` object is returned containing all the
            single messages sent.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_media_group(
            chat_id=self.chat.id,
            media=media,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities,
            allow_paid_broadcast=allow_paid_broadcast,
            business_connection_id=business_connection_id
        )

    async def reply_photo(
        self,
        photo: Union[str, BinaryIO],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        show_caption_above_media: bool = None,
        ttl_seconds: int = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        view_once: bool = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_photo* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo
            )

        Example:
            .. code-block:: python

                await message.reply_photo(photo)

        Parameters:
            photo (``str``):
                Photo to send.
                Pass a file_id as string to send a photo that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a photo from the Internet, or
                pass a file path as string to upload a new photo that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Photo caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            has_spoiler (``bool``, *optional*):
                Pass True if the photo needs to be covered with a spoiler animation.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            ttl_seconds (``int``, *optional*):
                Self-Destruct Timer.
                If you set a timer, the photo will self-destruct in *ttl_seconds*
                seconds after it was viewed.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            view_once (``bool``, *optional*):
                Self-Destruct Timer.
                If True, the photo will self-destruct after it was viewed.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_photo(
            chat_id=self.chat.id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            show_caption_above_media=show_caption_above_media,
            ttl_seconds=ttl_seconds,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            view_once=view_once,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_poll(
        self,
        question: str,
        options: List[str],
        is_anonymous: bool = True,
        type: "enums.PollType" = enums.PollType.REGULAR,
        allows_multiple_answers: bool = None,
        correct_option_id: int = None,
        question_parse_mode: Optional["enums.ParseMode"] = None,
        question_entities: Optional[List["types.MessageEntity"]] = None,
        explanation: str = None,
        explanation_parse_mode: "enums.ParseMode" = None,
        explanation_entities: List["types.MessageEntity"] = None,
        open_period: int = None,
        close_date: datetime = None,
        is_closed: bool = None,
        quote: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_parse_mode: Optional["enums.ParseMode"] = None,
        quote_entities: List["types.MessageEntity"] = None,
        quote_offset: Optional[int] = None,
        schedule_date: datetime = None,
        business_connection_id: str = None,
        options_parse_mode: List["types.MessageEntity"] = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_poll* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_poll(
                chat_id=message.chat.id,
                question="This is a poll",
                options=["A", "B", "C]
            )

        Example:
            .. code-block:: python

                await message.reply_poll("This is a poll", ["A", "B", "C"])

        Parameters:
            question (``str``):
                Poll question, 1-255 characters.

            options (List of ``str``):
                List of answer options, 2-10 strings 1-100 characters each.

            is_anonymous (``bool``, *optional*):
                True, if the poll needs to be anonymous.
                Defaults to True.

            type (:obj`~pyrogram.enums.PollType`, *optional*):
                Poll type, :obj:`~pyrogram.enums.PollType.QUIZ` or :obj:`~pyrogram.enums.PollType.REGULAR`.
                Defaults to :obj:`~pyrogram.enums.PollType.REGULAR`.

            allows_multiple_answers (``bool``, *optional*):
                True, if the poll allows multiple answers, ignored for polls in quiz mode.
                Defaults to False.

            correct_option_id (``int``, *optional*):
                0-based identifier of the correct answer option, required for polls in quiz mode.

            question_parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            question_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the poll question, which can be specified instead of
                *parse_mode*.

            explanation (``str``, *optional*):
                Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style
                poll, 0-200 characters with at most 2 line feeds after entities parsing.

            explanation_parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            explanation_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the poll explanation, which can be specified instead of
                *parse_mode*.

            open_period (``int``, *optional*):
                Amount of time in seconds the poll will be active after creation, 5-600.
                Can't be used together with *close_date*.

            close_date (:py:obj:`~datetime.datetime`, *optional*):
                Point in time when the poll will be automatically closed.
                Must be at least 5 and no more than 600 seconds in the future.
                Can't be used together with *open_period*.

            is_closed (``bool``, *optional*):
                Pass True, if the poll needs to be immediately closed.
                This can be useful for poll preview.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            quote_parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            quote_offset (``int``, *optional*):
                Offset for quote in original message.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            options_parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_poll(
            chat_id=self.chat.id,
            question=question,
            options=options,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            correct_option_id=correct_option_id,
            question_parse_mode=question_parse_mode,
            question_entities=question_entities,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            disable_notification=disable_notification,
            protect_content=protect_content,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_parse_mode=quote_parse_mode,
            quote_entities=quote_entities,
            quote_offset=quote_offset,
            schedule_date=schedule_date,
            business_connection_id=business_connection_id,
            options_parse_mode=options_parse_mode,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup
        )

    async def reply_sticker(
        self,
        sticker: Union[str, BinaryIO],
        quote: bool = None,
        emoji: str = "",
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_sticker* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_sticker(
                chat_id=message.chat.id,
                sticker=sticker
            )

        Example:
            .. code-block:: python

                await message.reply_sticker(sticker)

        Parameters:
            sticker (``str``):
                Sticker to send.
                Pass a file_id as string to send a sticker that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a .webp sticker file from the Internet, or
                pass a file path as string to upload a new sticker that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            emoji (``str``, *optional*):
                Emoji associated with this sticker.

            caption (``str``, *optional*):
                Sticker caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_sticker(
            chat_id=self.chat.id,
            sticker=sticker,
            emoji=emoji,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        quote: bool = None,
        foursquare_id: str = "",
        foursquare_type: str = "",
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        quote_entities: List["types.MessageEntity"] = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        """Bound method *reply_venue* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_venue(
                chat_id=message.chat.id,
                latitude=latitude,
                longitude=longitude,
                title="Venue title",
                address="Venue address"
            )

        Example:
            .. code-block:: python

                await message.reply_venue(latitude, longitude, "Venue title", "Venue address")

        Parameters:
            latitude (``float``):
                Latitude of the venue.

            longitude (``float``):
                Longitude of the venue.

            title (``str``):
                Name of the venue.

            address (``str``):
                Address of the venue.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            foursquare_id (``str``, *optional*):
                Foursquare identifier of the venue.

            foursquare_type (``str``, *optional*):
                Foursquare type of the venue, if known.
                (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            quote_text (``str``):
                Text of the quote to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_venue(
            chat_id=self.chat.id,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup
        )

    async def reply_video(
        self,
        video: Union[str, BinaryIO],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        show_caption_above_media: bool = None,
        ttl_seconds: int = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        video_start_timestamp: int = None,
        video_cover: Union[str, BinaryIO] = None,
        thumb: Union[str, BinaryIO] = None,
        supports_streaming: bool = True,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        no_sound: bool = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_video* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_video(
                chat_id=message.chat.id,
                video=video
            )

        Example:
            .. code-block:: python

                await message.reply_video(video)

        Parameters:
            video (``str``):
                Video to send.
                Pass a file_id as string to send a video that exists on the Telegram servers,
                pass a HTTP URL as a string for Telegram to get a video from the Internet, or
                pass a file path as string to upload a new video that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Video caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            has_spoiler (``bool``, *optional*):
                Pass True if the video needs to be covered with a spoiler animation.

            show_caption_above_media (``bool``, *optional*):
                Pass True to show the video caption above the video.

            ttl_seconds (``int``, *optional*):
                Self-Destruct Timer.
                If you set a timer, the video will self-destruct in *ttl_seconds*
                seconds after it was viewed.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            width (``int``, *optional*):
                Video width.

            height (``int``, *optional*):
                Video height.

            video_start_timestamp (``int``, *optional*):
                Video startpoint, in seconds.

            video_cover (``str`` | ``BinaryIO``, *optional*):
                Video cover.
                Pass a file_id as string to attach a photo that exists on the Telegram servers,
                pass a HTTP URL as a string for Telegram to get a video from the Internet,
                pass a file path as string to upload a new photo civer that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            supports_streaming (``bool``, *optional*):
                Pass True, if the uploaded video is suitable for streaming.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            no_sound (``bool``, *optional*):
                Pass True, if the uploaded video is a video message with no sound.
                Doesn't work for external links.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_video(
            chat_id=self.chat.id,
            video=video,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            show_caption_above_media=show_caption_above_media,
            ttl_seconds=ttl_seconds,
            duration=duration,
            width=width,
            height=height,
            video_start_timestamp=video_start_timestamp,
            video_cover=video_cover,
            thumb=thumb,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            no_sound=no_sound,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_video_note(
        self,
        video_note: Union[str, BinaryIO],
        quote: bool = None,
        duration: int = 0,
        length: int = 1,
        thumb: Union[str, BinaryIO] = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        quote_entities: List["types.MessageEntity"] = None,
        protect_content: bool = None,
        view_once: bool = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_video_note* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_video_note(
                chat_id=message.chat.id,
                video_note=video_note
            )

        Example:
            .. code-block:: python

                await message.reply_video_note(video_note)

        Parameters:
            video_note (``str``):
                Video note to send.
                Pass a file_id as string to send a video note that exists on the Telegram servers, or
                pass a file path as string to upload a new video note that exists on your local machine.
                Sending video notes by a URL is currently unsupported.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            length (``int``, *optional*):
                Video width and height.

            thumb (``str`` | ``BinaryIO``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            quote_text (``str``):
                Text of the quote to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            view_once (``bool``, *optional*):
                Self-Destruct Timer.
                If True, the video note will self-destruct after it was viewed.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_video_note(
            chat_id=self.chat.id,
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities,
            protect_content=protect_content,
            view_once=view_once,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_voice(
        self,
        voice: Union[str, BinaryIO],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        duration: int = 0,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        view_once: bool = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_voice* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_voice(
                chat_id=message.chat.id,
                voice=voice
            )

        Example:
            .. code-block:: python

                await message.reply_voice(voice)

        Parameters:
            voice (``str``):
                Audio file to send.
                Pass a file_id as string to send an audio that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an audio from the Internet, or
                pass a file path as string to upload a new audio that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Voice message caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            duration (``int``, *optional*):
                Duration of the voice message in seconds.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message

            quote_text (``str``):
                Text of the quote to be sent.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            view_once (``bool``, *optional*):
                Self-Destruct Timer.
                If True, the voice note will self-destruct after it was listened.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_voice(
            chat_id=self.chat.id,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            view_once=view_once,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_web_page(
        self,
        text: str = None,
        quote: bool = None,
        url: str = None,
        prefer_large_media: bool = None,
        prefer_small_media: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        effect_id: int = None,
        show_caption_above_media: bool = None,
        reply_to_message_id: int = None,
        reply_to_chat_id: Union[int, str] = None,
        reply_to_story_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        quote_offset: int = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "types.Message":
        """Bound method *reply_web_page* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_web_page(
                chat_id=message.chat.id,
                url="https://docs.pyrogram.org"
            )

        Example:
            .. code-block:: python

                await message.reply_web_page("https://docs.pyrogram.org")

        Parameters:
            text (``str``, *optional*):
                Text of the message to be sent.

            url (``str``, *optional*):
                Link that will be previewed.
                If url not specified, the first URL found in the text will be used.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            prefer_large_media (``bool``, *optional*):
                If True, media in the link preview will be larger.
                Ignored if the URL isn't explicitly specified or media size change isn't supported for the preview.

            prefer_small_media (``bool``, *optional*):
                If True, media in the link preview will be smaller.
                Ignored if the URL isn't explicitly specified or media size change isn't supported for the preview.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                for forum supergroups only.

            effect_id (``int``, *optional*):
                Unique identifier of the message effect.
                For private chats only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_to_chat_id (``int`` | ``str``, *optional*):
                If the message is a reply, ID of the original chat.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the target story.

            quote_text (``str``, *optional*):
                Text of the quote to be sent.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            quote_offset (``int``, *optional*):
                Offset for quote in original message.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent message is returned.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        if message_thread_id is None:
            message_thread_id = self.message_thread_id

        if business_connection_id is None:
            business_connection_id = self.business_connection_id

        return await self._client.send_web_page(
            chat_id=self.chat.id,
            text=text,
            url=url,
            prefer_large_media=prefer_large_media,
            prefer_small_media=prefer_small_media,
            parse_mode=parse_mode,
            entities=entities,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            effect_id=effect_id,
            show_caption_above_media=show_caption_above_media,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            reply_to_story_id=reply_to_story_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            quote_offset=quote_offset,
            schedule_date=schedule_date,
            protect_content=protect_content,
            business_connection_id=business_connection_id,
            allow_paid_broadcast=allow_paid_broadcast,
            reply_markup=reply_markup
        )

    async def edit_text(
        self,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        show_caption_above_media: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> "Message":
        """Bound method *edit_text* of :obj:`~pyrogram.types.Message`.

        An alias exists as *edit*.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text="hello"
            )

        Example:
            .. code-block:: python

                await message.edit_text("hello")

        Parameters:
            text (``str``):
                New text of the message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_text(
            chat_id=self.chat.id,
            message_id=self.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            show_caption_above_media=show_caption_above_media,
            reply_markup=reply_markup
        )

    edit = edit_text

    async def edit_caption(
        self,
        caption: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> "Message":
        """Bound method *edit_caption* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption="hello"
            )

        Example:
            .. code-block:: python

                await message.edit_caption("hello")

        Parameters:
            caption (``str``):
                New caption of the message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_caption(
            chat_id=self.chat.id,
            message_id=self.id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            reply_markup=reply_markup
        )

    async def edit_media(
        self,
        media: "types.InputMedia",
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> "Message":
        """Bound method *edit_media* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=media
            )

        Example:
            .. code-block:: python

                await message.edit_media(media)

        Parameters:
            media (:obj:`~pyrogram.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_media(
            chat_id=self.chat.id,
            message_id=self.id,
            media=media,
            reply_markup=reply_markup
        )

    async def edit_reply_markup(self, reply_markup: "types.InlineKeyboardMarkup" = None) -> "Message":
        """Bound method *edit_reply_markup* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_reply_markup(
                chat_id=message.chat.id,
                message_id=message.id,
                reply_markup=inline_reply_markup
            )

        Example:
            .. code-block:: python

                await message.edit_reply_markup(inline_reply_markup)

        Parameters:
            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`):
                An InlineKeyboardMarkup object.

        Returns:
            On success, if edited message is sent by the bot, the edited
            :obj:`~pyrogram.types.Message` is returned, otherwise True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_reply_markup(
            chat_id=self.chat.id,
            message_id=self.id,
            reply_markup=reply_markup
        )

    async def forward(
        self,
        chat_id: Union[int, str],
        message_thread_id: int = None,
        disable_notification: bool = None,
        hide_sender_name: bool = None,
        hide_captions: bool = None,
        schedule_date: datetime = None,
        allow_paid_broadcast: bool = None,
        video_start_timestamp: int = None
    ) -> Union["types.Message", List["types.Message"]]:
        """Bound method *forward* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.forward_messages(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_ids=message.id
            )

        Example:
            .. code-block:: python

                await message.forward(chat_id)

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            hide_sender_name (``bool``, *optional*):
                If True, the original author of the message will not be shown.

            hide_captions (``bool``, *optional*):
                If True, the original media captions will be removed.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            video_start_timestamp (``int``, *optional*):
                Video startpoint, in seconds.

        Returns:
            On success, the forwarded Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.forward_messages(
            chat_id=chat_id,
            from_chat_id=self.chat.id,
            message_ids=self.id,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            schedule_date=schedule_date,
            hide_sender_name=hide_sender_name,
            hide_captions=hide_captions,
            allow_paid_broadcast=allow_paid_broadcast,
            video_start_timestamp=video_start_timestamp
        )

    async def copy(
        self,
        chat_id: Union[int, str],
        caption: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        reply_to_chat_id: Union[int, str] = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        has_spoiler: bool = None,
        show_caption_above_media: bool = None,
        business_connection_id: str = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = object
    ) -> Union["types.Message", List["types.Message"]]:
        """Bound method *copy* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.copy_message(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_id=message.id
            )

        Example:
            .. code-block:: python

                await message.copy(chat_id)

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            caption (``string``, *optional*):
                New caption for media, 0-1024 characters after entities parsing.
                If not specified, the original caption is kept.
                Pass "" (empty string) to remove the caption.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the new caption, which can be specified instead of *parse_mode*.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                For supergroups only.

            reply_to_chat_id (``int``, *optional*):
                If the message is a reply, ID of the original chat.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            quote_text (``str``):
                Text of the quote to be sent.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            allow_paid_broadcast (``bool``, *optional*):
                If True, you will be allowed to send up to 1000 messages per second.
                Ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message.
                The relevant Stars will be withdrawn from the bot's balance.
                For bots only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.
                If not specified, the original reply markup is kept.
                Pass None to remove the reply markup.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the copied message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if self.service:
            log.warning("Service messages cannot be copied. chat_id: %s, message_id: %s",
                        self.chat.id, self.id)
        elif self.game and not await self._client.storage.is_bot():
            log.warning("Users cannot send messages with Game media type. chat_id: %s, message_id: %s",
                        self.chat.id, self.id)
        elif self.empty:
            log.warning("Empty messages cannot be copied.")
        elif self.text:
            return await self._client.send_message(
                chat_id,
                text=self.text,
                entities=self.entities,
                parse_mode=enums.ParseMode.DISABLED,
                disable_web_page_preview=not self.web_page,
                disable_notification=disable_notification,
                message_thread_id=message_thread_id,
                reply_to_chat_id=reply_to_chat_id,
                reply_to_message_id=reply_to_message_id,
                quote_text=quote_text,
                quote_entities=quote_entities,
                schedule_date=schedule_date,
                protect_content=protect_content,
                business_connection_id=business_connection_id,
                allow_paid_broadcast=allow_paid_broadcast,
                reply_markup=self.reply_markup if reply_markup is object else reply_markup
            )
        elif self.media:
            send_media = partial(
                self._client.send_cached_media,
                chat_id=chat_id,
                disable_notification=disable_notification,
                message_thread_id=message_thread_id,
                reply_to_message_id=reply_to_message_id,
                reply_to_chat_id=reply_to_chat_id,
                quote_text=quote_text,
                quote_entities=quote_entities,
                schedule_date=schedule_date,
                protect_content=protect_content,
                has_spoiler=self.has_media_spoiler if has_spoiler is None else has_spoiler,
                show_caption_above_media=self.show_caption_above_media if show_caption_above_media is None else show_caption_above_media,
                business_connection_id=business_connection_id,
                allow_paid_broadcast=allow_paid_broadcast,
                reply_markup=self.reply_markup if reply_markup is object else reply_markup
            )

            if self.photo:
                file_id = self.photo.file_id
            elif self.audio:
                file_id = self.audio.file_id
            elif self.document:
                file_id = self.document.file_id
            elif self.video:
                file_id = self.video.file_id
            elif self.animation:
                file_id = self.animation.file_id
            elif self.voice:
                file_id = self.voice.file_id
            elif self.sticker:
                file_id = self.sticker.file_id
            elif self.video_note:
                file_id = self.video_note.file_id
            elif self.contact:
                return await self._client.send_contact(
                    chat_id,
                    phone_number=self.contact.phone_number,
                    first_name=self.contact.first_name,
                    last_name=self.contact.last_name,
                    vcard=self.contact.vcard,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date,
                    allow_paid_broadcast=allow_paid_broadcast,
                    business_connection_id=business_connection_id
                )
            elif self.location:
                return await self._client.send_location(
                    chat_id,
                    latitude=self.location.latitude,
                    longitude=self.location.longitude,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date,
                    allow_paid_broadcast=allow_paid_broadcast,
                    business_connection_id=business_connection_id
                )
            elif self.venue:
                return await self._client.send_venue(
                    chat_id,
                    latitude=self.venue.location.latitude,
                    longitude=self.venue.location.longitude,
                    title=self.venue.title,
                    address=self.venue.address,
                    foursquare_id=self.venue.foursquare_id,
                    foursquare_type=self.venue.foursquare_type,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date,
                    allow_paid_broadcast=allow_paid_broadcast,
                    business_connection_id=business_connection_id
                )
            elif self.poll:
                return await self._client.send_poll(
                    chat_id,
                    question=self.poll.question,
                    options=[opt.text for opt in self.poll.options],
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date,
                    allow_paid_broadcast=allow_paid_broadcast,
                    business_connection_id=business_connection_id
                )
            elif self.game:
                return await self._client.send_game(
                    chat_id,
                    game_short_name=self.game.short_name,
                    disable_notification=disable_notification,
                    allow_paid_broadcast=allow_paid_broadcast,
                    message_thread_id=message_thread_id
                )
            else:
                raise ValueError("Unknown media type")

            if self.sticker or self.video_note:  # Sticker and VideoNote should have no caption
                return await send_media(
                    file_id=file_id,
                    message_thread_id=message_thread_id
                )
            else:
                if caption is None:
                    caption = self.caption or ""
                    caption_entities = self.caption_entities

                return await send_media(
                    file_id=file_id,
                    caption=caption,
                    parse_mode=parse_mode,
                    caption_entities=caption_entities,
                    message_thread_id=message_thread_id
                )
        else:
            raise ValueError("Can't copy this message")

    async def copy_media_group(
        self,
        chat_id: Union[int, str],
        captions: Union[List[str], str] = None,
        has_spoilers: Union[List[bool], bool] = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        reply_to_message_id: int = None,
        reply_to_chat_id: Union[int, str] = None,
        reply_to_story_id: int = None,
        quote_text: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        quote_entities: List["types.MessageEntity"] = None,
        quote_offset: int = None,
        schedule_date: datetime = None,
        show_caption_above_media: bool = None,
    ) -> List["types.Message"]:
        """Bound method *copy_media_group* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.copy_media_group(
                chat_id=chat_id,
                from_chat_id=from_chat_id,
                message_ids=message.id
            )

        Example:
            .. code-block:: python

                await message.copy_media_group("me")

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            captions (``str`` | List of ``str`` , *optional*):
                New caption for media, 0-1024 characters after entities parsing for each media.
                If not specified, the original caption is kept.
                Pass "" (empty string) to remove the caption.

                If a ``string`` is passed, it becomes a caption only for the first media.
                If a list of ``string`` passed, each element becomes caption for each media element.
                You can pass ``None`` in list to keep the original caption.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                For supergroups only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_to_chat_id (``int``, *optional*):
                If the message is a reply, ID of the original chat.

            reply_to_story_id (``int``, *optional*):
                If the message is a reply, ID of the target story.

            quote_text (``str``, *optional*):
                Text of the quote to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote text, which can be specified instead of *parse_mode*.

            quote_offset (``int``, *optional*):
                Offset for quote in original message.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

        Returns:
            List of :obj:`~pyrogram.types.Message`: On success, a list of copied messages is returned.
        """
        return await self._client.copy_media_group(
            chat_id=chat_id,
            from_chat_id=self.chat.id,
            message_id=self.id,
            captions=captions,
            has_spoilers=has_spoilers,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            reply_to_story_id=reply_to_story_id,
            quote_text=quote_text,
            parse_mode=parse_mode,
            quote_entities=quote_entities,
            quote_offset=quote_offset,
            schedule_date=schedule_date,
            show_caption_above_media=show_caption_above_media
        )

    async def delete(self, revoke: bool = True):
        """Bound method *delete* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.delete_messages(
                chat_id=chat_id,
                message_ids=message.id
            )

        Example:
            .. code-block:: python

                await message.delete()

        Parameters:
            revoke (``bool``, *optional*):
                Deletes messages on both parts.
                This is only for private cloud chats and normal groups, messages on
                channels and supergroups are always revoked (i.e.: deleted for everyone).
                Defaults to True.

        Returns:
            True on success, False otherwise.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.delete_messages(
            chat_id=self.chat.id,
            message_ids=self.id,
            revoke=revoke
        )

    async def click(
        self,
        x: Union[int, str] = 0,
        y: int = None,
        quote: bool = None,
        timeout: int = 10,
        request_write_access: bool = True,
        password: str = None
    ):
        """Bound method *click* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for clicking a button attached to the message instead of:

        - Clicking inline buttons:

        .. code-block:: python

            await client.request_callback_answer(
                chat_id=message.chat.id,
                message_id=message.id,
                callback_data=message.reply_markup[i][j].callback_data
            )

        - Clicking normal buttons:

        .. code-block:: python

            await client.send_message(
                chat_id=message.chat.id,
                text=message.reply_markup[i][j].text
            )

        Example:
            This method can be used in three different ways:

            1.  Pass one integer argument only (e.g.: ``.click(2)``, to click a button at index 2).
                Buttons are counted left to right, starting from the top.

            2.  Pass two integer arguments (e.g.: ``.click(1, 0)``, to click a button at position (1, 0)).
                The origin (0, 0) is top-left.

            3.  Pass one string argument only (e.g.: ``.click("Settings")``, to click a button by using its label).
                Only the first matching button will be pressed.

        Parameters:
            x (``int`` | ``str``):
                Used as integer index, integer abscissa (in pair with y) or as string label.
                Defaults to 0 (first button).

            y (``int``, *optional*):
                Used as ordinate only (in pair with x).

            quote (``bool``, *optional*):
                Useful for normal buttons only, where pressing it will result in a new message sent.
                If ``True``, the message will be sent as a reply to this message.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            timeout (``int``, *optional*):
                Timeout in seconds.

            request_write_access (``bool``, *optional*):
                Only used in case of :obj:`~pyrogram.types.LoginUrl` button.
                True, if the bot can send messages to the user.
                Defaults to ``True``.

            password (``str``, *optional*):
                When clicking certain buttons (such as BotFather's confirmation button to transfer ownership), if your account has 2FA enabled, you need to provide your account's password.
                The 2-step verification password for the current user. Only applicable, if the :obj:`~pyrogram.types.InlineKeyboardButton` contains ``requires_password``.

        Returns:
            -   The result of :meth:`~pyrogram.Client.request_callback_answer` in case of inline callback button clicks.
            -   The result of :meth:`~Message.reply()` in case of normal button clicks.
            -   A string in case the inline button is a URL, a *switch_inline_query* or a
                *switch_inline_query_current_chat* button.
            -   A string URL with the user details, in case of a WebApp button.
            -   A :obj:`~pyrogram.types.Chat` object in case of a ``KeyboardButtonUserProfile`` button.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ValueError: In case the provided index or position is out of range or the button label was not found.
            TimeoutError: In case, after clicking an inline button, the bot fails to answer within the timeout.
        """

        if isinstance(self.reply_markup, types.ReplyKeyboardMarkup):
            keyboard = self.reply_markup.keyboard
            is_inline = False
        elif isinstance(self.reply_markup, types.InlineKeyboardMarkup):
            keyboard = self.reply_markup.inline_keyboard
            is_inline = True
        else:
            raise ValueError("The message doesn't contain any keyboard")

        if isinstance(x, int) and y is None:
            try:
                button = [
                    button
                    for row in keyboard
                    for button in row
                ][x]
            except IndexError:
                raise ValueError(f"The button at index {x} doesn't exist")
        elif isinstance(x, int) and isinstance(y, int):
            try:
                button = keyboard[y][x]
            except IndexError:
                raise ValueError(f"The button at position ({x}, {y}) doesn't exist")
        elif isinstance(x, str) and y is None:
            label = x.encode("utf-16", "surrogatepass").decode("utf-16")

            try:
                button = [
                    button
                    for row in keyboard
                    for button in row
                    if label == button.text
                ][0]
            except IndexError:
                raise ValueError(f"The button with label '{x}' doesn't exists")
        else:
            raise ValueError("Invalid arguments")

        if is_inline:
            if button.callback_data:
                return await self._client.request_callback_answer(
                    chat_id=self.chat.id,
                    message_id=self.id,
                    callback_data=button.callback_data,
                    timeout=timeout
                )
            elif button.requires_password:
                if password is None:
                    raise ValueError(
                        "This button requires a password"
                    )

                return await self._client.request_callback_answer(
                    chat_id=self.chat.id,
                    message_id=self.id,
                    callback_data=button.callback_data,
                    password=password,
                    timeout=timeout
                )
            elif button.url:
                return button.url
            elif button.web_app:
                web_app = button.web_app

                bot_peer_id = (
                    self.via_bot and
                    self.via_bot.id
                ) or (
                    self.from_user and
                    self.from_user.is_bot and
                    self.from_user.id
                ) or None

                if not bot_peer_id:
                    raise ValueError(
                        "This button requires a bot as the sender"
                    )

                r = await self._client.invoke(
                    raw.functions.messages.RequestWebView(
                        peer=await self._client.resolve_peer(self.chat.id),
                        bot=await self._client.resolve_peer(bot_peer_id),
                        url=web_app.url,
                        platform=self._client.client_platform.value,
                        # TODO
                    )
                )
                return r.url
            elif button.user_id:
                return await self._client.get_chat(
                    button.user_id,
                    force_full=False
                )
            elif button.switch_inline_query:
                return button.switch_inline_query
            elif button.switch_inline_query_current_chat:
                return button.switch_inline_query_current_chat
            else:
                raise ValueError("This button is not supported yet")
        else:
            await self.reply(text=button, quote=quote)

    async def react(self, emoji: Union[int, str, List[Union[int, str]]] = None, big: bool = False) -> bool:
        """Bound method *react* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_reaction(
                chat_id=chat_id,
                message_id=message.id,
                emoji="🔥"
            )

        Example:
            .. code-block:: python

                await message.react(emoji="🔥")

        Parameters:
            emoji (``int`` | ``str`` | List of ``int`` | ``str``, *optional*):
                Reaction emoji.
                Pass None as emoji (default) to retract the reaction.
                Pass list of int or str to react multiple emojis.

            big (``bool``, *optional*):
                Pass True to show a bigger and longer reaction.
                Defaults to False.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.send_reaction(
            chat_id=self.chat.id,
            message_id=self.id,
            emoji=emoji,
            big=big
        )

    async def retract_vote(
        self,
    ) -> "types.Poll":
        """Bound method *retract_vote* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            client.retract_vote(
                chat_id=message.chat.id,
                message_id=message_id,
            )

        Example:
            .. code-block:: python

                message.retract_vote()

        Returns:
            :obj:`~pyrogram.types.Poll`: On success, the poll with the retracted vote is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.retract_vote(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def download(
        self,
        file_name: str = "",
        in_memory: bool = False,
        block: bool = True,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> str:
        """Bound method *download* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.download_media(message)

        Example:
            .. code-block:: python

                await message.download()

        Parameters:
            file_name (``str``, *optional*):
                A custom *file_name* to be used instead of the one provided by Telegram.
                By default, all files are downloaded in the *downloads* folder in your working directory.
                You can also specify a path for downloading files in a custom location: paths that end with "/"
                are considered directories. All non-existent folders will be created automatically.

            in_memory (``bool``, *optional*):
                Pass True to download the media in-memory.
                A binary file-like object with its attribute ".name" set will be returned.
                Defaults to False.

            block (``bool``, *optional*):
                Blocks the code execution until the file has been downloaded.
                Defaults to True.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the absolute path of the downloaded file as string is returned, None otherwise.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ``ValueError``: If the message doesn't contain any downloadable media
        """
        return await self._client.download_media(
            message=self,
            file_name=file_name,
            in_memory=in_memory,
            block=block,
            progress=progress,
            progress_args=progress_args,
        )

    async def vote(
        self,
        option: int,
    ) -> "types.Poll":
        """Bound method *vote* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            client.vote_poll(
                chat_id=message.chat.id,
                message_id=message.id,
                option=1
            )

        Example:
            .. code-block:: python

                message.vote(6)

        Parameters:
            option (``int``):
                Index of the poll option you want to vote for (0 to 9).

        Returns:
            :obj:`~pyrogram.types.Poll`: On success, the poll with the chosen option is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.vote_poll(
            chat_id=self.chat.id,
            message_id=self.id,
            options=option
        )

    async def pin(self, disable_notification: bool = False, both_sides: bool = False) -> "types.Message":
        """Bound method *pin* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.pin_chat_message(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await message.pin()

        Parameters:
            disable_notification (``bool``):
                Pass True, if it is not necessary to send a notification to all chat members about the new pinned
                message. Notifications are always disabled in channels.

            both_sides (``bool``, *optional*):
                Pass True to pin the message for both sides (you and recipient).
                Applicable to private chats only. Defaults to False.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the service message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.pin_chat_message(
            chat_id=self.chat.id,
            message_id=self.id,
            disable_notification=disable_notification,
            both_sides=both_sides
        )

    async def unpin(self) -> bool:
        """Bound method *unpin* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.unpin_chat_message(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await message.unpin()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.unpin_chat_message(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def read(self) -> bool:
        """Bound method *read* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.read_chat_history(
                chat_id=message.chat.id,
                max_id=message_id
            )

        Example:
            .. code-block:: python

                await message.read()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.read_chat_history(
            chat_id=self.chat.id,
            max_id=self.id
        )

    async def view(self) -> bool:
        """Bound method *view* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.view_messages(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await message.view()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.view_messages(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def pay(self) -> List[Union["types.Photo", "types.Video"]]:
        """Bound method *pay* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_payment_form(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await message.pay()

        Returns:
            List of :obj:`~pyrogram.types.Photo` | :obj:`~pyrogram.types.Video`: On success, the list of bought photos and videos is returned.
        """
        return await self._client.send_payment_form(
            chat_id=self.chat.id,
            message_id=self.id
        )
