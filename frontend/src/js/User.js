import { writable } from 'svelte/store';

export const currentUser = writable(null);
export const isAuthenticated = writable(false);

export function setCurrentUser(userData) {
  currentUser.set(userData);
  isAuthenticated.set(true);
  localStorage.setItem('currentUser', JSON.stringify(userData));
}

export function getCurrentUser() {
  const stored = localStorage.getItem('currentUser');
  if (stored) {
    const userData = JSON.parse(stored);
    currentUser.set(userData);
    isAuthenticated.set(true);
    return userData;
  }
  return null;
}

export function logoutUser() {
  currentUser.set(null);
  isAuthenticated.set(false);
  localStorage.removeItem('currentUser');
}

export function getUserId() {
  const stored = localStorage.getItem('currentUser');
  if (stored) {
    const userData = JSON.parse(stored);
    return userData.id;
  }
  return null;
}

export const userId = null;
