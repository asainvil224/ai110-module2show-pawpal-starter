# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My UML design includes classes for Owner, Pet , and Task. A TaskManager handles task operations, while a Scheduler generates the daily plan based on time and priorities. The result is stored in a Schedule, with an optional AppController connecting everything to the Streamlit UI.

**b. Design changes**

Yes, there were some relationship issues that I needed to fix. The design now better supports scenarios with multiple pets and ensures proper data relationships throughout the system.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers priority, available time and task status. I prioritized constraints based on core pet care needs and simplicity, priority and available time were essential for realistic, non-overwhelming schedules, while status filtering improved relevance without complexity.


**b. Tradeoffs**

My scheduler prioritizes respecting available time vs flexibility.Tasks are added only if they fit within the owner's available time, preventing over-scheduling. This enhances realism but may leave lower-priority tasks unscheduled if high-priority ones consume the time, without options for partial scheduling or time redistribution.



---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
