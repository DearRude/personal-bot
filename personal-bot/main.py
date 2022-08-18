from os import environ
from asyncio import sleep

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from txt_to_pic import source_pic, text_to_pic, pa
from pyrogram import Client, filters


scheduler = AsyncIOScheduler()
app = Client("personal-bot", session_string=environ["TG_STORE"])


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
    command = message.text.split()[1:]
    merged_text = list()
    for offset in range(1, 10):
        mess = [
            m async for m in client.get_chat_history(message.chat.id, limit=1, offset=1)
        ][0]
        if mess.from_user.id != message.from_user.id:
            break
        merged_text.append(mess.text)
        await mess.delete()
    await message.delete()
    await message.reply_text("\n".join(merged_text[::-1]))


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


async def send_schedule_message(client, message, chat_id):
    await message.copy(chat_id)


@app.on_message(filters.command("mkcron") & filters.user("me"))
async def schedule_message(client, message):
    job_name = message.text.split()[1]
    command = " ".join(message.text.split()[2:])
    if message.reply_to_message is not None:
        scheduler.add_job(
            send_schedule_message,
            CronTrigger.from_crontab(command),
            args=[client, message.reply_to_message, message.chat.id],
            id=job_name,
        )
        await message.reply_text(f"Job `{job_name}` is scheduled.")
    else:
        await message.reply_text("You should reply to a message")


@app.on_message(filters.command("rmcron") & filters.user("me"))
async def deschedule_message(client, message):
    job_name = message.text.split()[1]
    scheduler.remove_job(job_name)
    await message.reply_text(f"Job `{job_name}` is canceled.")


@app.on_message(filters.command("lscron") & filters.user("me"))
async def deschedule_message(client, message):
    jobs = "\n".join(
        [
            f"name: {job.id} \t\t next_run: {job.next_run_time}"
            for job in scheduler.get_jobs()
        ]
    )
    await message.reply_text(f"List jobs:\n`{jobs}`")


@app.on_message(filters.command("clear") & filters.user("me"))
async def delete_messages(client, message):
    deletion_count = 0

    command = message.text.split()[1:]
    message_iteration = client.get_chat_history(
        message.chat.id, limit=int(command[0]), offset=1
    )
    async for mess in message_iteration:
        deleted = await mess.delete()
        if deleted:
            deletion_count += 1
    await message.delete()
    counter = await message.reply(f"{deletion_count} messages deleted.")
    await sleep(5)
    await counter.delete()


scheduler.start()
app.run()
