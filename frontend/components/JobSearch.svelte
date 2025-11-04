<script>
    import { onMount } from 'svelte';
    import JobCard from './JobCard.svelte';

    let jobs = [];
    // let query = ""; // Commented out for now
    let error = null;
    let totalJobs = 0;
    let page = 0;
    let limit = 20;
    let hasPrev = false;
    let hasNext = false;
    let jobsCount = 0;

    async function loadJobs() {
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

            const offset = page * limit;
            // Fetch jobs and total jobs concurrently
            const [jobsResponse, totalResponse] = await Promise.all([
                fetch(`/jobs/?date=${helsinkiDate}&offset=${offset}&limit=${limit}`),
                fetch(`/jobs/total_jobs?date=${helsinkiDate}`)
            ]);

            if (!jobsResponse.ok || !totalResponse.ok) {
                throw new Error(`Fetch failed with status: ${jobsResponse.status} or ${totalResponse.status}`);
            }

            jobs = await jobsResponse.json();
            totalJobs = (await totalResponse.json()).count;
            hasPrev = page > 0;
            hasNext = (page + 1) * limit < totalJobs;
        } catch (err) {
            error = err.message;
            console.error('Fetch error details:', err);
        }
    }

    onMount(() => {
        loadJobs();
    });

    // Reactive: Re-fetch on page change
    $: page, loadJobs();

    $: jobsCount = totalJobs;

    function goToPrev() {
        if (hasPrev) {
            page--;
        }
    }

    function goToNext() {
        if (hasNext) {
            page++;
        }
    }
</script>


{#if error}
    <p>Error loading jobs: {error}</p>
{:else}
    <h1>{jobsCount} active job posts</h1>

    <div class="search-container">
        <!-- Search input commented out for now
        <input
            type="text"
            placeholder="Search job title..."
            bind:value={query}
            class="search-input"
        />
        -->

        <div class="job-list">
            {#if jobs.length === 0}
                <p>Loading jobs...</p>
            {:else}
                {#each jobs as item}
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

    <div class="pagination">
        <button disabled={!hasPrev} on:click={goToPrev}>Previous</button>
        <span>Page {page + 1} of {Math.ceil(totalJobs / limit)}</span>
        <button disabled={!hasNext} on:click={goToNext}>Next</button>
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
