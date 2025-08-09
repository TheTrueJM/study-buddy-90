<script>
  import { push } from "svelte-spa-router";
  import { setUserId } from "../js/User.js";
  import { authenticateUser } from "../js/api.js";

  let username = "";
  let password = "";
  let fail = false;

  const submit = () => {
    if (authenticateUser()) {
      setUserId(username);
    } else {
      fail = true;
    }
  };
</script>

<main style="padding:12px; display:flex; justify-content:center;">
  <div class="window" style="width:520px;">
    <div class="title-bar">
      <button class="close"></button>
      <h1 class="title">Login</h1>
      <button class="resize"></button>
    </div>
    <div class="separator"></div>
    <div class="window-pane">
      <div class="field-row">
        <input type="text" placeholder="Username" bind:value={username} />
      </div>
      <div class="field-row">
        <input type="password" placeholder="Password" bind:value={password} />
      </div>
      <div class="field-row" style="justify-content:flex-end;">
        <button>Cancel</button>
        <button class="default" on:click={submit}>Login</button>
      </div>
      <p class="subtext">
        Don't have an account? <a class="link" href="#">Sign Up</a>
      </p>
    </div>
  </div>
</main>

<style>
</style>
