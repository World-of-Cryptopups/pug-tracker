import dimscord, asyncdispatch, strutils, options, nenv

echo getEnvStr("TOKEN")
let discord = newDiscordClient(getEnvStr("TOKEN"))

proc messageCreate(s: Shard, m: Message) {.event(discord).} =
    let args = m.content.split(" ") # Splits a message.
    if m.author.bot or not args[0].startsWith("."): return
    let command = args[0][1..args[0].high]

    case command.toLowerAscii():
    of "test": # Sends a basic message.
        discard await discord.api.sendMessage(m.channel_id, "Success!")
    else:
        discard

proc onReady(s: Shard, r: Ready) {.event(discord).} =
    echo "Ready as: " & $r.user

    await s.updateStatus(activity = some ActivityStatus(
        name: "around.",
        kind: atPlaying
    ), status = "idle")

# Connect to Discord and run the bot.
waitFor discord.startSession(
    gateway_intents = {giGuildMessages, giGuilds}
)
