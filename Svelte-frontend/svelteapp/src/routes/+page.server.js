/** @type {import('./$types').PageServerLoad} */

export async function load() {
	try {
		const response = await fetch('http://127.0.0.1:5000/api/hour');

		if (!response.ok) {
			throw new Error('Failed to fetch time');
		}

		const data = await response.json();
		console.log(data);
		return {
			time: await data.hour
		};
	} catch (error) {
		console.error('Error fetching time:', error);
		return {
			time: -1
		};
	}
}
