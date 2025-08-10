import { writable } from 'svelte/store';
import { fetchStudents } from './api.js';

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

// Ensure a user is set: auto-login as first student
export async function ensureUser() {
  const existing = getCurrentUser();
  if (existing) return existing;
  try {
    const students = await fetchStudents();
    if (students && students.length > 0) {
      const first = students[0];
      setCurrentUser({
        id: first.id,
        name: first.name,
        fax_n: first.fax_n || '',
        pager_n: first.pager_n || '',
        avatar_url: first.avatar_url || ''
      });
      // Initialize joinedGroupIds with first available group if missing or empty
      try {
        const raw = localStorage.getItem('joinedGroupIds');
        const cur = raw ? JSON.parse(raw) : [];
        if (!Array.isArray(cur) || cur.length === 0) {
          const resp = await fetch('http://localhost:8000/groups');
          if (resp.ok) {
            const groups = await resp.json();
            if (Array.isArray(groups) && groups.length > 0) {
              localStorage.setItem('joinedGroupIds', JSON.stringify([String(groups[0].id)]));
            }
          }
        }
      } catch {}
      return first;
    }
  } catch (e) {
    // ignore
  }
  return null;
}
