from crewai import Agent, Task, Crew, Process
from crewai.tasks.task_output import TaskOutput
import json, requests, os
from groq import Groq
from langchain.tools import tool
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

# Define your LLaMA model
LLAMA_MODEL_NAME = "Groq Llama3.1 70b"

# Initialize ApifyClient
apify_client = ApifyClient(os.environ.get("APIFY_API_TOKEN"))


misceres_indeed_scraper = (os.environ.get("MISCERAS_INDEED_SCRAPER"))




import traceback





# AGENTS
#----------------------------------------------------------------

class JobSearchTools:
    @tool("Job Search Tool")
    def search_jobs(input_json: str) -> str:
        """Search for jobs listings using the job-api client of your choice ADD A JOB API TO THIS"""
        # Parse input JSON string
        try:
            input_data = json.loads(input_json)
            role = input_data["role"]
            location = input_data["location"]
            num_results = input_data["num_results"]
        except (json.JSONDecodeError, KeyError) as e:
            error_msg = f"JSON Parsing Error: {e}"
            print(f"Error: {error_msg}")
            return """The tool accepts input in JSON format with the following schema: {'role': '<role>', 'location': '<location>', 'num_results': <num_results>} Ensure to format the input accordingly."""

        # Prepare input for the Apify Actor
        run_input = {
            "position": role,
            "location": location,
            "maxItems": num_results,
            "parseCompanyDetails": False,
            "saveOnlyUniqueItems": True,
        }

        try:
            run = apify_client.actor(misceres_indeed_scraper).call(run_input=run_input)
            print(f"Apify response: {run}")
            dataset_id = run.get("defaultDatasetId", None)
            if not dataset_id:
                print("Error: Dataset ID is None")
                return "No valid data returned from Apify"
            # Continue processing dataset
        except Exception as e:
            print(f"Error while calling Apify: {e}")
            print(f"Full traceback: {traceback.format_exc()}")

        try:
            # Run the Apify Actor and fetch results
            run = apify_client.actor(misceres_indeed_scraper).call(run_input=run_input)
            dataset_id = run["defaultDatasetId"]
            results = []
            for item in apify_client.dataset(dataset_id).iterate_items():
                results.append(
                    f"Title: {item['title']}\n"
                    f"Company: {item.get('company', 'N/A')}\n"
                    f"Location: {item['location']}\n"
                    f"URL: {item['url']}\n"
                )
            return "\n\n".join(results)
        except Exception as e:
            error_msg = f"Error while running Apify actor or processing results: {str(e)}"
            print(f"Error: {error_msg}")
            return f"An error occurred while searching for jobs. Error details: {error_msg}\nFull Exception Trace: {traceback.format_exc()}"
            return f"An error occurred while searching for jobs: {e}"
        
def log_apify_input_and_result(run_input):
    print(f"Calling Apify with input: {run_input}")
    try:
        run = apify_client.actor(misceres_indeed_scraper).call(run_input=run_input)
        print(f"Apify response: {run}")
        return run
    except Exception as e:
        print(f"Error while calling Apify: {e}")
        print(f"Full traceback: {traceback.format_exc()}")
        


class GroqChatModel:
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name
        

    def generate_response(self, system_prompt, user_input):
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        return completion.choices[0].message.content

llm = GroqChatModel(client, LLAMA_MODEL_NAME)



        
def callback_function(output: TaskOutput):
    try:
        with open("task_output.txt", "a") as file:
            file.write(f"{output.result}\n\n")
        print("Results saved to task_output.txt")
    except Exception as e:
        print(f"Error in callback function: {e}")
        print(f"Full traceback: {traceback.format_exc()}")



# this agent is going to search for job listings and provide the details of those jobs
job_searcher_agent = Agent(
    role="Job Searcher",
    goal='Search for jobs in the field of interest, focusing on enhancing relevant skills and knowledge.',
    backstory="""You are actively searching for job opportunities that cater to my specific skill set and interests.""",
    verbose=True,
    llm=llm,
    allow_delegation=True,
    tools=[JobSearchTools().search_jobs]
)


# this agent is going through every single job we identified by the job_searcher_agent and list all the required skills then it provides guidence and advices on how to achieve those skills.
skills_development_agent = Agent(
    role="Skills Development Agent",
    goal='Provide advice on enhancing skills and knowledge in a particular field.',
    backstory="""You are an expert in your field, ready to provide guidance and advice on enhancing my skills and knowledge.""",
    verbose=True,
    llm=llm,
    allow_delegation=True
)

