import { PUBLIC_BASE_API_URL } from '$env/static/public';
import type { ErrorWithMessage } from './types';


export async function fetchCards() {
    try {
        return await fetchResource("cards");
    } catch (error) {
        console.error(`Error fetching cards!: ${getErrorMessage(getErrorMessage(error))}`);
        return [];
    }
}


export async function fetchAuthors() {
    try {
        return await fetchResource("users");
    } catch (error) {
        console.error(`Error fetching authors!: ${getErrorMessage(error)}`);
        return [];
    }
}


export async function fetchTypes() {
    try {
        return await fetchResource("card-types");
    } catch (error) {
        console.error(`Error fetching types!: ${getErrorMessage(error)}`);
        return [];
    }
}


async function fetchResource(resourceName: string) {
    const response = await fetch(`${PUBLIC_BASE_API_URL}/cardmaker/${resourceName}`);
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


