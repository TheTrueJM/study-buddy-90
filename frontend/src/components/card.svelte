<script>
    let { title } = $props();
</script>

<div class="window" style="width:960px;">
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