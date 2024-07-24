import { goto } from '$app/navigation';


export interface APICard {
    //TODO
}

export interface APICardTypes {
    //TODO
}



export class CardMakerApi {
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
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        return response;
    }

    private async post<T>(path: string, body: { [key: string]: any }): Promise<T | null> {
        let url = new URL(path, this.endpoint);
        const headers = {
            accept: 'application/json',
            'Content-Type': 'application/json',
        };
        const options = {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(body),
        };

        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        return response;
    }

    private async put<T>(path: string, body: { [key: string]: any }): Promise<T | null> {
        let url = new URL(path, this.endpoint);
        const headers = {
            accept: 'application/json',
            'Content-Type': 'application/json',
        };
        const options = {
            method: 'PUT',
            headers: headers,
            body: JSON.stringify(body),
        };

        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        return response;
    }

    private async delete<T>(path: string, body: { [key: string]: any }): Promise<T | null> {
        let url = new URL(path, this.endpoint);
        const headers = {
            accept: 'application/json',
            'Content-Type': 'application/json',
        };
        const options = {
            method: 'DELETE',
            headers: headers,
        };

        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        return response;
    }

    public async getCardTypes(): Promise<APICardTypes[]> {
        let response = await this.get<APICard>("/card-types");
        return response.json();
    }

    public async getCard(card_id): Promise<APICardTypes[]> {
        let response = await this.get<APICard>("/cards/" + card_id);
        return response.json();
    }

    public async createCard(card): Promise<APICardTypes[]> {
        let response = await this.post<APICard>("/cards", card);
        return response.json();
    }

    public async updateCard(card, card_id): Promise<APICardTypes[]> {
        let response = await this.put<APICard>("/cards/" + card_id, card);
        return response;
    }

    public async deleteCard(card_id, redirect_path): Promise<APICardTypes[]> {
        let response = await this.delete<APICard>("/cards/" + card_id);
        goto(redirect_path);
        return response;
    }
}