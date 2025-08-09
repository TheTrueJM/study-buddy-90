<script>
  import { push } from "svelte-spa-router";
  import Card from "../components/Card.svelte";

  // Assume user is already authenticated

  import { onMount } from "svelte";
  import { fetchUnits, fetchAvailableUnits, enrollInUnit } from "../js/api.js";
  import { ensureUser } from "../js/User.js";
  let units = [];
  let joinableUnits = [];
  let loadingJoinables = true;
  let toast = "";
  let search = { unit: units[0], looking: true, openMsg: true, note: "" };
  const post = () => alert("Posted! (demo)");
  async function loadJoinable() {
    try {
      await ensureUser();
      joinableUnits = await fetchAvailableUnits();
    } catch (e) {
      joinableUnits = [];
    } finally {
      loadingJoinables = false;
    }
  }
  onMount(async () => {
    try {
      const data = await fetchUnits();
      units = (data || []).map((u) => u.code);
    } catch (e) {
      units = [];
    }
    await loadJoinable();
  });
  async function addUnit(code) {
    try {
      const res = await enrollInUnit(code);
      if (res) {
        toast = `Enrolled in ${code}`;
        setTimeout(() => (toast = ""), 1500);
        loadingJoinables = true;
        await loadJoinable();
      }
    } catch (e) {
      toast = `Failed to enroll in ${code}`;
      setTimeout(() => (toast = ""), 1500);
    }
  }
</script>

<main
  style="padding:12px; display:flex; flex-direction:column; gap:12px; align-items:center;"
>
  <!-- Hero -->
  <Card title="Study Mates">
    <p>
      <strong>Find teammates for your uni assessments</strong> — retro Mac vibe,
      simple and fast.
    </p>
    <div class="field-row" style="justify-content:flex-end;">
      <button>About</button>
      <button class="default">Get Started</button>
    </div>
  </Card>

  <!-- Quick Post -->
  <Card title="Find a Team">
    <div class="field-row">
      <label for="unit">Unit</label>
      <select id="unit" bind:value={search.unit}>
        {#each units as u}<option value={u}>{u}</option>{/each}
      </select>
    </div>
    <div class="field-row">
      <label
        ><input type="checkbox" bind:checked={search.looking} /> Looking for team</label
      >
      <label
        ><input type="checkbox" bind:checked={search.openMsg} /> Open to messages</label
      >
    </div>
    <div class="field-row">
      <label for="note">Note</label>
      <input
        id="note"
        type="text"
        placeholder="Prefer weekdays 2–5pm"
        bind:value={search.note}
      />
    </div>
    <div class="field-row" style="justify-content:flex-end; margin-top:8px;">
      <button on:click={() => (search.note = "")}>Cancel</button>
      <button class="default" on:click={post}>Post</button>
    </div>
  </Card>

  <!-- Joinable Units -->
  <div class="window" style="width:960px;">
    <div class="title-bar">
      <button class="close"></button>
      <h1 class="title">Available Units</h1>
      <button class="resize"></button>
    </div>
    <div class="separator"></div>
    <div class="window-pane">
      {#if toast}
        <div class="alert-box outer-border inner-border" style="margin:12px 0;">
          <div class="alert-contents">{toast}</div>
        </div>
      {/if}
      {#if loadingJoinables}
        <p style="opacity:.7; padding:1rem 0; text-align:center;">
          Loading available units…
        </p>
      {:else if joinableUnits.length > 0}
        <ul style="padding-left:1rem;">
          {#each joinableUnits as u}
            <li class="field-row" style="justify-content:space-between;">
              <div>
                <strong>{u.code}</strong> — {u.name}
                {#if u.description}
                  <br /><span style="opacity:0.7; font-size:0.9em;"
                    >{u.description}</span
                  >
                {/if}
              </div>
              <div>
                <button class="default" on:click={() => addUnit(u.code)}
                  >Add</button
                >
              </div>
            </li>
          {/each}
        </ul>
      {:else}
        <p style="opacity:.7; padding:1rem 0; text-align:center;">
          No more units to join.
        </p>
      {/if}
    </div>
  </div>

  <!-- Removed demo groups list -->
</main>

<style>
</style>
