<script>
    import { onMount } from 'svelte';
    import JobCard from './JobCard.svelte';

    let jobs = [];
    let query = "";
    let error = null;
    let jobsCount = 0;
    let uniqueCount = 0;

    onMount(async () => {
        try {
            // Get current date in Helsinki timezone
            const now = new Date();

            // Use Intl.DateTimeFormat to get parts adjusted to Helsinki timezone
            const helsinkiDateParts = new Intl.DateTimeFormat('en-CA', {
                timeZone: 'Europe/Helsinki',
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
            }).formatToParts(now);

            // Build YYYY-MM-DD string
            const helsinkiDate = helsinkiDateParts
                .map(part => part.value)
                .join('')
                .replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3');


            const response = await fetch(`/jobs/?date=${helsinkiDate}`);
            if (!response.ok) {
                throw new Error(`Fetch failed with status: ${response.status}`);
            }
            jobs = await response.json();
        } catch (err) {
            error = err.message;
            console.error('Fetch error details:', err);
        }
    });

    $: jobsCount = jobs.length;
    $: uniqueCount = new Set(jobs.map(item => item.company_name)).size;

    $: filteredJobs = jobs.filter((job) =>
        job.job_title.toLowerCase().includes(query.toLowerCase())
    );
</script>


{#if error}
    <p>Error loading jobs: {error}</p>
{:else}
    <h1>{jobsCount} active job posts from {uniqueCount} companies</h1>

    <div class="search-container">
        <input
            type="text"
            placeholder="Search job title..."
            bind:value={query}
            class="search-input"
        />

        <div class="job-list">
            {#if jobs.length === 0}
                <p>Loading jobs...</p>
            {:else if filteredJobs.length === 0}
                <p class="no-results">No jobs found matching “{query}”.</p>
            {:else}
                {#each filteredJobs as item}
                    <JobCard
                        title={item.job_title}
                        company={item.company_name}
                        apply_url={item.apply_url}
                    >
                        {item.content}
                    </JobCard>
                {/each}
            {/if}
        </div>
    </div>
{/if}

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
