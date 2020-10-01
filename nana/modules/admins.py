import asyncio
import time

from emoji import get_emoji_regexp
from pyrogram import filters
from pyrogram.errors import (UsernameInvalid,
                             ChatAdminRequired,
                             PeerIdInvalid,
                             UserIdInvalid)
from pyrogram.types import ChatPermissions

from nana import app, Command
from nana.helpers.admincheck import admin_check, is_sudoadmin

__MODULE__ = "Admin"
__HELP__ = """
Module for Group Admins

──「 **Locks / Unlocks** 」──
-> `lock`
locks permission in the group

-> `unlock`
unlocks permission in the group

Supported Locks / Unlocks:
 `msg` | `media` | `stickers`
 `polls` | `info`  | `invite` |
 `animations` | `games` |
 `inlinebots` | `webprev` |
 `pin` | `all`

-> `vlock`
view group permissions

──「 **Promote / Demote** 」──
-> `promote`
Reply to a user to promote

-> `demote`
Reply to a user to demote

──「 **Ban / Unban** 」──
-> `ban`
Reply to a user to perform ban

-> `unban`
Reply to a user to perform unban

──「 **Kick User** 」──
-> `kick`
Reply to a user to kick from chat

──「 **Mute / Unmute** 」──
-> `mute`
Reply to a user to mute them forever

-> `mute 24`
Reply to a user to mute them for 24 hours

-> `unmute`
Reply to a user to unmute them

──「 **Message Pin** 」──
-> `pin`
Reply to a user to mute them forever

Supported pin types: `alert`, `notify`, `loud`
"""

# Mute permissions
mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_stickers=False,
    can_send_animations=False,
    can_send_games=False,
    can_use_inline_bots=False,
    can_add_web_page_previews=False,
    can_send_polls=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False
)

# Unmute permissions
unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_stickers=True,
    can_send_animations=True,
    can_send_games=True,
    can_use_inline_bots=True,
    can_add_web_page_previews=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False
)


@app.on_message(filters.me & filters.command(["pin"], Command))
async def pin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        get_group = await client.get_chat(chat_id)
        can_pin = await admin_check(message)
        if can_pin:
            try:
                if message.reply_to_message:
                    disable_notification = True
                    if len(message.command) >= 2 and message.command[1] in ['alert', 'notify', 'loud']:
                        disable_notification = False
                    await client.pin_chat_message(
                        message.chat.id,
                        message.reply_to_message.message_id,
                        disable_notification=disable_notification
                    )
                    await message.edit(
                            f"**Message Pinned**\n"
                            f"Chat: `{get_group.title}` (`{chat_id}`)"
                            )
                else:
                    await message.edit("`Reply to a message to pin`")
                    await asyncio.sleep(5)
                    await message.delete()
            except Exception as e:
                await message.edit("`Error!`\n"
                            f"**Log:** `{e}`"
                        )
                return
        else:
            await message.edit("`permission denied`")
            await asyncio.sleep(5)
            await message.delete()   
    else:
        await message.delete()


