import {json} from '@sveltejs/kit';

const backendIp = import.meta.env.VITE_BACKEND_URL;


export const POST = async ({request}) => {
    console.log("LOGIN POST received on FRONTEND server");
    const {username, password} = await request.json();

    // backend API call simulation
    const backendApiResult = await validateLogin(username, password);

    if(backendApiResult.error === "backendError") {
        return json({ result: false, error: "There was an error with our service. Please try again." }, { status: 501 });
    }

    if(backendApiResult.isValid) {
        // return json({ result: true , token: backendApiResult.token }, { status: 200 });
        return new Response(
            JSON.stringify({ result: true , token: backendApiResult.token }), 
            {
                status: 200,
                headers: {
                    'Set-Cookie': `authToken=${backendApiResult.token}; Path=/; HttpOnly; SameSite=Strict` // Secure flag can't bu used, as we are not over HTTPS
                },
            }
        );
    } else {
        return json({ result: false, error: "Invalid credentials!" }, { status: 401 });
    }
};

/**
 * @param {string} username
 * @param {string} password
 */
async function validateLogin(username, password) {
    // replace with API call

    try {
        const response = await fetch(backendIp + '/api/login', {
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
            return { isValid: true, token: data.token}; // Store the token in localStorage
        } else {
            return { isValid: false};
        }
    } catch (error) {
        return { isValid: false, error: "backendError"};
    }
}