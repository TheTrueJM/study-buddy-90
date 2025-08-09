// Auto-authenticate with user ID #1
export let userId = 1;

export function setUserId(authUserId) {
  userId = authUserId;
}

export function logoutUser() {
  userId = null;
}
