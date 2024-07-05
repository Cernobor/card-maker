<script lang="ts">
  import DOMPurify from "isomorphic-dompurify";
  export let name:string, type, tags = [], attributes:string, description:string;

  function pf_filter(text) {
    // Actions
    // text = text.replace(/\(A\)/gi, '<img class="activity" src="/imgs/one.webp" alt="One action">')
    //   .replace(/\(AA\)/gi, '<img class="activity" src="/imgs/two.webp" alt="Two actions">')
    //   .replace(/\(AAA\)/gi, '<img class="activity" src="/imgs/three.webp" alt="Three action">')
    //   .replace(/\(R\)/gi, '<img class="activity" src="/imgs/reaction.webp" alt="Reaction">')
    //   .replace(/\(F\)/gi, '<img class="activity" src="/imgs/free.webp" alt="Free action">');
    return text;
  }
</script>

<style>
  .card {
    width: calc(2.5in - 4mm);
    height: calc(3.5in - 4mm);
    font-size: 8pt;
    border: 2mm solid black;
    /*background-image: url("/bg.webp");*/
    background-clip: border-box;
    page-break-after: auto;
    page-break-inside: avoid;
  }
  .header {
    display: flex;
    justify-content: space-between;
    border-bottom: 2px solid black;
    padding: 0 4pt;
  }
  .name, .type {
    font-family: serif;
    font-size: 10pt;
    font-weight: bold;
  }
  .tags {
    padding: 1pt 4pt;
    display: flex;
    flex-wrap: wrap;
  }
  .tag {
    font-family: sans-serif;
    font-size: 6pt;
    font-variant: all-small-caps;
    color: white;
    background-color: #5e0000;
    padding: 0.5pt 1pt;
    border: 1pt solid #d9c484;
  }
  .uncommon {
    background-color: #98513d;
  }
  .rare {
    background-color: #002664;
  }
  .unique {
    background-color: #54166e;
  }
  .content {
    margin-top: 1pt;
  }
  .content div {
    padding: 0 4pt;
  }
  :global(section.content p) {
    padding-bottom: 2pt;
    margin: 0;
  }
  .description {
    border-top: 1pt solid black;
    text-align: justify;
  }
  :global(img.activity) {
    max-height: 8pt;
  }
  .description :global(img :not(.activity)) {
    display: block;
    margin: auto;
  }
</style>


<div class="card">
  <section class="header">
    <div class="name">{name}</div>
    <div class="type">{type}</div>
  </section>
  <section class="tags">
    {#each tags as tag}
      {#if tag.toLowerCase() == "uncommon" }
	<div class="tag uncommon">{tag}</div>
      {:else if tag.toLowerCase() == "rare" }
	<div class="tag rare">{tag}</div>
      {:else if tag.toLowerCase() == "unique" }
	<div class="tag unique">{tag}</div>
      {:else}
	<div class="tag">{tag}</div>
      {/if}
    {/each}
  </section>
  <section class="content">
    <div class="attributes">
      {@html pf_filter(DOMPurify.sanitize(attributes))}
    </div>
    <div class="description">
      {@html pf_filter(DOMPurify.sanitize(description))}
    </div>
  </section>
</div>

