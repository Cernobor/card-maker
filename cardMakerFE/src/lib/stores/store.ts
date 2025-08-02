import { writable } from 'svelte/store';
import CardMakerApi from '$lib/api';
import { PUBLIC_BASE_API_URL } from '$env/static/public';

const apiInstance = new CardMakerApi(PUBLIC_BASE_API_URL);
const { subscribe, set } = writable(apiInstance);

apiInstance.attachStore(set); // ✅ This links api instance to store updates
set(apiInstance); // initial store value

export const api = {
	subscribe,
	set,
	instance: apiInstance
};
