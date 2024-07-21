import { PUBLIC_BASE_API_URL } from '$env/static/public';
import { getErrorMessage } from "./errors";



export async function fetchCards() {
    try {
        return await fetchResource("cards");
    } catch (error) {
        console.error(`Error fetching cards!: ${getErrorMessage(error)}`);
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


export async function fetchTags() {
    try {
        return await fetchResource("tags");
    } catch (error) {
        console.error(`Error fetching tags!: ${getErrorMessage(error)}`);
        return [];
    }
}


async function fetchResource(resourceName: string) {
    const response = await fetch(`${PUBLIC_BASE_API_URL}/${resourceName}`);
    if (!response.ok) {
        throw new Error(`Resource ${resourceName} not available: ${response.status}`);
    }
    return response.json();
}





