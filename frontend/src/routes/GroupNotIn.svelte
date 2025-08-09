<!-- Mock-only UI. If connected to backend, load group details by ID and POST a join request; show pending state. -->
<script>
  import { push } from "svelte-spa-router";
  let group = {
    unit_code: "CAB302",
    num: 3,
    id: "G-214",
    max_members: 5,
    members: [
      {
        student_id: "n1234567",
        avatar: "https://cdn.discordapp.com/embed/avatars/1.png",
      },
      {
        student_id: "n2345678",
        avatar: "https://cdn.discordapp.com/embed/avatars/2.png",
      },
      {
        student_id: "n3456789",
        avatar: "https://cdn.discordapp.com/embed/avatars/3.png",
      },
    ],
  };

  let requested = false;
  function requestJoin() {
    if (requested) return;
    requested = true;
  }
</script>

<main style="padding:12px; display:flex; justify-content:center;">
  <div class="window" style="width:960px;">
    <div class="title-bar">
      <button class="close"></button>
      <h1 class="title">Group {group.num}</h1>
      <button class="resize"></button>
    </div>
    <div class="separator"></div>
    <div class="window-pane">
      <div class="details-bar" style="align-items:center;">
        <div class="field-row" style="gap:12px;">
          <div>Unit: <strong>{group.unit_code}</strong></div>
          <div>ID: <strong>{group.id}</strong></div>
        </div>
        <div class="heading">
          Members: <strong>{group.members.length}/{group.max_members}</strong>
        </div>
      </div>

      <h3 class="heading" style="margin:16px 0 6px;">Members</h3>
      <div style="padding:6px 0 8px;">
        <div style="display:flex; flex-wrap:wrap; gap:12px;">
          {#each group.members as m}
            <div class="standard-dialog" style="width:220px; flex:0 0 auto;">
              <div style="display:flex; align-items:center; gap:8px;">
                <img
                  src={m.avatar}
                  alt="avatar"
                  style="width:48px; height:48px; border:1.5px solid var(--secondary); object-fit:cover;"
                />
                <div style="font-family:Chicago_12; line-height:1.2;">
                  <div><strong>{m.student_id}</strong></div>
                </div>
              </div>
            </div>
          {/each}
        </div>
      </div>

      {#if requested}
        <div class="alert-box outer-border inner-border" style="margin:12px 0;">
          <div class="alert-contents">Join request sent</div>
        </div>
      {/if}

      <div class="field-row" style="justify-content:flex-end; margin-top:12px;">
        <button class="default" on:click={() => push(`/group/${group.id}`)}>View Group</button>
      </div>
    </div>
  </div>
</main>

<style>
</style>
