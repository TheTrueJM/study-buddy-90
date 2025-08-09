<script>
  // Mode: 'login' | 'register'
  const MODE = { LOGIN: "login", REGISTER: "register" };
  let mode = MODE.LOGIN;

  let loginForm = { email: "", password: "" };
  let regForm = { name: "", email: "", password: "", confirm: "" };

  const submitLogin = () => {
    if (!loginForm.email || !loginForm.password)
      return alert("Fill all fields.");
    alert(`Login: ${loginForm.email} (demo)`);
  };

  const submitRegister = () => {
    if (
      !regForm.name ||
      !regForm.email ||
      !regForm.password ||
      !regForm.confirm
    )
      return alert("Fill all fields.");
    if (regForm.password !== regForm.confirm)
      return alert("Passwords do not match.");
    alert(`Register: ${regForm.email} (demo)`);
  };
</script>

<!-- Overlay: center the card on screen -->
<div class="overlay">
  <div class="window auth" style="width: clamp(720px, 66vw, 920px);">
    <div class="title-bar">
      <button aria-label="Close" class="close"></button>
      <h1 class="title">Authentication</h1>
      <button aria-label="Resize" class="resize"></button>
    </div>
    <div class="separator"></div>

    <div
      class="window-pane"
      style="min-height:280px; display:flex; flex-direction:column;"
    >
      <!-- Center input area -->
      <div
        style="flex:1; display:flex; align-items:center; justify-content:center;"
      >
        <!-- Larger inputs/buttons: using global utility class -->
        <div class="ui-zoom-200" style="width:200px;">
          {#if mode === MODE.LOGIN}
            <div class="field-row field-100">
              <input
                type="email"
                placeholder="Email"
                bind:value={loginForm.email}
              />
            </div>
            <div class="field-row field-100">
              <input
                type="password"
                placeholder="Password"
                bind:value={loginForm.password}
              />
            </div>
            <div
              class="field-row"
              style="justify-content:center; margin-top:8px;"
            >
              <button
                class="btn-lg"
                on:click={() => (loginForm = { email: "", password: "" })}
                >Cancel</button
              >
              <button class="default btn-lg" on:click={submitLogin}
                >Log In</button
              >
            </div>
          {:else}
            <div class="field-row field-100">
              <input placeholder="Full name" bind:value={regForm.name} />
            </div>
            <div class="field-row field-100">
              <input
                type="email"
                placeholder="Email"
                bind:value={regForm.email}
              />
            </div>
            <div class="field-row field-100">
              <input
                type="password"
                placeholder="Password"
                bind:value={regForm.password}
              />
            </div>
            <div class="field-row field-100">
              <input
                type="password"
                placeholder="Confirm password"
                bind:value={regForm.confirm}
              />
            </div>
            <div
              class="field-row"
              style="justify-content:center; margin-top:8px;"
            >
              <button
                class="btn-lg"
                on:click={() =>
                  (regForm = {
                    name: "",
                    email: "",
                    password: "",
                    confirm: "",
                  })}>Cancel</button
              >
              <button class="default btn-lg" on:click={submitRegister}
                >Create account</button
              >
            </div>
          {/if}
        </div>
      </div>

      <!-- Bottom small toggles: bottom-right -->
      <div
        class="field-row"
        style="margin-top:auto; justify-content:flex-end; width:100%; padding:10px 12px 4px; gap:6px;"
      >
        <button
          class="btn-sm"
          class:default={mode === MODE.LOGIN}
          on:click={() => (mode = MODE.LOGIN)}>Go to Login</button
        >
        <button
          class="btn-sm"
          class:default={mode === MODE.REGISTER}
          on:click={() => (mode = MODE.REGISTER)}>Go to Sign Up</button
        >
      </div>
    </div>
  </div>
</div>

<style>
  /* Use existing background; only positioning here */
  .overlay {
    position: fixed;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px;
  }
  .auth .title-bar {
    height: 26px;
  }
  .auth .title-bar .title {
    font-size: 14px;
    line-height: 1;
  }
</style>
