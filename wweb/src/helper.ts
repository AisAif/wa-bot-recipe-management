import RasaClient, { RasaRequest } from "./clients/rasa.client";
import { Message } from "whatsapp-web.js";

const sendMessage = async (
  rasaClient: RasaClient,
  rasaRequest: RasaRequest,
  message: Message
) => {
  console.log(rasaRequest.sender);
  let chatbotResponses = await rasaClient.send({
    sender: rasaRequest.sender,
    message: rasaRequest.message,
  });
  chatbotResponses.forEach((response) => message.reply(response.text));
};

export { sendMessage };
