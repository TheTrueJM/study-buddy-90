<script>
  import { push } from "svelte-spa-router";
  import { onMount } from 'svelte';
  import { getUserId } from '../js/User.js';

  let myUnits = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    const uid = getUserId();
    if (!uid) {
      loading = false;
      error = 'You are not logged in.';
      return;
    }
    try {
      const response = await fetch(`http://localhost:8000/students/${uid}/enrolments`);
      if (!response.ok) throw new Error('Failed to fetch enrolled units');
      const enrolments = await response.json();
      
      // The enrollment endpoint already includes unit details
      myUnits = enrolments.map(enrolment => ({
        code: enrolment.unit_code,
        name: enrolment.unit_name,
        description: enrolment.description,
        completed: enrolment.completed,
        grade: enrolment.grade,
        availability: enrolment.availability
      }));
    } catch (err) {
      error = "Failed to load your enrolled units";
      console.error('Error fetching enrolled units:', err);
    } finally {
      loading = false;
    }
  });

  function goToDetails(code) {
    push(`/unit/${code}`);
  }
</script>

<main style="padding:12px; display:flex; flex-direction:column; gap:12px; align-items:center;">
  <div class="window" style="width:960px;">
    <div class="title-bar">
      <button class="close"></button>
      <h1 class="title">My Units</h1>
      <button class="resize"></button>
    </div>
    <div class="separator"></div>
    <div class="window-pane">
      {#if error}
        <div class="alert-box outer-border inner-border" style="margin:12px 0; background-color: #ff6b6b;">
          <div class="alert-contents">{error}</div>
        </div>
      {/if}

      {#if loading}
        <p style="text-align:center; opacity:0.7; padding:2rem;">Loading your enrolled units...</p>
      {:else if myUnits.length > 0}
        <ul style="padding-left:1rem;">
          {#each myUnits as u}
            <li class="field-row" style="justify-content:space-between;">
              <div>
                <strong>{u.code}</strong> — {u.name}
                {#if u.description}
                  <br><span style="opacity:0.7; font-size:0.9em;">{u.description}</span>
                {/if}
                {#if u.completed}
                  <br><span style="color: green; font-size:0.9em;">Completed {u.grade !== null ? `(Grade: ${u.grade})` : ''}</span>
                {:else}
                  <br><span style="color: blue; font-size:0.9em;">In Progress</span>
                {/if}
              </div>
              <div>
                <button class="default" on:click={() => goToDetails(u.code)}>View More Details</button>
              </div>
            </li>
          {/each}
        </ul>
      {:else}
        <p style="opacity:.7; padding:1rem 0; text-align:center;">You are not enrolled in any units yet.</p>
      {/if}
    </div>
  </div>
</main>

<style>
</style>
