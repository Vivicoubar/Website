const backendIp = import.meta.env.VITE_BACKEND_URL;

export async function load({cookies}) {
	let loadPayload: {[key:string]: any} = {};

	const authToken = cookies.get('authToken');
	const authenticated = await isAuthenticated(authToken);
	loadPayload.authenticated = authenticated;

	if (authenticated) {
		loadPayload.time = await fetchTime(authToken);
	} 
	console.log("loadPayload: ", loadPayload);
	return loadPayload;
}

async function fetchTime(authToken: string | undefined): Promise<{ hour: number; min: number }> {
	try {
		const response = await fetch(backendIp + '/api/hour', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ authToken: authToken })
        });
		if (!response.ok) {
			throw new Error('Failed to fetch time during BACKEND API call');
		}
		const data = await response.json();
		return {
			hour: data.hour,
			min: data.min
		};
	} catch (error) {
		console.error(error);
		return {
			hour: -1,
			min: -1
		};
	}
}

async function isAuthenticated(authToken: string | undefined): Promise<boolean> {
	try {
		const response = await fetch(backendIp + '/api/verifyjwt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ authToken: authToken })
        });
		if (response.ok) {
			const data = await response.json();
			const isAuth: boolean = data.authenticated;
			return isAuth;
		}
		return false;
	} catch (error) {
		console.error('Error while authenticating:', error);
		return false;
	}
}
