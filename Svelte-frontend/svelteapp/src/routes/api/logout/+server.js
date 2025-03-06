import {json} from '@sveltejs/kit';

const backendIp = import.meta.env.VITE_BACKEND_URL;

export const POST = async ({ request, cookies }) => {
    console.log("LOGOUT POST received on FRONTEND server");

    // cookies.set('authToken', '', {
    //     path: '/',
    //     expires: new Date(0),
    //     sameSite: 'strict',
    // });


    console.log("Cookie delete");


    return new Response(
        JSON.stringify({ success: true }), 
        {
            status: 200,
            headers: {
                'Set-Cookie': `authToken=''; Path=/; HttpOnly; Expires=Thu, 01 Jan 1970 00:00:01 GMT; SameSite=Strict` // Secure flag can't be used, as we are not over HTTPS
            },
        }
    );

    console.log(cookies.get('authToken'));

    return json({success: true});
};
