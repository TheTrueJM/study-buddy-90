<script>
  import { push, params } from "svelte-spa-router";
  import { logoutUser } from "../js/User.js";
  import Card from "../components/card.svelte";

  let path = window.location.href;
  let unitCode = path.split('/').pop();
  console.log(unitCode)
</script>

<main
  style="padding:12px; display:flex; flex-direction:column; gap:12px; align-items:center;"
>
    Testing
</main>

<style>
</style>
