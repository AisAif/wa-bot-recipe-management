import axios from "axios";

type RasaConfig = {
  url: string;
};

export type RasaRequest = {
    sender: string;
    message: string;
}

export type RasaResponse = {
    recipient_id: string;
    text: string;
}
class RasaClient {
  constructor(private config: RasaConfig) {}

  async send(request: RasaRequest): Promise<RasaResponse[]> {
      const response =  await axios.post(this.config.url, request);
      return response.status == 200 ? response.data : [];
  }
}
export default RasaClient;
