<script>
  import { onMount } from "svelte";
  import { push } from "svelte-spa-router";
  import { fetchGroups, fetchUnits } from "../js/api.js";

  let units = [];
  let groups = [];
  let loading = true;

  // Create-group UI removed to avoid hitting unsupported backend endpoints

  onMount(async () => {
    await loadData();
  });

  async function loadData() {
    try {
      loading = true;
      [units, groups] = await Promise.all([fetchUnits(), fetchGroups()]);
      // no-op
    } catch (error) {
      console.error("Failed to load data:", error);
    } finally {
      loading = false;
    }
  }

  // createGroup capability removed (backend lacks supporting method)
</script>

<main
  style="padding:12px; display:flex; flex-direction:column; gap:12px; align-items:center;"
>
  <div class="window" style="width:960px;">
    <div class="title-bar">
      <button class="close"></button>
      <h1 class="title">Assessments</h1>
      <button class="resize"></button>
    </div>
    <div class="separator"></div>
    <div class="window-pane">
        <div class="details-bar" style="align-items:center;">
          <div class="heading">View all groups</div>
        </div>

      

      {#if loading}
        <p style="text-align:center; opacity:0.7; padding:2rem;">Loading groups...</p>
      {:else if groups.length}
        <ul style="padding-left:1rem;">
          {#each groups as g}
            <li class="field-row" style="justify-content:space-between;">
              <div>
                <strong>Group {g.id}</strong> — {g.unit_code} — Assessment {g.num}
              </div>
              <div class="field-row" style="gap:6px;">
                <button on:click={() => push(`/group/${g.id}`)}>View</button>
                <button class="default" on:click={() => push(`/group/${g.id}`)}>More</button>
              </div>
            </li>
          {/each}
        </ul>
      {:else}
        <p style="text-align:center; opacity:0.7; padding:2rem;">
          No groups yet
        </p>
      {/if}
    </div>
  </div>
</main>

<style>
</style>
