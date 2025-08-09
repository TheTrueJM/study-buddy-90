<script>
  import { onMount } from "svelte";

  let audio;
  let stations = [
    {
      name: "Lainchan Radio",
      url: "https://radio.lainchan.org/listen/lainchan_radio_main/radio.mp3",
    },
    { name: "Lainzine Music", url: "https://radio.lainzine.org:8443/music" },
    {
      name: "Gensokyo Radio",
      url: "https://stream.gensokyoradio.net/2",
    },
  ];
  let selected = 0;
  let nowPlaying = stations[selected].name;
  let playing = false;

  async function setSrc(url) {
    if (!audio) return;
    audio.src = url;
    try {
      audio.load();
    } catch {}
    playing = false;
  }

  function handleStationChange(i) {
    selected = +i;
    nowPlaying = stations[selected].name;
    setSrc(stations[selected].url);
  }

  function togglePlay() {
    if (!audio) return;
    if (audio.paused) {
      audio.play();
    } else {
      audio.pause();
    }
  }

  onMount(() => {
    if (!audio) return;
    setSrc(stations[selected].url);
    audio.addEventListener("playing", () => {
      playing = true;
      if ("mediaSession" in navigator) {
        try {
          navigator.mediaSession.metadata = new MediaMetadata({
            title: nowPlaying,
          });
        } catch {}
      }
    });
    audio.addEventListener("pause", () => {
      playing = false;
    });
    audio.addEventListener("ended", () => {
      playing = false;
    });
    audio.addEventListener("error", () => {});
  });
</script>

<div class="radio inline">
  NOW PLAYING
  <div class="row">
    <select
      class="field"
      on:change={(e) => handleStationChange(e.target.value)}
      bind:value={selected}
    >
      {#each stations as s, i}
        <option value={i}>{s.name}</option>
      {/each}
    </select>
    <button class="btn" on:click={togglePlay}
      >{playing ? "Pause" : "Play"}</button
    >
  </div>
  <audio bind:this={audio}></audio>
</div>

<style>
  .radio {
    width: 100%;
    box-sizing: border-box;
    max-width: 244px;
    padding: 6px;
    border: 1px solid #000;
    background: #fff;
  }
  .row {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 6px;
    align-items: center;
    margin-bottom: 6px;
  }
  .field {
    width: 100%;
    box-sizing: border-box;
    font-size: 12px;
  }
  .btn {
    padding: 2px 8px;
    font-size: 12px;
  }
  .now {
    display: grid;
    grid-template-columns: 1fr;
    align-items: center;
    margin: 6px 0;
    gap: 6px;
  }
  .track {
    font-family: Monaco, monospace;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 11px;
  }
</style>
