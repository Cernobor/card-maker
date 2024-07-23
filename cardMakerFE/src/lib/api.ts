


export interface APICard {
    //TODO
}

export interface APICardTypes {
    //TODO
}



export class CardMakerApi{
    public constructor(api_endpoint: string) {
        this.endpoint = api_endpoint;
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


    public async getCardTypes(): Promise<APICardTypes[]> {
        let response = await this.get<APICard>("/card-types");
        return response.json();
    }
    public async getCard(): Promise<APICardTypes[]> {
        let response = await this.get<APICard>("/card-types");
        return response.json();
    }
}