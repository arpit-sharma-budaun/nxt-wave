import gradio as gr
import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Simple storage
users_db = {}
current_user = {"username": None, "logged_in": False}
guest_chat = []
current_session = {"saved": True}  # Track current session

# Simple chat function with loading state
def chat_with_ai(user_input, history):
    if not user_input.strip():
        return "", history, gr.update(visible=False)
    
    try:
        prompt = f"As a career advisor, answer: {user_input}"
        response = model.generate_content(prompt)
        response_text = response.text if hasattr(response, 'text') else str(response)
        # Add user message
        history.append({"role": "user", "content": user_input})
        # Add assistant response
        history.append({"role": "assistant", "content": response_text})
        
        # Mark session as unsaved
        current_session["saved"] = False
        
        return "", history, gr.update(visible=False)
    except Exception as e:
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": f"Error: {str(e)}"})
        return "", history, gr.update(visible=False)

def show_loading():
    return gr.update(visible=True)

def clear_chat():
    return [], "🗑️ Chat cleared!"

# Authentication functions
def signup(username, email, password, confirm_password):
    if not username or not email or not password:
        return "Please fill all fields"
    if password != confirm_password:
        return "Passwords don't match"
    if len(password) < 6:
        return "Password must be at least 6 characters"
    if username in users_db:
        return "Username already exists"
    
    users_db[username] = {
        "email": email,
        "password": password,
        "chats": []
    }
    return "Account created successfully! Please login."

def login(username, password):
    if not username or not password:
        return "Please enter username and password", "Guest Mode", gr.update(choices=[], value=None), gr.update(visible=False)
    
    if username not in users_db or users_db[username]["password"] != password:
        return "Invalid username or password", "Guest Mode", gr.update(choices=[], value=None), gr.update(visible=False)
    
    current_user["username"] = username
    current_user["logged_in"] = True
    
    # Load chat history for dropdown
    chat_list = get_chat_history_list()
    return f"Welcome back, {username}!", f"Logged in as: {username}", gr.update(choices=chat_list, value=None), gr.update(visible=True)

def logout():
    current_user["username"] = None
    current_user["logged_in"] = False
    return "Logged out successfully", "Guest Mode", gr.update(choices=[], value=None), gr.update(visible=False)

