<script lang="ts">
    import { page } from "$app/stores";
    import ErrorState from "$lib/components/ErrorState.svelte";
</script>

<div
    class="min-h-screen flex items-center justify-center bg-white"
    style="background: var(--color-bg-secondary);"
>
    <ErrorState
        title={$page.status === 404 ? "Page Not Found" : "Something went wrong"}
        message={$page.error?.message ||
            "We could not find the page you are looking for."}
        home={true}
    />
</div>
