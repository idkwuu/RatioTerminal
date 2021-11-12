/*
MIT License

Copyright (c) 2021 idkwuu

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

const { Client, Intents } = require("discord.js");
const client = new Client({
	intents: [
		Intents.FLAGS.GUILDS,
		Intents.FLAGS.GUILD_MESSAGES,
		Intents.FLAGS.GUILD_MESSAGE_REACTIONS,
	],
});

let overrides;
try {
	overrides = require("./overrides.json");
} catch {}

let timeouts = {};

const regex = /(?:^|\W)ratio+(?:$|\W)|counter(?:$|\W)/;

client.on("ready", () => {
	console.log(`Logged in as ${client.user.tag}!`);
});

client.on("messageCreate", async (message) => {
	if (message.author.bot || !message.guild) return;

	if (message.content == 'ratio bot send code!!') {
        return message.reply({
            files: ["./ratio.js"]
        });
    }

	if (!regex.test(message.content.toLowerCase())) return;

	let ratio;

	// Ratio overrides, in overrides.json

	const ratioOverride = overrides?.[message.author.id];
	if (ratioOverride) {
		ratio = ratioOverride === "accept";
	} else {
		ratio = Math.floor(Math.random() * 2) == 0;
	}

	// Timeout - one ratio per minute
	let timeoutdata = timeouts[message.author.id]
	if (timeoutdata != undefined) {
		let timediff = new Date() - timeoutdata;
		if (timediff >= 60000) {
			timeouts[message.author.id] = new Date();
		} else {
			message
				.react("💀")
				.catch((reason) => console.log("Couldn't add no ratio reaction: " + reason));
			return;
		}
	} else {
		timeouts[message.author.id] = new Date();
	}

	message
		.react(ratio ? "👍" : "👎")
		.catch((reason) => console.log("Couldn't add reaction: " + reason));
	message
		.reply({
			files: [
				ratio
					? "https://docs.idkwuu.dev/ratioaccepted.png"
					: "https://docs.idkwuu.dev/ratiodeclined.png",
			],
		})
		.catch((reason) => console.log("Couldn't send ratio image: " + reason));
});

client.login(process.env.RATIO_TERMINAL_TOKEN);
