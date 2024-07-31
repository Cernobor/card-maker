import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export const sessionData = writable({
	/**
	 * Initialize JWT token, username and user ID values.
	 */
	jwtToken: browser ? sessionStorage.getItem('jwtToken') || '' : '',
	username: browser ? sessionStorage.getItem('username') || '' : '',
	userId: browser ? sessionStorage.getItem('userId') || '' : ''
});

if (browser) {
	sessionData.subscribe(
		({ jwtToken, username, userId }: { jwtToken: string; username: string; userId: string }) => {
			/**
			 * Save new values to session storage if values are changed.
			 */
			sessionStorage.setItem('jwtToken', jwtToken);
			sessionStorage.setItem('username', username);
			sessionStorage.setItem('userId', userId);
		}
	);
}

export function clearSessionStorage() {
	/**
	 * Clear session storage and reinitialize session data to an empty string.
	 */
	if (browser) {
		sessionStorage.clear();

		sessionData.set({
			jwtToken: '',
			username: '',
			userId: ''
		});
	}
}
