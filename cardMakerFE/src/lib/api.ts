import { goto } from '$app/navigation';
import { clearSessionStorage, tokens } from './stores/tokens';
import type {
	CardBase,
	UserPublic,
	CardGet,
	CardCreate,
	CardType,
	UserCreate,
	Tag,
	UserLogin,
	JWTToken
} from './interfaces';

export default class CardMakerApi {
	/**
	 * Class for handling communication with API
	 */
	private endpoint: string;
	private jwtToken: string = '';
	public loggedIn: boolean;
	public currentUser: UserPublic | null = null;

	public constructor(api_endpoint: string) {
		this.endpoint = api_endpoint;
		// Get session values from store
		if (typeof window !== undefined) {
			tokens.subscribe((value) => {
				this.jwtToken = value.jwtToken;
				if (value.username !== '' && value.userId !== '') {
					this.currentUser = { username: value.username, id: Number(value.userId) };
				}
			});
		}
		this.loggedIn = this.jwtToken !== '';
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

	private async post<T>(path: string, body: { [key: string]: any }): Promise<T> {
		/**
		 * Post data to the endpoint.
		 *
		 * @param path - path to the resource
		 * @param body - request body
		 *
		 * @returns promise of the given type
		 *
		 * @throws HTTPError if not response ok
		 */
		let url = new URL(path, this.endpoint);
		const headers = {
			accept: 'application/json',
			'Content-Type': 'application/json',
			Authorization: `Bearer ${this.jwtToken}`
		};
		const options = {
			method: 'POST',
			headers: headers,
			body: JSON.stringify(body)
		};

		const response = await fetch(url, options);
		if (!response.ok) {
			throw new Error(`Response status: ${response.status}}`);
		}
		return response.json();
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
			'Content-Type': 'application/json',
			Authorization: `Bearer ${this.jwtToken}`
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
			'Content-Type': 'application/json',
			Authorization: `Bearer ${this.jwtToken}`
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
		 * @returns array of card types
		 */
		return await this.get<CardType[]>('/card-types');
	}

	public async getCard(cardId: number): Promise<CardGet> {
		/**
		 * Get card object by.
		 *
		 * @param cardId - ID of card
		 *
		 * @returns card object
		 */
		return await this.get<CardGet>('/cards/' + cardId);
	}

	public async getCards(): Promise<CardGet[]> {
		/**
		 * Get array of cards.
		 *
		 * @returns array of cards
		 */
		return await this.get<CardGet[]>('/cards');
	}

	public async createCard(card: CardCreate) {
		/**
		 * Create new card.
		 *
		 * @param card - card object
		 */
		await this.post('/cards', card);
	}

	public async updateCard(card: CardBase, cardId: number) {
		/**
		 * Update existing card with ID.
		 *
		 * @param card - card object
		 * @param cardId - ID of card to update
		 */
		await this.put('/cards/' + cardId, card);
	}

	public async deleteCard(crdiId: number, rediredcPath: string) {
		/**
		 * Delete existing card with ID.
		 *
		 * @param cardId - ID of card to delete
		 */
		await this.delete('/cards/' + crdiId);
		goto(rediredcPath);
	}

	public async getUsers(): Promise<UserPublic[]> {
		/**
		 * Get array of users.
		 *
		 * @returns array of users
		 */
		return await this.get<UserPublic[]>('/users');
	}

	public async getTags(): Promise<Tag[]> {
		/**
		 * Get array of tags.
		 *
		 * @returns array of tags
		 */
		return await this.get<Tag[]>('/tags');
	}

	public async createUser(user: UserCreate) {
		/**
		 * Create new user.
		 *
		 * @param user - user object
		 */
		await this.post('/users', user);
	}

	public async logIn(user: UserLogin) {
		/**
		 * Get JWT token and save it to the session store.
		 *
		 * @param user - user object with username and passeord
		 */
		const response = await this.post<JWTToken>('/users/me', user);
		this.jwtToken = response.access_token;
		this.loggedIn = true;
		this.currentUser = {
			username: user.username,
			id: response.user_id
		};
		tokens.set({
			jwtToken: this.jwtToken,
			username: this.currentUser.username,
			userId: String(this.currentUser.id)
		});
	}

	public logOut(rediredcPath: string) {
		/**
		 * Clear the session store.
		 *
		 * @param rediredcPath - where to redirect after logout
		 */
		this.jwtToken = '';
		this.currentUser = null;
		this.loggedIn = false;
		clearSessionStorage();
		goto(rediredcPath);
	}
}
