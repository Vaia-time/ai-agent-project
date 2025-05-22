
# Overview

This project is part of the Agent Development Kit Hackthon create by google.

We will be using this to write a simple app using ai agents to write politicians biographies.

It will consist on 4 agents (Planer, Researcher, Biography Writer, Reviewer) which will work together to write biographies based on a given name.

## Diagram
```mermaid
flowchart LR
    A[Planer] -->|Web_search| B(Researcher)
    B --> |Scraper| C(Biography Writer)
    C --> D{Reviewer}
    D --> |Approved| E[Output]
    D --> |Reject| A
  
```

## Key Features
### Tools:

- **Web_search:**
- **Scraper:**

### Agents:

- **Planer:**
- **Researcher:**
- **Biography Writer:**
- **Reviewer:**



## Requirements

The biographies should contain the following sections:

- Bio
- Early Life
- Professional Career
- Political Career
- Personal Life


### Bio
The Bio serves as a concise introduction to the politician, summarizing their current role, party affiliation, and key political positions.

**Key Elements:**
- Full name (including titles, if applicable)
- Political party
- Current or most significant political role
- Constituency (if applicable)
- Brief mention of major achievements or historical significance


### Early Life
This section provides background on the politician’s upbringing, education, and formative influences.

**Key Elements:**
- Date and place of birth
- Family background (parents’ professions, influence on political views)
- Education (schools, universities, notable achievements)
- Early political inclinations (if relevant)


### Professional Career
This section outlines the politician’s career before entering politics, highlighting key roles and achievements.

**Key Elements:**
- Major jobs (law, finance, media, etc.)
- Notable positions (e.g., barrister, CEO, journalist)
- Significant accomplishments (awards, recognitions)

### Political Career
This is the most detailed section, covering the politician’s journey in politics, key roles, elections, and major policy stances.

**Key Elements:**
- Entry into politics (first election, party affiliation)
- Key positions held (minister, party leader, etc.)
- Major political moments (leadership contests, resignations, policy shifts)
- Electoral successes and failures
- Impact on party and country

### Personal Life
This section humanizes the politician, covering family, hobbies, and personal beliefs.

**Key Elements:**
- Marital status and children
- Hobbies and interests
- Religious or ethical beliefs
- Any notable personal controversies (if relevant)


## Important Notes
- Accuracy: Always fact-check dates, titles, and key events.
- Neutral Tone: Avoid opinionated language; maintain an objective journalistic style.
- Consistency: Follow this structure for all biographies to ensure uniformity.