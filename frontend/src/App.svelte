<script>
  import Router from "svelte-spa-router";
  import { push } from "svelte-spa-router";

  import Navbar from "./components/navbar.svelte";

  import Authentication from "./routes/Authentication.svelte";
  import Units from "./routes/Units.svelte";
  import MyUnits from "./routes/MyUnits.svelte";
  import Unit from "./routes/Unit.svelte";
  import Group from "./routes/Group.svelte";
  import Groups from "./routes/Groups.svelte";
  import Assessments from "./routes/Assessments.svelte";
  import GroupNotIn from "./routes/GroupNotIn.svelte";
  import AssessmentGroups from "./routes/AssessmentGroups.svelte";

  const routes = {
    "/": Units, // Auto-redirect to units since user is authenticated
    "/units": Units,
    "/my-units": MyUnits,
    "/unit/:code": Unit,
    "/group/:id": Group,
    "/groups": Groups,
    "/assessments": Assessments,
    "/assessment-groups/:code/:num": AssessmentGroups,
    "/group-not-in": GroupNotIn,
  };

  import { userId } from "./js/User.js";
</script>

<main>
  <Navbar></Navbar>

  <Router {routes} />
</main>
