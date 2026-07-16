
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Use Case Prioritisation Assistant",
    page_icon="✅",
    layout="wide",
)

st.title("AI Use Case Prioritisation Assistant")

st.markdown(
    """
    ### About this tool

    This application provides a structured assessment of proposed AI, analytics,
    automation and digital use cases. It considers business value, implementation
    readiness, delivery capability, and risk and governance before recommending
    how the use case should be prioritised.

    The assessment result is **a recommendation to support discussion and
    decision-making**. It does not replace formal business, funding, data,
    cybersecurity, architecture, procurement or management approvals.
    """
)

with st.expander("How to use this app", expanded=True):
    st.markdown(
        """
        1. Enter the basic use case details in the sidebar.
        2. Answer every assessment question using **Yes**, **I am unsure**, or **No**.
        3. Select **I am unsure** when the answer has not been confirmed or there is
           insufficient evidence.
        4. Move your mouse over the **?** icon beside each question for additional guidance.
        5. Select **Assess Use Case** to view the recommended status, score,
           delivery route, clarification needs and priority actions.
        6. Use the recommendation as a starting point for discussion with the
           relevant business owner, product owner and technical or governance teams.

        For queries on the use of this application, contact
        [seet_jun_feng@swda.gov.sg](mailto:seet_jun_feng@swda.gov.sg).
        """
    )

