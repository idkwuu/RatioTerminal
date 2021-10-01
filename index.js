const { Client, Intents } = require('discord.js');
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_MESSAGE_REACTIONS] });

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('messageCreate', async message => {
    if (message.author.bot || !message.guild) return;
    const content = message.content.toLowerCase();
    if (content.includes('ratio')) {
        let ratioDeclined = Math.floor(Math.random() * 2) == 0;
        message.react(ratioDeclined ? '👎' : '👍').catch(reason => console.log('Couldn\'t add reaction: ' + reason))
        message.reply({
            files: [
                ratioDeclined
                    ? "https://docs.idkwuu.dev/ratiodeclined.png"
                    : "https://docs.idkwuu.dev/ratioaccepted.png"
            ]
        }).catch(reason => console.log('Couldn\'t send ratio image: ' + reason));
    }
});

client.login(process.env.RATIO_TERMINAL_TOKEN);