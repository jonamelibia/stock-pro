<script lang="ts">
    import {
        TrendingUp,
        Sparkles,
        BarChart3,
        Shield,
        Zap,
        ArrowRight,
    } from "lucide-svelte";
</script>

<div
    class="min-h-screen flex flex-col justify-center px-4 w-full"
    style="background: var(--color-bg-primary);"
>
    <div class="w-full max-w-[1600px] mx-auto text-center space-y-12">
        <!-- Logo -->
        <div class="flex items-center justify-center gap-3 mb-8">
            <div
                class="w-16 h-16 rounded-2xl flex items-center justify-center"
                style="background: var(--color-bg-elevated); border: 1px solid var(--color-border);"
            >
                <TrendingUp style="color: var(--color-accent);" size={32} />
            </div>
            <span
                class="text-3xl font-bold"
                style="color: var(--color-text-primary);">StockPro</span
            >
        </div>

        <!-- Main Content -->
        <div class="space-y-6">
            <h1
                class="text-5xl md:text-6xl font-bold leading-tight"
                style="color: var(--color-text-primary);"
            >
                Professional <span style="color: var(--color-accent);"
                    >Charting</span
                >
                & <br /> Technical Analysis
            </h1>
            <p
                class="text-xl max-w-2xl mx-auto"
                style="color: var(--color-text-secondary);"
            >
                Advanced charting tools, real-time data, and AI-powered insights
                for the modern trader.
            </p>
        </div>

        <!-- CTA -->
        <div
            class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4"
        >
            <a
                href="/auth/login"
                class="btn btn-primary"
                style="font-size: 1.1rem; padding: 14px 32px; border-radius: 99px;"
            >
                Get Started
                <ArrowRight size={20} />
            </a>
        </div>

        <!-- Features Grid -->
        <div class="grid md:grid-cols-3 gap-6 pt-12 text-left">
            <div class="card p-6">
                <BarChart3
                    class="mb-4"
                    size={24}
                    style="color: var(--color-accent);"
                />
                <h3
                    class="font-bold text-lg mb-2"
                    style="color: var(--color-text-primary);"
                >
                    Advanced Charts
                </h3>
                <p class="text-sm" style="color: var(--color-text-secondary);">
                    HTML5 charts with 100+ indicators and drawing tools.
                </p>
            </div>
            <div class="card p-6">
                <Sparkles
                    class="mb-4"
                    size={24}
                    style="color: var(--color-success);"
                />
                <h3
                    class="font-bold text-lg mb-2"
                    style="color: var(--color-text-primary);"
                >
                    AI Predictions
                </h3>
                <p class="text-sm" style="color: var(--color-text-secondary);">
                    Machine learning driven price forecasts.
                </p>
            </div>
            <div class="card p-6">
                <Zap
                    class="mb-4"
                    size={24}
                    style="color: var(--color-warning);"
                />
                <h3
                    class="font-bold text-lg mb-2"
                    style="color: var(--color-text-primary);"
                >
                    Real-time Data
                </h3>
                <p class="text-sm" style="color: var(--color-text-secondary);">
                    Low latency market data from global exchanges.
                </p>
            </div>
        </div>
    </div>
</div>
