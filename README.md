# AI Use Case Prioritisation Assistant

A Streamlit application that helps business users assess and prioritise proposed AI, analytics, automation and digital use cases through a structured questionnaire with three response options:

- **Yes**
- **I am unsure**
- **No**

The application evaluates each use case across mandatory readiness, business value, implementation readiness, delivery capability, and risk and governance. It then produces a prioritisation status, scoring breakdown, delivery-route recommendation, and actions for gaps or uncertainties.

---

## 1. Purpose

The application supports an initial, consistent discussion on whether a proposed use case should:

1. proceed to a bounded pilot;
2. undergo further scoping;
3. complete foundation work first; or
4. be held, narrowed or reframed.

It is a decision-support tool, not an approval system. Final decisions remain with the relevant business owner, product owner, governance body, data owner and technical stakeholders.

The rubric is designed to avoid two common problems:

- prioritising a use case merely because it is easy to implement, despite limited value; and
- attempting a valuable use case too early, before its data, workflow, system, capability or governance foundations are ready.

---

## 2. Key Features

### Three response options

Each question supports:

| Answer | Meaning | Weighted-question score |
|---|---|---:|
| **Yes** | The condition is confirmed and supported by reasonable evidence | 100% of the question weight |
| **I am unsure** | The condition is unconfirmed, evidence is incomplete, or the assessor does not know | 50% of the question weight |
| **No** | The condition is not met | 0% of the question weight |

No option is selected by default. Every question must be answered before the assessment can run.

### Mouse-over guidance

Each question has a Streamlit `help` tooltip. Hover over the question-mark icon to see guidance on how to interpret the question.

### Mandatory readiness gates

Five questions are mandatory gates. They do not contribute points, but their answers affect the prioritisation outcome:

- **Yes:** gate passes;
- **I am unsure:** gate is unresolved and prevents an immediate **Pilot Now** recommendation;
- **No:** gate fails and results in **Foundation Required**.

### Weighted scoring

The remaining questions have weights. The app calculates:

- overall score out of 100;
- Business Value score;
- Implementation Readiness score;
- Delivery Capability score; and
- Risk and Governance score.

### Uncertainty handling

“I am unsure” is not treated as the same as Yes or No.

It:

- receives half of the available points;
- is counted and displayed separately;
- generates a clarification action;
- prevents **Pilot Now** when it occurs in a mandatory gate, Implementation Readiness, or Risk and Governance question; and
- may result in **Scope Next** or **Foundation Required**, depending on the overall score.

### Downloadable results

The CSV export includes:

- assessment details;
- overall and category scores;
- status;
- failed and uncertain gate counts;
- total uncertainty count;
- delivery route; and
- every individual question response.

---

## 3. Project Structure

```text
ai-use-case-prioritisation/
├── app.py
├── requirements.txt
└── README.md
```

---

## 4. Installation

### Prerequisites

- Python 3.10 or later
- `pip`

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### requirements.txt

```text
streamlit>=1.35
pandas>=2.0
```

---

## 5. Use Case Details

The sidebar records:

- use case name;
- business unit or team;
- proposed business owner; and
- brief description.

These fields identify the assessment and are included in the CSV. They do not directly affect the score or recommendation.

For example, entering a business owner in the sidebar does not automatically pass the mandatory business-owner gate. The user must still answer the relevant assessment question.

---

## 6. Assessment Framework

The questionnaire contains:

1. five mandatory readiness gates; and
2. thirteen weighted questions.

The weighted questions have a maximum total of **95 raw points**. The raw score is normalised to a score out of 100.

---

## 7. Mandatory Readiness Gates

| Gate | Purpose |
|---|---|
| Named business owner | Confirms accountability for decisions, resources, user participation and outcomes |
| Clear problem and outcome | Confirms that the problem, target users and intended improvement are defined |
| Human review and override | Ensures an officer can review, correct, approve or reject outputs |
| Permitted and secure data use | Confirms that data or content can be legally and securely used |
| Measurable success | Confirms that the pilot can be evaluated against clear indicators |

### Gate effects

| Gate answer | Effect |
|---|---|
| **Yes** | Gate passes |
| **I am unsure** | Gate is unresolved; the use case cannot receive **Pilot Now** |
| **No** | Gate fails; status becomes **Foundation Required** |

