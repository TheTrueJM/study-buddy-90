<script>
  import { onMount } from 'svelte';
  import { fetchAvailableUnits, enrollInUnit } from '../js/api.js';

  let availableUnits = [];
  let enrolledCodes = [];
  let loading = true;
  let successVisible = false;
  let lastEnrolled = "";
  let error = null;

  onMount(async () => {
    try {
      availableUnits = await fetchAvailableUnits();
    } catch (err) {
      error = "Failed to load units";
    } finally {
      loading = false;
    }
  });

  async function enrol(unit) {
    try {
      const result = await enrollInUnit(unit.code);
      if (result) {
        if (!enrolledCodes.includes(unit.code)) {
          enrolledCodes = [...enrolledCodes, unit.code];
        }
        lastEnrolled = unit.code;
        successVisible = true;
        setTimeout(() => (successVisible = false), 1600);
      }
    } catch (err) {
      console.error('Enrollment failed:', err);
    }
  }

  let query = "";
  $: filtered = availableUnits.filter(
    (u) =>
      u.code.toLowerCase().includes(query.toLowerCase()) ||
      u.name.toLowerCase().includes(query.toLowerCase())
  );
</script>

<main style="padding:12px; display:flex; flex-direction:column; gap:12px; align-items:center;">
  <div class="window" style="width:960px;">
    <div class="title-bar">
      <button class="close"></button>
      <h1 class="title">Units</h1>
      <button class="resize"></button>
    </div>
    <div class="separator"></div>
    <div class="window-pane">
      <div class="field-row" style="justify-content:space-between;">
        <div class="field-row">
          <label for="search">Search</label>
          <input id="search" type="text" placeholder="e.g. CAB302" bind:value={query} />
        </div>
      </div>

      <h3 class="heading" style="margin:12px 0 6px;">Available Units</h3>
      
      {#if error}
        <div class="alert-box outer-border inner-border" style="margin:12px 0; background-color: #ff6b6b;">
          <div class="alert-contents">{error}</div>
        </div>
      {/if}

      {#if successVisible}
        <div class="alert-box outer-border inner-border" style="margin:12px 0;">
          <div class="alert-contents">Enrolled in {lastEnrolled}</div>
        </div>
      {/if}

      {#if loading}
        <p style="text-align:center; opacity:0.7; padding:2rem;">Loading units...</p>
      {:else if filtered.length > 0}
        <ul style="padding-left:1rem;">
          {#each filtered as u}
            <li class="field-row" style="justify-content:space-between;">
              <div>
                <strong>{u.code}</strong> — {u.name}
                {#if u.description}
                  <br><span style="opacity:0.7; font-size:0.9em;">{u.description}</span>
                {/if}
              </div>
              <div>
                <button class="default" disabled={enrolledCodes.includes(u.code)} on:click={() => enrol(u)}>
                  {enrolledCodes.includes(u.code) ? 'Enrolled' : 'Enrol in Unit'}
                </button>
              </div>
            </li>
          {/each}
        </ul>
      {:else}
        <p style="text-align:center; opacity:0.7; padding:2rem;">
          {query ? 'No matching units found.' : 'No units available for enrollment.'}
        </p>
      {/if}
    </div>
  </div>
</main>

<style>
</style>
