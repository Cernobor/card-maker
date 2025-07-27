import type { PageLoad } from './$types';

export const load: PageLoad = ({ url }) => {
	const createdParam = url.searchParams.get('created');
	const cardCreated = createdParam === 'true';
	return { cardCreated };
};