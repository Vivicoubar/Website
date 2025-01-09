/** @type {import('./$types').PageServerLoad} */
export async function load() {
	try {
		const response = await fetch('http://192.168.0.4:5000/hour');

		if (!response.ok) {
			throw new Error('Failed to fetch time');
		}

		const data = await response.json(); // Supposons que l'API retourne un objet { time: "HH:MM:SS" }

		return {
			time: data.time
		};
	} catch (error) {
		console.error('Error fetching time:', error);
		return {
			time: 'Erreur lors de la récupération de l’heure'
		};
	}
}
