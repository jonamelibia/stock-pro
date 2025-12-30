import { redirect } from '@sveltejs/kit';
import { GoogleAuthService } from '$lib/server/auth';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async () => {
	const authUrl = GoogleAuthService.getAuthUrl();
	throw redirect(302, authUrl);
};
