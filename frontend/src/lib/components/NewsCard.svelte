<script lang="ts">
    interface NewsItem {
        category: string;
        datetime: number;
        headline: string;
        id: number;
        image: string;
        related: string;
        source: string;
        summary: string;
        url: string;
    }

    interface Props {
        news: NewsItem[];
    }

    let { news = [] }: Props = $props();

    const ITEMS_PER_PAGE = 5;
    let currentPage = $state(1);

    // Reset page when news changes
    $effect(() => {
        if (news) {
            currentPage = 1;
        }
    });

    // Ensure news is an array before processing
    let safeNews = $derived(Array.isArray(news) ? news : []);
    let totalPages = $derived(Math.ceil(safeNews.length / ITEMS_PER_PAGE));
    let currentNews = $derived(
        safeNews.slice(
            (currentPage - 1) * ITEMS_PER_PAGE,
            currentPage * ITEMS_PER_PAGE,
        ),
    );

    function formatDate(timestamp: number): string {
        const date = new Date(timestamp * 1000);
        const now = new Date();
        const diff = now.getTime() - date.getTime();
        const hours = Math.floor(diff / (1000 * 60 * 60));

        if (hours < 1) {
            return "Just now";
        } else if (hours < 24) {
            return `${hours}h ago`;
        } else {
            const days = Math.floor(hours / 24);
            return `${days}d ago`;
        }
    }

    function nextPage() {
        if (currentPage < totalPages) currentPage++;
    }

    function prevPage() {
        if (currentPage > 1) currentPage--;
    }
</script>

{#if safeNews.length === 0}
    <div class="card p-8 text-center">
        <p class="text-secondary">No recent news available</p>
    </div>
{:else}
    <div class="card p-4 flex flex-col h-full">
        <div class="flex-1 space-y-2">
            {#each currentNews as item (item.id)}
                <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="flex gap-4 p-2 -mx-2 rounded-lg hover:bg-gray-50 transition-colors duration-200 ease-in-out group"
                >
                    {#if item.image}
                        <img
                            src={item.image}
                            alt={item.headline}
                            class="w-24 h-24 object-cover rounded-lg flex-shrink-0"
                        />
                    {/if}
                    <div class="flex-1 min-w-0 flex flex-col justify-center">
                        <h4
                            class="font-semibold text-primary mb-2 line-clamp-2 text-sm leading-relaxed group-hover:text-blue-600"
                            style="transition: color var(--transition-fast);"
                        >
                            {item.headline}
                        </h4>
                        <div
                            class="flex items-center gap-2 text-xs text-secondary"
                        >
                            <span
                                class="font-medium px-2 py-0.5 rounded-full"
                                style="background: var(--color-bg-secondary); color: var(--color-text-secondary);"
                            >
                                {item.source}
                            </span>
                            <span>•</span>
                            <span>{formatDate(item.datetime)}</span>
                        </div>
                    </div>
                </a>
            {/each}
        </div>

        {#if totalPages > 1}
            <div
                class="flex items-center justify-between pt-4 mt-6 border-t border-[var(--color-border)]"
            >
                <span class="text-xs text-secondary font-medium">
                    Page {currentPage} of {totalPages}
                </span>
                <div class="flex gap-2">
                    <button
                        onclick={prevPage}
                        disabled={currentPage === 1}
                        class="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                        style="font-size: var(--font-size-xs);"
                    >
                        Previous
                    </button>
                    <button
                        onclick={nextPage}
                        disabled={currentPage === totalPages}
                        class="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                        style="font-size: var(--font-size-xs);"
                    >
                        Next
                    </button>
                </div>
            </div>
        {/if}
    </div>
{/if}
