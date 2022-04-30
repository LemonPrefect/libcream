<!--
@file: Footer.svelte
@description: Website footer
@version: Redstone-release
-->
<script>
    import { 
        Grid
        , Row
        , Column
        , Link 
    } from "carbon-components-svelte";
    import Carbon16 from "carbon-icons-svelte/lib/Carbon16";
</script>

<footer class="bx--content">
    <Grid>
        <Row>
            <Column>LemonPrefect@Abyss, Code With <del>Desperation</del></Column>
        </Row>
        <Row>
            <Column>Proudly build with <Link href="https://svelte.dev/">Svelte</Link></Column>
        </Row>
        <Row>
            <Column>Framework <Link href="https://carbon-components-svelte.onrender.com/" icon={Carbon16}>IBM Carbon Design Svelte</Link></Column>
        </Row>
        <Row>
            <Column>Copyright 2022, Licensed as LGPLv3</Column>
        </Row>
        <Row>
            <Column>
                <a target="_blank" rel="noopener" href="http://beian.miit.gov.cn/">湘ICP备20002800号</a>
                <img src="/beian.png" alt=""/>
                <a href= "http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=43021102000188">湘公网安备43021102000188号</a>
            </Column>
        </Row>
    </Grid>
</footer> 

<style>
    footer {
        background: var(--cds-ui-01);
    }
</style>