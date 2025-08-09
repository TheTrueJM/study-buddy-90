<script>
  import { onMount } from "svelte";
  import { push } from "svelte-spa-router";
  import { params } from "svelte-spa-router";
  import { joinGroupMember } from '../js/api.js';
  import { ensureUser, getUserId } from '../js/User.js';

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
  let toast = "";
  let newGroupName = "";

  // Track joined groups locally for button disabling
  let joined = new Set();

  async function joinGroup(group) {
    if (joined.has(String(group.id))) return;
    await ensureUser();
    const uid = getUserId();
    const res = await joinGroupMember(group.id, uid);
    if (res) {
      joined = new Set(joined);
      joined.add(String(group.id));
    }
  }

  function viewDetails(group) {
    // Use numeric group ID directly to match backend
    push(`/group/${group.id}`);
  }

  import { fetchAssessmentGroups } from "../js/api.js";
  import { createAssessmentGroup } from "../js/api.js";

  onMount(async () => {
    if (!code || !num) {
      error = "Invalid assessment parameters";
      loading = false;
      return;
    }

    try {
      groups = await fetchAssessmentGroups(code, num);
    } catch (err) {
      error = "Failed to load groups for this assessment";
      console.error('Error fetching assessment groups:', err);
    } finally {
      loading = false;
    }
  });

  async function createGroup() {
    try {
      const res = await createAssessmentGroup(code, num, newGroupName.trim() || undefined);
      if (res) {
        toast = `Created ${res.name || 'group'}`;
        newGroupName = "";
        groups = await fetchAssessmentGroups(code, num);
        setTimeout(() => (toast = ""), 1500);
      }
    } catch (e) {
      toast = 'Failed to create group';
      setTimeout(() => (toast = ""), 1500);
    }
  }
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
      <div class="details-bar" style="align-items:center; gap:8px;">
        <div class="heading" style="flex:1;">Available Groups</div>
        <input placeholder="New group name (optional)" bind:value={newGroupName} style="width:240px;" />
        <button class="default" on:click={createGroup}>Create Group</button>
      </div>

      {#if error}
        <div class="alert-box outer-border inner-border" style="margin:12px 0; background-color: #ff6b6b;">
          <div class="alert-contents">{error}</div>
        </div>
      {/if}

      {#if toast}
        <div class="alert-box outer-border inner-border" style="margin:12px 0;">
          <div class="alert-contents">{toast}</div>
        </div>
      {/if}

      {#if loading}
        <p style="text-align:center; opacity:0.7; padding:2rem;">Loading groups...</p>
      {:else if groups.length > 0}
        <ul style="padding-left:1rem;">
          {#each groups as g}
            <li class="field-row" style="justify-content:space-between;">
              <div>
                <strong>{g.name || `Group ${g.id}`}</strong> — {g.unit_code} — Assessment {g.num}
              </div>
              <div class="field-row" style="gap:6px;">
                <button on:click={() => viewDetails(g)}>View Details</button>
                <button
                  class="default"
                  on:click={() => joinGroup(g)}
                  disabled={joined.has(String(g.id))}
                >
                  {joined.has(String(g.id)) ? "Joined" : "Join Group"}
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
