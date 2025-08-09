<script>
  import { push } from "svelte-spa-router";
  import { onMount } from "svelte";
  import { ensureUser, currentUser } from "../js/User.js";

  const go = (p) => (push ? push(p) : (location.hash = p));

  // No logout; app assumes user is authenticated

  onMount(() => {
    ensureUser();
  });
</script>

<div
  id="nav-root"
  style="position:fixed; top:8px; left:8px; z-index:1000; transform:scale(.88); transform-origin:top left;"
>
  <div class="window nav-window" style="width:320px">
    <div class="title-bar">
      <button aria-label="Close" class="close"></button>
      <h1 class="title">Study Buddy</h1>
      <button aria-label="Resize" class="resize"></button>
    </div>
    <div class="separator"></div>
    <div class="window-pane">
      <div class="user-info" style="margin-bottom: 8px; font-size: 12px;">
        Welcome, <strong>{$currentUser?.name || "User"}</strong>
      </div>
      <ul class="nav-list">
        <li>
          <button class="nav-link" on:click={() => go("/units")}>Units</button>
        </li>
        <li>
          <button class="nav-link" on:click={() => go("/my-units")}
            >My Units</button
          >
        </li>
        <li>
          <button class="nav-link" on:click={() => go("/groups")}
            >My Groups</button
          >
        </li>
      </ul>
    </div>
  </div>
</div>

<style>
  .nav-window {
    width: 260px;
  }
  .nav-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .nav-list li {
    margin: 2px 0;
  }
  .nav-link {
    width: 100%;
    text-align: left;
    background: none;
    border: none;
    color: blue;
    text-decoration: underline;
    cursor: pointer;
    font-family: inherit;
    font-size: 14px;
    padding: 2px 4px;
    display: block;
  }
  .nav-link:hover {
    color: darkblue;
  }
  .nav-link:active {
    color: red;
  }

  .logout-button {
    color: #dc2626 !important;
    font-weight: bold;
  }

  .logout-button:hover {
    color: #991b1b !important;
  }

  /* removed toggle styles */
</style>
