/** @type {import('./$types').PageLoad} */
export function load({ params }: { params: { id: string } }): { cardId: number } {
	/**
	 * Parse URL and get card ID from path parameters.
	 *
	 * @param param - path/query parameters (in this case only card id)
	 *
	 * @returns object containing card ID
	 */
	return {
		cardId: Number(params.id)
	};
}

export const prerender = false;
