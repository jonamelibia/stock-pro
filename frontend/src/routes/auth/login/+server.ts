import { redirect } from '@sveltejs/kit';
import { GoogleAuthService } from '$lib/server/auth';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
	const redirectUri = `${url.origin}/oauth`;
	const authUrl = GoogleAuthService.getAuthUrl(redirectUri);
	throw redirect(302, authUrl);
};