# this agent is going to identify the list of possible questions that can be asked and list all those questions
interview_preparation_coach = Agent(
    role="Interview Preparation Coach",
    goal='Prepare job searchers for interviews by conducting mock interviews and providing advice on effective questions and strategies.',
    backstory="""Expert in coaching job searchers on successful interview techniques, providing mock interviews and advice on effective questions and strategies.""",
    verbose=True,
    llm=llm,
    allow_delegation=True
)

# This agent will go through all the job listings and will give you guidance on how your resume should look like and how to write it.
career_advisor = Agent(
    role="Career Advisor",
    goal='Provide career advice and guidance, including resume building and professional development.',
    backstory="""As a career advisor, you provide comprehensive guidance on career development, resume building, and professional development.""",
    verbose=True,
    llm=llm,
    allow_delegation=True
)




# TASK
# -----------------------------------------------------------

#job_title = ["Data scientist", "Software engineer", "Data analyst", "Data engineer", "System developer"]
job_title = "Data scientist"
city = "Stockholm"
number_of_positions = 5


job_title = job_title or "Default Job Title"
city = city or "Default City"
number_of_positions = number_of_positions or 5

print(f"Job title: {job_title}, City: {city}, Number of positions: {number_of_positions}")

# Before calling the job_search_task, log the input and the result
def log_job_search_input_and_result(job_search_task):
    print(f"Input for job search task: {job_search_task.description}")
    result = job_search_task.run()
    print(f"Result from job search task: {result}")
    return result


# Define tasks for your agents




# it is going to search for current job openings for the provided job titles in the specified city using the Job Search tool 
job_search_task = Task(
    description=f"""Search for current job openings for the {job_title} in the city of {city} using the Job Search tool. Find {number_of_positions} vacant positions in total.
    Emphasize the key skills required.
    Find the salary, hybrid work or remote work or in person work and other details if possible.
    The tool accepts input in JSON format with the following schema: {'role': '<role>', 'location': '<location>', 'num_results': '<num_results>'} Ensure to format the input accordingly.""",
    agent=job_searcher_agent,
    tools=[JobSearchTools().search_jobs],
    callback=callback_function # the callback function is added at each step so that the output is stored in a file
)

job_search_task_result = log_job_search_input_and_result(job_search_task)


# it is going to help the job searcher identify the required skills for each of the {number_of_positions} job openings
skills_higlighting_task = Task(
    description=f"""For each of the {number_of_positions} job openings found, identify the required skills and highlight them in the resume.
    The tool accepts input in JSON format with the following schema: {'job_listings': '<list of job listings>'} Ensure to format the input accordingly.""",
    agent=skills_development_agent,
    context=[job_search_task],
    tools=[tool.HTMLParser(), tool.SkillIdentifier()],
    callback=callback_function
)


def generate_mock_questions(job_title):
    response = client.chat.completions.create(
        model=LLAMA_MODEL_NAME,
        messages=[
            {"role": "system", "content": f"Generate mock interview questions for the role of {job_title}."},
            {"role": "user", "content": f"What should I expect in a technical interview for a {job_title} role?"}
        ]
    )
    return response.choices[0].message.content

# it is going to help the job searcher prepare for the mock interviews for each of the {number_of_positions} job openings
interview_preparation_task = Task(
    description=f"""For each of the {number_of_positions} job openings found, prepare the job searcher for mock interviews. Conduct mock interviews and provide advice on effective questions and strategies.
    The tool accepts input in JSON format with the following schema: {'job_listings': '<list of job listings>'} Ensure to format the input accordingly.""",
    agent=interview_preparation_coach,
    context=[job_search_task],
    tools=[tool.MockInterviewer(), tool.QuestionGenerator()],
    callback=callback_function
)

# it is going to help the job searcher create a professional resume for each of the {number_of_positions} job openings
career_advisor_task = Task(
    description=f"""For each of the {number_of_positions} job openings found, provide career advice and guidance.
    The tool accepts input in JSON format with the following schema: {'job_listings': '<list of job listings>'} Ensure to format the input accordingly.""",
    agent=career_advisor,
    context=[job_search_task],
    tools=[tool.CareerAdvisor(), tool.ResumeBuilder()],
    callback=callback_function
)





# CREW
# ----------------------------------------------------------------

# Set up your crew with a sequential process (tasks executed sequentially by default)
job_search_crew = Crew(
    agent=[job_searcher_agent, skills_development_agent, interview_preparation_coach, career_advisor],
    tasks=[job_search_task, skills_higlighting_task, interview_preparation_task, career_advisor_task],
    process=Process.hierarchical,
    manager_llm=llm
)

try:
    crew_result = job_search_crew.kickoff()
    print(crew_result)
except Exception as e:
    print(f"Error during crew execution: {e}")
    print(f"Full traceback: {traceback.format_exc()}")