Mandatory gates have a weight of zero. Their purpose is to ensure that a high numerical score cannot override a fundamental governance or ownership gap.

---

## 8. Weighted Scoring Model

For every weighted question:

```text
Points achieved = question weight × answer multiplier
```

The multipliers are:

```python
ANSWER_MULTIPLIERS = {
    "Yes": 1.0,
    "I am unsure": 0.5,
    "No": 0.0,
}
```

### Example

For a question with a weight of 10:

| Answer | Points |
|---|---:|
| Yes | 10 |
| I am unsure | 5 |
| No | 0 |

The overall score is:

```text
Overall score = raw points achieved ÷ 95 × 100
```

---

## 9. Scoring Matrix

### 9.1 Business Value — 30 Raw Points

| Question | Weight |
|---|---:|
| Meaningful improvement to productivity, service, policy, operations or governance | 12 |
| Problem frequency or number of affected users/cases | 8 |
| Alignment with divisional, TPG or organisational priority | 5 |
| Reusability across teams, processes or policy areas | 5 |
| **Maximum** | **30** |

This category assesses whether the proposal addresses a real, material and strategically relevant problem.

### 9.2 Implementation Readiness — 35 Raw Points

| Question | Weight |
|---|---:|
| Pilot can start without major core-system changes | 10 |
| Required data or approved content is available and reliable | 10 |
| Business rules, workflow and decision points are clear | 7 |
| Existing approved platforms or tools can support the use case | 8 |
| **Maximum** | **35** |

This category assesses whether the use case can move from an idea to a practical pilot.

Implementation Readiness is important in the final logic. **Pilot Now** requires:

- a Readiness score of at least 70%; and
- no “I am unsure” answer within the Readiness category.

### 9.3 Delivery Capability — 20 Raw Points

| Question | Weight |
|---|---:|
| Sufficient internal capability | 8 |
| External or collaborative support is accessible | 6 |
| Pilot effort and timeframe are manageable | 6 |
| **Maximum** | **20** |

Potential delivery support includes GovTech, DSAD, interns, polytechnics, universities or approved vendors. The appropriate option depends on the nature and maturity of the work.

Educational partners and interns are generally better suited to exploratory analysis, bounded proofs of concept and prototypes than sole ownership of production systems or long-term maintenance.

### 9.4 Risk and Governance — 10 Raw Points

| Question | Weight |
|---|---:|
| System supports rather than makes final high-impact decisions | 5 |
| Privacy, security and data-sensitivity risks are manageable | 5 |
| **Maximum** | **10** |

A high score means the use case has a more manageable risk profile.

**Pilot Now** also requires no “I am unsure” answer within the Risk and Governance category.

---

## 10. Category Score Calculation

Each category is converted into a percentage.

Example:

```text
Readiness score =
Readiness points achieved ÷ 35 × 100
```

An “I am unsure” answer contributes half the relevant question weight to both the overall score and the corresponding category score.

---

## 11. Prioritisation Recommendation Logic

The app applies the conditions in sequence. The first matching condition determines the result.

| Sequence | Condition | Result |
|---:|---|---|
| 1 | One or more mandatory gates answered **No** | **Foundation Required** |
| 2 | Overall score below 50 | **Hold or Reframe** |
| 3 | Mandatory gate answered **I am unsure**, and score at least 65 | **Scope Next** |
| 4 | Mandatory gate answered **I am unsure**, and score from 50 to 64 | **Foundation Required** |
| 5 | Score at least 80, Readiness at least 70, and no Readiness/Risk uncertainty | **Pilot Now** |
| 6 | Score at least 65 | **Scope Next** |
| 7 | Score from 50 to 64 | **Foundation Required** |

### Important uncertainty rule

Even when the numerical score is high, the app will not recommend **Pilot Now** when:

- a mandatory gate is uncertain;
- an Implementation Readiness question is uncertain; or
- a Risk and Governance question is uncertain.

In these cases, the result is normally **Scope Next**, provided the score is at least 65.

This prevents incomplete information from being interpreted as confirmed readiness.

---

## 12. Status Outcomes

### Pilot Now

Requirements:

