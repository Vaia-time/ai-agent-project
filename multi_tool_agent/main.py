"""
Simple Example: Professional Research Agent Flow with Tavily Web Search

This is a simplified example showing how to use the ResearchAgent and AnswerAgent workflow
with Tavily web search capabilities.

Best Practice: Provide simple examples for easy adoption with clear async setup instructions.
"""

import os
import asyncio
from base_researcher import BaseResearchFlow
from early_life_prompts import refiner_instructions, reviewer_instructions, answer_instructions, researcher_instructions
from dotenv import load_dotenv

load_dotenv()

async def simple_research_example_async():
    """
    A simple async example demonstrating the research workflow with web search.
    
    Best Practice: Proper async execution following Google ADK patterns with error handling.
    """
    # Check for API key first - Best Practice: Fail fast with helpful error messages
    if not os.getenv("TAVILY_API_KEY"):
        print("❌ Error: TAVILY_API_KEY environment variable not set")
        print("\n💡 To run this example:")
        print("1. Get a Tavily API key from https://tavily.com")
        print("2. Set the environment variable:")
        print("   export TAVILY_API_KEY='your-api-key-here'")
        print("3. Or create a .env file with: TAVILY_API_KEY=your-api-key-here")
        return
    
    try:
        # Initialize the research flow
        print("🚀 Initializing Professional Research Agent with Web Search...")
        research_flow = BaseResearchFlow(
            researcher_instructions=researcher_instructions,
            reviewer_instructions=reviewer_instructions,
            refiner_instructions=refiner_instructions,
            answer_instructions=answer_instructions,
            app_name="test_app_name",
            user_id="test_user_id",
        )
        await research_flow.initialize_async()  # Complete async initialization
        
        # Example person to research
        person_name = "Keir Starmer"  # You can change this to any person's name
        
        print(f"\n🔍 Researching professional information for: {person_name}")
        print("=" * 60)
        print("Using Tavily web search for comprehensive, up-to-date information...")
        
        # Execute the research workflow (now async)
        summary = await research_flow.research_person(person_name)
        
        if summary:
            print("\n🎯 Final Professional Career Summary:")
            print("-" * 40)
            print(summary)
            
            # Show review process information for transparency
            review_status = research_flow.get_review_status()
            review_feedback = research_flow.get_review_feedback()
            
            if review_status and review_feedback:
                print(f"\n📋 Quality Review Status: {review_status}")
                print("📝 Review Process Details:")
                print("-" * 35)
                print(review_feedback)
            
            # Show the raw research data for transparency
            research_data = research_flow.get_research_data()
            if research_data:
                print("\n📊 Detailed Research Data (from Web Sources):")
                print("-" * 45)
                # Truncate if too long for readability
                truncated_data = research_data[:1500] + "..." if len(research_data) > 1500 else research_data
                print(truncated_data)
                
            print("\n✅ Iterative research and review process completed successfully!")
        else:
            print("❌ Could not generate professional summary.")
            
    except ValueError as e:
        if "TAVILY_API_KEY" in str(e):
            print(f"❌ Configuration Error: {e}")
            print("\n💡 Make sure your TAVILY_API_KEY is valid and properly set.")
        else:
            print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Please check your internet connection and API key.")

def simple_research_example():
    """
    Wrapper function that handles async execution.
    
    Best Practice: Use asyncio.run() for proper async execution in scripts
    """
    asyncio.run(simple_research_example_async())

if __name__ == "__main__":
    simple_research_example() 