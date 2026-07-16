
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Use Case Prioritisation Assistant",
    page_icon="✅",
    layout="wide",
)

st.title("AI Use Case Prioritisation Assistant")
st.caption(
    "Answer Yes or No to assess whether a proposed use case should be piloted now, "
    "scoped further, placed under foundation work, or held for redesign."
)

# -----------------------------
# Question configuration
# -----------------------------
QUESTIONS = [
    # Mandatory gates
    {
        "id": "owner",
        "section": "1. Mandatory Readiness Gates",
        "question": "Is there a named business owner who is accountable for the use case?",
        "help": "Select Yes when a specific person or role is accountable for decisions, resources, user participation and the outcome of the pilot.",
        "category": "Gate",
        "weight": 0,
        "critical": True,
    },
    {
        "id": "problem",
        "section": "1. Mandatory Readiness Gates",
        "question": "Is the business problem, target user and intended outcome clearly defined?",
        "help": "Select Yes when the problem is specific, the intended users are known and the expected improvement can be clearly described.",
        "category": "Gate",
        "weight": 0,
        "critical": True,
    },
    {
        "id": "human_review",
        "section": "1. Mandatory Readiness Gates",
        "question": "Can an officer review, approve or override the system output?",
        "help": "Select Yes when an officer can check, correct, approve or reject the system output before it is used.",
        "category": "Gate",
        "weight": 0,
        "critical": True,
    },
    {
        "id": "data_permission",
        "section": "1. Mandatory Readiness Gates",
        "question": "Can the required data or content be legally and securely used for a pilot?",
        "help": "Select Yes when the data owner is known, access is permitted and the data can be handled within applicable security and privacy requirements.",
        "category": "Gate",
        "weight": 0,
        "critical": True,
    },
    {
        "id": "success_metric",
        "section": "1. Mandatory Readiness Gates",
        "question": "Can success be measured using clear indicators such as time saved, quality, timeliness or user satisfaction?",
        "help": "Select Yes when there is a baseline or practical way to compare performance before and after the pilot.",
        "category": "Gate",
        "weight": 0,
        "critical": True,
    },

    # Value
    {
        "id": "high_value",
        "section": "2. Business Value",
        "question": "Will the use case deliver a meaningful improvement to productivity, service, policy, operations or governance?",
        "help": "Select Yes when the use case is expected to produce a clear and worthwhile improvement, rather than merely demonstrate a technology.",
        "category": "Value",
        "weight": 12,
        "critical": False,
    },
    {
        "id": "frequent_problem",
        "section": "2. Business Value",
        "question": "Does the problem occur frequently or affect a significant number of users or cases?",
        "help": "Select Yes when the issue is recurring, high-volume, resource-intensive or affects a meaningful number of users or cases.",
        "category": "Value",
        "weight": 8,
        "critical": False,
    },
    {
        "id": "strategic_alignment",
        "section": "2. Business Value",
        "question": "Is the use case aligned with an agreed divisional, TPG or organisational priority?",
        "help": "Select Yes when the use case directly supports an agreed business plan, management direction or organisational priority.",
        "category": "Value",
        "weight": 5,
        "critical": False,
    },
    {
        "id": "reusable",
        "section": "2. Business Value",
        "question": "Can the solution or approach be reused across more than one team, process or policy area?",
        "help": "Select Yes when the solution, workflow, data pipeline or component could be adapted for other teams or similar use cases.",
        "category": "Value",
        "weight": 5,
        "critical": False,
    },

    # Readiness
    {
        "id": "low_system_dependency",
        "section": "3. Implementation Readiness",
        "question": "Can the pilot start without major changes to TGS, MySF, CRM, OCC or other core systems?",
        "help": "Select Yes when the pilot can start using files, approved content, manual uploads, batch extracts or standalone tools without major live-system integration.",
        "category": "Readiness",
        "weight": 10,
        "critical": False,
    },
    {
        "id": "data_available",
        "section": "3. Implementation Readiness",
        "question": "Is the required data or approved content already available and sufficiently reliable?",
        "help": "Select Yes when the required data or documents exist, are accessible, reasonably complete, current and suitable for the pilot.",
        "category": "Readiness",
        "weight": 10,
        "critical": False,
    },
    {
        "id": "rules_clear",
        "section": "3. Implementation Readiness",
        "question": "Are the relevant business rules, workflow and decision points sufficiently clear and documented?",
        "help": "Select Yes when officers generally agree on how the process works, what rules apply and where decisions or exceptions occur.",
        "category": "Readiness",
        "weight": 7,
        "critical": False,
    },
    {
        "id": "existing_tools",
        "section": "3. Implementation Readiness",
        "question": "Can the use case be developed substantially using existing approved platforms or tools?",
        "help": "Select Yes when an existing approved platform can support most of the required functions through configuration or limited development.",
        "category": "Readiness",
        "weight": 8,
        "critical": False,
    },

    # Capability
    {
        "id": "internal_capability",
        "section": "4. Delivery Capability",
        "question": "Do we have sufficient internal business, product, data or technical capability to develop the pilot?",
        "help": "Select Yes when the organisation has enough business knowledge, product ownership and technical capability to design, test and manage the pilot.",
        "category": "Capability",
        "weight": 8,
        "critical": False,
    },
    {
        "id": "external_support",
        "section": "4. Delivery Capability",
        "question": "Where internal capability is insufficient, can GovTech, DSAD, an intern, polytechnic or university partner support the work?",
        "help": "Select Yes when a realistic delivery partner such as GovTech, DSAD, an intern, polytechnic or university is available and suitable.",
        "category": "Capability",
        "weight": 6,
        "critical": False,
    },
    {
        "id": "manageable_effort",
        "section": "4. Delivery Capability",
        "question": "Can a meaningful pilot be delivered within a manageable timeframe and effort?",
        "help": "Select Yes when a bounded pilot can be delivered without excessive time, cost, procurement, staffing or system changes.",
        "category": "Capability",
        "weight": 6,
        "critical": False,
    },

    # Risk
    {
        "id": "low_decision_risk",
        "section": "5. Risk and Governance",
        "question": "Will the system support rather than make final eligibility, funding, approval or enforcement decisions?",
        "help": "Select Yes when the system provides drafts, analysis, recommendations or alerts while authorised officers retain final decision-making responsibility.",
        "category": "Risk",
        "weight": 5,
        "critical": False,
    },
    {
        "id": "manageable_security",
        "section": "5. Risk and Governance",
        "question": "Are privacy, security and data sensitivity risks manageable using existing controls?",
        "help": "Select Yes when privacy, security and data sensitivity risks can be managed using approved platforms, access controls or limited datasets.",
        "category": "Risk",
        "weight": 5,
        "critical": False,
    },
]

