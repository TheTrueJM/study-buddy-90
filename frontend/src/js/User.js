// Auto-authenticate with user ID #1
export let userId = 1;

export function authenticateUser(authUserId) {
    userId = authUserId;
}

export function logoutUser() {
    userId = null;
}