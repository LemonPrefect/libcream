<!--
@file: __layout.svelte
@description: Svelte page layout
@version: Redstone-release
-->
<script>
import Footer from "$lib/Footer.svelte";
import Header from "$lib/Header.svelte";
import { Content } from "carbon-components-svelte";
export let role
</script>

<Header version="aqua" role={role}/>

<Content>
	<slot />
</Content>

<footer>
    <Footer />
</footer>

<!-- @author: Jingzhuo GUO -->
<!-- MAGIC Use flex to fix the issue when footer not in the bottom when content is not full enough -->
<svelte:head>
    <style>
        #svelte{
            display: flex;
            flex-flow: column;
            min-height: 100vh;
        }
        main{
            flex: 1 1 auto;
        }
        footer{
            flex: 0 0 auto;
        }
    </style>
</svelte:head>