MAX_SCORE = sum(q["weight"] for q in QUESTIONS)

# -----------------------------
# Inputs
# -----------------------------
with st.sidebar:
    st.header("Use Case Details")
    use_case_name = st.text_input("Use case name", placeholder="e.g. Policy and Rules Assistant")
    business_unit = st.text_input("Business unit / team", placeholder="e.g. DSPD")
    owner_name = st.text_input("Proposed business owner", placeholder="Name or role")
    notes = st.text_area("Brief description", placeholder="What problem is being solved?")

responses = {}

for section in sorted(set(q["section"] for q in QUESTIONS)):
    st.subheader(section)
    for q in [x for x in QUESTIONS if x["section"] == section]:
        responses[q["id"]] = st.radio(
            q["question"],
            options=["Yes", "No"],
            index=None,
            horizontal=True,
            key=q["id"],
            help=q.get("help"),
        )

# -----------------------------
# Scoring and recommendation
# -----------------------------
if st.button("Assess Use Case", type="primary", use_container_width=True):
    unanswered_questions = [
        q["question"]
        for q in QUESTIONS
        if responses.get(q["id"]) is None
    ]

    if unanswered_questions:
        st.error(
            f"Please answer all questions before assessment. "
            f"{len(unanswered_questions)} question(s) remain unanswered."
        )
        st.stop()

    yes = lambda qid: responses[qid] == "Yes"

    failed_gates = [
        q["question"]
        for q in QUESTIONS
        if q["critical"] and not yes(q["id"])
    ]

    score = sum(
        q["weight"]
        for q in QUESTIONS
        if not q["critical"] and yes(q["id"])
    )
    score_pct = round((score / MAX_SCORE) * 100)

    category_scores = {}
    for category in ["Value", "Readiness", "Capability", "Risk"]:
        cat_questions = [q for q in QUESTIONS if q["category"] == category]
        cat_max = sum(q["weight"] for q in cat_questions)
        cat_score = sum(q["weight"] for q in cat_questions if yes(q["id"]))
        category_scores[category] = round((cat_score / cat_max) * 100) if cat_max else 0

    # Status logic
    if failed_gates:
        status = "Foundation Required"
        status_explanation = (
            "The use case is not ready for active pilot development because one or more "
            "mandatory readiness conditions are not yet met."
        )
    elif score_pct >= 80 and category_scores["Readiness"] >= 70:
        status = "Pilot Now"
        status_explanation = (
            "The use case has strong value, adequate readiness and manageable delivery risk. "
            "Proceed to a bounded pilot with human review and agreed success measures."
        )
    elif score_pct >= 65:
        status = "Scope Next"
        status_explanation = (
            "The use case is promising but needs targeted scoping before development begins."
        )
    elif score_pct >= 50:
        status = "Foundation Required"
        status_explanation = (
            "The use case has potential, but important data, system, workflow, capability or "
            "governance gaps should be addressed first."
        )
    else:
        status = "Hold or Reframe"
        status_explanation = (
            "The current proposition is not sufficiently valuable or ready. Consider narrowing "
            "the scope, combining it with another use case, or revisiting it later."
        )

    # Recommended delivery route
    if yes("internal_capability") and yes("existing_tools"):
        delivery_route = "Business/DSPD-led configuration or prototype using existing approved tools"
    elif not yes("internal_capability") and yes("external_support"):
        delivery_route = "Collaborative prototype with GovTech, DSAD, intern, polytechnic or university support"
    elif yes("existing_tools"):
        delivery_route = "Configure an existing platform with specialist implementation support"
    else:
        delivery_route = "Formal discovery and system project assessment"

    # Gap recommendations
    gap_map = {
        "owner": "Confirm a named business owner and pilot users.",
        "problem": "Refine the problem statement, target users and intended outcome.",
        "human_review": "Define the officer review, approval and override process.",
        "data_permission": "Confirm data ownership, access approval and permitted pilot data.",
        "success_metric": "Define a baseline and measurable pilot success indicators.",
        "low_system_dependency": "Consider a standalone, batch-based or document-based pilot before live integration.",
        "data_available": "Identify the required datasets and address data quality or availability gaps.",
        "rules_clear": "Document and validate the workflow, business rules and decision points.",
        "existing_tools": "Assess whether AIBots, Pair, GovText, Opus, Plumber, Analytics.gov or another approved platform can meet the need.",
        "internal_capability": "Identify the internal product, business, data and technical skills required.",
        "external_support": "Explore support from GovTech, DSAD, interns, polytechnics, universities or vendors.",
        "manageable_effort": "Reduce the scope to a bounded pilot that can demonstrate value quickly.",
        "low_decision_risk": "Keep final decisions with officers and limit AI to drafting, analysis or recommendations.",
        "manageable_security": "Complete security, privacy and data sensitivity assessment before development.",
        "high_value": "Clarify the measurable business or user value.",
        "frequent_problem": "Validate the scale, frequency and cost of the problem.",
        "strategic_alignment": "Confirm alignment with an agreed organisational priority.",
        "reusable": "Consider whether common components can support other teams or workflows.",
    }

    recommendations = [
        gap_map[q["id"]]
        for q in QUESTIONS
        if not yes(q["id"]) and q["id"] in gap_map
    ]

    st.divider()
    st.header("Assessment Result")

    col1, col2, col3 = st.columns(3)
    col1.metric("Recommended Status", status)
    col2.metric("Overall Score", f"{score_pct}/100")
    col3.metric("Mandatory Gates Failed", len(failed_gates))

    st.info(status_explanation)
    st.write("**Recommended delivery route:**", delivery_route)

    chart_df = pd.DataFrame(
        {
            "Category": list(category_scores.keys()),
            "Score": list(category_scores.values()),
        }
    ).set_index("Category")
    st.bar_chart(chart_df)

    st.subheader("Priority Actions")
    if recommendations:
        for item in recommendations[:8]:
            st.write(f"- {item}")
    else:
        st.write("- No major readiness gaps identified. Proceed to pilot charter and implementation planning.")

    st.subheader("Suggested Next Decision")
    if status == "Pilot Now":
        st.success(
            "Approve a bounded pilot, confirm the pilot owner and users, select the delivery platform, "
            "and agree on the evaluation period and success measures."
        )
    elif status == "Scope Next":
        st.warning(
            "Conduct a short discovery exercise to resolve the lowest-scoring areas before seeking pilot approval."
        )
    elif status == "Foundation Required":
        st.warning(
            "Assign owners to close the identified foundation gaps, then reassess the use case."
        )
    else:
        st.error(
            "Do not start development yet. Reframe the use case around a clearer, smaller and more valuable problem."
        )

    # Downloadable assessment
    result_rows = [
        {
            "Use Case": use_case_name,
            "Business Unit": business_unit,
            "Business Owner": owner_name,
            "Status": status,
            "Overall Score": score_pct,
            "Value Score": category_scores["Value"],
            "Readiness Score": category_scores["Readiness"],
            "Capability Score": category_scores["Capability"],
            "Risk Score": category_scores["Risk"],
            "Delivery Route": delivery_route,
            "Description": notes,
        }
    ]
    result_df = pd.DataFrame(result_rows)
    st.download_button(
        "Download Assessment as CSV",
        data=result_df.to_csv(index=False).encode("utf-8"),
        file_name="use_case_prioritisation_assessment.csv",
        mime="text/csv",
        use_container_width=True,
    )