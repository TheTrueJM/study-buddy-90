<!-- Mock-only UI. If connected to backend, replace local arrays with fetches to load groups and units, and POST the create action. -->
<script>
  import { push } from "svelte-spa-router";

  let units = [{ code: "CAB302" }, { code: "CAB201" }, { code: "IFB295" }];

  let groups = [
    { id: "G-101", unit_code: "CAB302", num: 1, members: 3, max: 5 },
    { id: "G-214", unit_code: "CAB201", num: 2, members: 2, max: 4 },
    { id: "G-377", unit_code: "IFB295", num: 1, members: 4, max: 6 },
  ];

  let showCreate = false;
  let createForm = { unit_code: units[0].code, num: 1 };
  let toast = "";

  function createGroup() {
    if (!createForm.unit_code || createForm.num < 1) return;
    const newId = `G-${Math.floor(100 + Math.random() * 900)}`;
    groups = [
      ...groups,
      {
        id: newId,
        unit_code: createForm.unit_code,
        num: createForm.num,
        members: 1,
        max: 5,
      },
    ];
    toast = "Group created";
    showCreate = false;
    setTimeout(() => (toast = ""), 1500);
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

      {#if groups.length}
        <ul style="padding-left:1rem;">
          {#each groups as g}
            <li class="field-row" style="justify-content:space-between;">
              <div>
                <strong>{g.id}</strong> — {g.unit_code} — Assessment {g.num}
                <span style="opacity:.7;">({g.members}/{g.max})</span>
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
