import { Bot, DiscordenoMessage, sendMessage } from "https://deno.land/x/discordeno@13.0.0-rc15/mod.ts";

export default function sendFile(bot: Bot, message: DiscordenoMessage, fileName: string, asReply = true) {
    const file = Deno.readFileSync(fileName)
    sendMessage(bot, message.channelId,
        {
            file: { blob: new Blob([file.buffer], { type: 'text/plain' }), name: fileName },
            messageReference: {
                messageId: asReply ? message.id : undefined,
                failIfNotExists: true
            }
        }
    )
        .catch((e) => console.log("Error sending file (" + fileName + "): "+ e))
}