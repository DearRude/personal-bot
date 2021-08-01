from time import sleep
from os import environ

import toml
from personal_bot.txt_to_pic import source_pic, text_to_pic, pa
from pyrogram import Client, filters

dir_conf = environ.get("PB_CONF_DIR", ".")
confs = toml.load(f"{dir_conf}/conf.toml")

app = Client(confs["pyrogram"]["session_store"],
             api_id=confs["pyrogram"]["api_id"],
             api_hash=confs["pyrogram"]["api_hash"])

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


@app.on_message(filters.command(["clear", "siktir"]) & filters.user(["me", 37087739]))
async def delete_messages(client, message):
    mes_id, deletion_count = message.message_id, 0
    command = message.text.split()[1:]
    message_iteration = client.iter_history(message.chat.id,
        limit=int(command[0]), offset=1)
    async for mess in message_iteration:
        deleted = await mess.delete()
        if deleted:
            deletion_count += 1
    await message.reply_text(f"{deletion_count} messages deleted.")

app.run()
