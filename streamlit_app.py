from streamlit_extras.colored_header import colored_header
from streamlit_extras.mention import mention
from streamlit_extras.badges import badge
import streamlit as st
from lyzr import QABot
import configparser
import tempfile
import os


st.set_page_config(layout="wide", initial_sidebar_state="expanded")
config = configparser.ConfigParser()
config.read("./config.ini")

# Read config file
MODEL = config["MODEL"]["LLM"]
MATCH_PERCENTAGE = config["DETAILED_PROMPTS"]["MATCH_PERCENTAGE"]
MISSING_SKILLS = config["DETAILED_PROMPTS"]["MISSING_SKILLS"]
GRAMMAR_MISTAKES = config["DETAILED_PROMPTS"]["GRAMMAR_MISTAKES"]
ROADMAP = config["DETAILED_PROMPTS"]["ONLINE_COURSES"]
SALARY = config["DETAILED_PROMPTS"]["SALARY"]
CAREER_ADVICE = config["DETAILED_PROMPTS"]["CAREER_ADVICE"]
ADDITIONAL_POINTS = config["DETAILED_PROMPTS"]["ADDITIONAL_POINTS"]

MATCH_PERCENTAGE_SHORT = config["SHORT_PROMPTS"]["MATCH_PERCENTAGE"]
MISSING_SKILLS_SHORT = config["SHORT_PROMPTS"]["MISSING_SKILLS"]
GRAMMAR_MISTAKES_SHORT = config["SHORT_PROMPTS"]["GRAMMAR_MISTAKES"]
ROADMAP_SHORT = config["SHORT_PROMPTS"]["ONLINE_COURSES"]
SALARY_SHORT = config["SHORT_PROMPTS"]["SALARY"]
CAREER_ADVICE_SHORT = config["SHORT_PROMPTS"]["CAREER_ADVICE"]
ADDITIONAL_POINTS_SHORT = config["SHORT_PROMPTS"]["ADDITIONAL_POINTS"]


# Define session state variables
if 'response' not in st.session_state:
    st.session_state['response'] = None
if 'match_percent' not in st.session_state:
    st.session_state['match_percent'] = "Match percentage"
if 'missing_skills' not in st.session_state:
    st.session_state['missing_skills'] = "Missing skills"
if 'add_points' not in st.session_state:
    st.session_state['add_points'] = "Additional points"
if 'gram_errors' not in st.session_state:
    st.session_state['gram_errors'] = "Grammatical mistakes"
if 'roadmap' not in st.session_state:
    st.session_state['roadmap'] = "Roadmap"
if 'salary' not in st.session_state:
    st.session_state['salary'] = "Salary prediction"
if 'future' not in st.session_state:
    st.session_state['future'] = "Future opportunities"

if 'detail' not in st.session_state:
    st.session_state['detail'] = "Detailed"
if 'short' not in st.session_state:
    st.session_state['short'] = "Short"


# Map prompts
detailed_dict = {
    st.session_state['match_percent'] : MATCH_PERCENTAGE,
    st.session_state['missing_skills'] : MISSING_SKILLS,
    st.session_state['add_points'] : ADDITIONAL_POINTS,
    st.session_state['gram_errors'] : GRAMMAR_MISTAKES,
    st.session_state['roadmap'] : ROADMAP,
    st.session_state['salary'] : SALARY,
    st.session_state['future'] : CAREER_ADVICE
}

short_dict = {
    st.session_state['match_percent'] : MATCH_PERCENTAGE_SHORT,
    st.session_state['missing_skills'] : MISSING_SKILLS_SHORT,
    st.session_state['add_points'] : ADDITIONAL_POINTS_SHORT,
    st.session_state['gram_errors'] : GRAMMAR_MISTAKES_SHORT,
    st.session_state['roadmap'] : ROADMAP_SHORT,
    st.session_state['salary'] : SALARY_SHORT,
    st.session_state['future'] : CAREER_ADVICE_SHORT
}


# Input form
with st.sidebar:
    with st.form(key="form1"):
        os.environ["OPENAI_API_KEY"] = st.text_input("OpenAI API", type="password")
        input_file = st.file_uploader("Upload Resume PDFs", type="pdf")
        job_description = st.text_area("Job Description")
        output_format = st.radio("Output Scale", [st.session_state['detail'], st.session_state['short']])
        input_query = st.radio("Select the Query", [
            st.session_state['match_percent'],
            st.session_state['missing_skills'],
            st.session_state['add_points'],
            st.session_state['gram_errors'],
            st.session_state['roadmap'],
            st.session_state['salary'],
            st.session_state['future'],
        ])

        temperature = st.slider(label="Temperature", min_value=0.1, max_value=2.0, value=0.5, )
        submitBtn = st.form_submit_button("Submit")
    llm_params = ({"model": MODEL, "temperature": temperature})

# Read input pdf
    if input_file:
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, input_file.name)
        with open(file_path, "wb") as f:
                f.write(input_file.getvalue())
    
# select respective prompt
    if submitBtn:
        if output_format == st.session_state['detail']:
            for key, value in detailed_dict.items():
                if key == input_query:
                    qa_bot = QABot.pdf_qa(
                        input_files=[file_path],
                        llm_params=llm_params,
                        system_prompt=value
                    )
        else:
            for key, value in short_dict.items():
                if key == input_query:
                    qa_bot = QABot.pdf_qa(
                        input_files=[file_path],
                        llm_params=llm_params,
                        system_prompt=value
                    )

        st.session_state['response'] = qa_bot.query(job_description)


col1, col2 = st.columns([0.85, 0.15])

with col1:
    colored_header(
        label="Application Tracking System and Resume Analyser",
        description="Analyse the resume for insights and improvements",
        color_name="red-70",
    )
    if st.session_state.response is None:
        st.caption("Upload the resume and analyse it")
    else:
        st.info(f"{output_format} output for {input_query}")
        st.success(st.session_state['response'].response)


with col2:
    colored_header(
        label="Connect",
        description="",
        color_name="red-70",
    )
    with st.form(key="form2"):
        badge(type="pypi", name="lyzr")
        badge(type="twitter", name="lyzrai")
        badge(type="github", name="LyzrCore/lyzr")
        badge(type="github", name="sabhashanki/lyzr_shankesh")
        mention(
            label="LinkedIn",
            icon="🔗",  
            url="https://www.linkedin.com/in/shankeshrajums",
        )
        mention(
            label="Lyzr SDK",
            icon="🔗", 
            url="https://docs.lyzr.ai/lyzr-sdk/opensource/",
        )
        submitBtn2 = st.form_submit_button("With ❤️ \n Shankesh Raju MS")
        if submitBtn2:
            st.balloons()
            st.snow()
            st.toast("Thanks for supporting us!!!")
