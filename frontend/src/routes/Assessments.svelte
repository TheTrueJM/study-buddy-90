<script>
  import { onMount } from "svelte";
  import { push } from "svelte-spa-router";
  import { fetchGroups, fetchUnits } from "../js/api.js";

  let units = [];
  let groups = [];
  let loading = true;

  let showCreate = false;
  let createForm = { unit_code: "", num: 1 };
  let toast = "";

  onMount(async () => {
    await loadData();
  });

  async function loadData() {
    try {
      loading = true;
      [units, groups] = await Promise.all([fetchUnits(), fetchGroups()]);
      if (units.length > 0) {
        createForm.unit_code = units[0].code;
      }
    } catch (error) {
      console.error("Failed to load data:", error);
    } finally {
      loading = false;
    }
  }

  async function createGroup() {
    if (!createForm.unit_code || createForm.num < 1) return;
    
    try {
      const response = await fetch("http://localhost:8000/groups", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          unit_code: createForm.unit_code,
          num: createForm.num,
        }),
      });
      
      if (response.ok) {
        toast = "Group created";
        await loadData();
        showCreate = false;
        setTimeout(() => (toast = ""), 1500);
      } else {
        toast = "Failed to create group";
        setTimeout(() => (toast = ""), 1500);
      }
    } catch (error) {
      toast = "Error creating group";
      setTimeout(() => (toast = ""), 1500);
    }
  }
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
        <div class="field-row" style="gap:6px;">
          <button on:click={() => (showCreate = !showCreate)}
            >{showCreate ? "Close" : "Create Group"}</button
          >
        </div>
      </div>

      {#if toast}
        <div class="alert-box outer-border inner-border" style="margin:12px 0;">
          <div class="alert-contents">{toast}</div>
        </div>
      {/if}

      {#if showCreate}
        <div class="standard-dialog" style="margin:12px 0;">
          <div class="field-row">
            <label for="unit">Unit</label>
            <select id="unit" bind:value={createForm.unit_code}>
              {#each units as u}
                <option value={u.code}>{u.code}</option>
              {/each}
            </select>
          </div>
          <div class="field-row">
            <label for="anum">Assessment</label>
            <input
              id="anum"
              type="number"
              min="1"
              bind:value={createForm.num}
            />
          </div>
          <div
            class="field-row"
            style="justify-content:flex-end; margin-top:8px;"
          >
            <button on:click={() => (showCreate = false)}>Cancel</button>
            <button class="default" on:click={createGroup}>Create</button>
          </div>
        </div>
      {/if}

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
