
import { PUBLIC_BASE_API_URL } from '$env/static/public';
export interface APICard {
    //TODO
}



export class CardMakerApi{
    public constructor() {
        this.endpoint = PUBLIC_BASE_API_URL;
    }

    private async get<T>(path: string, params: { [key: string]: string } = {}): Promise<T | null> {
        const urlparams = new URLSearchParams(params);
        let url = new URL(path, this.endpoint);
        url.search = urlparams.toString();
        const headers = {
            accept: 'application/json',
        };
        const options = {
            method: 'GET',
            headers: headers,
        };
        console.log(url);
        const response = await fetch(url, options);
        if (! response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
       
        return response;
    }


    public async getCardTypes(): Promise<APICard[]> {
        let response = await this.get<APICard>("/card-types");
        return response.json();
    }


}