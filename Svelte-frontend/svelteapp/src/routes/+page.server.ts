import { backendIp } from '../store.js';

export async function load() {
	const authenticated = await isAuthenticated();
	const time = await fetchTime();
	return {
		time: time,
		isAuthenticated: authenticated
	};
}

async function fetchTime(): Promise<{ hour: number; min: number }> {
	try {
		const response = await fetch(backendIp + '/api/hour');
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

async function isAuthenticated(): Promise<boolean> {
	try {
		const response = await fetch(backendIp + '/api/verifyjwt');
		if (response.ok) {
			const data = await response.json();
			const isAuth: boolean = data.authenticated;
			return isAuth;
		}
		return false;
	} catch (error) {
		console.error('Error fetching time:', error);
		return false;
	}
}
