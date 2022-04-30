<!--
@file: $lib/ImageTile.svelte
@description: ClickableTile with ImageLoader combined
@version: Redstone-release
-->
<script>
    import { 
        ClickableTile,
        ImageLoader 
    } from "carbon-components-svelte";

    export let href;
    export let src;
    export let title;
    export let content;
</script>

<ClickableTile href={href} target="_blank">
    <ImageLoader src={src}></ImageLoader>
    <h5 style="padding-top: 0.8rem; display: flex;">{title}</h5>
    <span style="padding-top: 0.8rem; display: flex;">{content}</span>
</ClickableTile>