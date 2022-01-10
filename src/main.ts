/*
> Source code: https://github.com/idkwuu/RatioTerminal

MIT License

Copyright (c) 2022 idkwuu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

import { createBot, startBot} from "https://deno.land/x/discordeno@13.0.0-rc15/mod.ts";
import {enableCachePlugin, enableCacheSweepers} from "https://deno.land/x/discordeno_cache_plugin@0.0.18/mod.ts";
import handleRatio from "./handleRatio.ts";
import sendFile from "./helpers.ts";

const BOT_TOKEN = Deno.env.get("RATIO_TERMINAL_TOKEN") || ""
const BOT_ID = BigInt(atob(BOT_TOKEN.split(".")[0]))

// RATIO_TERIMNAL_TOKEN is undefined
if (BOT_TOKEN == "") {
    console.log("RATIO_TERMINAL_TOKEN is not defined.")
    Deno.exit(1)
}

const regex = /(?:^|\W)ratio+(?:$|\W)|counter(?:$|\W)/;

const baseBot = createBot({
    token: BOT_TOKEN,
    botId: BOT_ID,
    intents: ["Guilds", "GuildMessages", "GuildMessageReactions"],
    events: {
        ready() {
            // Connected
            console.log("Ready to fire some ratios.")
        },
        messageCreate(bot, message) {
            // Process message
            switch (message.content) {
                case "ratio bot send code!!": {
                    sendFile(bot, message, 'main.ts')
                    sendFile(bot, message, 'handleRatio.ts', false)
                    sendFile(bot, message, 'helpers.ts', false)
                    return
                }
                case "ratio bot send overrides!!": {
                    sendFile(bot, message, 'overrides.json')
                    return
                }
                default: {
                    if (!regex.test(message.content.toLowerCase())) return;
                    handleRatio(bot, message)
                }
            }
        }
    }
})

const bot = enableCachePlugin(baseBot)

enableCacheSweepers(bot)

await startBot(bot)
