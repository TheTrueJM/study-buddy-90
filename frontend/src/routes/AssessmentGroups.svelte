<script>
  import { onMount } from "svelte";
  import { push } from "svelte-spa-router";
  import { params } from "svelte-spa-router";
  import { createGroupRequest } from '../js/api.js';

  // Route params
  let code = "";
  let num = "";
  $: code =
    ($params && $params.code) ||
    (typeof location !== "undefined" ? location.hash.split("/")[2] || "" : "");
  $: num =
    ($params && $params.num) ||
    (typeof location !== "undefined" ? location.hash.split("/")[3] || "" : "");

  let groups = [];
  let loading = true;
  let error = null;

  // Track join requests locally
  let requested = new Set();

  async function requestJoin(group) {
    if (requested.has(group.id)) return;
    
    try {
      const result = await createGroupRequest(group.id);
      if (result) {
        requested = new Set(requested);
        requested.add(group.id);
      }
    } catch (err) {
      console.error('Failed to request join:', err);
    }
  }

  function viewDetails(group) {
    // Create a consistent ID format for the group detail page
    const groupId = `${group.unit_code}-${group.num}-${group.id}`;
    push(`/group/${groupId}`);
  }

  onMount(async () => {
    if (!code || !num) {
      error = "Invalid assessment parameters";
      loading = false;
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/units/${code}/assessments/${num}/groups`);
      if (!response.ok) throw new Error('Failed to fetch groups');
      groups = await response.json();
    } catch (err) {
      error = "Failed to load groups for this assessment";
      console.error('Error fetching assessment groups:', err);
    } finally {
      loading = false;
    }
  });
</script>

<main style="padding:12px; display:flex; justify-content:center;">
  <div class="window" style="width:960px;">
    <div class="title-bar">
      <button class="close"></button>
      <h1 class="title">{code || "Unit"} — Assessment {num}</h1>
      <button class="resize"></button>
    </div>
    <div class="separator"></div>
    <div class="window-pane">
      <div class="details-bar" style="align-items:center;">
        <div class="heading">Available Groups</div>
      </div>

      {#if error}
        <div class="alert-box outer-border inner-border" style="margin:12px 0; background-color: #ff6b6b;">
          <div class="alert-contents">{error}</div>
        </div>
      {/if}

      {#if loading}
        <p style="text-align:center; opacity:0.7; padding:2rem;">Loading groups...</p>
      {:else if groups.length > 0}
        <ul style="padding-left:1rem;">
          {#each groups as g}
            <li class="field-row" style="justify-content:space-between;">
              <div>
                <strong>Group {g.id}</strong> — {g.unit_code} — Assessment {g.num}
                <span style="opacity:.7;">(Members: {g.current_members || 0}/{g.max_members || 4})</span>
              </div>
              <div class="field-row" style="gap:6px;">
                <button on:click={() => viewDetails(g)}>View Details</button>
                <button
                  class="default"
                  on:click={() => requestJoin(g)}
                  disabled={requested.has(g.id)}
                >
                  {requested.has(g.id) ? "Requested" : "Request to Join"}
                </button>
              </div>
            </li>
          {/each}
        </ul>
      {:else}
        <p style="text-align:center; opacity:0.7; padding:2rem;">
          No groups available yet for this assessment.
        </p>
      {/if}
    </div>
  </div>
</main>

<style>
</style>
