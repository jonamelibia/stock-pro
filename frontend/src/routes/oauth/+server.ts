import { redirect } from '@sveltejs/kit';
import { GoogleAuthService } from '$lib/server/auth';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url, cookies }) => {
    const code = url.searchParams.get('code');

    if (!code) {
        throw redirect(302, '/');
    }

    try {
        const user = await GoogleAuthService.getUserFromCode(code);

        // Store user session in cookie
        cookies.set('session', JSON.stringify({
            id: user.id,
            email: user.email,
            name: user.name,
            picture: user.picture
        }), {
            path: '/',
            httpOnly: true,
            sameSite: 'lax',
            secure: process.env.NODE_ENV === 'production',
            maxAge: 60 * 60 * 24 * 7 // 7 days
        });

        // Redirect to home
        throw redirect(302, '/');
    } catch (error) {
        console.error('OAuth callback error:', error);
        throw redirect(302, '/?error=auth_failed');
    }
};
