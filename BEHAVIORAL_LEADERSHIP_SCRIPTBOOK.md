# Amazon 16 Leadership Principles & FAANG Behavioral Master Scriptbook
## Candidate: Gunaseelan N | Target: L5 / L6 (SDE III / Senior SWE / Tech Lead)
*Mapped to Amazon, Google ("Googleyness"), Meta ("Move Fast & Build Quality"), and Microsoft*

---

# How to Score "Strong Hire" on FAANG Behavioral Interviews
1. **Never speak in generalities ("We did this")**: Senior and Staff candidates are evaluated on **your individual agency and scope of influence**. Always speak as *"I architected...", "I decided...", "I persuaded..."*.
2. **Quantify the outcome**: Every story MUST end with measurable business, engineering, or latency impact (e.g., "$99\%+$ sprint adherence", "$90\%$ error reduction", "$10$ engineers unblocked").
3. **Use the STAR Method**:
   * **Situation** (15%): Set the high-stakes context quickly.
   * **Task** (10%): What was your specific responsibility?
   * **Action** (60%): Technical and leadership steps YOU took.
   * **Result** (15%): Quantified metrics, long-term impact, and learnings.

---

# 1. Customer Obsession (Amazon LP #1)
> *Leaders start with the customer and work backwards. They work vigorously to earn and keep customer trust.*

### Question: "Tell me about a time you went above and beyond to solve a customer pain point."
* **Situation**: While supporting our enterprise No-Code platform at Vaken, overseas clients processing invoices and financial documents reported frequent extraction failures using our legacy OCR module, requiring manual intervention on dozens of documents daily.
* **Task**: As the technical lead, I needed to eliminate customer friction and provide a resilient, automated extraction system without requiring customers to re-format their documents.
* **Action**:
  1. I gathered raw customer sample documents that had failed (skewed tables, multi-column receipts, faded scans) and analyzed the root cause.
  2. Rather than patching fragile regex scripts, I spearheaded the **AI xChange** initiative, migrating from OCR to multimodal LLM APIs with enforced JSON schemas.
  3. Built an internal visual validation preview where customers could see real-time field mappings and confidence scores.
* **Result**: Reduced document extraction errors by over **90%**, slashed customer ticket volume for invoice processing to near zero, and increased client platform adoption across enterprise finance teams.

---

# 2. Ownership (Amazon LP #2)
> *Leaders are owners. They think long term and don’t sacrifice long-term value for short-term results. They never say 'that's not my job'.*

### Question: "Tell me about a time you took ownership of a critical issue outside your defined scope."
* **Situation**: During a critical production release of our iOS MDM Engine, the mobile engineering squad ran into intermittent device enrollment failures during network handoffs (Wi-Fi to 4G). While the backend team’s APIs were technically returning HTTP 200, the overall client onboarding experience was failing.
* **Task**: Instead of dismissing the bug as a client-side network issue, I stepped in to identify the end-to-end root cause across the boundary of mobile OS and server.
* **Action**:
  1. Set up Charles Proxy and packet capture on test iPhones to trace mutual TLS (mTLS) handshake terminations during IP address switches.
  2. Discovered that the backend session token was strictly tied to the initial client IP, terminating the enrollment session upon cellular handover.
  3. Re-architected our authentication token verification to validate device UDID identity certificates rather than transient network IPs, and coordinated with mobile teams to test across varied carrier connections.
* **Result**: Solved the enrollment drop-off, increasing initial device onboarding success from 84% to 99.8% across enterprise fleets.

---

# 3. Invent and Simplify (Amazon LP #3)
> *Leaders expect and require innovation and invention from their teams and always find ways to simplify.*

