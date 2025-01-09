<script lang="ts">
    import type { PageData } from './$types';

    let { data }: { data: PageData } = $props();
    export const csr = false;
    // Make server side fetch to 192.168.0.4/5000
    fetch('http://192.168.0.4:5000')
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });

</script>

<main>
    <h1>Home</h1>
    <p>{data}</p>
</main>


