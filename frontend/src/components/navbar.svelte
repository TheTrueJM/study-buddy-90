<script>
  import { push } from "svelte-spa-router";
  const go = (p) => (push ? push(p) : (location.hash = p));
</script>

<div
  style="position:fixed; top:8px; left:8px; z-index:1000; transform:scale(.88); transform-origin:top left;"
>
  <div class="window" style="width:320px;">
    <div class="title-bar">
      <button aria-label="Close" class="close"></button>
      <h1 class="title">Study Buddy</h1>
      <button aria-label="Resize" class="resize"></button>
    </div>
    <div class="separator"></div>
    <div class="window-pane">
      <div class="field-row" style="gap:6px;">
        <button on:click={() => go("/")}>Authentication</button>
        <button on:click={() => go("/units")}>Units</button>
      </div>
    </div>
  </div>
</div>
