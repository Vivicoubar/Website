<script>
	import { page } from '$app/state';
	import { onMount } from 'svelte';
	let { isAuthenticated } = page.data;
	let { hour, min } = page.data.time;
	// Load Bootstrap with unmount
	onMount(async () => {
		await import('bootstrap/dist/css/bootstrap.min.css');
		// @ts-ignore
		await import('bootstrap/dist/js/bootstrap.min.js');
	});
</script>

<nav class="navbar navbar-expand-lg bg-body-tertiary">
	<div class="container-fluid">
		<a class="navbar-brand" href="/">Unsecure Website</a>
		<button
			class="navbar-toggler"
			type="button"
			data-bs-toggle="collapse"
			data-bs-target="#navbarSupportedContent"
			aria-controls="navbarSupportedContent"
			aria-expanded="false"
			aria-label="Toggle navigation"
		>
			<span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="navbarSupportedContent">
			<ul class="navbar-nav me-auto mb-2 mb-lg-0">
				<li class="nav-item">
					<a class="nav-link active" aria-current="page" href="/">Home</a>
				</li>
				<li class="nav-item dropdown">
					<a
						class="nav-link dropdown-toggle"
						role="button"
						data-bs-toggle="dropdown"
						aria-expanded="false"
						href="#navbar"
					>
						Menu
					</a>
					<ul class="dropdown-menu">
						<li><a class="dropdown-item" href="/login">Login</a></li>
					</ul>
				</li>
			</ul>
		</div>
	</div>
</nav>
<main>
	<div class="d-flex flex-column align-items-center justify-content-center">
		<div class="card m-5">
			<h5 class="card-header">Heure actuelle</h5>
			<div class="card-body">
				<div class="card-text">
					{#if isAuthenticated}
						{#if hour !== -1}
							<p>L’heure est : {hour}h{min}</p>
						{:else}
							<p>Erreur en récupérant l'heure. Veuillez réessayer plus tard.</p>
						{/if}
					{:else}
						<p>Vous devez être connecté pour voir l'heure.</p>
					{/if}
				</div>
			</div>
		</div>
		<div>
			<button onclick={() => (window.location.href = '/login')}>Se connecter</button>
			<button
				onclick={() => {
					localStorage.removeItem('jwt');
					window.location.href = '/';
				}}>Se déconnecter</button
			>
		</div>
	</div>
</main>
