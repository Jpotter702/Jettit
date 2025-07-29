---
title: Key Features
tags: [features, reddit, projects, github]

---

The [RedditHarbor](https://github.com/socius-org/RedditHarbor) repository is a toolkit for collecting and storing Reddit data in a structured way, aimed at researchers who require large-scale Reddit datasets for analysis.

### Key Features:

* **Streamlined Data Collection**: Uses Reddit’s API to gather posts, comments, and user profiles directly.
* **Privacy-Focused**: Supports anonymization by avoiding the collection of personally identifiable information (PII).
* **Custom Data Storage**: Allows storing collected data in your own secure database (e.g., Supabase).
* **Export Ready**: Easily export data to formats like CSV, JSON, or JSONL for integration with analytical tools.
* **Efficient Tracking**: Monitors Reddit activity over time with temporal metrics like upvote ratios and post scores.
* **Smart Updates**: Automatically adjusts data collection frequency based on dataset size and API efficiency.

### Installation:

```bash
pip install redditharbor
```

You’ll need Reddit API credentials and a Supabase account to store the data.

### Usage:

The tool provides functions to log in to Reddit and Supabase, then collect data from subreddits. You can tailor the collection to specific needs such as limiting post counts, filtering by popularity, or including user metadata.

Let me know if you'd like help setting it up, modifying the code, or analyzing the data it collects.