- all mandatory gates are Yes;
- overall score is at least 80;
- Readiness score is at least 70;
- no Readiness question is uncertain; and
- no Risk and Governance question is uncertain.

Recommended action:

- approve a bounded pilot;
- confirm the owner and users;
- select the delivery platform;
- agree on the baseline, evaluation period and success measures; and
- retain human review.

### Scope Next

Typical reasons:

- overall score is between 65 and 79;
- the score is high but readiness is below 70;
- a mandatory gate is uncertain; or
- uncertainty remains in Readiness or Risk and Governance.

Recommended action:

- conduct focused discovery;
- gather evidence;
- confirm ownership, data, workflow, tool fit or controls; and
- reassess before pilot approval.

### Foundation Required

Typical reasons:

- a mandatory gate is answered No;
- a mandatory gate is uncertain and the score is only moderate; or
- the overall score is between 50 and 64.

Recommended action:

- assign owners to resolve foundational gaps;
- improve data and workflow readiness;
- confirm governance and capability;
- then reassess.

### Hold or Reframe

Requirement:

- overall score is below 50, unless a failed mandatory gate has already produced **Foundation Required**.

Recommended action:

- narrow the scope;
- clarify the problem;
- reconsider the solution;
- combine it with another use case; or
- defer further investment.

---

## 13. Recommended Delivery Route Logic

The delivery route is separate from the prioritisation status.

- **Status:** whether the use case should proceed now.
- **Delivery route:** the broad approach for developing it.

The route uses answers to:

- internal capability;
- existing approved tools; and
- external support.

| Key conditions | Recommended route |
|---|---|
| Internal capability = Yes and existing tools = Yes | **Business/DSPD-led configuration or prototype using existing approved tools** |
| Internal capability = Yes and existing tools = No | **Business-led custom prototype or technical discovery before formal development** |
| Internal capability = No and external support = Yes | **Collaborative prototype with GovTech, DSAD, intern, polytechnic or university support** |
| Existing tools = Yes and external support = Yes | **Configure an existing approved platform with specialist or partner support** |
| Any key route answer is uncertain and no clearer rule applies | **Delivery route requires clarification** |
| Existing tools = Yes but support is not confirmed | **Configure an existing platform after securing specialist implementation support** |
| No suitable internal, platform or partner route | **Formal discovery and system project assessment** |

A delivery-route recommendation does not override the status. A use case can have a plausible delivery route but still require foundation work or reframing.

---

## 14. Gap and Uncertainty Actions

### Questions answered No

A No answer creates a gap action, such as:

- confirm a business owner;
- refine the problem statement;
- identify data sources;
- document business rules;
- assess approved tools;
- secure internal or external capability;
- reduce the pilot scope; or
- complete privacy and security assessment.

### Questions answered I am unsure

Each uncertain answer creates a clarification action:

```text
Obtain evidence and confirm: [question]
```

The app displays:

- total uncertain answers;
- unconfirmed mandatory conditions; and
- a dedicated Clarifications Required section.

---

## 15. Input Validation

No radio option is preselected:

```python
index=None
```

The user must answer every question. If any response remains blank, the assessment stops and displays an error.

“I am unsure” should be selected instead of leaving a question unanswered when the user genuinely does not know or cannot confirm the answer.

---

## 16. Assessment Output

The app displays:

- Recommended Status
- Overall Score
- Mandatory Gates Failed
- Uncertain Answers
- Recommended Delivery Route
- category score bar chart
- Mandatory Gaps
- Unconfirmed Mandatory Conditions
- Clarifications Required
- Priority Actions
- Suggested Next Decision

---

## 17. CSV Export

The CSV includes:

| Field | Description |
|---|---|
| Use Case | Name entered in the sidebar |
| Business Unit | Business unit or team |
| Business Owner | Proposed owner |
| Status | Recommended prioritisation status |
| Overall Score | Normalised score out of 100 |
| Value Score | Business Value percentage |
| Readiness Score | Implementation Readiness percentage |
| Capability Score | Delivery Capability percentage |
| Risk Score | Risk and Governance percentage |
| Mandatory Gates Failed | Number of mandatory gates answered No |
| Mandatory Gates Uncertain | Number of mandatory gates answered I am unsure |
| Total Uncertain Answers | Total uncertainty count |
| Delivery Route | Recommended delivery approach |
| Description | Use-case description |
| Response fields | Individual Yes, I am unsure or No answer for every question |

