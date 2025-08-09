<script>
  import { push } from "svelte-spa-router";
  const go = (p) => (push ? push(p) : (location.hash = p));
</script>

<div
  style="position:fixed; top:8px; left:8px; z-index:1000; transform:scale(.88); transform-origin:top left;"
>
  <div class="window" style="width:360px;">
    <div class="title-bar">
      <button aria-label="Close" class="close"></button>
      <h1 class="title">Study Buddy</h1>
      <button aria-label="Resize" class="resize"></button>
    </div>
    <div class="separator"></div>
    <div class="window-pane">
      <div class="field-row" style="gap:6px; flex-wrap:wrap;">
        <button class="link-button" on:click={() => go("/")}>Authentication</button>
        <button class="link-button" on:click={() => go("/units")}>Units</button>
        <button class="link-button" on:click={() => go("/my-units")}>My Units</button>
        <button class="link-button" on:click={() => go("/assessments")}>Assessments</button>
        <button class="link-button" on:click={() => go("/groups")}>My Groups</button>
      </div>
    </div>
  </div>
</div>

<style>
  .link-button {
    background: none;
    border: none;
    color: blue;
    text-decoration: underline;
    cursor: pointer;
    font-family: inherit;
    font-size: inherit;
    padding: 2px 4px;
  }
  
  .link-button:hover {
    color: darkblue;
  }
  
  .link-button:active {
    color: red;
  }
</style>
