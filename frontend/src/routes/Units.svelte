<script>
  import { push } from "svelte-spa-router";
  import { logoutUser } from "../js/User.js";
  import Card from "../components/Card.svelte";

  logoutUser();

  let units = ["CAB302", "CAB202", "CAB222", "IFB104", "IAB201"];
  let search = { unit: units[0], looking: true, openMsg: true, note: "" };
  let groups = [
    {
      name: "Team Retro",
      unit: "CAB302",
      members: "3/4",
      time: "Weekdays 2–5pm",
    },
    { name: "Night Owls", unit: "CAB202", members: "2/4", time: "After 8pm" },
    { name: "Data Ninjas", unit: "CAB222", members: "1/4", time: "Weekends" },
  ];
  const post = () => alert("Posted! (demo)");
  const refresh = () => alert("Refreshed! (demo)");
</script>

<main
  style="padding:12px; display:flex; flex-direction:column; gap:12px; align-items:center;"
>
  <!-- Hero -->
  <Card title="Study Buddy">
    <p>
        <strong>Find teammates for your uni assessments</strong> — retro Mac vibe,
        simple and fast.
    </p>
    <div class="field-row" style="justify-content:flex-end;">
        <button>About</button>
        <button class="default">Get Started</button>
    </div>
  </Card>

  <!-- Quick Post -->
  <Card title="Find a Team">
    <div class="field-row">
        <label for="unit">Unit</label>
        <select id="unit" bind:value={search.unit}>
          {#each units as u}<option value={u}>{u}</option>{/each}
        </select>
      </div>
      <div class="field-row">
        <label
          ><input type="checkbox" bind:checked={search.looking} /> Looking for team</label
        >
        <label
          ><input type="checkbox" bind:checked={search.openMsg} /> Open to messages</label
        >
      </div>
      <div class="field-row">
        <label for="note">Note</label>
        <input
          id="note"
          type="text"
          placeholder="Prefer weekdays 2–5pm"
          bind:value={search.note}
        />
      </div>
      <div class="field-row" style="justify-content:flex-end; margin-top:8px;">
        <button on:click={() => (search.note = "")}>Cancel</button>
        <button class="default" on:click={post}>Post</button>
      </div>
  </Card>

  <!-- Groups -->
  <card>
      <ul style="padding-left:1rem;">
        {#each groups as g}
          <li class="field-row" style="justify-content:space-between;">
            <div>
              <strong>{g.name}</strong> — {g.unit} — {g.members}
              <span style="opacity:.7;">({g.time})</span>
            </div>
            <div>
              <button>View</button><button class="default">Join</button>
            </div>
          </li>
        {/each}
      </ul>
      <div class="field-row" style="justify-content:flex-end;">
        <button on:click={refresh}>Refresh</button>
      </div>
    </card>
</main>

<style>
</style>
