import os
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw

# --------------------------------------------------------------------------
NAME = "Shin Limchiu"                    
SECTION = "CSIT 349 - G01"       
PROGRAM = "BS Information Technology, 4th Year" 
TAGLINE = "Aspiring AI engineer who loves building useful things."  
EMAIL = "limchiu200272@gmail.com"              
PHOTO_PATH = "1.jpg"              # put your photo next to app.py

st.set_page_config(
    page_title=f"{NAME} | Portfolio",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------------------------------
SKILLS = pd.DataFrame(
    {
        "Skill": ["Python", "SQL", "Streamlit", "Machine Learning", "HTML/CSS", "Git", "Communication"],
        "Category": ["Programming", "Data", "Programming", "AI", "Web", "Tools", "Soft Skills"],
        "Level": [80, 65, 60, 55, 50, 70, 75],   # 0-100, your honest self-rating
        "Years": [3, 2, 1, 1, 2, 2, 4],
    }
)


PROJECTS = [
    {
        "title": "Student Information Management System",
        "role": "Full-Stack Developer",
        "tools": ["Java", "Spring Boot", "MySQL", "VS Code"],
        "outcome": "Developed a system that manages student information and records, including adding, viewing, updating, and deleting data.",
        "link": "",
    },
    {
        "title": "Dormitory Management System",
        "role": "Backend Developer",
        "tools": ["PHP", "MySQL", "HTML", "CSS"],
        "outcome": "Created a web-based system for managing dormitory rooms, tenant information, and occupancy records.",
        "link": "",
    },
    {
        "title": "Hangman Game",
        "role": "C++ Programmer",
        "tools": ["C++", "Data Structures", "VS Code", "Git"],
        "outcome": "Developed a console-based word guessing game using stacks and linked lists to apply data structures and programming concepts.",
        "link": "",
    },
]


MILESTONES = pd.DataFrame(
    {
        "Year": [2002, 2008, 2008, 2024],           
        "Milestone": [
            "Born in Cebu City, Philippines",
            "Started high school in University of San Carlos",
            "Entered university last 2008 in University of San Carlos",
            "Built my first AI project last 2024",
        ],
    }
)

# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "likes" not in st.session_state:
    st.session_state.likes = 0


def profile_image():
    """Use your photo if present, otherwise a clearly labeled stand-in."""
    if os.path.exists(PHOTO_PATH):
        return Image.open(PHOTO_PATH)
    img = Image.new("RGB", (400, 400), "#C7D2FE")
    d = ImageDraw.Draw(img)
    d.ellipse((140, 70, 260, 190), fill="#4F46E5")
    d.ellipse((90, 210, 310, 420), fill="#4F46E5")
    d.text((120, 370), "PLACEHOLDER PHOTO", fill="white")
    return img


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.image(profile_image(), width="stretch")
    st.header(NAME)
    st.caption(f"{PROGRAM}\n\n{SECTION}")
    st.divider()

    st.subheader("Page settings")
    show_balloons = st.checkbox("Celebrate when I send a message", value=True)
    st.markdown(f"📧 {EMAIL}")

    if st.button("👍 Like this site"):
        st.session_state.likes += 1
        st.toast("Thanks for the like!")
    st.write(f"Likes: **{st.session_state.likes}**")

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.title(f"👋 Hi, I'm {NAME}")
st.markdown(f"##### {TAGLINE}")
st.caption(f"{PROGRAM} · {SECTION}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Projects", len(PROJECTS))
m2.metric("Skills tracked", len(SKILLS))
m3.metric("Years coding", int(SKILLS["Years"].max()), delta="+1 this year")
m4.metric("Site likes", st.session_state.likes)

tab_about, tab_skills, tab_projects, tab_contact = st.tabs(
    ["🙋 About & Story", "📊 Skills", "🛠 Projects", "✉️ Contact"]
)

# --------------------------------------------------------------------------
# About & Autobiography
# --------------------------------------------------------------------------
with tab_about:
    left, right = st.columns([1, 2], gap="large")
    with left:
        st.image(profile_image(), caption=NAME, width="stretch")
    with right:
        st.header("About me")
        st.write(
            " I'm Shin Limchiu, a BSIT student from Cebu City, Philippines. I am someone who values learning, growth, and new experiences. As I continue my journey in Information Technology, I aim to develop my knowledge and skills, overcome challenges, and prepare myself for a successful future in the tech industry."
        )
        st.header("My story")
        story = st.radio(
            "Choose a chapter",
            ["Background", "Education", "Interests"],
            horizontal=True,
        )
        if story == "Background":
            st.write("I was born in Cebu City, Philippines.")
        elif story == "Education":
            st.write("BSIT student at Cebu Institute of Technology University.")
        else:
            st.write("Playing online or mobile games, watching movies, and exploring new technologies are some of my interests.")

    st.subheader("Milestones")
    st.table(MILESTONES.set_index("Year"))

    with st.expander("A fun fact about me"):
        st.write("I enjoy learning random facts about different things.")
        st.write("I enjoy staying up late, especially when doing things I love.")
        st.write("I enjoy trying new things, even outside my comfort zone.")
        

# --------------------------------------------------------------------------
# Skills
# --------------------------------------------------------------------------
with tab_skills:
    st.header("Skills")
    st.write("TODO: Describe in a sentence or two how you picked up these skills.")

    f1, f2 = st.columns(2)
    with f1:
        cats = st.multiselect(
            "Filter by category",
            sorted(SKILLS["Category"].unique()),
            default=sorted(SKILLS["Category"].unique()),
        )
    with f2:
        min_level = st.slider("Minimum skill level", 0, 100, 0, step=5)

    view = SKILLS[SKILLS["Category"].isin(cats) & (SKILLS["Level"] >= min_level)]

    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.dataframe(view, hide_index=True, width="stretch")
    with c2:
        if view.empty:
            st.info("No skills match these filters.")
        else:
            st.bar_chart(view.set_index("Skill")["Level"])

    top = SKILLS.loc[SKILLS["Level"].idxmax()]
    st.write(f"My strongest skill is **{top['Skill']}** ({top['Level']}/100).")
    st.progress(int(top["Level"]) / 100, text=f"{top['Skill']} proficiency")

    st.download_button(
        "⬇️ Download skills as CSV",
        SKILLS.to_csv(index=False),
        file_name="skills.csv",
        mime="text/csv",
    )

# --------------------------------------------------------------------------
# Projects
# --------------------------------------------------------------------------
with tab_projects:
    st.header("Projects")
    all_tools = sorted({t for p in PROJECTS for t in p["tools"]})
    picked = st.selectbox("Show projects that use...", ["All tools"] + all_tools)

    for p in PROJECTS:
        if picked != "All tools" and picked not in p["tools"]:
            continue
        with st.container(border=True):
            st.subheader(p["title"])
            a, b = st.columns([1, 2])
            a.markdown(f"**Role:** {p['role']}")
            a.markdown("**Tools:** " + ", ".join(p["tools"]))
            b.write(p["outcome"])
            if p["link"]:
                b.link_button("View project", p["link"])

    st.divider()
    st.subheader("Project activity")
    st.caption("TODO: replace this sample with real data, e.g. hours spent per project.")
    hours = pd.DataFrame(
        np.random.default_rng(1).integers(2, 12, size=(6, len(PROJECTS))),
        columns=[p["title"] for p in PROJECTS],
        index=["Wk 1", "Wk 2", "Wk 3", "Wk 4", "Wk 5", "Wk 6"],
    )
    st.line_chart(hours)

# --------------------------------------------------------------------------
# Contact / feedback
# --------------------------------------------------------------------------
with tab_contact:
    st.header("Contact & feedback")
    with st.form("contact_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        visitor = c1.text_input("Your name")
        topic = c2.selectbox("Topic", ["Feedback", "Collaboration", "Question", "Just saying hi"])
        message = st.text_area("Message", height=120)
        submitted = st.form_submit_button("Send")

    if submitted:
        if not visitor or not message:
            st.warning("Please enter your name and a message.")
        else:
            st.session_state.messages.append(
                {"time": datetime.now().strftime("%H:%M"), "from": visitor, "topic": topic, "message": message}
            )
            st.success(f"Thanks, {visitor}! Your {topic.lower()} was received.")
            if show_balloons:
                st.balloons()

    if st.session_state.messages:
        st.subheader("Messages sent this session")
        st.dataframe(pd.DataFrame(st.session_state.messages), hide_index=True, width="stretch")

st.divider()
st.caption(f"© {datetime.now().year} {NAME} · {SECTION}")