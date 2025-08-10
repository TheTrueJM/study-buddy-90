<script>
  import gifUrl from "../assets/qut_rotate_final.gif";
  export let alt = "QUT rotating";
  export let title = "";
</script>

<div class="corner-gif" aria-hidden="true">
  <img src={gifUrl} alt={alt} {title} />
  
</div>

<style>
  .corner-gif {
    position: fixed;
    left: 8px;
    bottom: 8px;
    z-index: 999; /* Below navbar (1000), above content */
    pointer-events: none; /* Don’t block clicks */
  }

  .corner-gif img {
    display: block;
    height: auto;
  }
</style>

