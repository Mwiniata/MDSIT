import streamlit as st
import openai
import datetime

# Set page configuration
st.set_page_config(page_title="👨‍🏫 AI Teaching Faculty Team", layout="centered")

# Initialize session state
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = ''
if 'topic' not in st.session_state:
    st.session_state['topic'] = ''

def call_openai_api(prompt, api_key):
    """Call OpenAI API with error handling"""
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI teaching assistant specialized for ADHD learners."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Agent prompts for ADHD learner at Media Design School
AGENT_PROMPTS = {
    "Professor": """You are Dr. Sarah Mitchell, creating a knowledge foundation for a 30-year-old male IT student at Media Design School Auckland who has ADHD and has been away from computers for 12 years.

TOPIC: {topic}

Create a comprehensive but ADHD-friendly knowledge base that includes:
1. 🎯 Why this matters for IT careers in Auckland (specific jobs and salaries)
2. ⚡ Simple explanation with everyday analogies
3. 📚 Core concepts in bite-sized chunks (2-3 sentences each)
4. 💻 Real applications at Auckland tech companies
5. 🔗 Connections to current semester subjects (Data Structures, Cloud Computing, Networking, Cybersecurity)
6. 🧠 Memory aids for ADHD learners

Use lots of white space, clear headers, and confidence-building language.""",

    "Academic_Advisor": """You are James Chen, academic advisor for career changers with ADHD at Media Design School.

TOPIC: {topic}

Create a realistic learning roadmap for a 30-year-old returning to tech:
1. 🎯 4-6 week timeline with ADHD accommodations
2. ⏰ Daily 20-30 minute study sessions
3. ⚡ Energy-based task scheduling
4. 💰 Auckland job market connections
5. 🏆 Milestone celebrations and progress tracking
6. 💪 Confidence building for career changers

Format as week-by-week plan with specific daily tasks.""",

    "Research_Librarian": """You are Maria Rodriguez, expert in ADHD-friendly learning resources.

TOPIC: {topic}

Curate learning resources that are:
1. 🎥 ADHD-friendly (visual, short, engaging)
2. 📖 Time-estimated for planning
3. ⭐ Difficulty-rated clearly
4. 🌏 Relevant to Auckland/NZ job market
5. 🛠️ Connected to semester tools (AWS, Python, NETCAD, VS)
6. 📱 Available in multiple formats

Include free resources, time estimates, and why each is good for ADHD learners.""",

    "Teaching_Assistant": """You are Alex Kim, specializing in hands-on ADHD learning.

TOPIC: {topic}

Create practice materials with:
1. 🏆 5-10 minute "quick wins" for immediate satisfaction
2. 📈 Progressive difficulty building
3. 📋 Step-by-step instructions with checkpoints
4. 💼 Portfolio-building opportunities
5. 🌏 Auckland business scenarios
6. 🔧 Integration with semester tools
7. 🎉 Achievement celebrations

Focus on confidence building and hireable skills for Auckland IT market."""
}

# Streamlit UI
st.title("👨‍🏫 AI Teaching Faculty Team")
st.markdown("**Specialized for ADHD Learners & Career Changers at Media Design School**")

# Sidebar for API key
with st.sidebar:
    st.title("🔑 Setup")
    st.session_state['openai_api_key'] = st.text_input("OpenAI API Key", type="password")
    st.info("Get your key from: https://platform.openai.com/api-keys")

if not st.session_state['openai_api_key']:
    st.error("Please enter your OpenAI API key in the sidebar.")
    st.stop()

# Student profile info
st.info("""
🎯 **Optimized for:** 30-year-old career changer with ADHD  
📚 **Subjects:** Data Structures, Cloud Computing, Networking, Cybersecurity  
🛠️ **Tools:** NETCAD, AWS, Python, Visual Studio  
🌏 **Focus:** Auckland job market and practical outcomes
""")

# Topic input
st.session_state['topic'] = st.text_input(
    "What do you want to learn?", 
    placeholder="e.g., Python fundamentals, AWS basics, Network security..."
)

# Generate button
if st.button("🚀 Deploy Your Teaching Faculty", type="primary"):
    if not st.session_state['topic']:
        st.error("Please enter a topic to learn about.")
    else:
        st.success(f"Deploying AI Faculty for: **{st.session_state['topic']}**")
        
        # Create tabs for responses
        tab1, tab2, tab3, tab4 = st.tabs(["🧠 Professor", "🗺️ Advisor", "📚 Librarian", "✍️ Assistant"])
        
        agents = [
            ("Professor", tab1, "📚 Creating knowledge foundation..."),
            ("Academic_Advisor", tab2, "🗺️ Designing learning roadmap..."),
            ("Research_Librarian", tab3, "📖 Curating resources..."),
            ("Teaching_Assistant", tab4, "✍️ Creating practice materials...")
        ]
        
        for agent_name, tab, loading_text in agents:
            with tab:
                with st.spinner(loading_text):
                    prompt = AGENT_PROMPTS[agent_name].format(topic=st.session_state['topic'])
                    response = call_openai_api(prompt, st.session_state['openai_api_key'])
                    
                    if not response.startswith("Error"):
                        st.markdown(response)
                        
                        # Download button for each response
                        filename = f"{agent_name}_{st.session_state['topic'].replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.md"
                        st.download_button(
                            label=f"📥 Download {agent_name.replace('_', ' ')} Report",
                            data=response,
                            file_name=filename,
                            mime="text/markdown"
                        )
                    else:
                        st.error(response)

# Footer
st.markdown("---")
st.markdown("### 👥 Your AI Teaching Faculty:")
st.markdown("""
- **🧠 Dr. Sarah Mitchell**: ADHD-friendly knowledge foundations
- **🗺️ James Chen**: Realistic learning paths for career changers  
- **📚 Maria Rodriguez**: Curated resources for different learning styles
- **✍️ Alex Kim**: Hands-on practice and portfolio projects

**All specialized for ADHD learners in Auckland's IT job market!**
""")
