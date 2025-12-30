<script lang="ts">
    import { Github, Twitter, Linkedin } from "lucide-svelte";

    const currentYear = new Date().getFullYear();
</script>

<footer class="mt-12" style="background: #131722; color: #d1d4dc;">
    <div
        class="w-full px-4 md:px-6 py-6 flex flex-col md:flex-row justify-between items-center gap-4 border-t border-[#2a2e39]"
    >
        <p class="text-xs text-[#787b86]">
            © {currentYear} StockPro Inc. All rights reserved.
        </p>

        <div class="flex items-center gap-4">
            <a
                href="#"
                class="text-[#787b86] hover:text-[#d1d4dc] transition-colors"
            >
                <Twitter size={20} />
            </a>
            <a
                href="https://github.com"
                target="_blank"
                rel="noreferrer"
                class="text-[#787b86] hover:text-[#d1d4dc] transition-colors"
            >
                <Github size={20} />
            </a>
            <a
                href="#"
                class="text-[#787b86] hover:text-[#d1d4dc] transition-colors"
            >
                <Linkedin size={20} />
            </a>
        </div>
    </div>
</footer>
