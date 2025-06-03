
import os
import logging
from typing import Optional
import uuid
from dotenv import load_dotenv

from google.adk.agents import Agent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.langchain_tool import LangchainTool
from google.genai import types
from langchain_community.tools import TavilySearchResults

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")

class BaseResearchFlow:  
    def __init__(self, model_name: str = MODEL_NAME, researcher_instructions: str = None, reviewer_instructions: str = None, refiner_instructions: str = None, answer_instructions: str = None, app_name: str = None, user_id: str = None):
        """
        Initialize the research flow with proper agent setup and Tavily integration.
        
        Args:
            model_name: The LLM model to use for both agents
            
        Raises:
            ValueError: If TAVILY_API_KEY is not set in environment
        """
        self.model_name = model_name
        self.session_service = InMemorySessionService()
        self.session = None
        self.runner = None
        self.session_id = str(uuid.uuid4())
        self.app_name = app_name
        self.user_id = user_id
        self.researcher_instructions = researcher_instructions
        self.answer_instructions = answer_instructions
        self.reviewer_instructions = reviewer_instructions
        self.refiner_instructions = refiner_instructions
        self._setup_tools()
        self._setup_agents()
    
    def _setup_tools(self):
        """
        Setup Tavily search tool, using LangchainTool wrapper for third-party tool integration
        """
        try:
            tavily_search = TavilySearchResults(
                max_results=10,
                search_depth="advanced",
                include_answer=False,
                include_raw_content=True,
                include_images=False,
            )
            
            self.tavily_tool = LangchainTool(tool=tavily_search)
            
        except Exception as e:
            logger.error(f"Failed to initialize Tavily search tool: {e}")
            raise
    
    def _setup_agents(self):
        """
        Setup individual agents with clear responsibilities and proper state management.
        
        Best Practices:
        - Using proper Google ADK multi-agent patterns
        - Implementing Review/Critique Pattern (Generator-Critic) from ADK docs
        - Single responsibility principle for each agent
        - Clear instructions and descriptions with output_key
        - Tool integration for enhanced capabilities
        """
        
        self.research_agent = Agent(
            name="ResearchAgent",
            model=self.model_name,
            instruction=self.researcher_instructions,
            tools=[self.tavily_tool],
            output_key="research_data"
        )
        
        # AnswerAgent - Responsible for creating professional summaries
        self.answer_agent = Agent(
            name="AnswerAgent",
            model=self.model_name,
            instruction=self.answer_instructions,
            output_key="answer_summary"
        )
        
        # ReviewerAgent - Evaluates answer quality and identifies missing information
        # Following Google ADK Review/Critique Pattern (Generator-Critic)
        self.reviewer_agent = Agent(
            name="ReviewerAgent",
            model=self.model_name,
            instruction=self.reviewer_instructions,
            output_key="review_result"
        )
        
        
        # Refiner Agent - Handles additional research or summary updates based on review
        self.refiner_agent = Agent(
            name="RefinerAgent",
            model=self.model_name,
            instruction=self.refiner_instructions,
            output_key="refinement_action"
        )
        
        # Base Research and Summary workflow using SequentialAgent
        self.base_workflow = SequentialAgent(
            name="BaseResearchWorkflow",
            sub_agents=[self.research_agent, self.answer_agent]
        )
        
        # For now, let's use a simpler SequentialAgent approach instead of LoopAgent
        # to ensure compatibility while we debug the multi-agent patterns
        self.workflow_agent = SequentialAgent(
            name="IterativeResearchWorkflow",  
            sub_agents=[self.base_workflow, self.reviewer_agent]
        )
    
    async def initialize_async(self):
        """
        Complete the async initialization of session and runner.
        
        Best Practice: Separate async initialization from __init__
        """
        await self._setup_session_and_runner()

    async def _setup_session_and_runner(self):
        """
        Setup session and runner with proper error handling.
        
        Best Practice: Proper async session management and error handling
        """
        try:
            self.session = await self.session_service.create_session(
                app_name=self.app_name, 
                user_id=self.user_id, 
                session_id=self.session_id
            )
            self.runner = Runner(
                agent=self.workflow_agent, 
                app_name=self.app_name, 
                session_service=self.session_service
            )
            logger.info("Session and runner initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize session and runner: {e}")
            raise
    
    async def research_person(self, person_name: str) -> Optional[str]:
        """
        Execute the complete iterative research workflow with quality review and refinement.
        
        Args:
            person_name: The name of the person to research
            
        Returns:
            Professional summary of the person or None if error occurs
            
        Best Practice: Uses Google ADK multi-agent patterns (SequentialAgent + LoopAgent)
        """
        if not person_name or not person_name.strip():
            logger.error("Person name cannot be empty")
            return None
        
        try:
            # Initialize session state
            self.session.state['person_name'] = person_name.strip()
            logger.info(f"Starting iterative research workflow for: {person_name}")
            
            # Create user message to trigger the workflow
            content = types.Content(
                role='user', 
                parts=[types.Part(text=f"Research and create an early life biography section summary for {person_name}")]
            )
            
            # Execute the complete workflow using Google ADK patterns
            print(f"🔍 Starting comprehensive research and review workflow for {person_name}...")
            
            final_response = None
            async for event in self.runner.run_async(
                user_id=self.user_id, 
                session_id=self.session_id, 
                new_message=content
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        final_response = event.content.parts[0].text
                        logger.info("Iterative research workflow completed successfully")
                        break
            
            answer_summary = self.session.state.get('answer_summary')
            if answer_summary:
                return answer_summary
            elif final_response:
                return final_response
            else:
                logger.warning("No final summary available after workflow completion")
                return None
                
        except Exception as e:
            logger.error(f"Error during iterative research workflow: {e}")
            return None
    
    def get_research_data(self) -> Optional[str]:
        """
        Get the raw research data from the last workflow execution.
        
        Provide access to intermediate results for debugging
        """
        return self.session.state.get('research_data') if self.session else None
    
    def get_review_feedback(self) -> Optional[str]:
        """
        Get the reviewer feedback from the last workflow execution.
        
        Provide transparency into the review process
        """
        review_result = self.session.state.get('review_result') if self.session else None
        if review_result:
            if "APPROVED:" in review_result:
                return review_result.replace("APPROVED:", "").strip()
            elif "NEEDS_IMPROVEMENT:" in review_result:
                parts = review_result.split("|")
                return parts[0].replace("NEEDS_IMPROVEMENT:", "").strip()
        return None
    
    def get_review_status(self) -> Optional[str]:
        """
        Get the final review status from the last workflow execution.
        """
        review_result = self.session.state.get('review_result') if self.session else None
        if review_result:
            if review_result.startswith("APPROVED:"):
                return "APPROVED"
            elif review_result.startswith("NEEDS_IMPROVEMENT:"):
                return "NEEDS_IMPROVEMENT"
        return None