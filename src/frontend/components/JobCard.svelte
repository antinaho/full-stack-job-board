<script>
  export let title;
  export let company;
  export let apply_url;
</script>

<div class="job-card">
  <h3><a href={apply_url}>{title}</a></h3>
  <h5>{company}</h5>
</div>

<style>
  .job-card {
    background-color: #1e1e1e;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
  }

  .job-card:hover {
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 6px 20px rgba(0, 150, 255, 0.3);
    transform: translateY(-3px);
  }

  h3 {
    margin: 0 0 0.4rem;
    font-weight: 700;
    font-size: 1.15rem;
  }

  h3 a {
    color: #e6f0ff;
    text-decoration: none;
    transition: color 0.3s ease;
  }

  h3 a:hover {
    color: #79c0ff;
  }

  h5 {
    margin: 0;
    font-weight: 400;
    color: #b0b0b0;
    font-size: 0.95rem;
  }
</style>
