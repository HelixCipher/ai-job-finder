# Job Search AI Agent System

A multi-agent system that automates job searching and career guidance using state-of-the-art language models and web scraping. The system leverages the CrewAI framework to coordinate multiple specialized agents, including a job searcher, skills developer, interview coach, and career advisor.

## Overview

This project automates the process of finding job openings and providing career guidance by:
- **Searching Job Listings:** Scrapes current job listings for a given role and location using an Apify actor.
- **Identifying Required Skills:** Highlights key skills required for each job opening.
- **Mock Interview Preparation:** Generates interview questions and strategies.
- **Career Advisory:** Offers guidance on resume building and professional development.

The system uses Groq's LLaMA model for natural language processing and LangChain tools for additional functionalities.

## Project Structure

```
job_search_ai_agent/
├── .env                 # Environment variables file (see below)
├── job_search_agent.py  # Main Python script with agents, tasks, and crew setup
├── requirements.txt     # List of Python dependencies
├── task_output.txt      # File where task outputs are logged
└── README.md            # This file
```





------------

## Prerequisites

- **Python 3.8+**
- **API Credentials:**
  - `GROQ_API_KEY`: Your API key for Groq's LLaMA model.
  - `APIFY_API_TOKEN`: Your API token for the Apify client.
  - `MISCERAS_INDEED_SCRAPER`: The identifier for the Apify actor used to scrape job listings.
- Required Python packages listed in `requirements.txt`.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/A-L-E-X-W/ai-job-finder-WIP-.git

   cd ai-job-finder-WIP-


2. Create and activate a virtual environment (recommended):

python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Set up your environment variables:

Create a .env file in the project root with the following content:

- GROQ_API_KEY=your_groq_api_key

- APIFY_API_TOKEN=your_apify_api_token

- MISCERAS_INDEED_SCRAPER=your_apify_actor_id


### Usage

Run the main script to kick off the job search and career guidance process:

python job_search_agent.py

When executed, the system will:

* Initialize Groq and Apify clients using your API keys.
* Define several agents with distinct roles:
* Job Searcher: Searches for job openings using the Apify job search tool.
* Skills Development Agent: Identifies and highlights key skills from the job listings.
* Interview Preparation Coach: Generates mock interview questions and strategies.
* Career Advisor: Provides resume building advice and overall career guidance.
* Set up tasks for each agent and coordinate their execution using a Crew with a hierarchical process.
* Log task outputs to task_output.txt.

### Code Highlights
#### JobSearchTools Class

* Purpose: Implements the search_jobs tool to scrape job listings.
* Input Schema: Accepts JSON with keys: role, location, num_results.
* Output: Returns formatted job listings with details such as title, company, location, and URL.

### GroqChatModel Class

* Purpose: Wraps Groq's chat completion API to generate responses from the LLaMA model.
* Usage: Used by agents for natural language responses and guidance.

### Agents & Tasks

* Job Searcher Agent: Executes a task to find job listings.
* Skills Development Agent: Analyzes listings to extract required skills.
* Interview Preparation Coach: Provides mock interview questions and preparatory advice.
* Career Advisor: Offers resume tips and career guidance.
* Task Callback: A callback function logs outputs to task_output.txt for later review.

### Crew Execution

* Crew Object: Orchestrates the sequential execution of tasks using the CrewAI framework.
* Process: Uses a hierarchical process to ensure tasks are executed in the correct order.

### Extending the System

* Add New Tools: Use the @tool decorator to integrate additional functionalities.
* Customize Agents: Adjust roles, goals, and backstories to suit new job search scenarios.
* Improve Logging: Enhance the callback function for better monitoring and debugging.

### Troubleshooting

    Environment Variables: Verify that your .env file is correctly set up with all required API keys.
    API Credentials: Ensure the keys for Groq and Apify are valid and have sufficient permissions.
    Logs: Check task_output.txt for detailed logs and error messages if tasks fail.

### Future Enhancements

* Integrate additional job search APIs to broaden the range of job listings.
* Implement parallel processing for faster task execution.
* Enhance personalization by tailoring career advice based on user profiles.

### License

This project is licensed under the MIT License.

### Contributing

Contributions are welcome! Please fork the repository, create a new branch for your changes, and open a pull request. For major changes, please open an issue first to discuss what you would like to change.

### Acknowledgments

* CrewAI Framework: For providing a robust agent-based architecture.
* Groq & Apify: For their APIs that enable natural language processing and job data scraping.
* LangChain Tools: For additional functionalities that enhance the agents' capabilities.

