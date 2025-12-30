<script lang="ts">
    import { AlertTriangle, RefreshCw, Home } from "lucide-svelte";

    interface Props {
        title?: string;
        message?: string;
        retry?: () => void;
        home?: boolean;
    }

    let {
        title = "Unable to load data",
        message = "An unexpected error occurred. Please try again later.",
        retry,
        home = true,
    }: Props = $props();
</script>

<div
    class="flex flex-col items-center justify-center p-8 text-center max-w-md mx-auto"
>
    <div
        class="w-16 h-16 rounded-2xl bg-red-50 flex items-center justify-center mb-6 shadow-sm border border-red-100"
    >
        <AlertTriangle class="text-danger" size={32} />
    </div>

    <h3 class="text-xl font-bold text-gray-900 mb-2">{title}</h3>
    <p class="text-gray-500 mb-8 leading-relaxed">{message}</p>

    <div class="flex items-center gap-3">
        {#if retry}
            <button
                onclick={retry}
                class="btn bg-white border border-gray-200 text-gray-900 hover:bg-gray-50 shadow-sm"
            >
                <RefreshCw size={18} />
                Try Again
            </button>
        {/if}

        {#if home}
            <a href="/" class="btn btn-primary shadow-sm">
                <Home size={18} />
                Go Home
            </a>
        {/if}
    </div>
</div>
