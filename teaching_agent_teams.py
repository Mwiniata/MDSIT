import streamlit as st
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools
import os
import datetime

# Set page configuration
st.set_page_config(page_title="👨‍🏫 AI Teaching Agent Team", layout="centered")

# Initialize session state for API keys and topic
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = ''
if 'serpapi_api_key' not in st.session_state:
    st.session_state['serpapi_api_key'] = ''
if 'topic' not in st.session_state:
    st.session_state['topic'] = ''

# Function to create local documents (temporary solution)
def create_local_document(agent_name, topic, content):
    """Create local markdown file with agent response"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.replace(' ', '_').replace('/', '_')
    filename = f"{agent_name}_{safe_topic}_{timestamp}.md"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {agent_name} Report - {topic}\n\n")
            f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(content)
        return filename
    except Exception as e:
        return f"Error creating file: {e}"

# Streamlit sidebar for API keys
with st.sidebar:
    st.title("API Keys Configuration")
    st.session_state['openai_api_key'] = st.text_input("Enter your OpenAI API Key", type="password").strip()
    st.session_state['serpapi_api_key'] = st.text_input("Enter your SerpAPI Key (optional)", type="password").strip()
    
    st.info("Note: Documents will be saved locally as markdown files until Google Docs integration is fixed.")

# Validate required API keys
if not st.session_state['openai_api_key']:
    st.error("Please enter your OpenAI API key in the sidebar.")
    st.stop()

# Set the OpenAI API key from session state
os.environ["OPENAI_API_KEY"] = st.session_state['openai_api_key']

# Create agents with ADHD-friendly instructions for your profile
professor_agent = Agent(
    name="Professor_Dr_Sarah_Mitchell",
    role="Knowledge Foundation Builder for ADHD Adult Learner", 
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
    tools=[],
    instructions=[
        """You are Dr. Sarah Mitchell, creating a knowledge base for a 30-year-old male IT student at Media Design School Auckland who has ADHD and has been away from computers for 12 years.

        STUDENT PROFILE:
        - Returning to tech after 12-year gap
        - ADHD - needs structure, frequent breaks, bite-sized information
        - Adult learner - values career relevance and practical applications
        - Currently studying: Data Structures & Algorithms, Cloud Computing, Data & Networking, Cybersecurity

        CREATE COMPREHENSIVE KNOWLEDGE BASE:
        1. Start with "Why this matters for your IT career in Auckland"
        2. Use simple, everyday language with analogies (cars, cooking, etc.)
        3. Break complex topics into small chunks (2-3 sentences max)
        4. Include frequent break suggestions
        5. Connect to real Auckland job opportunities and salaries
        6. Use ADHD-friendly formatting with lots of white space
        7. Include confidence-building statements throughout
        8. Relate to current semester subjects when possible

        Format with clear headers, bullet points, and visual breaks."""
    ],
    show_tool_calls=True,
    markdown=True,
)

academic_advisor_agent = Agent(
    name="Academic_Advisor_James_Chen",
    role="Learning Path Designer for Career Changer",
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
    tools=[],
    instructions=[
        """You are James Chen, academic advisor specializing in career transitions for ADHD learners.

        Create a learning roadmap that:
        1. Acknowledges the student is 30 and changing careers
        2. Provides realistic timelines with ADHD accommodations
        3. Breaks learning into 15-30 minute daily sessions
        4. Includes energy-based scheduling (high/medium/low energy tasks)
        5. Connects to Auckland job market and salary expectations
        6. Addresses age concerns positively
        7. Integrates with current semester subjects
        8. Includes milestone celebrations and progress tracking

        Format as a week-by-week plan with specific daily tasks."""
    ],
    show_tool_calls=True,
    markdown=True
)

# Only add SerpAPI if key is provided
research_tools = []
if st.session_state['serpapi_api_key']:
    research_tools.append(SerpApiTools(api_key=st.session_state['serpapi_api_key']))

research_librarian_agent = Agent(
    name="Research_Librarian_Maria_Rodriguez",
    role="ADHD-Friendly Resource Curator",
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
    tools=research_tools,
    instructions=[
        """You are Maria Rodriguez, expert librarian specializing in ADHD-friendly learning resources.

        Curate resources that:
        1. Are ADHD-friendly (short videos, interactive content, visual learning)
        2. Include time estimates for each resource
        3. Rate difficulty levels clearly
        4. Focus on Auckland/NZ job market relevance
        5. Provide multiple learning modalities (visual, hands-on, reading)
        6. Include both free and premium options
        7. Connect to current semester tools (AWS, Python, VS, NETCAD)
        8. Suggest optimal times to use each resource type

        If SerpAPI is available, search for current resources. Otherwise, recommend well-known platforms."""
    ],
    show_tool_calls=True,
    markdown=True,
)

teaching_assistant_agent = Agent(
    name="Teaching_Assistant_Alex_Kim",
    role="Practice Coordinator for Adult ADHD Learner",
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
    tools=research_tools,
    instructions=[
        """You are Alex Kim, teaching assistant specializing in hands-on learning for ADHD students.

        Create practice materials that:
        1. Start with 5-10 minute "quick wins" for immediate satisfaction
        2. Build to longer projects gradually
        3. Include step-by-step instructions with visual confirmations
        4. Provide troubleshooting for common mistakes
        5. Connect exercises to portfolio building
        6. Include real-world Auckland business scenarios
        7. Integrate with semester tools and subjects
        8. Offer multiple difficulty levels for different energy states
        9. Include achievement celebrations and progress tracking

        Focus on building confidence while developing hireable skills."""
    ],
    show_tool_calls=True,
    markdown=True,
)

# Streamlit main UI
st.title("👨‍🏫 AI Teaching Faculty Team for ADHD Learners")
st.markdown("**Specialized for Media Design School IT Student - Career Changer with ADHD**")

# Add info about the student profile
st.info("""
🎯 **Optimized for:** 30-year-old career changer with ADHD returning to tech after 12 years
📚 **Current Subjects:** Data Structures & Algorithms, Cloud Computing, Data & Networking, Cybersecurity
🛠️ **Tools:** NETCAD, AWS, Python, Visual Studio
🌏 **Focus:** Auckland job market and practical career outcomes
""")

# Query bar for topic input
st.session_state['topic'] = st.text_input(
    "Enter the topic you want to learn about:", 
    placeholder="e.g., Python basics, AWS fundamentals, Network security, etc."
)

# Start button
if st.button("🚀 Deploy Teaching Faculty", type="primary"):
    if not st.session_state['topic']:
        st.error("Please enter a topic.")
    else:
        st.success(f"Deploying AI Teaching Faculty for: **{st.session_state['topic']}**")
        
        # Store responses and filenames
        responses = {}
        filenames = {}
        
        # Generate responses with loading animations
        agents = [
            ("Professor", professor_agent, "📚 Creating Knowledge Foundation..."),
            ("Academic Advisor", academic_advisor_agent, "🗺️ Designing Learning Roadmap..."),
            ("Research Librarian", research_librarian_agent, "📖 Curating Learning Resources..."),
            ("Teaching Assistant", teaching_assistant_agent, "✍️ Creating Practice Materials...")
        ]
        
        for agent_name, agent, loading_text in agents:
            with st.spinner(loading_text):
                response: RunResponse = agent.run(
                    f"Topic: {st.session_state['topic']}. Remember this is for a 30-year-old ADHD student at Media Design School Auckland changing careers to IT.",
                    stream=False
                )
                responses[agent_name] = response
                
                # Create local document
                filename = create_local_document(
                    agent_name.replace(" ", "_"), 
                    st.session_state['topic'], 
                    response.content
                )
                filenames[agent_name] = filename
        
        # Display success message and file links
        st.success("✅ Complete Teaching Package Generated!")
        
        st.markdown("### 📄 Generated Documents:")
        for agent_name, filename in filenames.items():
            if not filename.startswith("Error"):
                st.markdown(f"- **{agent_name}**: `{filename}` 📥")
            else:
                st.error(f"- **{agent_name}**: {filename}")

        # Display responses in tabs for better organization
        tab1, tab2, tab3, tab4 = st.tabs(["🧠 Professor", "🗺️ Academic Advisor", "📚 Research Librarian", "✍️ Teaching Assistant"])
        
        with tab1:
            st.markdown("### Dr. Sarah Mitchell - Knowledge Foundation")
            st.markdown(responses["Professor"].content)
        
        with tab2:
            st.markdown("### James Chen - Learning Roadmap")
            st.markdown(responses["Academic Advisor"].content)
            
        with tab3:
            st.markdown("### Maria Rodriguez - Resource Library")
            st.markdown(responses["Research Librarian"].content)
            
        with tab4:
            st.markdown("### Alex Kim - Practice Materials")
            st.markdown(responses["Teaching Assistant"].content)

# Information about the agents
st.markdown("---")
st.markdown("### 👥 Your AI Teaching Faculty:")
st.markdown("""
- **🧠 Dr. Sarah Mitchell (Professor)**: Creates ADHD-friendly knowledge foundations with career connections
- **🗺️ James Chen (Academic Advisor)**: Designs realistic learning paths for career changers
- **📚 Maria Rodriguez (Research Librarian)**: Curates accessible resources for different learning styles  
- **✍️ Alex Kim (Teaching Assistant)**: Creates hands-on practice materials and portfolio projects

**All agents are specialized for ADHD learners and Auckland's IT job market!**
""")

st.markdown("### 🔧 Troubleshooting:")
st.markdown("""
- Documents are currently saved as local markdown files
- To enable Google Docs: Set up Composio authentication properly
- SerpAPI is optional - agents work without it
- All responses are also displayed in the interface above
""")
