<script>
  import { push } from "svelte-spa-router";
  import { authenticateUser } from "../js/User.js";

  let email = "",
    password = "";
  const submit = () => {
    alert("Login demo");
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
        <input type="email" placeholder="Email" bind:value={email} />
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