### Question: "Describe a complex problem you solved by simplifying the system."
* **Situation**: Inside the Sovablu platform, users needed to define recurring background workflows, data sync jobs, and alerts. Early proposals suggested implementing separate cron listeners for each distinct module, which would have created massive code duplication and maintenance sprawl.
* **Task**: Design a unified, platform-wide Job Scheduler component and execution framework that any component could reuse seamlessly.
* **Action**:
  1. Architected a centralized **Enterprise Job Scheduler engine** with intuitive UI configuration screens and a unified execution contract.
  2. Decoupled the scheduling definition (Cron expression / Interval) from the execution payload (Webhook / Internal Service Call / AI agent invocation).
  3. Integrated a distributed lock mechanism using Redis to ensure high availability and prevent duplicate job executions across scaled nodes.
* **Result**: Consolidated scheduling for over 5 different product domains into a single reusable framework, cutting new feature development time for automated tasks by 70%.

---

# 4. Are Right, A Lot (Amazon LP #4)
> *Leaders have strong judgment and good instincts. They seek diverse perspectives and work to disconfirm their beliefs.*

### Question: "Tell me about a time you made a difficult technical decision with incomplete information."
* **Situation**: When architecting GalaxyONE’s multi-agent code generation pipeline, the engineering team debated between using fine-tuned small open-source models versus orchestrating state-of-the-art hosted multimodal models with custom agentic tools.
* **Task**: Choose an architecture that delivered production reliability within a tight quarterly launch window.
* **Action**:
  1. I hypothesized that fine-tuning would create long-term maintenance overhead and struggle with rapid changes in enterprise UI frameworks.
  2. Ran a structured 1-week spike: built a prototype using model function calling with JSON schema enforcement against 20 complex application prompts.
  3. The prototype demonstrated that multi-agent decomposition with tool execution provided deterministic outputs and faster iteration cycles than fine-tuning.
* **Result**: We launched GalaxyONE on schedule using the multi-agent tool architecture, which allowed us to easily swap or upgrade underlying foundational models without retraining.

---

# 5. Hire and Develop the Best / People Leadership (Amazon LP #6)
> *Leaders raise the performance bar with every hire and promotion. They develop leaders and take seriously their role in coaching others.*

### Question: "How do you mentor and grow engineers on your team?"
* **Situation**: Leading a team of 10 engineers on the MDM and platform initiatives, I noticed that several junior developers were hesitant to take ownership of complex backend modules due to fear of breaking production.
* **Task**: Build engineering confidence, raise technical competence, and develop junior engineers into independent module owners.
* **Action**:
  1. Implemented **Architecture RFCs (Request for Comments)** where junior engineers authored design proposals for their features before writing code, receiving constructive peer feedback.
  2. Replaced high-stress debugging sessions with blameless post-mortems and pair programming.
  3. Assigned each junior engineer end-to-end ownership of an isolated module (e.g. file chunking, UI validation) paired with a senior mentor.
* **Result**: Over the course of 12 months, two junior developers were promoted to senior engineers, and overall PR review cycles decreased from 3.5 days to under 24 hours.

---

# 6. Have Backbone; Disagree and Commit (Amazon LP #13)
> *Leaders are obligated to respectfully challenge decisions when they disagree, even when doing so is uncomfortable or exhausting. Once a decision is determined, they commit wholly.*

### Question: "Tell me about a time you strongly disagreed with a peer or leadership decision."
* **Situation**: During a platform architecture sprint, a senior architect proposed maintaining document assets directly inside our primary relational database using `BLOB` columns to avoid managing external object storage infrastructure.
* **Task**: Convince the team that storing raw files in the relational database would catastrophically degrade database backup times and query performance under enterprise scale.
* **Action**:
  1. Rather than arguing subjectively, I created an empirical load test demonstrating database replication lag and buffer pool eviction when reading 50 concurrent 10MB files.
  2. Outlined a clear alternative architecture: **Sovablu Drive**, using object storage with pre-signed upload URLs and storing only lightweight metadata in the database.
  3. Walked through the cost difference: object storage was ~80% cheaper per gigabyte than high-IOPS provisioned database storage.
* **Result**: The team unanimously agreed to adopt the object storage architecture (Sovablu Drive), preventing severe database scaling bottlenecks down the road.
