import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export const tokens = writable({
	jwtToken: browser ? sessionStorage.getItem('jwtToken') || '' : '',
	username: browser ? sessionStorage.getItem('username') || '' : '',
	userId: browser ? sessionStorage.getItem('userId') || '' : ''
});

if (browser) {
	tokens.subscribe(
		({ jwtToken, username, userId }: { jwtToken: string; username: string; userId: string }) => {
			sessionStorage.setItem('jwtToken', jwtToken);
			sessionStorage.setItem('username', username);
			sessionStorage.setItem('userId', userId);
		}
	);
}

tokens.set({
	jwtToken: '',
	username: '',
	userId: ''
});

export function clearSessionStorage() {
	if (browser) {
		sessionStorage.clear();

		tokens.set({
			jwtToken: '',
			username: '',
			userId: ''
		});
	}
}
