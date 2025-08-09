<script>
  import { onMount } from "svelte";
  import { push } from "svelte-spa-router";
  import { params } from "svelte-spa-router";
  import { fetchUnitAssessments } from '../js/api.js';
  import { userId } from '../js/User.js';

  // Read unit code from route (with fallback)
  let code = "";
  $: code = ($params && $params.code) || (typeof location !== 'undefined' ? (location.hash.split("/")[2] || "") : "");

  let loading = true;
  let error = "";
  let unit = null;
  let assessments = [];

  // Enrolment preferences - connected to user's enrolment record
  let prefs = {
    preferred_days: "",
    preferred_times: "",
    team_size: 4,
    notes: "",
  };

  async function savePrefs() {
    try {
      const response = await fetch(`http://localhost:8000/enrolments/${code}/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          grade: 0.0, // Keep existing grade
          completed: false, // Keep existing completion status
          availability: `Days: ${prefs.preferred_days}, Times: ${prefs.preferred_times}, Team Size: ${prefs.team_size}, Notes: ${prefs.notes}`
        })
      });
      if (response.ok) {
        successVisible = true;
        setTimeout(() => (successVisible = false), 1600);
      }
    } catch (err) {
      console.error('Failed to save preferences:', err);
    }
  }

  let successVisible = false;

  onMount(async () => {
    loading = true;
    error = "";
    
    if (!code) {
      error = "Unit not found.";
      loading = false;
      return;
    }

    try {
      // Fetch unit details
      const unitResponse = await fetch(`http://localhost:8000/units/${code}`);
      if (!unitResponse.ok) {
        if (unitResponse.status === 404) {
          error = "Unit not found.";
        } else {
          throw new Error('Failed to fetch unit');
        }
        loading = false;
        return;
      }
      unit = await unitResponse.json();

      // Fetch unit assessments
      assessments = await fetchUnitAssessments(code);

      // Fetch current user's enrollment to get preferences
      try {
        const enrolmentResponse = await fetch(`http://localhost:8000/students/${userId}/enrolments`);
        if (enrolmentResponse.ok) {
          const enrolments = await enrolmentResponse.json();
          const currentEnrolment = enrolments.find(e => e.unit_code === code);
          if (currentEnrolment && currentEnrolment.availability) {
            // Parse availability string to populate preferences
            const availability = currentEnrolment.availability;
            // Simple parsing - in a real app you might want more robust parsing
            if (availability.includes('Days:')) {
              const daysMatch = availability.match(/Days:\s*([^,]*)/);
              if (daysMatch) prefs.preferred_days = daysMatch[1].trim();
            }
            if (availability.includes('Times:')) {
              const timesMatch = availability.match(/Times:\s*([^,]*)/);
              if (timesMatch) prefs.preferred_times = timesMatch[1].trim();
            }
          }
        }
      } catch (prefErr) {
        console.log('Could not load preferences:', prefErr);
      }

    } catch (err) {
      error = "Failed to load unit details.";
      console.error('Error loading unit:', err);
    } finally {
      loading = false;
    }
  });
</script>

<main style="padding:12px; display:flex; justify-content:center;">
  <div class="window" style="width:960px;">
    <div class="title-bar">
      <button class="close"></button>
      <h1 class="title">{code || 'Unit'}</h1>
      <button class="resize"></button>
    </div>
    <div class="separator"></div>
    <div class="window-pane">
      {#if loading}
        <div class="standard-dialog" style="margin:8px 0;">
          <div class="field-row">Loading unit details… (mock)</div>
        </div>
      {:else if error}
        <div class="alert-box outer-border inner-border" style="margin:12px 0;">
          <div class="alert-contents">{error}</div>
        </div>
      {:else}
        <div class="details-bar" style="align-items:center;">
          <div class="field-row" style="gap:12px;">
            <div>Code: <strong>{unit.code}</strong></div>
            <div>Name: <strong>{unit.name}</strong></div>
          </div>
        </div>

        {#if unit.description}
          <h3 class="heading" style="margin:16px 0 6px;">About</h3>
          <p style="margin:0 0 8px;">{unit.description}</p>
        {/if}
      {/if}

      <h3 class="heading" style="margin:16px 0 6px;">Enrolment Preferences</h3>
      <div class="standard-dialog" style="max-width:720px;">
        <div class="field-row">
          <label for="days">Preferred Days</label>
          <input id="days" type="text" bind:value={prefs.preferred_days} />
        </div>
        <div class="field-row">
          <label for="times">Preferred Times</label>
          <input id="times" type="text" bind:value={prefs.preferred_times} />
        </div>
        <div class="field-row">
          <label for="size">Team Size</label>
          <input id="size" type="number" min="1" max="8" bind:value={prefs.team_size} />
        </div>
        <div class="field-row">
          <label for="notes">Notes</label>
          <input id="notes" type="text" bind:value={prefs.notes} />
        </div>
        <div class="field-row" style="justify-content:flex-end; margin-top:8px;">
          <button on:click={() => (prefs = { preferred_days: "", preferred_times: "", team_size: 4, notes: "" })}>Clear</button>
          <button class="default" on:click={savePrefs}>Save Preferences</button>
        </div>
      </div>

      {#if successVisible}
        <div class="alert-box outer-border inner-border" style="margin:12px 0;">
          <div class="alert-contents">Preferences saved successfully</div>
        </div>
      {/if}

      <h3 class="heading" style="margin:16px 0 6px;">Assessments</h3>
      {#if assessments.length > 0}
        <ul style="padding-left:1rem;">
          {#each assessments as a}
            <li class="field-row" style="justify-content:space-between;">
              <div>
                <strong>Assessment {a.num}</strong>
                <span style="opacity:.75;">
                  (Size: {a.size}, Grade: {a.grade}%, Due: Week {a.due_week})
                </span>
                {#if a.group_formation_week}
                  <br><span style="color: blue; font-size:0.9em;">Group formation: Week {a.group_formation_week}</span>
                {/if}
              </div>
              <div>
                <button on:click={() => push(`/assessment-groups/${unit.code}/${a.num}`)}>View Groups</button>
              </div>
            </li>
          {/each}
        </ul>
      {:else}
        <p style="opacity:.7; padding:1rem 0; text-align:center;">No assessments available for this unit.</p>
      {/if}
    </div>
  </div>
  
</main>

<style>
</style>
