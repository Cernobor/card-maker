import { goto } from '$app/navigation';
import { getErrorMessage } from './errors';
import type { UserPublic, CardGet, CardCreate, CardType, UserCreate, Tag } from './interfaces';

export default class CardMakerApi {
	/**
	 * Class for handling communication with API
	 *
	 * @todo Implement 'getToken' method and save token into cookies.
	 */
	private endpoint: string;
	//private JWTToken: string;
	public constructor(api_endpoint: string) {
		this.endpoint = api_endpoint;
	}

	private async get<T>(path: string, params: { [key: string]: string } = {}): Promise<T> {
		/**
		 * Get resource from endpoint.
		 *
		 * @param path - path to the resource
		 * @param params - query parameters
		 *
		 * @returns promise of the resource
		 *
		 * @throws HTTPError if not response ok
		 */
		const urlparams = new URLSearchParams(params);
		let url = new URL(path, this.endpoint);
		url.search = urlparams.toString();
		const headers = {
			accept: 'application/json'
		};
		const options = {
			method: 'GET',
			headers: headers
		};
		const response = await fetch(url, options);
		if (!response.ok) {
			throw new Error(`Response status: ${response.status}`);
		}
		return response.json() as T;
	}

	private async post(path: string, body: { [key: string]: any }) {
		/**
		 * Post data to the endpoint.
		 *
		 * @param path - path to the resource
		 * @param body - request body
		 *
		 * @throws HTTPError if not response ok
		 */
		let url = new URL(path, this.endpoint);
		const headers = {
			accept: 'application/json',
			'Content-Type': 'application/json'
		};
		const options = {
			method: 'POST',
			headers: headers,
			body: JSON.stringify(body)
		};

		const response = await fetch(url, options);
		if (!response.ok) {
			throw new Error(`Response status: ${response.status}`);
		}
	}

	private async put(path: string, body: { [key: string]: any }) {
		/**
		 * Put data to the endpoint.
		 *
		 * @param path - path to the resource
		 * @param body - request body
		 *
		 * @throws HTTPError if not response ok
		 */
		let url = new URL(path, this.endpoint);
		const headers = {
			'Content-Type': 'application/json'
		};
		const options = {
			method: 'PUT',
			headers: headers,
			body: JSON.stringify(body)
		};

		const response = await fetch(url, options);
		if (!response.ok) {
			throw new Error(`Response status: ${response.status}`);
		}
	}

	private async delete(path: string) {
		/**
		 * Delete data on the endpoint.
		 *
		 * @param path - path to the resource
		 *
		 * @throws HTTPError if not response ok
		 */
		let url = new URL(path, this.endpoint);
		const headers = {
			'Content-Type': 'application/json'
		};
		const options = {
			method: 'DELETE',
			headers: headers
		};

		const response = await fetch(url, options);
		if (!response.ok) {
			throw new Error(`Response status: ${response.status}`);
		}
	}

	public async getCardTypes(): Promise<CardType[]> {
		/**
		 * Get array of types of cards (e.g. Aspekt).
		 *
		 * @returns array of card types or an empty array if error
		 */
		try {
			return await this.get<CardType[]>('/card-types');
		} catch (error) {
			console.error(`Error getting card types: ${getErrorMessage(error)}`);
			return [];
		}
	}

	public async getCard(cardId: number): Promise<CardGet | null> {
		/**
		 * Get card object by.
		 *
		 * @param cardId - ID of card
		 *
		 * @returns card object of null if error
		 */
		try {
			return await this.get<CardGet>('/cards/' + cardId);
		} catch (error) {
			console.error(`Error getting card types: ${getErrorMessage(error)}`);
			return null;
		}
	}

	public async getCards(): Promise<CardGet[]> {
		/**
		 * Get array of cards.
		 *
		 * @returns array of cards or an empty array if error
		 */
		try {
			return await this.get<CardGet[]>('/cards');
		} catch (error) {
			console.error(`Error getting cards: ${getErrorMessage(error)}`);
			return [];
		}
	}

	public async createCard(card: CardCreate) {
		/**
		 * Create new card or alert if not success.
		 *
		 * @param card - card object
		 */
		try {
			await this.post('/cards', card);
		} catch (error) {
			console.error(`Error creating card: ${getErrorMessage(error)}`);
			alert('Během tvorby karty nastala chyba. Zkus to znova.');
		}
	}

	public async updateCard(card: CardCreate, cardId: number) {
		/**
		 * Update existing card with ID or alert if not success.
		 *
		 * @param card - card object
		 * @param cardId - ID of card to update
		 */
		try {
			await this.put('/cards/' + cardId, card);
		} catch (error) {
			console.error(`Error updating card: ${getErrorMessage(error)}`);
		}
	}

	public async deleteCard(crdiId: number, rediredcPath: string) {
		/**
		 * Delete existing card with ID or alert if not success.
		 *
		 * @param cardId - ID of card to delete
		 */
		goto(rediredcPath);
		try {
			await this.delete('/cards/' + crdiId);
			goto(rediredcPath);
		} catch (error) {
			console.error(`Error deleting card ${crdiId}: ${getErrorMessage(error)}`);
		}
	}

	public async getUsers(): Promise<UserPublic[]> {
		/**
		 * Get array of users.
		 *
		 * @returns array of users or an empty array if error
		 */
		try {
			return this.get<UserPublic[]>('/users');
		} catch (error) {
			console.error(`Error getting users: ${getErrorMessage(error)}`);
			return [];
		}
	}

	public async getTags(): Promise<Tag[] | null> {
		/**
		 * Get array of tags.
		 *
		 * @returns array of tags or an empty array if error
		 */
		try {
			return this.get<Tag[]>('/tags');
		} catch (error) {
			console.error(`Error getting tags: ${getErrorMessage(error)}`);
			return [];
		}
	}

	public async createUser(user: UserCreate) {
		/**
		 * Create new user or alert if not success.
		 *
		 * @param user - user object
		 */
		try {
			this.post('/users', user);
		} catch (error) {
			console.error(`Error creating user: ${getErrorMessage(error)}`);
		}
	}
}
