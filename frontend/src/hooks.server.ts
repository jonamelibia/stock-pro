import type { Handle } from '@sveltejs/kit';
import { redirect } from '@sveltejs/kit';

const publicPaths = ['/landing', '/auth/login', '/oauth'];

export const handle: Handle = async ({ event, resolve }) => {
    const session = event.cookies.get('session');

    if (session) {
        try {
            event.locals.user = JSON.parse(session);
        } catch (e) {
            event.cookies.delete('session', { path: '/' });
        }
    }

    // Redirect root to appropriate page
    if (event.url.pathname === '/') {
        if (event.locals.user) {
            throw redirect(302, '/dashboard');
        } else {
            throw redirect(302, '/landing');
        }
    }

    // Protect all routes except public paths
    if (!event.locals.user && !publicPaths.includes(event.url.pathname)) {
        throw redirect(302, '/landing');
    }

    return resolve(event);
};
