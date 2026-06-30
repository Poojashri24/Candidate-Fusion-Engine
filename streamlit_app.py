import os
import json
import pandas as pd
import streamlit as st

from projection.projection import Projection

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Candidate Fusion Engine",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Candidate Fusion Engine")
st.caption("Identity Resolution & Candidate Profile Fusion")

# =====================================================
# Load Canonical Profiles
# =====================================================

with open(
    "output/canonical_profiles.json",
    "r",
    encoding="utf8"
) as f:

    data = json.load(f)

profiles = data["profiles"]

# =====================================================
# Sidebar
# =====================================================

st.sidebar.title("Candidate Dashboard")

candidate = st.sidebar.selectbox(

    "Select Candidate",

    profiles,

    format_func=lambda x: x["full_name"]

)

st.sidebar.markdown("---")

st.sidebar.metric(

    "Total Candidates",

    len(profiles)

)

merged = sum(

    1

    for p in profiles

    if len(p.get("matched_sources", [])) > 1

)

st.sidebar.metric(

    "Merged Profiles",

    merged

)

# =====================================================
# Main Layout
# =====================================================

left, right = st.columns(

    [2, 1],

    gap="large"

)

# =====================================================
# LEFT PANEL
# =====================================================

with left:

    st.header("Candidate Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Confidence",

        candidate.get("overall_confidence", 0)

    )

    c2.metric(

        "Emails",

        len(candidate.get("emails", []))

    )

    c3.metric(

        "Skills",

        len(candidate.get("skills", []))

    )

    st.divider()

    # -------------------------------------------------

    st.subheader("Basic Information")

    st.write("**Name** :", candidate["full_name"])

    st.write("**Headline** :", candidate.get("headline", "Not Available"))

    st.write("**Emails** :", candidate["emails"])

    st.write("**Phones** :", candidate["phones"])

    st.write("**Location** :", candidate["location"])

    if candidate.get("links", {}).get("linkedin"):
        st.write("**LinkedIn** :", candidate["links"]["linkedin"][0])

    if candidate.get("links", {}).get("github"):
        st.write("**GitHub** :", candidate["links"]["github"][0])

    if candidate.get("links", {}).get("portfolio"):
        st.write("**Portfolio** :", candidate["links"]["portfolio"][0])

    # -------------------------------------------------

    st.subheader("Skills")

    skill_names = [

        s["name"]

        for s in candidate.get("skills", [])

    ]

    st.write(skill_names)

    # -------------------------------------------------

    st.subheader("Experience")

    if candidate["experience"]:

        st.table(

            candidate["experience"]

        )

    else:

        st.info("No Experience Found")

    # -------------------------------------------------

    st.subheader("Education")

    if candidate["education"]:

        st.table(

            candidate["education"]

        )

    else:

        st.info("No Education Found")

    # -------------------------------------------------

    with st.expander(

        "Identity Resolution",

        expanded=True

    ):

        rows = []

        for src in candidate.get(

            "matched_sources",

            []

        ):

            if isinstance(src, dict):

                rows.append({

                    "Source": src["source"],

                    "Matched On": src["matched_on"],

                    "Score": src["match_score"]

                })

            else:

                rows.append({

                    "Source": src,

                    "Matched On": "Initial Registration",

                    "Score": 1.0

                })

        st.table(rows)
    # =====================================================
    # Merge Decisions
    # =====================================================

    with st.expander("Merge Decisions"):

        if candidate.get("decision_log"):

            st.table(candidate["decision_log"])

        else:

            st.info("No Merge Decisions")

    # =====================================================
    # Provenance
    # =====================================================

    with st.expander("Provenance"):

        if candidate.get("provenance"):

            st.table(candidate["provenance"])

        else:

            st.info("No Provenance Information")

    # =====================================================
    # Recruiter CSV
    # =====================================================

    with st.expander("Recruiter CSV"):

        if os.path.exists("input/recruiter.csv"):

            csv = pd.read_csv("input/recruiter.csv")

            st.dataframe(csv, use_container_width=True)

    # =====================================================
    # Resume Files
    # =====================================================

    with st.expander("Resume Files"):

        folder = "input/resumes"

        if os.path.exists(folder):

            files = [

                f

                for f in os.listdir(folder)

                if f.endswith(".pdf")

            ]

            st.write(files)

        else:

            st.warning("Resume folder not found.")

    # =====================================================
    # Recruiter Notes
    # =====================================================

    with st.expander("Recruiter Notes"):

        folder = "input/notes"

        if os.path.exists(folder):

            notes = [

                f

                for f in os.listdir(folder)

                if f.endswith(".txt")

            ]

            if notes:

                for note in notes:

                    with st.expander(note):

                        with open(

                            os.path.join(folder, note),

                            encoding="utf8"

                        ) as f:

                            st.text(f.read())

            else:

                st.info("No recruiter notes found.")

# =====================================================
# RIGHT PANEL
# =====================================================

with right:

    st.header("Runtime Projection")

    st.write(
        "Generate different JSON formats at runtime without changing the backend."
    )

    templates = {

        "Minimal": {

            "fields": [

                {

                    "path": "candidate_name",

                    "from": "full_name"

                },

                {

                    "path": "email",

                    "from": "emails[0]"

                }

            ],

            "include_confidence": False,

            "include_provenance": False,

            "missing": "omit"

        },

        "HR System": {

            "fields": [

                {

                    "path": "employee_name",

                    "from": "full_name"

                },

                {

                    "path": "designation",

                    "from": "headline"

                },

                {

                    "path": "email",

                    "from": "emails[0]"

                },

                {

                    "path": "phone",

                    "from": "phones[0]"

                },

                {

                    "path": "skills",

                    "from": "skills[].name"

                },

                {

                    "path": "city",

                    "from": "location.city"

                },

                {

                    "path": "country",

                    "from": "location.country"

                }

            ],

            "include_confidence": True,

            "include_provenance": False,

            "missing": "omit"

        },

        "Strict Validation": {

            "fields": [

                {

                    "path": "employee_name",

                    "from": "full_name",

                    "required": True

                },

                {

                    "path": "github_profile",
                    "from": "links.github[0]",
                    "required": True
                },
                {
                    "path": "linkedin_profile",
                    "from": "links.linkedin[0]"
                }

            ],

            "include_confidence": False,

            "include_provenance": False,

            "missing": "error"

        }

    }

    template = st.selectbox(

        "Projection Template",

        list(templates.keys())

    )

    config_text = st.text_area(

        "Editable Runtime Configuration",

        value=json.dumps(

            templates[template],

            indent=4

        ),

        height=300

    )

    st.info("""

Supported Field Paths

• full_name

• headline

• emails[0]

• phones[0]

• location.city

• location.country

• skills[].name

• experience

• education

Normalization

• canonical

• E164

Missing Options

• omit

• null

• error

""")

    col1, col2 = st.columns(2)

    apply = col1.button(

        "🚀 Apply",

        use_container_width=True

    )

    reset = col2.button(

        "Reset",

        use_container_width=True

    )

    if reset:

        st.rerun()

    if apply:

        try:

            runtime_config = json.loads(config_text)

            projected = Projection.apply(

                candidate,

                runtime_config

            )

            st.success("Projection Successful")

            st.subheader("Projected JSON")

            st.json(projected)

            st.download_button(

                "⬇ Download Projected JSON",

                data=json.dumps(

                    projected,

                    indent=4

                ),

                file_name="projected_profile.json",

                mime="application/json",

                use_container_width=True

            )

        except Exception as e:

            st.error("Schema Validation Failed")

            st.error(str(e))