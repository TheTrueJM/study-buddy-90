<script>
  import Router from 'svelte-spa-router';

  import Navbar from './components/navbar.svelte';

  import Authentication from './routes/Authentication.svelte';
  import Units from './routes/Units.svelte';

  const routes = {
    '/': Authentication,
    '/units': Units,
  };


  import { userId } from './js/User.js';
</script>

<main>
  <Navbar> </Navbar>

  <Router {routes} />
</main>