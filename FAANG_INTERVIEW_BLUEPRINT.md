# FAANG / MANGA Senior & Staff Engineering Interview Master Blueprint
## Candidate: Gunaseelan N | Target: L5 / L6 (Senior / Staff / Technical Lead)
*Tailored for Google, Meta, Amazon, Apple, Netflix, Microsoft*

---

# The FAANG/MANGA Bar for 10+ Years Experience (L5/L6)
At FAANG, candidates with 10+ years are evaluated on three core pillars:
1. **Large Scale System Design (HLD & Deep Dives)**: Designing for hundreds of millions of users, global replication, P99 latency SLAs, partition tolerance, and cost efficiency.
2. **Coding & Data Structures (DSA)**: Flawless algorithmic problem solving in 45 minutes, clean idiomatic code, edge-case vigilance, and precise Time/Space complexity analysis.
3. **Behavioral & Leadership Principles (L6 Staff Bar)**: Amazon Leadership Principles, Google's "Googleyness & Leadership", Meta's "Move Fast & Build with Impact". Scope of influence across multiple teams.

---

# Table of Contents
1. [Part 1: Large-Scale System Design (FAANG Framework)](#part-1-large-scale-system-design-faang-framework)
2. [Part 2: Deep-Dive Design Architectures for Gunaseelan's Profile](#part-2-deep-dive-design-architectures-for-gunaseelans-profile)
   - [Design 1: Global Distributed Job Scheduler (Google Cloud Tasks / AWS EventBridge Scale)](#design-1-global-distributed-job-scheduler)
   - [Design 2: Planetary-Scale Asset & Drive Storage (Google Drive / S3 Tiering)](#design-2-planetary-scale-asset--drive-storage)
   - [Design 3: Autonomous Agentic Code-Generation Engine (Like Gemini Code Assist / GalaxyONE)](#design-3-autonomous-agentic-code-generation-engine)
   - [Design 4: Mobile Fleet Management & Notification Hub (Apple APNs & MDM Scale)](#design-4-mobile-fleet-management--notification-hub)
3. [Part 3: FAANG Algorithmic Coding Patterns (Must-Master for L5/L6)](#part-3-faang-algorithmic-coding-patterns)
4. [Part 4: Company-Specific Interview Rubrics & Strategies](#part-4-company-specific-interview-rubrics--strategies)
   - [Google (L5/L6 Senior / Staff SWE)](#google-l5l6-interview-rubric)
   - [Amazon (SDE III / Principal SDE)](#amazon-sde-iii-interview-rubric)
   - [Meta (E5/E6 Senior / Staff SWE)](#meta-e5e6-interview-rubric)
   - [Apple & Microsoft](#apple--microsoft-rubric)
5. [Part 5: FAANG Behavioral Master Stories (STAR Framework mapped to Amazon 16 LPs)](#part-5-faang-behavioral-master-stories)

---

# Part 1: Large-Scale System Design (FAANG Framework)

When a FAANG interviewer asks a design question (e.g., *"Design an enterprise scheduler"* or *"Design Google Drive"*), they give you an ambiguous 1-line prompt. Use this **4-Step FAANG Rubric (45 minutes)**:

```
┌────────────────────────────────────────────────────────┐
│ 1. Requirements & Back-of-Envelope (0 - 8 mins)        │
│    - Functional & Non-Functional Requirements          │
│    - DAU, QPS, Storage, Read/Write Ratio, Latency SLA  │
├────────────────────────────────────────────────────────┤
│ 2. High-Level Architecture & API Design (8 - 20 mins)  │
│    - Core Components, Data Flow, Data Schemas (SQL/NoSQL)│
├────────────────────────────────────────────────────────┤
│ 3. Deep-Dive Core Bottlenecks (20 - 38 mins)           │
│    - Concurrency, Partitioning, Caching, Consensus     │
│    - Failure Scenarios, Data Consistency & Idempotency │
├────────────────────────────────────────────────────────┤
│ 4. Wrap-up, Bottlenecks & Metrics (38 - 45 mins)       │
│    - Monitoring, P99 Latency, Disaster Recovery        │
└────────────────────────────────────────────────────────┘
```

### Essential Back-of-the-Envelope Math (Memorize This)
* $1 \text{ day} \approx 86,400 \text{ seconds} \approx 10^5 \text{ seconds}$.
* $100 \text{ Million Daily Active Users (DAU)}$, each making 10 requests/day:
  $$\text{Average QPS} = \frac{10^8 \times 10}{10^5} = 10,000 \text{ requests/sec}$$
  $$\text{Peak QPS} = 2 \times \text{Average QPS} = 20,000 \text{ requests/sec}$$
* Storage: $10^8 \text{ users} \times 1\text{MB/day} \approx 100\text{TB/day} \approx 36.5\text{PB/year}$.
* Latency numbers:
  * L1 cache reference: $\sim 1 \text{ ns}$
  * Main memory (RAM) reference: $\sim 100 \text{ ns}$
  * SSD random read: $\sim 100 \text{ } \mu\text{s}$
  * Cross-datacenter round trip (US to Europe): $\sim 150 \text{ ms}$

---

# Part 2: Deep-Dive Design Architectures for Gunaseelan's Profile

## Design 1: Global Distributed Job Scheduler
*(Ties directly to your Sovablu Scheduler experience)*

### 1. Requirements:
* **Functional**: Support recurring (Cron) and one-time delayed jobs; execute jobs with at-least-once or exactly-once semantics; support custom job payloads and callbacks.
* **Non-Functional**: Scalable to $10^8$ jobs/day ($1,000$ to $5,000$ triggers/sec), high availability ($99.99\%$), execution latency $< 1\text{s}$ of scheduled time.

### 2. High-Level Architecture:
```
                                 [Client API Requests]
                                           │
                                           ▼
                                   [API Gateway & Auth]
                                           │
                                           ▼
                                 [Job Management Service]
                                           │
                        ┌──────────────────┴──────────────────┐
                        ▼                                     ▼
             [Primary Database: PostgreSQL]            [Metadata Cache]
             (Job definition, Owner, History)          (Redis / Memcached)
                        │
                        ▼
                 [Time-Bucket Partition Engine]
                        │
                        ▼
            [Redis Cluster ZSET (Sorted Sets)]
         (Key: "schedule:bucket:timestamp", Score: Epoch)
                        │
                        ▼
               [Poller / Dispatcher Fleet]
                        │
                        ▼
           [Distributed Queue: Kafka / SQS]
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
 [Worker Pool 1]  [Worker Pool 2]  [Worker Pool 3]
       │                │                │
       └────────────────┼────────────────┘
                        ▼
          [Dead-Letter Queue (DLQ) & Alerting]
```

### 3. FAANG Deep-Dive Points (What gets you an L6 hire decision):
1. **Time-Wheel / Redis ZSet Sharding**:
   * If millions of jobs trigger at the top of the hour (e.g. 09:00:00), a single Redis instance gets overwhelmed.
   * **Solution**: Hash slot sharding into $N$ buckets: `bucket_id = hash(job_id) % N`. Each poller thread only inspects its assigned bucket (`ZRANGEBYSCORE bucket_3 0 <current_time>`).
2. **Distributed Locking & Double Execution Prevention**:
   * Use **Redis Redlock** or database `SELECT ... FOR UPDATE SKIP LOCKED`.
   * Ensure workers are **idempotent**: Assign each execution a unique `idempotency_key = hash(job_id + scheduled_time)`. Before execution, write key to Redis with a TTL; if already present, skip.
3. **Handling Long-Running vs Quick Tasks**:
   * Separate queue tiers: **Fast Lane** ($< 2\text{s}$ tasks) and **Slow Lane** ($> 30\text{s}$ batch tasks) to prevent head-of-line blocking.

---

## Design 2: Planetary-Scale Asset & Drive Storage
*(Ties to your Sovablu Drive & File Framework experience)*

### 1. Requirements:
* Support file uploads, downloads, automatic folder hierarchies, deduplication, thumbnailing, and access control lists (ACLs). Scale to 500 Million users.

### 2. Deep-Dive Concepts:
```
           [Client] ──(1. Initiate Upload)──> [Metadata API Server]
              │                                      │
              │                               (2. Verify Quota &
              │                               Generate Signed URLs)
              │                                      │
              │ <──(3. Return Pre-signed URLs)───────┘
              │
              ├──(4. Upload Chunks directly in parallel)──> [Object Storage (S3 / GCS)]
                                                                    │
                                                           (5. Storage Event Hook)
                                                                    │
                                                                    ▼
                                                            [Kafka Event Topic]
                                                                    │
                                                  ┌─────────────────┼─────────────────┐
                                                  ▼                 ▼                 ▼
                                            [Virus Scan]     [Transcode Worker] [Search Indexer]
```

1. **Chunked & Resumable Upload Protocol (TUS Protocol)**:
   * Files larger than 20MB are split into 4MB chunks client-side.
   * If a connection drops after uploading 85% of a 2GB video, the client asks the server for the byte offset and resumes without restarting from scratch.
2. **Block-Level Content-Addressable Storage (CAS) Deduplication**:
   * Compute SHA-256 hash for each chunk. If an identical chunk already exists in storage (e.g. popular corporate template), save metadata pointer only, reducing physical storage consumption by up to 30%.
3. **Consistent Hashing for Metadata**:
   * Distribute folder tree metadata across database shards using consistent hashing on `user_id`.

---

## Design 3: Autonomous Agentic Code-Generation Engine
*(Directly ties to your GalaxyONE & Prompt Orchestration experience)*

### 1. Requirements:
* Convert user natural-language specifications into full-stack enterprise code and database schemas. Manage multi-agent coordination, tool execution, context window budgets, and hallucination safeguards.

### 2. High-Level Multi-Agent Loop:
```
                       [User Natural Language Prompt]
                                     │
                                     ▼
                       [Agent Orchestration Gateway]
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │      Supervisor / Router Agent      │
                  │   (Deconstructs into Task Graph)    │
                  └──────────────────┬──────────────────┘
                                     │
                 ┌───────────────────┼───────────────────┐
                 ▼                   ▼                   ▼
         [Data Schema Agent] [Business Logic Agent] [UI Layout Agent]
                 │                   │                   │
                 └───────────────────┼───────────────────┘
                                     │
                                     ▼
                      [Agent Tool Execution Sandbox]
                      (Docker / Firecracker MicroVM)
                         - Run migrations
                         - Execute JUnit tests
                         - Validate JSON Schema
                                     │
                                     ▼
                    [Output Verification & Reflection]
                     Passed? ──No──> Feedback loop to Agent
                        │
                       Yes
                        ▼
           [Commit to Production Workspace / Visual Designer]
```

### 3. FAANG Deep-Dive Points:
1. **Managing State & Context Window Exhaustion**:
   * Pass only relevant sub-schemas to domain agents rather than the entire codebase. Use a shared **Vector Index + Semantic Graph** to retrieve only the schema context relevant to the prompt.
2. **Deterministic Output Guarantees**:
   * Never rely on free-form text. Use constrained decoding with JSON Schema enforcement.
3. **Execution Sandbox Security**:
   * Agentic tools executing code must run in isolated **Firecracker MicroVMs** or gVisor sandboxes with no root privileges and strict network egress rules to prevent SSRF and security vulnerabilities.

---

# Part 3: FAANG Algorithmic Coding Patterns

At the L5/L6 level, coding interviews test your speed, code readability, and mastery of core algorithmic patterns. Focus your practice on these top 6 patterns:

### 1. Two Pointers & Sliding Window
* **Use Case**: Substrings, arrays, contiguous sequence problems.
* **Classic Problems**:
  * *Longest Substring Without Repeating Characters* (LeetCode 3)
  * *Minimum Window Substring* (LeetCode 76)
  * *Trapping Rain Water* (LeetCode 42)

### 2. Fast & Slow Pointers / Monotonic Stack
* **Use Case**: Cycle detection, next greater element, histogram areas.
* **Classic Problems**:
  * *Daily Temperatures* (LeetCode 739)
  * *Largest Rectangle in Histogram* (LeetCode 84)

### 3. Breadth-First Search (BFS) & Depth-First Search (DFS) on Graphs
* **Use Case**: Shortest paths in unweighted graphs, connected components, dependency resolution (Topological Sort).
* **Classic Problems**:
  * *Word Ladder* (LeetCode 127)
  * *Course Schedule I & II* (LeetCode 207, 210) — directly mirrors job scheduling dependencies!
  * *Number of Islands* (LeetCode 200)

### 4. Dynamic Programming & Memoization
* **Use Case**: Optimization problems with overlapping subproblems and optimal substructure.
* **Classic Problems**:
  * *Coin Change* (LeetCode 322)
  * *Longest Increasing Subsequence* (LeetCode 300)
  * *Word Break* (LeetCode 139)

### 5. Heap / Priority Queue (Top 'K' Elements)
* **Use Case**: Stream processing, finding median in real time, task scheduling.
* **Classic Problems**:
  * *Merge k Sorted Lists* (LeetCode 23)
  * *Find Median from Data Stream* (LeetCode 295)
  * *Task Scheduler* (LeetCode 621)

### 6. Trie & String Processing
* **Use Case**: Autocomplete, prefix matching, word search.
* **Classic Problems**:
  * *Implement Trie* (LeetCode 208)
  * *Word Search II* (LeetCode 212)

---

# Part 4: Company-Specific Interview Rubrics & Strategies

## Google (L5/L6 Senior / Staff SWE)
* **Interview Loop Breakdown**:
  * 2 System Design rounds (1 HLD + 1 Data/API/Domain specific).
  * 2-3 Coding rounds (Focus on graphs, dynamic programming, clean edge-case handling).
  * 1 "Googlyness & Leadership" round.
* **Google Evaluator Expectations**:
  * Google cares deeply about **correctness and scalability at massive data volume**.
  * Always address: What happens if an entire datacenter region goes dark? How do you partition data across thousands of machines?

## Amazon (SDE III / Principal SDE)
* **Interview Loop Breakdown**:
  * 1 Bar Raiser round (Senior leader from a different organization).
  * 2 System Design rounds.
  * 1 Coding / Data Structures round.
  * **Every single round** spends 20–25 minutes solely on **Amazon Leadership Principles (LPs)**!
* **Key LPs to Master**:
  * *Customer Obsession*: Designing systems with customer impact as the north star.
  * *Ownership*: Stepping up when something broke outside your direct responsibility.
  * *Invent and Simplify*: Simplifying complex architectures (e.g. migrating OCR to GenAI).
  * *Deliver Results*: Meeting strict enterprise deadlines with high quality.

## Meta (E5/E6 Senior / Staff SWE)
* **Interview Loop Breakdown**:
  * 2 System Design rounds (Speed is essential: Meta expects you to move fast and cover API, schema, and scaling within 35 minutes).
  * 2 Coding rounds (Speed-intensive: usually 2 LeetCode mediums in 45 minutes).
  * 1 Behavioral round (Focus on: Driving ambiguous initiatives and resolving interpersonal conflicts).
* **Meta Evaluator Expectations**:
  * "Move fast with stable infrastructure." Show that you choose pragmatic, high-impact solutions over over-engineered ones.

## Apple & Microsoft
* **Apple**: Team-specific hiring. Deep questions on **OS fundamentals, concurrency, memory management, and end-to-end device/server integration** (Your Apple MDM experience will be a huge advantage here).
* **Microsoft**: High focus on enterprise architecture, cloud scale (Azure), microservices, API backward compatibility, and team mentoring.

---

# Part 5: FAANG Behavioral Master Stories

Use the **STAR (Situation, Task, Action, Result)** structure with quantified outcomes.

### Story 1: Invent & Simplify / Technical Innovation
* **Company LP Fit**: Amazon (*Invent and Simplify*), Google (*Technical Innovation*), Meta (*Move Fast*).
* **Situation**: In our enterprise platform, document data extraction relied on traditional OCR and manual regex parsers. Customers regularly encountered broken parses on varied invoices, costing dozens of hours in manual support.
* **Task**: Modernize the extraction architecture to achieve high reliability without blowing cloud operating costs.
* **Action**:
  * Evaluated traditional OCR fine-tuning vs. Multimodal GenAI extraction through an empirical benchmark of 100 enterprise invoice formats.
  * Engineered a hybrid pipeline: used fast OCR for digital text verification and routed complex unstructured documents to Multimodal LLMs with enforced JSON Schemas.
  * Implemented prompt caching and rate-limiting to protect backend latency.
* **Result**: Reduced extraction errors by over 90%, cut customer onboarding configuration time from days to minutes, and established the foundational pattern for our AI xChange component.

### Story 2: Deliver Results / Navigating Ambiguity under High Stakes
* **Company LP Fit**: Amazon (*Deliver Results*, *Bias for Action*), Google (*Leadership*).
* **Situation**: When architecting the iOS MDM Engine at Vaken, our enterprise client required strict compliance with Apple MDM protocols with a firm launch deadline. The protocols had intricate cryptographic payload specs and zero margin for error.
* **Task**: Lead a 10-engineer team to architect, build, and deliver the backend engine on schedule.
* **Action**:
  * Decomposed Apple's technical documentation into clear API contracts and modular sprint epics.
  * Set up automated CI/CD pipelines, strict code reviews, and paired senior developers with junior teammates.
  * Ran weekly technical demos with overseas client leadership to clear requirement doubts proactively.
* **Result**: Delivered 100% on schedule with 99%+ sprint milestone adherence, zero critical production vulnerabilities, and earned client renewal for expanded enterprise modules.

### Story 3: Have Backbone; Disagree and Commit
* **Company LP Fit**: Amazon (*Have Backbone*), Meta (*Resolve Conflict*).
* **Situation**: During a platform architecture review, a proposal was made to build a complex distributed scheduler entirely from scratch using raw database polling rather than leveraging Redis and existing message queues.
* **Task**: Advocate for a scalable, maintainable architecture while maintaining strong team alignment.
* **Action**:
  * Avoided emotional debate; presented a benchmark analysis showing how raw DB polling would degrade database CPU under high concurrency.
  * Demonstrated that using Redis Sorted Sets with distributed locking would provide sub-second trigger accuracy with significantly lower operational overhead.
  * Partnered with the proposing engineer to co-author the final RFC, incorporating their ideas for custom error callbacks.
* **Result**: The team unanimously adopted the Redis-backed architecture, saving estimated weeks of bespoke concurrency debugging and delivering rock-solid job execution in production.

---

# Part 6: Daily FAANG Preparation Roadmap (8-Week Plan)

```
┌────────────────────────────────────────────────────────────────────────┐
│ Weeks 1 - 3: Coding & DSA Patterns                                     │
│ - 2 LeetCode Mediums daily (Sliding Window, Trees, Graphs, DP).        │
│ - Practice writing clean code on a whiteboard or plain Google Doc.     │
├────────────────────────────────────────────────────────────────────────┤
│ Weeks 4 - 6: System Design Mastery                                     │
│ - Practice 1 complete system design every 2 days.                      │
│ - Master: Distributed Scheduler, Cloud Drive, Notification Hub,        │
│   Rate Limiter, Key-Value Store, and Chat System.                      │
├────────────────────────────────────────────────────────────────────────┤
│ Weeks 7 - 8: Behavioral (STAR Stories) & Mock Interviews               │
│ - Write down and rehearse your 6 core STAR stories out loud.           │
│ - Conduct 3-5 peer or platform mock interviews for HLD and Coding.     │
└────────────────────────────────────────────────────────────────────────┘
```
