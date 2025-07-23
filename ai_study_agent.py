import asyncio
import platform
import re
from collections import defaultdict
import random

# Mock NLP functions (replace with actual NLP library like spaCy or transformers if available)
def summarize_text(text, max_sentences=5):
    """Summarize text into concise bullet points."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    key_points = sentences[:min(max_sentences, len(sentences))]
    return [f"- {point}" for point in key_points]

def generate_quiz(text, num_questions=3):
    """Generate simple multiple-choice quizzes from text."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    quiz = []
    for i in range(min(num_questions, len(sentences))):
        question = sentences[i]
        correct_answer = "True"
        wrong_answer = "False"
        quiz.append({
            "question": f"Is this statement true? {question}",
            "options": [correct_answer, wrong_answer],
            "correct": correct_answer
        })
    return quiz

# Main AI Agent Workflow
class StudyAgent:
    def __init__(self):
        self.notes = defaultdict(list)
        self.quizzes = defaultdict(list)

    def process_lecture(self, lecture_id, content):
        """Process a lecture to generate notes and quiz."""
        # Generate summary notes
        summary = summarize_text(content)
        self.notes[lecture_id] = summary

        # Generate quiz
        quiz = generate_quiz(content)
        self.quizzes[lecture_id] = quiz

    def get_notes(self, lecture_id):
        """Retrieve notes for a lecture."""
        return self.notes.get(lecture_id, ["No notes available."])

    def get_quiz(self, lecture_id):
        """Retrieve quiz for a lecture."""
        return self.quizzes.get(lecture_id, ["No quiz available."])

# HTML output for displaying results
def format_output(lecture_id, notes, quiz):
    """Format notes and quiz as HTML for display."""
    html = f"<h2>Lecture {lecture_id} Summary</h2><ul>"
    for note in notes:
        html += f"<li>{note}</li>"
    html += "</ul><h2>Quiz</h2><ol>"
    for q in quiz:
        html += f"<li>{q['question']}<br>"
        for opt in q['options']:
            html += f"<input type='radio' name='q{q['question'][:10]}' value='{opt}'> {opt}<br>"
        html += f"<p>Correct Answer: {q['correct']}</p></li>"
    html += "</ol>"
    return html

# Example usage
async def main():
    agent = StudyAgent()
    
    # Sample lecture content (replace with user-provided content)
    sample_lecture = """
    Introduction to Programming. Programming involves writing code. Python is a popular language. 
    It is used for web development. Variables store data. Loops repeat tasks.
    """
    lecture_id = "IT101_Lecture1"
    
    # Process lecture
    agent.process_lecture(lecture_id, sample_lecture)
    
    # Get results
    notes = agent.get_notes(lecture_id)
    quiz = agent.get_quiz(lecture_id)
    
    # Display results (in a real app, this would update a web interface)
    output = format_output(lecture_id, notes, quiz)
    print(output)  # For Pyodide, this could be redirected to a DOM element

# Run the agent
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())