import { Client, LocalAuth } from "whatsapp-web.js";
import * as qrcode from "qrcode-terminal";
import RasaClient from "./rasa.client";
import { sendMessage } from "../helper";

const rasaClient = new RasaClient({
  url: "http://localhost:5005/webhooks/rest/webhook",
});

const client = new Client({
  puppeteer: {
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  },
  authStrategy: new LocalAuth({
    dataPath: "./auth-data",
  }),
});

client.on("ready", () => {
  console.log("Client is ready!");
});

client.on("qr", (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on("message", async (message) => {
  const chat = await message.getChat();
  if (!chat.isGroup) {
    // Handle message from DM
    await sendMessage(
      rasaClient,
      {
        sender: (await message.getContact()).number,
        message: message.body,
      },
      message
    );
  } else {
    // Handle message from group
    const mentions = await message.getMentions();
    mentions.forEach(async (mention) => {
      await sendMessage(
        rasaClient,
        {
          sender: (await message.getContact()).number,
          message: message.body,
        },
        message
      );
    });
  }
});

export default client;
