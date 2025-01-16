import { writable } from 'svelte/store';

export const backendIp = writable('http://0.0.0.0:5000');
