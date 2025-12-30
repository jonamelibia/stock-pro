# StockPro

StockPro is a modern, real-time stock analysis dashboard built with **SvelteKit** and **Taiwind CSS**. It provides users with live market data, interactive charts, and company news, powered by the Finnhub API.

## 🚀 Features

- **Real-time Dashboard**: View popular stocks and market trends at a glance.
- **Detailed Analysis**: Deep dive into company metrics, interactive TradingView charts, and key financial indicators.
- **Latest News**: Stay updated with relevant company news fetched in real-time.
- **Secure Authentication**: Google OAuth integration for secure user access.
- **Responsive Design**: Fully optimized for desktop and mobile devices.
- **Dark Mode Footer**: Sleek, professional UI aesthetics.

## 🛠️ Tech Stack

- **Framework**: [SvelteKit](https://kit.svelte.dev/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Data Provider**: [Finnhub API](https://finnhub.io/)
- **Charts**: TradingView Widgets
- **Icons**: Lucide Svelte
- **Auth**: Auth.js (Google Provider)

## ⚙️ Environment Variables

To run this project locally or deploy it, you need to set up the following environment variables.

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `FINNHUB_API_KEY` | Your free API key from [Finnhub](https://finnhub.io/) |
| `GOOGLE_CLIENT_ID` | OAuth Client ID from Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | OAuth Client Secret from Google Cloud Console |
| `AUTH_SECRET` | A random string for session encryption (generate with `openssl rand -base64 32`) |

## 💻 Local Development

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd stock-pro/frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the development server:**
    ```bash
    npm run dev
    ```

4.  **Open your browser:**
    Navigate to `http://localhost:5173`.

## ☁️ Deploying to Vercel

This project is configured with `@sveltejs/adapter-auto`, which automagically optimizes the build for Vercel.

1.  **Push your code to GitHub/GitLab/Bitbucket.**
2.  **Log in to [Vercel](https://vercel.com/).**
3.  **Import your project:**
    *   Click "Add New..." > "Project".
    *   Select your repository.
4.  **Configure Project:**
    *   **Framework Preset**: SvelteKit (should be auto-detected).
    *   **Root Directory**: Ensure it points to `frontend` if that's where your `package.json` is.
5.  **Environment Variables:**
    *   Copy all values from your `.env` file into the Vercel "Environment Variables" section.
6.  **Deploy:**
    *   Click "Deploy". Vercel will build and launch your application.

### ⚠️ Important for Production
Make sure your Google OAuth callback URLs in the Google Cloud Console include your Vercel production domain (e.g., `https://your-project.vercel.app/auth/callback/google`).
