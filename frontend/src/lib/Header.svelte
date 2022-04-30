<!--
@file: Header.svelte
@description: Website header
@version: Redstone-release
-->
<script>
    import "carbon-components-svelte/css/all.css";
    import {
        Header
    } from "carbon-components-svelte";
    export let version;
</script>

<Header company="-L-" href="/">
    <span slot="platform" class="platform-name">Libcヽ(✿ﾟ▽ﾟ)ノ<code>{version}</code></span>
</Header>

<style>
    .platform-name code{
    margin-left: var(--cds-spacing-02);
    font-size: var(--cds-code-01-font-size);
    font-weight: var(--cds-code-01-font-weight);
    letter-spacing: var(--cds-code-01-letter-spacing);
    line-height: var(--cds-code-01-line-height);
    color: #c6c6c6;
    }
</style>