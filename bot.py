from telethon import events, TelegramClient, Button
import logging
from telethon.tl.functions.users import GetFullUserRequest as us
import os


logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN", None)

bot = TelegramClient(
        "Whisper",
        api_id=6,
        api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e"
        ).start(
                bot_token=TOKEN
                )
db = {}

@bot.on(events.NewMessage(pattern="^[!?/]start$"))
async def stsrt(event):
    await event.reply(
            "**Salam, Mən @sjrvan 'ın boş vaxtında hazırlanmış gizli mesaj botuyam istifadə qaydasını yəqinki bilirsən!\n\nİstifadə qaydası:@nnbazbot Salam Şirvan! @sjrvan**",
            buttons=[
                [Button.switch_inline("Mesaj yaz!", query="")]
                ]
            )


@bot.on(events.InlineQuery())
async def die(event):
    if len(event.text) != 0:
        return
    me = (await bot.get_me()).username
    dn = event.builder.article(
            title="Mən Gizli Mesaj botuyam!",
            description="Mən gizli mesaj botuyam!\n(c) @Sjrvan",
            text=f"**Mən Gizli Mesaj Botuyam**\n`@{me} Salam UserID|Message`\n**(c) Sjrvan**",
            buttons=[
                [Button.switch_inline(" Go Inline ", query="wspr ")]
                ]
            )
    await event.answer([dn])
    
@bot.on(events.InlineQuery(pattern="wspr"))
async def inline(event):
    me = (await bot.get_me()).username
    try:
        inp = event.text.split(None, 1)[1]
        user, msg = inp.split("|")
    except IndexError:
        await event.answer(
                [], 
                switch_pm=f"@{me} [UserID]|[Message]",
                switch_pm_param="start"
                )
    except ValueError:
        await event.answer(
                [],
                switch_pm=f"Mənə bir mesaj ver!",
                switch_pm_param="start"
                )
    try:
        ui = await bot(us(user))
    except BaseException:
        await event.answer(
                [],
                switch_pm="Xətalı User ID/Username",
                switch_pm_param="start"
                )
        return
    db.update({"user_id": ui.user.id, "msg": msg, "self": event.sender.id})
    text = f"""
Gizli Mesaj Göndərilib 
Arasında [{ui.user.first_name}](tg://user?id={ui.user.id})!
Klik et mesajı görüntülə!
**Qeyd:** __Yalnız {ui.user.first_name} mesajı aça bilər!__
    """
    dn = event.builder.article(
            title="Gizli mesajdır! Kiminsə şəxsi söhbətinə qarışa bilmərik(",
            description="Gizli mesajdır! Kiminsə şəxsi söhbətinə qarışa bilmərik(",
            text=text,
            buttons=[
                [Button.inline(" Mesaja Bax🔔 ", data="wspr")]
                ]
            )
    await event.answer(
            [dn],
            switch_pm="Gizli mesajdır! Kiminsə şəxsi söhbətinə qarışa bilmərik(",
            switch_pm_param="start"
            )


@bot.on(events.CallbackQuery(data="wspr"))
async def ws(event):
    user = int(db["user_id"])
    lol = [int(db["self"])]
    lol.append(user)
    if event.sender.id not in lol:
        await event.answer("🔐 Gizli mesajdır! Kiminsə şəxsi söhbətinə qarışa bilmərik!", alert=True)
        return
    msg = db["msg"]
    if msg == []:
        await event.anwswer(
                "Xəta!\nDeyəsən mesaj serverimdən bu mesaj silinib!", alert=True)
        return
    await event.answer(msg, alert=True)

print("Succesfully Started Bot!")
bot.run_until_disconnected()