---

## 18. Worked Example

Assume all mandatory gates are Yes.

Weighted responses produce:

- Value: 25 out of 30;
- Readiness: 28 out of 35;
- Capability: 14 out of 20;
- Risk: 10 out of 10.

Raw score:

```text
25 + 28 + 14 + 10 = 77
```

Overall score:

```text
77 ÷ 95 × 100 = 81
```

Readiness score:

```text
28 ÷ 35 × 100 = 80
```

With no uncertainty in Readiness or Risk, the result is:

> **Pilot Now**

If one Readiness answer changes from Yes to I am unsure, it receives half points. Even if the recalculated overall score remains at least 80, the uncertainty prevents Pilot Now and the likely result becomes:

> **Scope Next**

---

## 19. Interpretation Guidance

### Answer Yes only when reasonably confirmed

A Yes answer should be supported by reasonable evidence, agreement or an identifiable source.

### Use I am unsure for unresolved matters

Use I am unsure when:

- evidence is incomplete;
- the relevant owner has not confirmed;
- data access has not been checked;
- platform capability is unknown;
- an assumption is being made; or
- the assessor does not have enough knowledge.

### A high score is not formal approval

The app does not replace:

- business approval;
- budget approval;
- data-owner approval;
- architecture review;
- cybersecurity review;
- legal review;
- procurement; or
- production governance.

### A lower score is not necessarily rejection

The assessment may identify specific work needed before reassessment.

---

## 20. Customising the Rubric

Questions are stored in the `QUESTIONS` list:

```python
{
    "id": "data_available",
    "section": "3. Implementation Readiness",
    "question": "Is the required data available?",
    "help": "Guidance shown in the mouse-over tooltip.",
    "category": "Readiness",
    "weight": 10,
    "critical": False,
}
```

### Change answer multipliers

Update:

```python
ANSWER_MULTIPLIERS = {
    "Yes": 1.0,
    "I am unsure": 0.5,
    "No": 0.0,
}
```

For example, uncertainty could be made more conservative by changing its multiplier from `0.5` to `0.25`.

Any change should be tested against sample use cases and agreed by the rubric owner.

### Add a weighted question

1. Add it to `QUESTIONS`.
2. Assign a category and weight.
3. Set `critical` to `False`.
4. Add a corresponding gap action.
5. Review the thresholds and sample outcomes.

`MAX_SCORE` is recalculated automatically.

### Add a mandatory gate

Set:

```python
"weight": 0,
"critical": True
```

### Change status thresholds

Edit the status logic in `app.py`. Any threshold change should be tested against:

- clear quick wins;
- valuable but integration-heavy cases;
- low-value easy cases;
- high-risk public-facing cases; and
- cases with several uncertain answers.

---

## 21. Suggested Future Enhancements

Potential improvements include:

1. making sidebar identification fields mandatory;
2. checking consistency between the named owner field and the owner gate;
3. requiring evidence or comments for Yes and I am unsure answers;
4. comparing multiple use cases in one portfolio table;
5. displaying Value versus Readiness on a prioritisation matrix;
6. allowing controlled administration of weights and thresholds;
7. saving assessment history and reassessments;
8. recording assessor and assessment date;
9. adding management review and approval;
10. recommending specific approved tools;
11. adding cost, duration and resource estimates;
12. versioning the rubric; and
13. analysing which uncertainties occur most frequently across the portfolio.

---

## 22. Governance Recommendation

Before official use, agree on:

- question wording;
- weights and uncertainty multiplier;
- status thresholds;
- mandatory gates;
- evidence required for Yes;
- when I am unsure is acceptable;
- who owns clarification actions;
- who makes the final decision;
- review frequency; and
- exception handling.

The rubric should be reviewed as platforms, capabilities, systems and governance requirements change.

---

## 23. Disclaimer

The application provides an initial structured assessment based on user responses.

Its recommendation depends on:

- accurate answers;
- appropriate use of I am unsure;
- consistent interpretation;
- available evidence; and
- suitable business and technical review.

It should not be the sole basis for funding, procurement, production deployment or high-impact operational decisions.
