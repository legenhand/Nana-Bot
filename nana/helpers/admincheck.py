from pyrogram.types import Message


async def admin_check(message: Message) -> bool:
    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await client.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    admin_strings = [
        "creator",
        "administrator"
    ]
    # https://git.colinshark.de/PyroBot/PyroBot/src/branch/master/pyrobot/modules/admin.py#L69
    if check_status.status not in admin_strings:
        return False
    else:
        return True


async def is_sudoadmin(message: Message) -> bool:
    client = message._client
    check_user = await client.get_chat_member(message.chat.id, message.from_user.id)
    user_type = check_user.status
    if user_type == "member":
        return False
    if user_type == "administrator":
        add_adminperm = check_user.can_promote_members
        if add_adminperm:
            return True
        return False
    return True
