<!-- <h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p> -->

<script>
	import { page } from "$app/state";
    let time = page.data.time;
</script>

<h1>Heure actuelle</h1>
<p>L’heure est : {time}</p>