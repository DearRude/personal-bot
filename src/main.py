from os import environ
from time import sleep

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from txt_to_pic import source_pic, text_to_pic, pa
from pyrogram import Client, filters


scheduler = AsyncIOScheduler()
app = Client(
    environ["TG_STORE"], api_id=int(environ["API_ID"]), api_hash=environ["API_HASH"]
)


@app.on_message(filters.command("pic") & filters.user("me"))
async def make_pic(client, message):
    reply_mes = message.reply_to_message

    command = message.text.split(maxsplit=2)[1:]

    name = reply_mes.from_user.first_name
    name += f" {reply_mes.from_user.last_name}" if reply_mes.from_user.last_name else ""

    name = command[1] if len(command) == 2 else name
    align = command[0] if len(command) >= 1 else "center"

    text_to_pic(reply_mes.text, name, align=align)
    await reply_mes.reply_photo(source_pic / "sticker.png")
    await client.send_document("me", source_pic / "sticker.png")


@app.on_message(filters.command("uuid4") & filters.user("me"))
async def make_uuid(client, message):
    from uuid import uuid4

    command = message.text.split()[1:]
    if len(command) > 0 and command[0] == "hex":
        await message.reply_text(f"`{uuid4().hex}`", quote=True)
    else:
        await message.reply_text(f"`{uuid4()}`", quote=True)


@app.on_message(filters.command("merge") & filters.user("me"))
async def merge_messages(client, message):
    mes_id, deletion_count = message.message_id, 0
    command = message.text.split()[1:]
    message_iteration = client.iter_history(
        message.chat.id, limit=int(command[0]), offset=1
    )
    merged_text = list()
    async for mess in message_iteration:
        merged_text.append(mess.text)
        deleted = await mess.delete()
    await message.delete()
    await message.reply_text("\n".join(merged_text[::-1]), quote=True)


@app.on_message(filters.command("sticker") & filters.user("me"))
async def make_sticker(client, message):
    reply_mes = message.reply_to_message

    command = message.text.split(maxsplit=2)[1:]

    name = reply_mes.from_user.first_name
    name += f" {reply_mes.from_user.last_name}" if reply_mes.from_user.last_name else ""
    name = command[1] if len(command) == 2 else name
    align = command[0] if len(command) >= 1 else "center"

    text_to_pic(reply_mes.text, name, align=align)
    await reply_mes.reply_sticker(source_pic / "sticker.webp")


@app.on_message(filters.command("addsticker") & filters.user("me"))
async def add_to_sticker(client, message):
    command = message.text.split()[1:]
    await client.send_message("@Stickers", "/addsticker")
    await client.send_message("@Stickers", command[0])
    await client.send_document("@Stickers", source_pic / "sticker.png")
    await client.send_message("@Stickers", "👾")
    await client.send_message("@Stickers", "/done")
    await message.reply_text("Done.")


async def send_schedule_message(client, message, text):
    await message.reply_text(text)


@app.on_message(filters.command("schedule") & filters.user("me"))
async def schedule_message(client, message):
    command = ' '.join(message.text.split()[1:])
    if message.reply_to_message is not None:
        scheduler.add_job(
            send_schedule_message,
            CronTrigger.from_crontab(command),
            args=[client, message, message.reply_to_message.text],
        )
        await message.reply_text("Message scheduled.")
    else:
        await message.reply_text("You should reply to a message")


@app.on_message(filters.command("clear") & filters.user("me"))
async def delete_messages(client, message):
    mes_id, deletion_count = message.message_id, 0
    command = message.text.split()[1:]
    message_iteration = client.iter_history(
        message.chat.id, limit=int(command[0]), offset=1
    )
    async for mess in message_iteration:
        deleted = await mess.delete()
        if deleted:
            deletion_count += 1
    await message.reply_text(f"{deletion_count} messages deleted.")


scheduler.start()
app.run()
