<!-- <script>
    import FetchData from '../../lib/components/FetchHour.svelte';
</script>

<main>
    <h1>Home</h1>
    <FetchData />
</main> -->

<script>
    export let time; // La variable "time" est injectée par le rendu côté serveur
</script>

<h1>Heure actuelle</h1>
<p>L’heure est : {time}</p>
