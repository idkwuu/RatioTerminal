const { Client, Intents } = require('discord.js');
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_MESSAGE_REACTIONS] });

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('messageCreate', async message => {
	if (message.author.bot || !message.guild) return;
	const content = message.content.toLowerCase();
    if (content.includes('ratio')) {
        let random = Math.floor(Math.random() * 2);
        message.react(random == 0 ? '👎' : '👍')
        message.reply({
            files: [
                random == 0 
                    ? "https://docs.idkwuu.dev/ratiodeclined.png"
                    : "https://docs.idkwuu.dev/ratioaccepted.png"
            ]
        });
    }
});

client.login(process.env.RATIO_TERMINAL_TOKEN);