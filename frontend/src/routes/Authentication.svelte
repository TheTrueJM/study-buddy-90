<script>
  import { push } from "svelte-spa-router";
  import { setCurrentUser } from "../js/User.js";
  import { authenticateUser } from "../js/api.js";

  let username = "";
  let password = "";
  let fail = false;
  let loading = false;

  const submit = async () => {
    if (!username.trim() || !password.trim()) {
      fail = true;
      return;
    }

    loading = true;
    fail = false;
    
    try {
      const result = await authenticateUser(username, password);
      if (result.success) {
        setCurrentUser(result.student);
        push("/units");
      } else {
        fail = true;
      }
    } catch {
      fail = true;
    } finally {
      loading = false;
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
        <button class="default" on:click={submit} disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </div>
      {#if fail}
        <p class="error-text" style="color: red; text-align: center; margin-top: 8px;">
          Invalid username or password. Please try again.
        </p>
      {/if}
      <p class="subtext">
        Don't have an account? <a class="link" href="#">Sign Up</a>
      </p>
    </div>
  </div>
</main>

<style>
</style>
