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
  import CornerGif from "./components/CornerGif.svelte";
  import SiteButtons from "./components/SiteButtons.svelte";
  import RadioPlayer from "./components/RadioPlayer.svelte";
  import { onMount } from 'svelte';

  import { getCurrentUser, isAuthenticated } from "./js/User.js";
  import { get } from "svelte/store";

  const routes = {
    "/": Authentication,
    "/login": Authentication,
    "/units": Units,
    "/my-units": MyUnits,
    "/unit/:code": Unit,
    "/group/:id": Group,
    "/groups": Groups,
    "/assessments": Assessments,
    "/assessment-groups/:code/:num": AssessmentGroups,
    "/group-not-in": GroupNotIn,
  };

  getCurrentUser();

  function routeGuard(detail) {
    const currentRoute = detail.location || window.location.hash.slice(1);
    const authenticated = get(isAuthenticated);

    if (!authenticated && currentRoute !== "/" && currentRoute !== "/login") {
      push("/");
      return false;
    }

    if (authenticated && (currentRoute === "/" || currentRoute === "/login")) {
      push("/units");
      return false;
    }

    return true;
  }

  let radioTop = 180;
  function positionRadio() {
    const el = document.querySelector('#nav-root .window');
    const rect = el ? el.getBoundingClientRect() : null;
    radioTop = rect ? rect.bottom + 8 : 180;
  }
  onMount(() => {
    positionRadio();
    const el = document.querySelector('#nav-root .window');
    let ro;
    if (window.ResizeObserver) {
      ro = new ResizeObserver(positionRadio);
      if (el) ro.observe(el);
    }
    window.addEventListener('resize', positionRadio);
    return () => {
      window.removeEventListener('resize', positionRadio);
      if (ro) ro.disconnect();
    };
  });
</script>

<main>
  <div class="retro-banner" aria-hidden="true">
    <marquee behavior="scroll" direction="left" scrollamount="5">
      Welcome to Study Buddy 2000! Best viewed at 1024×768 in Netscape Navigator · SIGN UP NOW!!!
    </marquee>
  </div>
  <Navbar></Navbar>
  <div style="position:fixed; left:8px; z-index:990; width:260px;" style:top={`${radioTop}px`}>
    <RadioPlayer />
  </div>

  <Router {routes} on:routeEvent={routeGuard} />
  <CornerGif />
  <SiteButtons />
  <div class="crt-mask" aria-hidden="true"></div>
</main>

<style>
  .retro-banner {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 28px;
    z-index: 950;
    pointer-events: none;
    background: linear-gradient(
      90deg,
      #ff00cc,
      #6600ff 25%,
      #00ffff 50%,
      #00ff66 75%,
      #ffff00
    );
    background-size: 200% 100%;
    animation: banner-sheen 10s linear infinite;
    box-shadow:
      inset 0 -2px rgba(0, 0, 0, 0.35),
      0 2px 0 rgba(255, 255, 255, 0.25);
    color: black;
    font-weight: bold;
    text-transform: uppercase;
    text-shadow:
      0 1px #fff,
      0 0 6px rgba(255, 255, 255, 0.6);
    filter: saturate(1.2);
  }
  .retro-banner marquee {
    line-height: 28px;
    font-size: 12px;
  }
  @keyframes banner-sheen {
    0% {
      background-position: 0% 50%;
    }
    100% {
      background-position: 200% 50%;
    }
  }
</style>