@app.on_message(filters.me & filters.command(["mute"], Command))
async def mute_hammer(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        get_group = await client.get_chat(chat_id)
        can_mute = await admin_check(message)
        if can_mute:
            if message.reply_to_message:
                try:
                    get_mem = await client.get_chat_member(
                            chat_id,
                            message.reply_to_message.from_user.id
                            )
                    if len(message.text.split()) == 2 and message.text.split()[1] == "24":
                        await client.restrict_chat_member(
                            chat_id=message.chat.id,
                            user_id=message.reply_to_message.from_user.id,
                            permissions=mute_permission,
                            until_date=int(time.time() + 86400)
                        )
                        await message.edit(
                            f"**Muted for 24 hours**\n"
                            f"User: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                            f"(`{get_mem.user.id}`)\n"
                            f"Chat: `{get_group.title}` (`{chat_id}`)"
                            )
                    else:
                        await client.restrict_chat_member(
                            chat_id=message.chat.id,
                            user_id=message.reply_to_message.from_user.id,
                            permissions=mute_permission
                        )
                        await message.edit(
                            f"**Muted Indefinitely**\n"
                            f"User: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                            f"(`{get_mem.user.id}`)\n"
                            f"Chat: `{get_group.title}` (`{chat_id}`)"
                            )
                except Exception as e:
                    await message.edit("`Error!`\n"
                            f"**Log:** `{e}`"
                        )
                    return
            else:
                await message.edit("`Reply to a user to mute them`")
                await asyncio.sleep(5)
                await message.delete()
        else:
            await message.edit("`permission denied`")
            await asyncio.sleep(5)
            await message.delete()
    else:
        await message.delete()

@app.on_message(filters.me & filters.command(["unmute"], Command))
async def unmute(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        get_group = await client.get_chat(chat_id)
        can_unmute = await admin_check(message)
        if can_unmute:
            try:
                if message.reply_to_message:
                    get_mem = await client.get_chat_member(
                            chat_id,
                            message.reply_to_message.from_user.id
                            )
                    await client.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.reply_to_message.from_user.id,
                        permissions=unmute_permissions
                    )
                    await message.edit(
                            f"**Unmuted**\n"
                            f"User: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                            f"(`{get_mem.user.id}`)\n"
                            f"Chat: `{get_group.title}` (`{chat_id}`)"
                            )
                else:
                    await message.edit("`Reply to a user to mute them`")
                    await asyncio.sleep(5)
                    await message.delete()
            except Exception as e:
                await message.edit("`Error!`\n"
                        f"**Log:** `{e}`"
                    )
                return
        else:
            await message.edit("`permission denied`")
            await asyncio.sleep(5)
            await message.delete()
    else:
        await message.delete()


@app.on_message(filters.me & filters.command(["kick"], Command))
async def kick_user(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        get_group = await client.get_chat(chat_id)
        can_kick = await admin_check(message)
        if can_kick:
            if message.reply_to_message:

                try:
                    get_mem = await client.get_chat_member(
                        chat_id,
                        message.reply_to_message.from_user.id
                        )
                    await client.kick_chat_member(chat_id, get_mem.user.id, int(time.time() + 45))
                    await message.edit(
                        f"**Kicked**\n"
                        f"User: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                        f"(`{get_mem.user.id}`)\n"
                        f"Chat: `{get_group.title}` (`{chat_id}`)"
                        )

                except ChatAdminRequired:
                    await message.edit("`permission denied`")
                    await asyncio.sleep(5)
                    await message.delete()
                    return

                except Exception as e:
                    await message.edit("`Error!`\n"
                        f"**Log:** `{e}`"
                    )
                    return

            else:
                await message.edit("`Reply to a user to kick`")
                await asyncio.sleep(5)
                await message.delete()
                return

        else:
            await message.edit("`permission denied`")
            await asyncio.sleep(5)
            await message.delete()
    else:
        await message.delete()


@app.on_message(filters.me & filters.command(["ban"], Command))
async def ban_usr(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        get_group = await client.get_chat(chat_id)
        can_ban = await admin_check(message)

        if can_ban:
            if message.reply_to_message:
                user_id = message.reply_to_message.from_user.id
            else:
                await message.edit("`reply to a user to ban.`")
                await asyncio.sleep(5)
                await message.delete()

            if user_id:
                try:
                    get_mem = await client.get_chat_member(chat_id, user_id)
                    await client.kick_chat_member(chat_id, user_id)
                    await message.edit(
                        f"**Banned**\n"
                        f"User: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                        f"(`{get_mem.user.id}`)\n"
                        f"Chat: `{get_group.title}` (`{chat_id}`)"
                        )

                except UsernameInvalid:
                    await message.edit("`invalid username`")
                    await asyncio.sleep(5)
                    await message.delete()
                    return

                except PeerIdInvalid:
                    await message.edit("`invalid username or userid`")
                    await asyncio.sleep(5)
                    await message.delete()
                    return

                except UserIdInvalid:
                    await message.edit("`invalid userid`")
                    await asyncio.sleep(5)
                    await message.delete()
                    return

                except ChatAdminRequired:
                    await message.edit("`permission denied`")
                    await asyncio.sleep(5)
                    await message.delete()
                    return

                except Exception as e:
                    await message.edit(f"**Log:** `{e}`")
                    return

        else:
            await message.edit("`permission denied`")
            await asyncio.sleep(5)
            await message.delete()
            return
    else:
        await message.delete()


@app.on_message(filters.me & filters.command(["unban"], Command))
async def unban_usr(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        get_group = await client.get_chat(chat_id)
        can_unban = await admin_check(message)
        if can_unban:
            if message.reply_to_message:
                try:
                    get_mem = await client.get_chat_member(
                        chat_id,
                        message.reply_to_message.from_user.id
                        )
                    await client.unban_chat_member(chat_id, get_mem.user.id)
                    await message.edit(
                        f"**Unbanned**\n"
                        f"User: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                        f"(`{get_mem.user.id}`)\n"
                        f"Chat: `{get_group.title}` (`{chat_id}`)"
                        )

                except Exception as e:
                    await message.edit(f"**Log:** `{e}`")
                    return

            else:
                await message.edit("`Reply to a user to unban`")
                await asyncio.sleep(5)
                await message.delete()
                return
        else:
            await message.edit("`permission denied`")
            await asyncio.sleep(5)
            await message.delete()
    else:
        await message.delete()


@app.on_message(filters.me & filters.command(["promote"], Command))
async def promote_usr(client, message):
    if message.chat.type in ['group', 'supergroup']:
        cmd = message.command
        custom_rank = ""
        chat_id = message.chat.id
        get_group = await client.get_chat(chat_id)
        can_promo = await is_sudoadmin(message)

        if can_promo:
            if message.reply_to_message:
                get_mem = await client.get_chat_member(
                            chat_id,
                            message.reply_to_message.from_user.id
                            )
                user_id = message.reply_to_message.from_user.id
                custom_rank = get_emoji_regexp().sub(u'', " ".join(cmd[1:]))

                if len(custom_rank) > 15:
                    custom_rank = custom_rank[:15]
            else:
                await message.edit("`reply to a user to promote`")
                await asyncio.sleep(5)
                await message.delete()
                return

            if user_id:
                try:
                    await client.promote_chat_member(chat_id, user_id,
                                                    can_change_info=True,
                                                    can_delete_messages=True,
                                                    can_restrict_members=True,
                                                    can_invite_users=True,
                                                    can_pin_messages=True)

                    await asyncio.sleep(2)
                    await client.set_administrator_title(chat_id, user_id, custom_rank)
                    await message.edit(
                            f"**Promoted**\n"
                            f"User: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                            f"(`{get_mem.user.id}`)\n"
                            f"Chat: `{get_group.title}` (`{chat_id}`)"
                            )

                except UsernameInvalid:
                    await message.edit("`invalid username`")
                    await asyncio.sleep(5)
                    await message.delete()
                    return
                except PeerIdInvalid:
                    await message.edit("`invalid username or userid`")
                    await asyncio.sleep(5)
                    await message.delete()
                    return
                except UserIdInvalid:
                    await message.edit("`invalid userid`")
                    await asyncio.sleep(5)
                    await message.delete()
                    return

                except ChatAdminRequired:
                    await message.edit("`permission denied`")
                    await asyncio.sleep(5)
                    await message.delete()
                    return

                except Exception as e:
                    await message.edit(f"**Log:** `{e}`")
                    return

        else:
            await message.edit("`permission denied`")
            await asyncio.sleep(5)
            await message.delete()
    else:
        await message.delete()


@app.on_message(filters.me & filters.command(["demote"], Command))
async def demote_usr(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        get_group = await client.get_chat(chat_id)
        can_demote = await is_sudoadmin(message)

        if can_demote:
            if message.reply_to_message:
                try:
                    get_mem = await client.get_chat_member(
                        chat_id,
                        message.reply_to_message.from_user.id
                        )
                    await client.promote_chat_member(chat_id, get_mem.user.id,
                                                    can_change_info=False,
                                                    can_delete_messages=False,
                                                    can_restrict_members=False,
                                                    can_invite_users=False,
                                                    can_pin_messages=False)

                    await message.edit(
                            f"**Demoted**\n"
                            f"User: [{get_mem.user.first_name}](tg://user?id={get_mem.user.id}) "
                            f"(`{get_mem.user.id}`)\n"
                            f"Chat: `{get_group.title}` (`{chat_id}`)"
                            )
                except ChatAdminRequired:
                    await message.edit("`permission denied`")
                    await asyncio.sleep(5)
                    await message.delete()
                    return

                except Exception as e:
                    await message.edit(f"**Log:** `{e}`")
                    return

            if not message.reply_to_message:
                await message.edit("`reply to a user to demote.`")
                return
        else:
            await message.edit("``permission denied`")
    else:
        await message.delete()


@app.on_message(filters.me & filters.command(["lock"], Command))
async def lock_permission(client, message):
    """locks group permission"""
    if message.chat.type in ['group', 'supergroup']:
        cmd = message.command
        is_admin = await admin_check(message)
        if not is_admin:
            await message.delete()
            return
        msg = ""
        media = ""
        stickers = ""
        animations = ""
        games = ""
        inlinebots = ""
        webprev = ""
        polls = ""
        info = ""
        invite = ""
        pin = ""
        perm = ""
        lock_type = " ".join(cmd[1:])
        chat_id = message.chat.id
        if not lock_type:
            await message.edit("`can't lock the void`")
            await asyncio.sleep(5)
            await message.delete()
            return

        get_perm = await client.get_chat(chat_id)

        msg = get_perm.permissions.can_send_messages
        media = get_perm.permissions.can_send_media_messages
        stickers = get_perm.permissions.can_send_stickers
        animations = get_perm.permissions.can_send_animations
        games = get_perm.permissions.can_send_games
        inlinebots = get_perm.permissions.can_use_inline_bots
        webprev = get_perm.permissions.can_add_web_page_previews
        polls = get_perm.permissions.can_send_polls
        info = get_perm.permissions.can_change_info
        invite = get_perm.permissions.can_invite_users
        pin = get_perm.permissions.can_pin_messages

        if lock_type == "all":
            try:
                await client.set_chat_permissions(chat_id, ChatPermissions())
                await message.edit("`Locked all permission from this Chat!`")
                await asyncio.sleep(5)
                await message.delete()

            except Exception as e:
                await message.edit(
                    text="`permission denied`\n"
                    f"**Log:** `{e}`")

            return

        if lock_type == "msg":
            msg = False
            perm = "messages"

        elif lock_type == "media":
            media = False
            perm = "audios, documents, photos, videos, video notes, voice notes"

        elif lock_type == "stickers":
            stickers = False
            perm = "stickers"

        elif lock_type == "animations":
            animations = False
            perm = "animations"

        elif lock_type == "games":
            games = False
            perm = "games"

        elif lock_type == "inlinebots":
            inlinebots = False
            perm = "inline bots"

        elif lock_type == "webprev":
            webprev = False
            perm = "web page previews"

        elif lock_type == "polls":
            polls = False
            perm = "polls"

        elif lock_type == "info":
            info = False
            perm = "info"

        elif lock_type == "invite":
            invite = False
            perm = "invite"

        elif lock_type == "pin":
            pin = False
            perm = "pin"

        else:
            await message.edit("`Invalid Lock Type!`")
            await asyncio.sleep(5)
            await message.delete()
            return

        try:
            await client.set_chat_permissions(chat_id,
                                            ChatPermissions(can_send_messages=msg,
                                                            can_send_media_messages=media,
                                                            can_send_stickers=stickers,
                                                            can_send_animations=animations,
                                                            can_send_games=games,
                                                            can_use_inline_bots=inlinebots,
                                                            can_add_web_page_previews=webprev,
                                                            can_send_polls=polls,
                                                            can_change_info=info,
                                                            can_invite_users=invite,
                                                            can_pin_messages=pin))

            await message.edit(text=f"`Locked {perm} for this chat!`")
            await asyncio.sleep(5)
            await message.delete()

        except Exception as e:
            await message.edit("`Error!`\n"
                f"**Log:** `{e}`")
    else:
        await message.delete()


@app.on_message(filters.me & filters.command(["unlock"], Command))
async def unlock_permission(client, message):
    """unlocks group permission"""
    if message.chat.type in ['group', 'supergroup']:
        cmd = message.command
        is_admin = await admin_check(message)
        if not is_admin:
            await message.delete()
            return

        umsg = ""
        umedia = ""
        ustickers = ""
        uanimations = ""
        ugames = ""
        uinlinebots = ""
        uwebprev = ""
        upolls = ""
        uinfo = ""
        uinvite = ""
        upin = ""
        uperm = "" # pylint:disable=E0602

        unlock_type = " ".join(cmd[1:])
        chat_id = message.chat.id

        if not unlock_type:
            await message.edit("`can't unlock the void`")
            await asyncio.sleep(5)
            await message.delete()
            return

        get_uperm = await client.get_chat(chat_id)

        umsg = get_uperm.permissions.can_send_messages
        umedia = get_uperm.permissions.can_send_media_messages
        ustickers = get_uperm.permissions.can_send_stickers
        uanimations = get_uperm.permissions.can_send_animations
        ugames = get_uperm.permissions.can_send_games
        uinlinebots = get_uperm.permissions.can_use_inline_bots
        uwebprev = get_uperm.permissions.can_add_web_page_previews
        upolls = get_uperm.permissions.can_send_polls
        uinfo = get_uperm.permissions.can_change_info
        uinvite = get_uperm.permissions.can_invite_users
        upin = get_uperm.permissions.can_pin_messages

        if unlock_type == "all":
            try:
                await client.set_chat_permissions(chat_id,
                                                ChatPermissions(can_send_messages=True,
                                                                can_send_media_messages=True,
                                                                can_send_stickers=True,
                                                                can_send_animations=True,
                                                                can_send_games=True,
                                                                can_use_inline_bots=True,
                                                                can_send_polls=True,
                                                                can_change_info=True,
                                                                can_invite_users=True,
                                                                can_pin_messages=True,
                                                                can_add_web_page_previews=True))

                await message.edit("`Unlocked all permission from this Chat!`")
                await asyncio.sleep(5)
                await message.delete()

            except Exception as e:
                await message.edit("`permission denied`\n"
                    f"**Log:** `{e}`")
            return

        if unlock_type == "msg":
            umsg = True
            uperm = "messages"

        elif unlock_type == "media":
            umedia = True
            uperm = "audios, documents, photos, videos, video notes, voice notes"

        elif unlock_type == "stickers":
            ustickers = True
            uperm = "stickers"

        elif unlock_type == "animations":
            uanimations = True
            uperm = "animations"

        elif unlock_type == "games":
            ugames = True
            uperm = "games"

        elif unlock_type == "inlinebots":
            uinlinebots = True
            uperm = "inline bots"

        elif unlock_type == "webprev":
            uwebprev = True
            uperm = "web page previews"

        elif unlock_type == "polls":
            upolls = True
            uperm = "polls"

        elif unlock_type == "info":
            uinfo = True
            uperm = "info"

        elif unlock_type == "invite":
            uinvite = True
            uperm = "invite"

        elif unlock_type == "pin":
            upin = True
            uperm = "pin"

        else:
            await message.edit("`Invalid Unlock Type!`")
            await asyncio.sleep(5)
            await message.delete()
            return

        try:
            await client.set_chat_permissions(chat_id,
                                            ChatPermissions(can_send_messages=umsg,
                                                            can_send_media_messages=umedia,
                                                            can_send_stickers=ustickers,
                                                            can_send_animations=uanimations,
                                                            can_send_games=ugames,
                                                            can_use_inline_bots=uinlinebots,
                                                            can_add_web_page_previews=uwebprev,
                                                            can_send_polls=upolls,
                                                            can_change_info=uinfo,
                                                            can_invite_users=uinvite,
                                                            can_pin_messages=upin))

            await message.edit(f"`Unlocked {uperm} for this chat!`")
            await asyncio.sleep(5)
            await message.delete()

        except Exception as e:
            await message.edit("`Error!`\n"
                f"**Log:** `{e}`")
    else:
        await message.delete()


@app.on_message(filters.me & filters.command(["vlock"], Command))
async def view_perm(client, message):
    """view group permission"""
    if message.chat.type in ['group', 'supergroup']:
        is_admin = await admin_check(message)
        if not is_admin:
            await message.delete()
            return

        v_perm = ""
        vmsg = ""
        vmedia = ""
        vstickers = ""
        vanimations = ""
        vgames = ""
        vinlinebots = ""
        vwebprev = ""
        vpolls = ""
        vinfo = ""
        vinvite = ""
        vpin = ""

        v_perm = await client.get_chat(message.chat.id)

        def convert_to_emoji(val: bool):
            if val is True:
                return "<code>True</code>"
            return "<code>False</code>"

        vmsg = convert_to_emoji(v_perm.permissions.can_send_messages)
        vmedia = convert_to_emoji(v_perm.permissions.can_send_media_messages)
        vstickers = convert_to_emoji(v_perm.permissions.can_send_stickers)
        vanimations = convert_to_emoji(v_perm.permissions.can_send_animations)
        vgames = convert_to_emoji(v_perm.permissions.can_send_games)
        vinlinebots = convert_to_emoji(v_perm.permissions.can_use_inline_bots)
        vwebprev = convert_to_emoji(v_perm.permissions.can_add_web_page_previews)
        vpolls = convert_to_emoji(v_perm.permissions.can_send_polls)
        vinfo = convert_to_emoji(v_perm.permissions.can_change_info)
        vinvite = convert_to_emoji(v_perm.permissions.can_invite_users)
        vpin = convert_to_emoji(v_perm.permissions.can_pin_messages)

        if v_perm is not None:
            try:
                permission_view_str = ""

                permission_view_str += "<b>Chat permissions:</b>\n"
                permission_view_str += f"<b>Send Messages:</b> {vmsg}\n"
                permission_view_str += f"<b>Send Media:</b> {vmedia}\n"
                permission_view_str += f"<b>Send Stickers:</b> {vstickers}\n"
                permission_view_str += f"<b>Send Animations:</b> {vanimations}\n"
                permission_view_str += f"<b>Can Play Games:</b> {vgames}\n"
                permission_view_str += f"<b>Can Use Inline Bots:</b> {vinlinebots}\n"
                permission_view_str += f"<b>Webpage Preview:</b> {vwebprev}\n"
                permission_view_str += f"<b>Send Polls:</b> {vpolls}\n"
                permission_view_str += f"<b>Change Info:</b> {vinfo}\n"
                permission_view_str += f"<b>Invite Users:</b> {vinvite}\n"
                permission_view_str += f"<b>Pin Messages:</b> {vpin}\n"

                await message.edit(permission_view_str)

            except Exception as e:
                await message.edit(
                    text="`Error!`\n"
                    f"**Log:** `{e}`")
    else:
        await message.delete()