<script>
  import { goto } from "../router.js";
  let email = "",
    password = "";
  const submit = () => {
    alert("Login demo");
    goto("/");
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
        <button on:click={() => goto("/")}>Cancel</button>
        <button class="default" on:click={submit}>Login</button>
      </div>
    </div>
  </div>
</main>
