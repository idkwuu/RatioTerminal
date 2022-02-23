import { DiscordenoMessage } from "https://deno.land/x/discordeno@13.0.0-rc15/src/transformers/message.ts";
import {addReaction, Bot, sendMessage} from "https://deno.land/x/discordeno@13.0.0-rc15/mod.ts";

// <User ID, Date>
const timeouts = new Map<bigint, Date | undefined>([])

// <User ID, override>
let overrides: Record<string, string> = {}
try {
    overrides = JSON.parse(await Deno.readTextFile("overrides.json"))
// deno-lint-ignore no-unused-vars
} catch (e) { 
    // When the warning is sus!
}

export default function handleThisRatio(bot: Bot, message: DiscordenoMessage) {
    const timeoutData: Date | undefined = timeouts.get(message.authorId) || undefined
    
    if (timeoutData != undefined) {
        const timeDiff = new Date().getTime() - timeoutData.getTime()
        // One ratio per minute
        if (timeDiff >= 15000) {
            timeouts.set(message.authorId, new Date())
        } else {
            addReaction(bot, message.channelId, message.id, "💀")
                .catch((e) => console.log("Error reacting (bad ratio): " + e))
            return
        }
    }

    timeouts.set(message.authorId, new Date())

    // Check for a ratio override
    const ratioOverride: string | undefined = overrides[message.authorId.toString()]
    let ratioResult: boolean
    if (ratioOverride != undefined) {
        ratioResult = ratioOverride === "accept"
    } else {
        ratioResult = Math.floor(Math.random() * 2) === 0
    }

    addReaction(bot, message.channelId, message.id, ratioResult ? "👍" : "👎")
        .catch((e) => console.log("Error reacting (ratio reaction): " + e))
    
    sendMessage(bot, message.channelId, 
        {
            content: ratioResult
                ? "https://docs.idkwuu.dev/ratioaccepted.png"
                : "https://docs.idkwuu.dev/ratiodeclined.png",
            messageReference: {
                messageId: message.id,
                failIfNotExists: true
            }
        }
    )
        .catch((e) => console.log("Error reacting (ratio image): " + e))

}
