/** @type {import('./$types').PageLoad} */
export function load({ params }) {
    return {
        card_id: params.id,
    }
}

export const prerender = false;