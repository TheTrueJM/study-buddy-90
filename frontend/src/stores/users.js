import { writable } from "svelte/store";

const saved = JSON.parse(sessionStorage.getItem("user") || "null");

export const user = writable(
  saved ?? { isLoggedIn: false, email: null, tokens: null }
);

export function login(email, tokens) {
  const data = { isLoggedIn: true, email, tokens };
  user.set(data);
  sessionStorage.setItem("user", JSON.stringify(data));
}

export function logout() {
  user.set({ isLoggedIn: false, email: null, tokens: null });
  sessionStorage.removeItem("user");
}
