<script>
    import {
        ButtonSet, 
        Button,
        TextInput
    } from "carbon-components-svelte"
    import TrashCan from "carbon-icons-svelte/lib/TrashCan16";
    export let address;
    export let identifier;
    export let disabled = false;
    export let id;

    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
    </script>

<div style="padding: 0.4rem 0">
    <ButtonSet>
        <TextInput 
        hideLabel 
        placeholder="Function" 
        bind:value={identifier} 
        on:change={() => {
            dispatch("change", {});
        }} 
        />
        <div style="width: 26%">
            <TextInput 
            hideLabel 
            placeholder="Address" 
            bind:value={address} 
            on:change={() => {
                dispatch("change", {});
            }} 
            />
        </div>
        <Button 
        size="field" 
        kind="secondary" 
        iconDescription="Delete" 
        style="width: 2.5rem" 
        icon={TrashCan}
        bind:disabled
        tooltipPosition="right"
        on:click={() => {
            dispatch("delete", {id: id});
        }}
        ></Button>
    </ButtonSet>
</div>
