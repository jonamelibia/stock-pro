import { OAuth2Client } from 'google-auth-library';
import { env } from '$env/dynamic/private';

const client = new OAuth2Client(
    env.GOOGLE_CLIENT_ID,
    env.GOOGLE_CLIENT_SECRET,
    'http://localhost:5173/oauth'
);

export const GoogleAuthService = {
    /**
     * Generate the Google OAuth URL for user login
     */
    getAuthUrl(): string {
        const url = client.generateAuthUrl({
            access_type: 'offline',
            scope: [
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'
            ],
            prompt: 'consent'
        });
        return url;
    },

    /**
     * Exchange authorization code for tokens and get user info
     */
    async getUserFromCode(code: string) {
        try {
            // Get tokens from authorization code
            const { tokens } = await client.getToken(code);
            client.setCredentials(tokens);

            // Get user info
            const ticket = await client.verifyIdToken({
                idToken: tokens.id_token!,
                audience: env.GOOGLE_CLIENT_ID
            });

            const payload = ticket.getPayload();

            if (!payload) {
                throw new Error('No payload in token');
            }

            return {
                id: payload.sub,
                email: payload.email,
                name: payload.name,
                picture: payload.picture,
                tokens
            };
        } catch (error) {
            console.error('Error getting user from code:', error);
            throw error;
        }
    },

    /**
     * Verify a token and get user info
     */
    async verifyToken(token: string) {
        try {
            const ticket = await client.verifyIdToken({
                idToken: token,
                audience: env.GOOGLE_CLIENT_ID
            });

            const payload = ticket.getPayload();

            if (!payload) {
                return null;
            }

            return {
                id: payload.sub,
                email: payload.email,
                name: payload.name,
                picture: payload.picture
            };
        } catch (error) {
            console.error('Error verifying token:', error);
            return null;
        }
    }
};
