<script>
    import JobCard from './JobCard.svelte';
    export let jobs = [];

    let query = "";

    $: filteredJobs = jobs.filter((job) =>
        job.job_title.toLowerCase().includes(query.toLowerCase())
    );
</script>

<div class="search-container">
  <input
    type="text"
    placeholder="Search jobs..."
    bind:value={query}
    class="search-input"
  />

  <div class="job-list">
    {#each filteredJobs as item}
      <JobCard
        title={item.job_title}
        company={item.company_name}
        apply_url={item.apply_url}
      >
        {item.content}
      </JobCard>
    {/each}

    {#if filteredJobs.length === 0}
      <p class="no-results">No jobs found matching “{query}”.</p>
    {/if}
  </div>
</div>

<style>
  .search-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .search-input {
    padding: 0.75rem 1rem;
    font-size: 1rem;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background-color: #1a1a1a;
    color: #fff;
    outline: none;
    transition: all 0.2s ease;
  }

  .search-input:focus {
    border-color: rgba(0, 150, 255, 0.5);
    box-shadow: 0 0 10px rgba(0, 150, 255, 0.3);
  }

  .job-list {
    display: grid;
    gap: 1rem;
  }

  .no-results {
    color: #888;
    font-size: 0.95rem;
    text-align: center;
  }
</style>
