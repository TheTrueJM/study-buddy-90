<script>
  import { onMount } from 'svelte';
  import { push } from "svelte-spa-router";
  import { fetchMyGroups, fetchGroupRequests, deleteGroupRequest } from '../js/api.js';

  let myGroups = [];
  let pendingRequests = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    try {
      const [groups, requests] = await Promise.all([
        fetchMyGroups(),
        fetchGroupRequests()
      ]);
      myGroups = groups;
      pendingRequests = requests;
    } catch (err) {
      error = "Failed to load groups";
    } finally {
      loading = false;
    }
  });

  function openGroup(g) {
    const groupId = `${g.unit_code}-${g.num}-${g.id}`;
    push(`/group/${groupId}`);
  }

  async function cancelRequest(request) {
    try {
      const result = await deleteGroupRequest(request.group_id || request.id);
      if (result) {
        pendingRequests = pendingRequests.filter(r => (r.group_id || r.id) !== (request.group_id || request.id));
      }
    } catch (err) {
      console.error('Failed to cancel request:', err);
    }
  }
</script>

<main style="padding:12px; display:flex; flex-direction:column; gap:12px; align-items:center;">
  <div class="window" style="width:960px;">
    <div class="title-bar">
      <button class="close"></button>
      <h1 class="title">My Groups</h1>
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
        <p style="text-align:center; opacity:0.7; padding:2rem;">Loading your groups...</p>
      {:else if myGroups.length}
        <ul style="padding-left:1rem;">
          {#each myGroups as g}
            <li class="field-row" style="justify-content:space-between;">
              <div>
                <strong>Group {g.id}</strong> — {g.unit_code} — Assessment {g.num}
                <span style="opacity:.7;">(Members: {g.members || 0}/{g.max_members || 4})</span>
                {#if g.unread}
                  <span style="margin-left:8px;">• {g.unread} unread</span>
                {/if}
              </div>
              <div class="field-row" style="gap:6px;">
                <button on:click={() => openGroup(g)}>Open</button>
                <button class="default" on:click={() => openGroup(g)}>Message</button>
              </div>
            </li>
          {/each}
        </ul>
      {:else}
        <p style="text-align:center; opacity:0.7; padding:2rem;">You haven't joined any groups yet.</p>
      {/if}
    </div>
  </div>

  {#if !loading && pendingRequests.length}
    <div class="window" style="width:960px;">
      <div class="title-bar">
        <button class="close"></button>
        <h1 class="title">Pending Requests</h1>
        <button class="resize"></button>
      </div>
      <div class="separator"></div>
      <div class="window-pane">
        <ul style="padding-left:1rem;">
          {#each pendingRequests as request}
            <li class="field-row" style="justify-content:space-between;">
              <div>
                <strong>{request.id || request.group_id}</strong> — {request.unit_code} — Assessment {request.num}
                <span style="opacity:.7;">({request.members || 0}/{request.max_members || request.max || 5})</span>
                <span style="margin-left:8px; color:orange;">• Request pending</span>
              </div>
              <div class="field-row" style="gap:6px;">
                <button on:click={() => openGroup(request)}>View</button>
                <button class="default" on:click={() => cancelRequest(request)}>Cancel Request</button>
              </div>
            </li>
          {/each}
        </ul>
      </div>
    </div>
  {/if}
</main>

<style>
</style>
