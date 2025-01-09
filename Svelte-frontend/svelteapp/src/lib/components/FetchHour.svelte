<script lang="ts">
    import { onMount } from 'svelte';

    let data: any = null;
    let error: string | null = null;

    // Fetch data when the component is mounted
    onMount(async () => {
        try {
            const response = await fetch('http://192.168.0.4:5000');
            if (!response.ok) {
                throw new Error(`Failed to fetch: ${response.statusText}`);
            }
            data = await response.json();
        } catch (err) {
            error = err.message || 'An unknown error occurred';
        }
    });
</script>

<main>
    {#if error}
        <p>Error: {error}</p>
    {:else if data}
        <p>Data: {JSON.stringify(data)}</p>
    {:else}
        <p>Loading...</p>
    {/if}
</main>
