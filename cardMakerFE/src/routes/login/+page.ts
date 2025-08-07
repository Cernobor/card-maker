import type { PageLoad } from './$types';

export const load: PageLoad = ({ url }) => {
	const created = url.searchParams.get('created');
	const userCreated = created === 'true';
	return { userCreated };
};

export const prerender = false;