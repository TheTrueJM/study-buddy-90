<script>
  import { onMount } from 'svelte';
  import { params } from "svelte-spa-router";
  import { fetchGroupDetails, createGroupRequest } from '../js/api.js';

  let id = "";
  let group = null;
  let loading = true;
  let error = null;
  
  // Mock user membership check - in real app would check from backend
  const currentUserId = 1;
  const myGroupIds = new Set(["G-214", "G-101"]);
  
  let joined = false;
  let requested = false;
  let messages = [];
  let incomingRequests = [];
  let draft = "";

  $: id = ($params && $params.id) || (typeof location !== 'undefined' ? (location.hash.split("/")[2] || "") : "");

  onMount(async () => {
    if (id) {
      await loadGroup();
    }
  });

  $: if (id) {
    loadGroup();
  }

  async function loadGroup() {
    try {
      loading = true;
      group = await fetchGroupDetails(id);
      
      if (group) {
        joined = myGroupIds.has(id) || group.members.some(m => m.student_id === currentUserId);
        messages = group.messages || [];
        incomingRequests = group.incoming_requests || [];
      } else {
        error = "Group not found";
      }
    } catch (err) {
      error = "Failed to load group details";
    } finally {
      loading = false;
    }
  }

  function acceptRequest(studentId) {
    const request = incomingRequests.find(r => r.student_id === studentId);
    if (request && group.members.length < group.max_members) {
      group.members = [...group.members, request];
      incomingRequests = incomingRequests.filter(r => r.student_id !== studentId);
      group = { ...group };
    }
  }

  function rejectRequest(studentId) {
    incomingRequests = incomingRequests.filter(r => r.student_id !== studentId);
  }

  function send() {
    const text = draft.trim();
    if (!text || !joined) return;
    messages = [...messages, { id: Date.now(), from: "You", text }];
    draft = "";
  }

  async function requestJoin() {
    if (joined || requested) return;
    
    try {
      const result = await createGroupRequest(group.group_id || id);
      if (result) {
        requested = true;
      }
    } catch (err) {
      console.error('Failed to request join:', err);
    }
  }
</script>

<main style="padding:12px; display:flex; justify-content:center;">
  <div class="window" style="width:960px;">
    <div class="title-bar">
      <button class="close"></button>
      <h1 class="title">Group {group?.num || id}</h1>
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
        <p style="text-align:center; opacity:0.7; padding:2rem;">Loading group details...</p>
      {:else if group}
        <div class="details-bar" style="align-items:center;">
          <div class="field-row" style="gap:12px;">
            <div>Unit: <strong>{group.unit_code}</strong></div>
            <div>ID: <strong>{group.id || id}</strong></div>
          </div>
          <div class="heading">
            Members: <strong>{group.members?.length || 0}/{group.max_members || 5}</strong>
          </div>
        </div>

        <h3 class="heading" style="margin:16px 0 6px;">Members</h3>
        <div style="padding:6px 0 8px;">
          {#if group.members && group.members.length > 0}
            <div style="display:flex; flex-wrap:wrap; gap:12px;">
              {#each group.members as m}
                <div class="standard-dialog" style="width:280px; flex:0 0 auto;">
                  <div style="display:flex; align-items:center; gap:8px;">
                    <img
                      src={m.avatar || "https://cdn.discordapp.com/embed/avatars/0.png"}
                      alt="avatar"
                      style="width:48px; height:48px; border:1.5px solid var(--secondary); object-fit:cover;"
                    />
                    <div style="font-family:Chicago_12; line-height:1.2; flex:1;">
                      <div><strong>{m.name || m.student_id}</strong></div>
                      {#if !joined && m.availability}
                        <div style="font-size:11px; opacity:0.8; margin-top:2px;">
                          Available: {m.availability}
                        </div>
                      {/if}
                    </div>
                  </div>
                </div>
              {/each}
            </div>
          {:else}
            <p style="text-align:center; opacity:0.7; padding:1rem;">No members in this group yet.</p>
          {/if}
        </div>

      {#if joined}
        <!-- Chat window only visible when joined -->
        <div class="standard-dialog" style="margin-top:12px;">
          <h3 class="heading" style="margin:0 0 8px;">Group Chat</h3>
          <div class="outer-border inner-border" style="height:280px; overflow:auto; padding:8px; background:var(--primary);">
            {#each messages as m}
              <div style="margin-bottom:6px;">
                <strong>{m.from}:</strong> {m.text}
              </div>
            {/each}
          </div>
          <div class="field-row" style="margin-top:8px;">
            <input type="text" placeholder="Type a message" bind:value={draft} on:keydown={(e)=> e.key==='Enter' && send()} />
            <button class="default" on:click={send}>Send</button>
          </div>
        </div>

        <!-- Pending join requests section for group leaders/members -->
        {#if incomingRequests.length > 0}
          <div class="standard-dialog" style="margin-top:12px;">
            <h3 class="heading" style="margin:0 0 8px;">Pending Join Requests</h3>
            <div style="display:flex; flex-direction:column; gap:8px;">
              {#each incomingRequests as request}
                <div class="field-row" style="justify-content:space-between; align-items:center; padding:8px; background:rgba(0,0,0,0.05); border-radius:4px;">
                  <div style="display:flex; align-items:center; gap:8px;">
                    <img
                      src={request.avatar}
                      alt="avatar"
                      style="width:32px; height:32px; border:1px solid var(--secondary); object-fit:cover; border-radius:2px;"
                    />
                    <div style="font-family:Chicago_12; line-height:1.2;">
                      <div><strong>{request.name}</strong></div>
                      <div style="font-size:11px; opacity:0.8;">
                        Available: {request.availability}
                      </div>
                    </div>
                  </div>
                  <div class="field-row" style="gap:6px;">
                    <button class="default" on:click={() => acceptRequest(request.student_id)}>Accept</button>
                    <button on:click={() => rejectRequest(request.student_id)}>Reject</button>
                  </div>
                </div>
              {/each}
            </div>
          </div>
        {/if}
      {/if}

        {#if !joined}
          <div class="field-row" style="justify-content:flex-end; margin-top:12px;">
            <button class="default" on:click={requestJoin} disabled={requested}>{requested ? 'Requested' : 'Request to Join Group'}</button>
          </div>
        {/if}
      {:else}
        <p style="text-align:center; opacity:0.7; padding:2rem;">Group not found.</p>
      {/if}
    </div>
  </div>
</main>

<style>
</style>
