<script>
  export let buttons = [
    {
      img: "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.qut.edu.au%2F__data%2Fassets%2Fimage%2F0007%2F909781%2Fqut-logo-og-1200.jpg&f=1&nofb=1&ipt=9f7825fdf0da2b90fa74cf6c557e97c5acee23416d6b6520546675fa4cad1b4d",
      alt: "QUT Logo",
      colors: ["#00407a", "#001a3d"],
      fg: "#fff",
      href: "https://www.qut.edu.au/",
    },
    {
      img: "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Facademics.fresnostate.edu%2Fcanvas%2Fimages%2FLogo_Canvas_Red_Horizontal.png&f=1&nofb=1&ipt=77e0d838214eb4f85187e608a27cd609ebdb924d982f1775e34636dfb96b10b3",
      alt: "Canvas Logo",
      colors: ["#00407a", "#001a3d"],
      fg: "#fff",
      href: "https://canvas.qut.edu.au/",
    },
    {
      text: "HiQ",
      colors: ["#00407a", "#001a3d"],
      fg: "#fff",
      href: "https://qutvirtual4.qut.edu.au/web/qut/hiq",
    },
    {
      text: "Library",
      colors: ["#00407a", "#001a3d"],
      fg: "#fff",
      href: "https://www.library.qut.edu.au/",
    },
    {
      text: "Support",
      colors: ["#00407a", "#001a3d"],
      fg: "#fff",
      href: "https://www.qut.edu.au/study/student-life/student-support",
    },
    {
      text: "Contact",
      colors: ["#00407a", "#001a3d"],
      fg: "#fff",
      href: "https://www.qut.edu.au/about/contact",
    },
  ];
</script>

<div class="site-buttons" aria-label="Site buttons" role="group">
  {#each buttons as b}
    <a
      class="btn88x31"
      href={b.href || "#"}
      style="--c1:{b.colors[0]}; --c2:{b.colors[1]}; --fg:{b.fg}"
    >
      {#if b.img}
        <img src={b.img} alt={b.alt} width="88" height="31" />
      {:else}
        {b.text}
      {/if}
    </a>
  {/each}
  <slot />
</div>

<style>
  .site-buttons {
    position: fixed;
    right: 8px;
    bottom: 8px;
    z-index: 999;
    display: grid;
    grid-template-columns: repeat(3, 88px);
    gap: 6px;
    align-items: start;
    justify-items: start;
    pointer-events: none;
  }
  .btn88x31 {
    width: 88px;
    height: 31px;
    background: linear-gradient(var(--c1), var(--c2));
    border: 1px solid #000;
    box-shadow:
      0 0 0 1px #fff inset,
      0 0 8px rgba(0, 0, 0, 0.35);
    color: var(--fg);
    font:
      700 9px/31px Monaco,
      monospace;
    text-align: center;
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    pointer-events: auto;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .btn88x31:hover {
    filter: brightness(1.1) contrast(1.05);
  }
  .btn88x31 img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }
</style>
