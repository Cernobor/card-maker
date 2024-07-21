
export interface APICard {
    //TODO
}



export class CardMakerApi{
    public constructor(endpoint: string) {
        this.endpoint = endpoint;
    }

    private async get<T>(path: string, params: { [key: string]: string } = {}): Promise<Result<T | null>> {
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
        let response = await fetch(url, options);
        if (response.status == 404) {
            return Result.ok(null);
        }
        if (! response.ok) {
            return Result.err(new Error("Failed to fetch: " + response.statusText));
        }
        let data = await response.json();
        return Result.ok(data);
    }

    public async getCard(): Promise<APICard[]> {
        let response = await this.get<APIBareosClientList>("/cards");
        if (response.isErr) {
            throw response.error;
        }
        if (response.value == null) {
            return [];
        }
        return Object.values(response.value.clients);
    }

    public async getCardTypes(): Promise<APICard[]> {
        let response = await this.get<APIBareosClientList>("/card-types");
        if (response.isErr) {
            throw response.error;
        }
        if (response.value == null) {
            return [];
        }
        return Object.values(response.value.clients);
    }


}