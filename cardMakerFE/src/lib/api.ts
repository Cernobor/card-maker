import type { CardSpec, ErrorWithMessage } from './types';

const PREFIX = '/api';

export async function getCards() {
    try {
        return await fetchResource("cards");
    } catch (error) {
        console.error(`Error fetching cards!: ${getErrorMessage(getErrorMessage(error))}`);
        return [];
    }
}


export async function getCard(id: number) {
    try {
        return await fetchResource(`cards/${id}`);
    } catch (error) {
        console.error(`Error fetching cards!: ${getErrorMessage(getErrorMessage(error))}`);
    }
}


export async function getAuthors() {
    try {
        return await fetchResource("users");
    } catch (error) {
        console.error(`Error fetching authors!: ${getErrorMessage(error)}`);
        return [];
    }
}


export async function getTypes() {
    try {
        return await fetchResource("card-types");
    } catch (error) {
        console.error(`Error fetching types!: ${getErrorMessage(error)}`);
        return [];
    }
}


export async function getTags() {
    try {
        return await fetchResource("tags");
    } catch (error) {
        console.error(`Error fetching tags!: ${getErrorMessage(error)}`);
        return [];
    }
}


export function createCard(cardSpec: CardSpec) {
    const requestBody = JSON.stringify(cardSpec);
    console.log('TOTO SE POSÍLÁ');
    console.log(requestBody);
    return fetch(`${PREFIX}/cards`, {
        method: 'POST',
        headers: {
            'content-type': 'application/json'
        },
        body: requestBody
    });
}


export function updateCard(id: number, cardSpec: CardSpec) {
    const requestBody = JSON.stringify(cardSpec);
    return fetch(`${PREFIX}/cards/${id}`, {
        method: 'PUT',
        headers: {
            'content-type': 'application/json'
        },
        body: requestBody
    });
}


async function fetchResource(resourceName: string) {
    const response = await fetch(`${PREFIX}/${resourceName}`);
    if (!response.ok) {
        throw new Error(`Resource ${resourceName} not available: ${response.status}`);
    }
    return response.json();
}


function isErrorWithMessage(error: unknown): error is ErrorWithMessage {
	return (
		typeof error === 'object' &&
		error !== null &&
		'message' in error &&
		typeof (error as Record<string, unknown>).message === 'string'
	)
}


function toErrorWithMessage(maybeError: unknown): ErrorWithMessage {
	if (isErrorWithMessage(maybeError)) return maybeError

	try {
		return new Error(JSON.stringify(maybeError))
	} catch {
		// fallback in case there's an error stringifying the maybeError
		// like with circular references for example.
		return new Error(String(maybeError))
	}
}


function getErrorMessage(error: unknown) {
	return toErrorWithMessage(error).message
}


