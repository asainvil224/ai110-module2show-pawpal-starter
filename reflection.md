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

I used copilot to help brainstorm what classes to create and what features to implement. I then used copilot to complete repetitive tasks. Asking copilot to look over the codebase and suggest changes were helpful.


**b. Judgment and verification**

When copilot was refactoring some of the code, I didn't like how it was starting to become unreadable, so I reverted the changes. I was verifying what AI was suggesting by testing out the changes.


---

## 4. Testing and Verification

**a. What you tested**

I tested ask status changes, task counting, chronological ordering in schedules, daily recurrence creation, and conflict detection for overlapping times. These tests were important because it ensured consistant logic.


**b. Confidence**

I am 90% sure my scheduler works. If I had more time I would test for tasks with zero or excessive duration


---

## 5. Reflection

**a. What went well**

I'm satisfied with the overall output of the program.

**b. What you would improve**

I would pontentially improve the UI and refine some of the edge cases.

**c. Key takeaway**

AI is a very powerful tool that can help speed up the process of designing and implementation.
