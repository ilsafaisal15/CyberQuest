import gradio as gr
import random
import os
from groq import Groq

# 🔐 Set your Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)
GROQ_MODEL = "llama3-8b-8192"

# 🧠 AI Mentor Function
def mentor_bot(user_choice, current_threat):
    prompt = f"""
    You are a cybersecurity expert mentor helping students understand and handle security threats.

    Threat Log:
    {current_threat}

    Student Action:
    {user_choice}

    Analyze if the student's action is correct, explain why or why not, and teach them how to handle such situations.
    """
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful cybersecurity tutor."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# 📂 Threat Log Samples
security_logs = [
    "Multiple failed login attempts from IP 192.168.1.5",
    "Unusual outbound traffic detected on port 4444",
    "Employee downloaded a large number of files at midnight",
    "Antivirus alert: Trojan detected in email attachment",
    "Access to restricted server from unknown device",
    "High number of requests to login endpoint from a single IP",
    "Sudden installation of unknown software on user machine",
    "Suspicious DNS queries to known malicious domains",
]

# 🎯 Suggested Actions
actions = [
    "Block the IP address",
    "Quarantine the affected system",
    "Notify the IT administrator",
    "Reset all passwords",
    "Perform a full system scan",
    "Ignore the threat",
    "Check user access logs",
    "Update antivirus definitions"
]

# 🔁 State
current_threat = ""
mentor_response = ""
hint_message = ""

# 🚀 Generate Threat
def generate_threat():
    global current_threat, mentor_response, hint_message
    current_threat = random.choice(security_logs)
    mentor_response = ""
    hint_message = ""
    return current_threat, gr.update(visible=True), gr.update(choices=actions, value=None), "", ""

# ✅ Submit Action
def handle_action(user_choice):
    global mentor_response
    if not current_threat:
        return "No threat generated. Please click 'Generate Threat' first.", ""
    mentor_response = mentor_bot(user_choice, current_threat)
    return user_choice, mentor_response

# 💡 Hint Generator
hints = {
    "login attempts": "Consider blocking the IP if brute force is suspected.",
    "outbound traffic": "Could indicate data exfiltration or malware activity.",
    "downloaded files": "Watch for insider threats or compromised credentials.",
    "Trojan": "Quarantine and remove the file immediately.",
    "restricted server": "Check user access and device authorization.",
    "login endpoint": "Rate limit or block abusive IP addresses.",
    "unknown software": "May indicate malware. Perform a full scan.",
    "DNS queries": "Could be C2 activity. Monitor and block malicious domains."
}

def get_hint():
    global current_threat
    for key in hints:
        if key.lower() in current_threat.lower():
            return hints[key]
    return "Try analyzing the log carefully — look for anomalies."

# 🎨 Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""# 🛡️ HackDefender - Cybersecurity AI Game
### Learn cybersecurity by defending against real-world threats!""")

    threat_display = gr.Textbox(label="🔐 Threat Log", interactive=False)
    generate_btn = gr.Button("🔄 Generate Threat")

    with gr.Row():
        action_radio = gr.Radio(label="⚔️ Your Action", choices=[], interactive=True)
        submit_btn = gr.Button("✅ Submit Action")

    with gr.Accordion("💡 Need a Hint?", open=False):
        hint_output = gr.Textbox(label="Hint", interactive=False)
        hint_btn = gr.Button("Get Hint")

    choice_display = gr.Textbox(label="📌 Your Choice", interactive=False)
    mentor_output = gr.Textbox(label="🧠 AI Mentor Explanation", interactive=False, lines=5)

    # Actions
    generate_btn.click(generate_threat, outputs=[threat_display, action_radio, action_radio, choice_display, mentor_output])
    submit_btn.click(handle_action, inputs=action_radio, outputs=[choice_display, mentor_output])
    hint_btn.click(lambda: get_hint(), outputs=hint_output)

# 🧪 Launch App
demo.launch(debug=True)
