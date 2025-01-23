<script lang="ts">
	import { onMount } from 'svelte';
	import { backendIp } from '../../store';

	// Variable to store user input values
	let username: string = '';
	let password: string = '';

	// Function to handle login
	const handleLogin = async (event: Event) => {
		event.preventDefault(); // Prevent default form submission

		try {
			const response = await fetch(backendIp + '/api/register', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ username, password })
			});

			const data = await response.json();
			console.log(data);

			if (data.result) {
				// If login is successful, store authentication token in a cookie
				const data = await response.json();
				let reg = data.get('registered');
				if (reg) {
					alert('User registered');
				} else {
					alert('User not registered');
				}
			} else {
				alert('Invalid credentials');
			}
		} catch (error) {
			console.error('Error:', error);
		}
	};

	// Fetch bootstrap once the component has mounted
	onMount(async () => {
		await import('bootstrap/dist/css/bootstrap.min.css');
	});
</script>

<main class="container mt-5">
	<!-- Login Form -->
	<h1 class="text-center mb-4">Register Page</h1>

	<form onsubmit={handleLogin}>
		<div class="mb-3">
			<label for="username" class="form-label">Username:</label>
			<input type="text" id="username" class="form-control" bind:value={username} required />
		</div>

		<div class="mb-3">
			<label for="password" class="form-label">Password:</label>
			<input
				type="password"
				id="current-password"
				class="form-control"
				bind:value={password}
				required
			/>
		</div>

		<button type="submit" class="btn btn-primary w-100">Register</button>
	</form>
	<div class="d-flex justify-content-center">
		<button class="btn w-50" onclick={() => (window.location.href = '/')}
			>Retour à la page d'accueil</button
		>
	</div>
</main>

<style>
	/* Optional custom styles */
	main {
		max-width: 600px;
		margin: 0 auto;
	}
</style>
