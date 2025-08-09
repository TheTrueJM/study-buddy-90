export let userId = null;

export function authenticateUser(authUserId) {
    userId = authUserId;
}

export function logoutUser() {
    userId = null;
}