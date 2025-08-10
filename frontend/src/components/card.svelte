<script>
  let { title } = $props();
</script>

<div class="window" style="width:600px;">
  <div class="title-bar">
    <button class="close"></button>
    <h1 class="title">{title}</h1>
    <button class="resize"></button>
  </div>
  <div class="separator"></div>

  <div class="window-pane">
    <slot></slot>
  </div>
</div>

<style>
  .window-pane {
    text-align: center;
  } /* 텍스트 가운데 */
  .window-pane .field-row {
    justify-content: center;
  } /* 버튼/폼 줄도 가운데 */
</style>