st.caption(
    "Answer Yes, I am unsure or No to assess whether a proposed use case should "
    "be piloted now, scoped further, placed under foundation work, or held for redesign."
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

ANSWER_OPTIONS = ["Yes", "I am unsure", "No"]

# Scoring multiplier applied to each weighted question.
# Yes receives full points, I am unsure receives half points, and No receives zero.
ANSWER_MULTIPLIERS = {
    "Yes": 1.0,
    "I am unsure": 0.5,
    "No": 0.0,
}

# -----------------------------
# Inputs
# -----------------------------
with st.sidebar:
    st.header("Use Case Details")
    use_case_name = st.text_input(
        "Use case name",
        placeholder="e.g. Policy and Rules Assistant",
    )
    business_unit = st.text_input(
        "Business unit / team",
        placeholder="e.g. DSPD",
    )
    owner_name = st.text_input(
        "Proposed business owner",
        placeholder="Name or role",
    )
    notes = st.text_area(
        "Brief description",
        placeholder="What problem is being solved?",
    )

    st.caption(
        "These details identify the assessment record. "
        "They do not directly affect the score."
    )

responses = {}

for section in sorted(set(q["section"] for q in QUESTIONS)):
    st.subheader(section)

    for q in [x for x in QUESTIONS if x["section"] == section]:
        responses[q["id"]] = st.radio(
            q["question"],
            options=ANSWER_OPTIONS,
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

    def answer_is(question_id: str, answer: str) -> bool:
        return responses[question_id] == answer

    def answer_multiplier(question_id: str) -> float:
        return ANSWER_MULTIPLIERS[responses[question_id]]

    failed_gates = [
        q["question"]
        for q in QUESTIONS
        if q["critical"] and answer_is(q["id"], "No")
    ]

    uncertain_gates = [
        q["question"]
        for q in QUESTIONS
        if q["critical"] and answer_is(q["id"], "I am unsure")
    ]

    uncertain_questions = [
        q
        for q in QUESTIONS
        if answer_is(q["id"], "I am unsure")
    ]

    score = sum(
        q["weight"] * answer_multiplier(q["id"])
        for q in QUESTIONS
        if not q["critical"]
    )
    score_pct = round((score / MAX_SCORE) * 100)

    category_scores = {}

    for category in ["Value", "Readiness", "Capability", "Risk"]:
        category_questions = [
            q for q in QUESTIONS if q["category"] == category
        ]
        category_maximum = sum(q["weight"] for q in category_questions)
        category_score = sum(
            q["weight"] * answer_multiplier(q["id"])
            for q in category_questions
        )

        category_scores[category] = (
            round((category_score / category_maximum) * 100)
            if category_maximum
            else 0
        )

    readiness_or_risk_uncertainty = any(
        q["category"] in {"Readiness", "Risk"}
        and answer_is(q["id"], "I am unsure")
        for q in QUESTIONS
    )

    # -----------------------------
    # Prioritisation status logic
    # -----------------------------
    if failed_gates:
        status = "Foundation Required"
        status_explanation = (
            "One or more mandatory readiness conditions have been answered No. "
            "The use case should not proceed to active pilot development until "
            "these foundational gaps are resolved."
        )

    elif score_pct < 50:
        status = "Hold or Reframe"
        status_explanation = (
            "The current proposition does not yet demonstrate sufficient combined "
            "value, readiness, capability and manageable risk. Narrow, redesign or "
            "reconsider the use case before investing further."
        )

    elif uncertain_gates:
        if score_pct >= 65:
            status = "Scope Next"
            status_explanation = (
                "The use case appears promising, but one or more mandatory readiness "
                "conditions remain unconfirmed. Resolve these uncertainties before "
                "seeking approval for a pilot."
            )
        else:
            status = "Foundation Required"
            status_explanation = (
                "Mandatory readiness conditions remain unconfirmed and the overall "
                "score is moderate. Complete the required foundation and clarification "
                "work before reassessment."
            )

    elif (
        score_pct >= 80
        and category_scores["Readiness"] >= 70
        and not readiness_or_risk_uncertainty
    ):
        status = "Pilot Now"
        status_explanation = (
            "The use case has strong value, adequate readiness and manageable delivery "
            "risk. No readiness or risk question remains uncertain. Proceed to a bounded "
            "pilot with human review and agreed success measures."
        )

    elif score_pct >= 65:
        status = "Scope Next"
        if readiness_or_risk_uncertainty:
            status_explanation = (
                "The use case has a promising score, but uncertainty remains in "
                "implementation readiness or risk and governance. Clarify these matters "
                "before an immediate pilot is recommended."
            )
        else:
            status_explanation = (
                "The use case is promising but needs targeted scoping before "
                "development begins."
            )

    else:
        status = "Foundation Required"
        status_explanation = (
            "The use case has potential, but important data, system, workflow, "
            "capability or governance gaps should be addressed first."
        )

    # -----------------------------
    # Recommended delivery route
    # -----------------------------
    internal_capability = responses["internal_capability"]
    existing_tools = responses["existing_tools"]
    external_support = responses["external_support"]

    if internal_capability == "Yes" and existing_tools == "Yes":
        delivery_route = (
            "Business/DSPD-led configuration or prototype using existing approved tools"
        )

    elif internal_capability == "Yes" and existing_tools == "No":
        delivery_route = (
            "DSPD-led custom prototype or technical discovery before formal development"
        )

    elif internal_capability == "No" and external_support == "Yes":
        delivery_route = (
            "Collaborative prototype with GovTech, DSAD, intern, polytechnic "
            "or university support"
        )

    elif existing_tools == "Yes" and external_support == "Yes":
        delivery_route = (
            "Configure an existing approved platform with specialist or partner support"
        )

    elif "I am unsure" in {
        internal_capability,
        existing_tools,
        external_support,
    }:
        delivery_route = (
            "Delivery route requires clarification of internal capability, "
            "platform fit and available partner support"
        )

    elif existing_tools == "Yes":
        delivery_route = (
            "Configure an existing platform after securing specialist implementation support"
        )

    else:
        delivery_route = "Formal discovery and system project assessment"

    # -----------------------------
    # Gap and uncertainty recommendations
    # -----------------------------
    gap_map = {
        "owner": "Confirm a named business owner and pilot users.",
        "problem": "Refine the problem statement, target users and intended outcome.",
        "human_review": "Define the officer review, approval and override process.",
        "data_permission": "Confirm data ownership, access approval and permitted pilot data.",
        "success_metric": "Define a baseline and measurable pilot success indicators.",
        "low_system_dependency": "Consider a standalone, batch-based or document-based pilot before live integration.",
        "data_available": "Identify the required datasets and address data quality or availability gaps.",
        "rules_clear": "Document and validate the workflow, business rules and decision points.",
        "existing_tools": "Assess whether an approved platform can meet the need or whether custom development is required.",
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

    no_actions = [
        gap_map[q["id"]]
        for q in QUESTIONS
        if answer_is(q["id"], "No") and q["id"] in gap_map
    ]

    uncertainty_actions = [
        f'Obtain evidence and confirm: {q["question"]}'
        for q in uncertain_questions
    ]

    # -----------------------------
    # Display result
    # -----------------------------
    st.divider()
    st.header("Assessment Result")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Recommended Status", status)
    col2.metric("Overall Score", f"{score_pct}/100")
    col3.metric("Mandatory Gates Failed", len(failed_gates))
    col4.metric("Uncertain Answers", len(uncertain_questions))

    st.info(status_explanation)
    st.write("**Recommended delivery route:**", delivery_route)

    chart_dataframe = pd.DataFrame(
        {
            "Category": list(category_scores.keys()),
            "Score": list(category_scores.values()),
        }
    ).set_index("Category")

    st.bar_chart(chart_dataframe)

    if failed_gates:
        st.subheader("Mandatory Gaps")
        for failed_gate in failed_gates:
            st.write(f"- {failed_gate}")

    if uncertain_gates:
        st.subheader("Unconfirmed Mandatory Conditions")
        for uncertain_gate in uncertain_gates:
            st.write(f"- {uncertain_gate}")

    if uncertainty_actions:
        st.subheader("Clarifications Required")
        for action in uncertainty_actions:
            st.write(f"- {action}")

    st.subheader("Priority Actions")

    if no_actions:
        for action in no_actions[:8]:
            st.write(f"- {action}")
    elif not uncertainty_actions:
        st.write(
            "- No major readiness gaps or uncertainties identified. "
            "Proceed according to the recommended status."
        )
    else:
        st.write(
            "- No questions were answered No. Resolve the uncertainties listed above."
        )

    st.subheader("Suggested Next Decision")

    if status == "Pilot Now":
        st.success(
            "Approve a bounded pilot, confirm the pilot owner and users, select the "
            "delivery platform, and agree on the evaluation period and success measures."
        )

    elif status == "Scope Next":
        st.warning(
            "Conduct a focused discovery exercise to resolve uncertain or weak areas "
            "before seeking pilot approval."
        )

    elif status == "Foundation Required":
        st.warning(
            "Assign owners to close the identified foundation gaps and uncertainties, "
            "then reassess the use case."
        )

    else:
        st.error(
            "Do not start development yet. Reframe the use case around a clearer, "
            "smaller and more valuable problem."
        )

    # -----------------------------
    # Downloadable assessment
    # -----------------------------
    result_row = {
        "Use Case": use_case_name,
        "Business Unit": business_unit,
        "Business Owner": owner_name,
        "Status": status,
        "Overall Score": score_pct,
        "Value Score": category_scores["Value"],
        "Readiness Score": category_scores["Readiness"],
        "Capability Score": category_scores["Capability"],
        "Risk Score": category_scores["Risk"],
        "Mandatory Gates Failed": len(failed_gates),
        "Mandatory Gates Uncertain": len(uncertain_gates),
        "Total Uncertain Answers": len(uncertain_questions),
        "Delivery Route": delivery_route,
        "Description": notes,
    }

    for q in QUESTIONS:
        result_row[f'Response - {q["id"]}'] = responses[q["id"]]

    result_dataframe = pd.DataFrame([result_row])

    st.download_button(
        "Download Assessment as CSV",
        data=result_dataframe.to_csv(index=False).encode("utf-8"),
        file_name="use_case_prioritisation_assessment.csv",
        mime="text/csv",
        use_container_width=True,
    )