# Chat history functions
def save_current_chat(history):
    if not current_user["logged_in"]:
        return "Please login to save chats"
    if not history:
        return "No chat to save"
    if current_session["saved"]:
        return "Chat already saved"
    
    username = current_user["username"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create chat session with first user message as title
    title = "New Chat"
    for msg in history:
        if msg["role"] == "user":
            title = msg["content"][:30] + "..." if len(msg["content"]) > 30 else msg["content"]
            break
    
    chat_data = {
        "title": title,
        "timestamp": timestamp,
        "messages": history.copy()
    }
    
    if "chat_history" not in users_db[username]:
        users_db[username]["chat_history"] = []
    
    users_db[username]["chat_history"].append(chat_data)
    current_session["saved"] = True
    return "✅ Chat saved successfully!"

def get_chat_history_list():
    if not current_user["logged_in"]:
        return []
    
    username = current_user["username"]
    if "chat_history" not in users_db[username]:
        return []
    
    return [f"{chat['timestamp']} - {chat['title']}" for chat in users_db[username]["chat_history"]]

def load_chat_history(selected_chat):
    if not current_user["logged_in"]:
        return [], "Please login to load chats"
    if not selected_chat:
        return [], "Please select a chat to load"
    
    username = current_user["username"]
    if "chat_history" not in users_db[username]:
        return [], "No chat history found"
    
    # Find the selected chat
    for chat in users_db[username]["chat_history"]:
        chat_label = f"{chat['timestamp']} - {chat['title']}"
        if chat_label == selected_chat:
            return chat["messages"], "✅ Chat loaded successfully!"
    
    return [], "Chat not found"

def new_chat():
    current_session["saved"] = True
    return [], gr.update(value=None), "✅ New chat started!"

# Assessment function
def assess_career(q1, q2, q3, q4, q5):
    if not all([q1, q2, q3, q4, q5]):
        return "Please answer all questions"
    
    try:
        prompt = f"""Career assessment:
        1. Work environment: {q1}
        2. Work style: {q2}
        3. Task preference: {q3}
        4. Work-life balance: {q4}
        5. Routine preference: {q5}
        
        Suggest 3 career paths with explanations."""
        
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"Error: {str(e)}"

# Other functions
def analyze_skills(skills, role):
    if not skills or not role:
        return "Please fill both fields"
    try:
        prompt = f"Skills: {skills}, Target: {role}. Identify gaps and learning path."
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"Error: {str(e)}"

def resume_tips(job, level):
    if not job or not level:
        return "Please fill both fields"
    try:
        prompt = f"Resume tips for {job} at {level} level. Give 5 specific tips."
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"Error: {str(e)}"

def market_insights(field, location):
    if not field or not location:
        return "Please fill both fields"
    try:
        prompt = f"Job market insights for {field} in {location}. Include salary and trends."
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"Error: {str(e)}"

def learning_resources(skill, style):
    if not skill or not style:
        return "Please fill both fields"
    try:
        prompt = f"Learning resources for {skill} with {style} learning style."
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"Error: {str(e)}"

# Create interface
with gr.Blocks(title="🎯 AI Career Advisor") as demo:
    gr.Markdown("# 🎯 AI Career & Skills Advisor")
    gr.Markdown("*✨ Powered by Gemini - Your personal career guidance assistant*")
    
    # Auth section
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🔐 Authentication")
            with gr.Tabs():
                with gr.Tab("🔑 Login"):
                    login_user = gr.Textbox(label="👤 Username")
                    login_pass = gr.Textbox(label="🔒 Password", type="password")
                    login_btn = gr.Button("🚀 Login")
                    
                with gr.Tab("📝 Sign Up"):
                    signup_user = gr.Textbox(label="👤 Username")
                    signup_email = gr.Textbox(label="📧 Email")
                    signup_pass = gr.Textbox(label="🔒 Password", type="password")
                    signup_confirm = gr.Textbox(label="🔒 Confirm Password", type="password")
                    signup_btn = gr.Button("✨ Create Account")
            
            auth_msg = gr.Textbox(label="📢 Status", interactive=False)
            user_status = gr.Markdown("👤 **Guest Mode**")
            logout_btn = gr.Button("🚪 Logout", visible=False)
            
            # Chat History
            gr.Markdown("### 💬 Chat History")
            chat_history_dropdown = gr.Dropdown(label="📚 Previous Chats", choices=[], interactive=True)
            with gr.Row():
                load_chat_btn = gr.Button("📂 Load")
                new_chat_btn = gr.Button("➕ New")
        
        with gr.Column(scale=2):
            with gr.Tabs():
                # Chat Tab
                with gr.Tab("💬 AI Chat"):
                    chatbot = gr.Chatbot(label="🤖 Career Assistant", height=400)
                    with gr.Row():
                        msg = gr.Textbox(label="💭 Your Message", placeholder="Ask about careers, skills, or job market...", scale=4)
                        send_btn = gr.Button("📤 Send", scale=1)
                    loading = gr.HTML("⏳ Thinking...", visible=False)
                    with gr.Row():
                        clear_btn = gr.Button("🗑️ Clear Chat")
                        save_btn = gr.Button("💾 Save Chat")
                    save_msg = gr.Textbox(label="💾 Save Status", interactive=False)
                
                # Assessment Tab
                with gr.Tab("📋 Career Assessment"):
                    gr.Markdown("### 🎯 Discover Your Ideal Career Path")
                    q1 = gr.Radio(["Office", "Remote", "Hybrid", "Outdoors"], label="🏢 Preferred work environment?")
                    q2 = gr.Radio(["Team collaboration", "Independent work", "Leadership", "Mixed"], label="👥 Work style preference?")
                    q3 = gr.Radio(["Creative tasks", "Analytical tasks", "People-focused", "Technical tasks"], label="🎨 Task preference?")
                    q4 = gr.Radio(["High flexibility", "Standard hours", "Results-focused", "Structured schedule"], label="⚖️ Work-life balance priority?")
                    q5 = gr.Radio(["Varied daily tasks", "Consistent routine", "Project-based", "Mixed routine"], label="📅 Routine preference?")
                    assess_btn = gr.Button("🎯 Get Career Recommendations")
                    assessment_result = gr.Textbox(label="📊 Your Career Assessment", lines=10)
                
                # Skills Tab
                with gr.Tab("🎯 Skills Analysis"):
                    gr.Markdown("### 🔍 Identify Your Skills Gap")
                    current_skills = gr.Textbox(label="💪 Current Skills", placeholder="Python, SQL, Project Management...")
                    target_role = gr.Textbox(label="🎯 Target Role", placeholder="Data Scientist, Product Manager...")
                    skills_btn = gr.Button("🔍 Analyze Skills Gap")
                    skills_result = gr.Textbox(label="📈 Skills Analysis", lines=8)
                
                # Resume Tab
                with gr.Tab("📄 Resume Tips"):
                    gr.Markdown("### ✨ Enhance Your Resume")
                    job_role = gr.Textbox(label="💼 Job Role", placeholder="Software Engineer, Marketing Manager...")
                    experience_level = gr.Radio(["Entry Level", "Mid Level", "Senior Level"], label="📊 Experience Level")
                    resume_btn = gr.Button("📝 Get Resume Tips")
                    resume_result = gr.Textbox(label="💡 Resume Enhancement Tips", lines=8)
                
                # Market Tab
                with gr.Tab("📊 Market Insights"):
                    gr.Markdown("### 📈 Job Market Intelligence")
                    field = gr.Textbox(label="🏭 Industry/Field", placeholder="Technology, Healthcare, Finance...")
                    location = gr.Textbox(label="📍 Location", placeholder="San Francisco, New York, Remote...")
                    market_btn = gr.Button("📊 Get Market Insights")
                    market_result = gr.Textbox(label="📈 Market Analysis", lines=8)
                
                # Learning Tab
                with gr.Tab("📚 Learning Resources"):
                    gr.Markdown("### 🎓 Personalized Learning Path")
                    skill_to_learn = gr.Textbox(label="🎯 Skill to Learn", placeholder="Machine Learning, Digital Marketing...")
                    learning_style = gr.Radio(["Visual", "Hands-on", "Reading", "Video-based"], label="🧠 Learning Style")
                    learning_btn = gr.Button("📚 Find Resources")
                    learning_result = gr.Textbox(label="🎓 Learning Recommendations", lines=8)

    # Event handlers
    msg.submit(chat_with_ai, [msg, chatbot], [msg, chatbot, loading])
    send_btn.click(chat_with_ai, [msg, chatbot], [msg, chatbot, loading])
    msg.submit(show_loading, [], [loading])
    send_btn.click(show_loading, [], [loading])
    
    clear_btn.click(clear_chat, [], [chatbot, save_msg])
    save_btn.click(save_current_chat, [chatbot], [save_msg])
    
    # Auth events
    signup_btn.click(signup, [signup_user, signup_email, signup_pass, signup_confirm], [auth_msg])
    login_btn.click(login, [login_user, login_pass], [auth_msg, user_status, chat_history_dropdown, logout_btn])
    logout_btn.click(logout, [], [auth_msg, user_status, chat_history_dropdown, logout_btn])
    
    # Chat history events
    load_chat_btn.click(load_chat_history, [chat_history_dropdown], [chatbot, save_msg])
    new_chat_btn.click(new_chat, [], [chatbot, chat_history_dropdown, save_msg])
    
    # Tool events
    assess_btn.click(assess_career, [q1, q2, q3, q4, q5], [assessment_result])
    skills_btn.click(analyze_skills, [current_skills, target_role], [skills_result])
    resume_btn.click(resume_tips, [job_role, experience_level], [resume_result])
    market_btn.click(market_insights, [field, location], [market_result])
    learning_btn.click(learning_resources, [skill_to_learn, learning_style], [learning_result])

if __name__ == "__main__":
    demo.launch(share=True)