<script>
  import { push } from 'svelte-spa-router';
</script>

<nav>
    <div class="container">
        <a href="/" on:click|preventDefault={() => push('/')}>Authentication</a>
        <a href="/units" on:click|preventDefault={() => push('/units')}>Units</a>
    </div>
</nav>

<style>

</style>