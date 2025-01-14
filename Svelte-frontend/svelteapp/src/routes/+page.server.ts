import type { Cookies } from '@sveltejs/kit';

export async function load({ cookies }) {
	const authenticated = isAuthenticated(cookies);
	const time = await fetchTime();
	return {
		time: time,
		isAuthenticated: authenticated
	};
}

async function fetchTime(): Promise<{ hour: number; min: number }> {
	try {
		const response = await fetch('http://127.0.0.1:5000/api/hour');
		if (!response.ok) {
			throw new Error('Failed to fetch time');
		}
		const data = await response.json();
		return {
			hour: data.hour,
			min: data.min
		};
	} catch (error) {
		console.error('Error fetching time:', error);
		return {
			hour: -1,
			min: -1
		};
	}
}

function isAuthenticated(cookies: Cookies): boolean {
	const authToken = cookies.get('auth_token');
	return !!authToken; // If authToken exists, the user is authenticated (not secure obviously)
}
