import { PUBLIC_BASE_API_URL } from '$env/static/public';
import { CardMakerApi } from '$lib/api';

export let api = new CardMakerApi(PUBLIC_BASE_API_URL);
