import warnings
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool,ScrapeWebsiteTool
import os 
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings('ignore')

##Load the environment variables
api_key=os.environ['OPENAI_API_KEY']
model_name=os.environ["OPENAI_MODEL_NAME"]
serp_key=os.environ["SERPER_API_KEY"] 

#Intialize tools


def run_crew(citizen,visit_country):
    search_tool=SerperDevTool()
    scrape_tool=ScrapeWebsiteTool()

    # Agent 1: Researcher
    researcher = Agent(
        role="Visa agent researcher",
        goal="Make sure to find if citizen of {citizenship} requires a visa travel"
        "to {visiting_country} and come up with a step by step guide plan along with the documents required"
        "to apply the visa" ,
        Tools = [scrape_tool, search_tool],
        verbose=True,
        backstory=(
            "As a visa agent researcher, your prowess in "
            "navigating and extracting critical "
            "information for visa applications "
            "Your skills help pinpoint the necessary "
            "documents and the process required to apply"
            "toursit visa for {{visiting_country}}. "
            
            
        )
    )


    # Agent 2: Planner
    planner = Agent(
        role="Visa agent planner",
        goal="Create a plan to apply visa depending on finding of research agent" ,
        Tools = [scrape_tool, search_tool],
        verbose=True,
        backstory=(
            "With a knack for organization and foresight, you excel in"
            "crafting detailed step by step plan to apply visa for {{visiting_country}}"
            "Also provide information of the website where we need to apply the visa on"
        
            
        )
    )


    #Create Task 

    # Task for Researcher Agent: Extract Job Requirements
    visa_task = Task(
        description=(
            "Analyze whether the citizen of {{citizenship}} "
            "requires a visa to travel to {{visiting_country}}"
            "You can reply no visa required or visa required "
        
        ),
        expected_output=(
            "Whether the person requies a visa to travel to {{travel_country}}."
        
        ),
       
        agent=researcher,
        async_execution=False
    )


    planning_task = Task(
        description=(
            "Using the research_findings provided, create a  plan"
            "that outlines the steps necessary and documents required for applying visa"
            "for {{visiting_country}}."
        ),
        expected_output='A detailed plan based on research findings.',
        async_execution=False,
        agent=planner,
        inputs={'research_findings': '{visa_task_ouput}'}
    )


    crew = Crew(
        agents=[researcher,planner],
        tasks=[visa_task,planning_task]
      
    )

    return crew.kickoff(inputs={"visiting_country": visit_country, "citizenship": citizen})

                                  
                    
 





