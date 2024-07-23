import { PUBLIC_BASE_API_URL } from '$env/static/public';
import { CardMakerApi } from '$lib/api';
import { writable } from "svelte/store";
//token will be used in foture by login
//možná nefunguje reaktivita, bude to chtít vyzkoušet
export let api = writable("token", ()=>{new CardMakerApi(PUBLIC_BASE_API_URL)})
