import { PUBLIC_BASE_API_URL } from '$env/static/public';
import { getErrorMessage } from "./errors";
import type { Tag, UserPublic, CardType, CardGet } from "./interfaces";

export async function fetchCards(): Promise<object|CardGet[]|[]> {
    /**
     * Base function for GET methods.
     * 
     * @returns promise of array of cards or empty array if no cards are fetched
     */
    try {
        return await fetchResource("cards");
    } catch (error) {
        console.error(`Error fetching cards!: ${getErrorMessage(error)}`);
        return [];
    }
}

export async function fetchUsers(): Promise<object|UserPublic[]|[]> {
    /**
     * Base function for GET methods.
     * 
     * @returns promise of array of users or empty array if no users are fetched
     */
    try {
        return await fetchResource("users");
    } catch (error) {
        console.error(`Error fetching authors!: ${getErrorMessage(error)}`);
        return [];
    }
}

export async function fetchTypes(): Promise<object|CardType[]|[]> {
    /**
     * Base function for GET methods.
     * 
     * @returns promise of array of card types or empty array if no card types are fetched
     */
    try {
        return await fetchResource("card-types");
    } catch (error) {
        console.error(`Error fetching types!: ${getErrorMessage(error)}`);
        return [];
    }
}

export async function fetchTags(): Promise<object|Tag[]|[]> {
    /**
     * Base function for GET methods.
     * 
     * @returns promise of array of tags or empty array if no tags are fetched
     */
    try {
        return await fetchResource("tags");
    } catch (error) {
        console.error(`Error fetching tags!: ${getErrorMessage(error)}`);
        return [];
    }
}

async function fetchResource(resourceName: string): Promise<object> {
    /**
     * Base function for GET methods.
     * 
     * @param resourceName - name of recource in uri
     * @returns promise of object of response
     */
    const response = await fetch(`${PUBLIC_BASE_API_URL}/${resourceName}`);
    if (!response.ok) {
        throw new Error(`Resource ${resourceName} not available: ${response.status}`);
    }
    return response.json();
}





