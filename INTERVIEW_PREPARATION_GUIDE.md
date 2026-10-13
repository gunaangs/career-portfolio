# Complete Interview Preparation Master Guide
## Gunaseelan N — Lead Software Engineer / Technical Architect
*Specializations: Agentic AI Systems, Enterprise Platforms (No-Code Core), Distributed Systems (Java/Spring), Mobile (React Native/Android)*

---

# Table of Contents
1. [Module 1: Agentic AI & GenAI Systems Deep-Dive](#module-1-agentic-ai--genai-systems-deep-dive)
2. [Module 2: High-Level System Design (HLD) Master Architectures](#module-2-high-level-system-design-hld-master-architectures)
3. [Module 3: Java, Concurrency & Spring Boot Enterprise Engineering](#module-3-java-concurrency--spring-boot-enterprise-engineering)
4. [Module 4: Mobile & Full-Stack Architecture (React Native & React)](#module-4-mobile--full-stack-architecture-react-native--react)
5. [Module 5: Engineering Leadership, Behavioral & STAR Stories](#module-5-engineering-leadership-behavioral--star-stories)
6. [Module 6: Top 30 Rapid-Fire Technical Questions & Ideal Answers](#module-6-top-30-rapid-fire-technical-questions--ideal-answers)

---

# Module 1: Agentic AI & GenAI Systems Deep-Dive

As a contributor to **GalaxyONE** and **AI xChange**, interviewers will expect you to be significantly ahead of typical candidates who only know basic prompt wrappers.

```
       [User Intent / Plain Language Spec]
                       │
                       ▼
         ┌───────────────────────────┐
         │  GalaxyONE Solution Engine│
         │ (Supervisor / Planner)    │
         └─────────────┬─────────────┘
                       │ Task Decomposition
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Data Copilot │ │Logic Copilot │ │Layout Copilot│
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
┌────────────────────────────────────────────────┐
│             Tool Calling Execution             │
│ (Schema Generator, Rule Engine, UI Synthesizer)│
└───────────────────────┬────────────────────────┘
                        │
                        ▼
          [Direct Visual Artifact Output]
         (Data, Logic & UI Visual Designers)
```

### 1.1 What is an Agentic Workflow vs. Standard LLM Prompting?
* **Standard Prompting**: A stateless, single-turn request-response pattern (`Input Prompt -> LLM -> Output Text`). Has no ability to verify truth, inspect environments, or correct errors.
* **Agentic System**: An autonomous loop where the LLM acts as the **reasoning engine**. It breaks down high-level intent into multi-step execution plans:
  $$\text{Perceive} \longrightarrow \text{Reason / Plan} \longrightarrow \text{Tool Action} \longrightarrow \text{Observe Environment} \longrightarrow \text{Reflect \& Self-Correct}$$
* **Core Loops**:
  * **ReAct (Reason + Act)**: Interleaves chain-of-thought reasoning with tool actions.
  * **Plan-and-Solve**: Generates the complete task DAG (directed acyclic graph) first, then invokes specialized sub-agents.

### 1.2 Multi-Agent Architecture (GalaxyONE Paradigm)
* **The Coordinator / Supervisor Pattern**: A top-level *Solution Copilot* decomposes complex enterprise system requirements (e.g., "Build an Inventory Approval Workflow with Email Alerts") into specialized domains.
* **Domain Copilots**:
  * **Data Copilot**: Generates ER diagrams, normalizes schemas, verifies foreign keys and data types.
  * **Logic Copilot**: Converts natural business rules into code-free decision tables and workflow state machines.
  * **Layout Copilot**: Maps wireframes and form requirements to responsive UI component trees.
* **Inter-Agent Communication**: Pass structured context via JSON payloads; maintain a central shared blackboard or state store.

### 1.3 Custom Agentic Tool Creation & Function Calling
* **Tool Contract**: Tools are exposed to the LLM via standardized JSON Schema specifying tool name, description, parameters, required fields, and constraints.
* **The Execution Loop**:
  1. User prompt + available tool schemas are sent in the API request.
  2. LLM returns a structured `tool_calls` object instead of prose:
     ```json
     {
       "name": "create_table_schema",
       "arguments": {
         "table_name": "invoices",
         "columns": [
           {"name": "id", "type": "UUID", "primary_key": true},
           {"name": "amount", "type": "DECIMAL(12,2)"}
         ]
       }
     }
     ```
  3. Your backend executes the function natively, validates constraints, and captures standard output or error codes.
  4. The result is appended to the message array (`role: "tool"`) and re-sent to the LLM to complete execution or take corrective action.

### 1.4 AI xChange: OCR to GenAI Migration (Case Study)
* **The Problem with Legacy OCR**:
  * Traditional OCR engines (Tesseract, pure heuristic OCR) only return raw spatial text coordinates bounding boxes.
  * Extracting nested key-value pairs, multi-line invoice line items, tilted tables, or varied receipts required brittle regex scripts that broke whenever vendor formats changed.
* **The Modern Multimodal GenAI Solution**:
  * Send document images directly to multimodal LLMs (e.g., Claude 3.5 Sonnet, GPT-4o, Gemini 1.5 Pro) with strict **Structured Output enforcement** (JSON schema / Instructor / Pydantic).
  * **Hybrid Strategy for Scale & Cost**:
    * Run lightweight OCR first to check for high-confidence machine-printed text or digital PDF streams.
    * Route complex, ambiguous, or handwritten documents to Multimodal LLMs.
    * Use cached prompt templates to minimize token overhead and latency.
* **Accuracy Improvement**: Error rates on nested invoice tables typically drop from ~18-25% down to under 2%.

---

# Module 2: High-Level System Design (HLD) Master Architectures

## Architecture 1: Enterprise Distributed Job Scheduler
*(Directly showcases your Sovablu Scheduler screen & engine work)*

```
[Web Admin UI] ──(REST)──> [API Gateway]
                                 │
                                 ▼
                     [Scheduler Service Cluster]
                     (Cron parser, DAG Builder)
                                 │
               ┌─────────────────┴─────────────────┐
               ▼                                   ▼
        [PostgreSQL / MySQL]               [Redis Cluster]
     (Persistent Job Definitions)     (Distributed Lock & ZSet Timer)
               │                                   │
               └─────────────────┬─────────────────┘
                                 ▼
                    [Queue: RabbitMQ / Kafka]
                                 │
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
    [Worker Node 1]        [Worker Node 2]        [Worker Node 3]
    (Executes Tasks)       (Executes Tasks)       (Executes Tasks)
          │                      │                      │
          └──────────────────────┴──────────────────────┘
                                 │
                     [Dead Letter Queue / Alerting]
```

### Key Technical Talking Points:
1. **Preventing Double Execution**:
   * Use **Distributed Locks via Redis** (`SET key token NX PX 30000`) or database row-level locking (`SELECT ... FOR UPDATE SKIP LOCKED`).
2. **Scheduling Mechanism**:
   * Store pending tasks in a **Redis Sorted Set (ZSET)** where the score is the `epoch_execution_timestamp`.
   * Leader workers poll `ZRANGEBYSCORE key 0 <current_time> LIMIT 0 N` to pull tasks ready to trigger.
3. **Fault Tolerance & Heartbeats**:
   * Workers send heartbeats every 10 seconds. If a worker dies mid-job, the supervisor timeout expires and pushes the job back to the queue for retry.
4. **Idempotency**:
   * Every scheduled execution has a unique `ExecutionId = hash(JobId + ScheduledTimestamp)`. Workers record execution start and end in a deduplication table.

---

## Architecture 2: Cloud Asset & File Management Engine (Sovablu Drive)

```
[Client App] ──1. Request Upload URL──> [Asset API Service]
     │                                           │
     │ <──2. Pre-signed S3/GCS Upload URL────────┘
     │
     └──3. Direct Chunked Binary Stream (S3/GCS/MinIO)──> [Object Storage]
                                                                │
                                                4. Upload Event Notification
                                                                ▼
                                                      [Kafka / Event Hub]
                                                                │
                                       ┌────────────────────────┼────────────────────────┐
                                       ▼                        ▼                        ▼
                                [Virus Scanner]         [Thumbnail Worker]      [Metadata Indexer]
                                (ClamAV)                (Image/Video transcode) (PostgreSQL & Elasticsearch)
```

### Key Technical Talking Points:
1. **Pre-signed Upload URLs**:
   * Avoid bottlenecking application servers with gigabytes of raw binary files. The backend generates a cryptographically signed upload URL; client streams directly to object storage.
2. **Chunked / Resumable Uploads**:
   * Break large files into 5MB chunks. Each chunk is verified via MD5/SHA-256 hash. If network drops on chunk 14 of 20, the client resumes from chunk 14.
3. **Deduplication**:
   * Calculate SHA-256 hash of the entire payload before storage. If hash exists, point metadata pointer to existing block storage rather than duplicating bytes.
4. **Access Control & Multi-Tenancy**:
   * Files mapped to Tenant ID and workspace ACLs (Access Control Lists). Download links are ephemeral, short-lived signed URLs (valid for 5–15 minutes).

---

## Architecture 3: Mobile Device Management (MDM) Engine
*(Reflects your iOS Apple MDM and Android Management API experience)*

```
[IT Admin Web Console]
          │
          ▼
   [MDM Core API] ──(Push Notification Trigger)──> [Apple APNs / Google FCM]
          │                                                    │
     [Command Queue]                                     Silent Push Wakeup
     (Enrollment, Lock, Profile)                               │
          │                                                    ▼
          └───────────HTTP Poll for Pending Commands──────── [Managed Device]
                      (Cert-based Mutual TLS)            (iOS / Android Kiosk)
```

### Key Technical Talking Points:
1. **Asynchronous Command Architecture**:
   * Mobile devices cannot maintain open server sockets 24/7 due to battery and network constraints.
   * Server sends a lightweight silent push packet through **APNs / FCM**.
   * The device wakes up in the background and initiates a **Mutual TLS (mTLS)** HTTPS session to fetch queued commands.
2. **Command State Machine**:
   * Status transitions: `Queued -> Sent -> Acknowledged -> Executed -> Error`.
3. **Kiosk Mode / Lockdown Enforcement**:
   * Android Enterprise Device Owner mode: Disables status bar, disables USB file transfer, pins app package via `startLockTask()`.

---

# Module 3: Java, Concurrency & Spring Boot Enterprise Engineering

### 3.1 Concurrency & Multithreading
* **Java Memory Model (JMM)**:
  * `volatile`: Guarantees visibility across CPU caches and prevents instruction reordering; does **not** guarantee atomicity (e.g., `count++` is not atomic).
  * `AtomicInteger` / `AtomicReference`: Leverage hardware-level Compare-And-Swap (CAS) instructions for non-blocking thread-safety.
* **Thread Pool Tuning (`ThreadPoolExecutor`)**:
  * Four critical parameters: `corePoolSize`, `maximumPoolSize`, `keepAliveTime`, and `workQueue` (ArrayBlockingQueue vs LinkedBlockingQueue).
  * **Rule of Thumb**:
    $$\text{CPU-bound tasks}: N_{\text{threads}} = N_{\text{cores}} + 1$$
    $$\text{I/O-bound tasks}: N_{\text{threads}} = N_{\text{cores}} \times \left(1 + \frac{\text{Wait Time}}{\text{Compute Time}}\right)$$
* **Virtual Threads (Project Loom / Java 21+)**:
  * Unlike OS-managed platform threads (heavyweight, ~1MB stack), virtual threads are managed by the JVM (~few hundred bytes). Perfect for high-concurrency blocking I/O (REST API calls, DB queries).

### 3.2 Spring Boot & Microservices Best Practices
* **Bean Scopes**: `singleton` (default), `prototype`, `request`, `session`.
* **Transaction Management (`@Transactional`)**:
  * How it works: Dynamic proxy wrapping target method with JDBC transaction commit/rollback.
  * **Gotcha**: Calling a `@Transactional` method from within the same class bypasses the proxy; transactional semantics will fail unless self-injected or delegated to another bean.
  * Propagation levels: `REQUIRED` (default), `REQUIRES_NEW` (runs in isolated autonomous transaction).
* **Resilience Patterns**:
  * **Circuit Breaker** (Resilience4j): Opens circuit when failure rate exceeds threshold (e.g. 50% over 10 calls) to prevent cascading system collapse.
  * **Rate Limiting**: Token bucket or Leaky bucket algorithm via Redis to prevent noisy neighbor degradation.

---

# Module 4: Mobile & Full-Stack Architecture (React Native & React)

### 4.1 React Native Deep Architecture
* **Old Architecture vs New Architecture**:
  * **Old**: JavaScript Thread $\longleftrightarrow$ Asynchronous JSON Bridge $\longleftrightarrow$ Native Thread. Serializing JSON over the bridge caused performance stutter during high-frequency gestures or animations.
  * **New Architecture**:
    * **JSI (JavaScript Interface)**: JS can hold direct C++ host references to native objects without JSON stringification.
    * **Fabric Renderer**: Unified C++ core rendering pipeline supporting concurrent rendering and synchronous layout measurements.
    * **TurboModules**: Native modules loaded lazily on demand instead of loading everything upfront at app startup.

### 4.2 Security & Offline-First Mobile Design
*(Directly relates to your Secure Notes & MoneyWise apps)*
* **Cryptographic Storage**:
  * Key generation using PBKDF2 or Argon2 password hashing.
  * AES-256-GCM symmetric encryption for payload confidentiality and integrity authentication.
  * Store root encryption keys inside hardware-backed storage (**Android Keystore / iOS Keychain**), guarded by Biometric Prompt (`BiometricManager.Authenticators.BIOMETRIC_STRONG`).
* **Offline Reconciliation**:
  * SQLite/Room as the single source of truth locally.
  * Append-only transaction log with monotonic version timestamps (`updated_at`, `is_deleted` soft-delete flag) to resolve concurrent server sync conflicts using Last-Write-Wins (LWW) or CRDTs.

---

# Module 5: Engineering Leadership, Behavioral & STAR Stories

As a Team Leader of 10 engineers, interviewers want to see how you think about delivery, people, and engineering culture.

### Story 1: Mentoring 10 Engineers & High-Stakes Deadline Delivery
* **Situation**: We were delivering the core iOS MDM Engine for an international enterprise customer with hard contractual milestones. Several junior engineers were unfamiliar with Apple’s binary MDM payload specs and mobile security standards.
* **Task**: Ensure zero milestone slips while maintaining strict security compliance and code quality across 10 developers.
* **Action**:
  1. Broke down complex Apple documentation into modular developer RFCs and API contracts.
  2. Implemented automated PR checks, JUnit coverage standards, and paired senior developers with junior teammates.
  3. Instituted daily 15-minute standups focused exclusively on unblocking dependency bottlenecks.
* **Result**: Achieved 99%+ sprint milestone adherence, zero critical defects in production release, and two junior engineers grew into autonomous module owners.

### Story 2: Technical Disagreement / Architecture Choice
* **Situation**: When architecting document extraction for AI xChange, the team was divided between tuning legacy OCR regex rules vs. migrating to modern GenAI/LLM-enabled endpoints.
* **Task**: Lead technical decision-making with objective benchmarks rather than subjective opinions.
* **Action**:
  1. Set up an empirical proof-of-concept (PoC) testing 100 varied invoice layouts (skewed tables, low contrast, receipts).
  2. Measured extraction accuracy, API latency, and operational cost per 1,000 pages for both approaches.
  3. Demonstrated that while GenAI cost slightly more per call, it reduced manual exception verification by 85%, creating a massive net ROI.
* **Result**: Team unanimously aligned on the GenAI migration path, accelerating feature release by two months.

---

# Module 6: Top 30 Rapid-Fire Technical Questions & Ideal Answers

### Agentic AI & GenAI
1. **How do you prevent an AI agent from entering an infinite loop?**
   * *Answer:* Enforce a strict `max_iterations` counter, track cyclic tool call signatures, and implement timeout breakers.
2. **What is the difference between RAG and Agentic RAG?**
   * *Answer:* Standard RAG retrieves once upfront. Agentic RAG allows the model to inspect initial search results, realize if data is insufficient, reformulate its query, and retrieve again across multiple sources.
3. **How do you handle context window limits when agents generate large artifacts?**
   * *Answer:* Chunk generation, maintain state in external databases, and summarize conversational history before passing to next agent loops.
4. **Why use structured outputs over plain text parsing?**
   * *Answer:* Structured outputs enforce JSON schemas natively through constrained token decoding at the model engine level, guaranteeing valid parsing without regex breakage.

### System Design & Concurrency
5. **How do you scale a database write bottleneck?**
   * *Answer:* Sharding / horizontal partitioning by tenant ID, queueing writes via Kafka, batch inserts, and offloading reads to replicas.
6. **What is the difference between optimistic and pessimistic locking?**
   * *Answer:* Optimistic uses version columns (`WHERE version = 1`), best for low write contention. Pessimistic locks database rows (`SELECT FOR UPDATE`), best for high-contention financial ledgers.
7. **Explain the CAP theorem.**
   * *Answer:* In a distributed data store with network partitioning (P), you must choose between Consistency (C) (all nodes see latest data) or Availability (A) (every request receives a response, but may be stale).
8. **How does Redis achieve high performance despite being single-threaded?**
   * *Answer:* In-memory operations, non-blocking I/O multiplexing (`epoll`), and avoidance of thread context-switching overhead.

### Java & Spring
9. **Difference between `HashMap` and `ConcurrentHashMap`?**
   * *Answer:* `HashMap` is not thread-safe. `ConcurrentHashMap` uses bucket-level synchronized locks and CAS operations, allowing concurrent reads without blocking and fine-grained concurrent writes.
10. **What is garbage collection stop-the-world pause?**
    * *Answer:* Phase during GC mark/sweep where application threads are temporarily halted to accurately trace live object references.
11. **Difference between `@Component`, `@Service`, and `@Repository`?**
    * *Answer:* Functionally all are Spring stereotypes managed as beans; `@Repository` additionally translates database-specific SQLExceptions into Spring's unified `DataAccessException`.
12. **What is connection pooling?**
    * *Answer:* Maintaining a cache of active database connections (e.g., HikariCP) to avoid the heavy TCP handshake and authentication latency of creating a connection per query.

### Mobile & Architecture
13. **Why use AES-256-GCM over AES-256-CBC?**
    * *Answer:* GCM provides authenticated encryption (protects confidentiality and verifies data has not been tampered with), preventing padding oracle attacks inherent in CBC mode.
14. **How do you prevent UI freezing in React Native?**
    * *Answer:* Offload heavy calculations to background threads via native modules or web workers, use `InteractionManager`, and implement the New Architecture (Fabric/JSI).
15. **How does biometric authentication protect secret keys?**
    * *Answer:* The OS Keystore locks the private key in a Hardware Security Module (TEE / Secure Enclave) and only releases it after local biometric sensor validation.

---
*Created for Gunaseelan N — Comprehensive Interview Preparation & Engineering Revision Kit*
