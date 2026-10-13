# FAANG / MANGA High-Level & Low-Level System Design Workbook
## Candidate: Gunaseelan N | Target: L5 / L6 (Senior & Staff Software Engineer / Tech Lead)

---

# Architecture 1: Planetary-Scale Distributed Job Scheduler (Google Cloud Tasks / AWS EventBridge Scale)

```
[Client / Upstream Microservices]
               │
               ▼  HTTPS / gRPC
     ┌───────────────────┐
     │   API Gateway     │ (Rate Limiting, mTLS, JWT Authentication)
     └─────────┬─────────┘
               │
               ▼
     ┌───────────────────┐
     │ Scheduler Service │
     │   (Stateless)     │
     └─────────┬─────────┘
               │
               ├─────────────────────────────────────────┐
               ▼ Write Metadata                           ▼ Cache / Rapid Lookup
     ┌───────────────────┐                     ┌───────────────────┐
     │ PostgreSQL /      │                     │ Redis Metadata    │
     │ CockroachDB       │                     │ Cache             │
     │ (Sharded by OrgId)│                     └───────────────────┘
     └───────────────────┘
               │
               ▼ Dispatch Trigger Time
     ┌─────────────────────────────────────────────────────────────┐
     │       Partitioned Redis Cluster (Time-Wheel ZSET)           │
     │ Key: `slot:{bucket_id}:{timestamp_minute}`  Score: epoch_sec│
     └──────────────────────────────┬──────────────────────────────┘
                                    │
                                    ▼ Poll & Acquire Distributed Lock (Redlock)
     ┌─────────────────────────────────────────────────────────────┐
     │                 Dispatcher Fleet (Go / Java)                │
     └──────────────────────────────┬──────────────────────────────┘
                                    │ Push runnable tasks
                                    ▼
     ┌─────────────────────────────────────────────────────────────┐
     │         Partitioned Message Broker (Apache Kafka)           │
     │ Topics: `scheduler.fast`, `scheduler.slow`, `scheduler.io`   │
     └──────────────┬──────────────────────────────┬───────────────┘
                    │                              │
                    ▼                              ▼
     ┌─────────────────────────────┐┌─────────────────────────────┐
     │    Worker Fleet (Fast)      ││    Worker Fleet (Batch)     │
     │ (<2s compute, HTTP webhook) ││ (>30s compute, DB ETL, AI)  │
     └──────────────┬──────────────┘└──────────────┬──────────────┘
                    │                              │
                    └──────────────┬───────────────┘
                                   ▼
                    ┌──────────────────────────────┐
                    │ Dead Letter Queue (DLQ)      │
                    │ + Kafka Schema Registry      │
                    └──────────────────────────────┘
```

### 1. Requirements & Scale Estimation
* **Scale**: 100 Million scheduled tasks per day $\approx 1,200$ tasks/sec average, $5,000$ tasks/sec peak.
* **Latency SLA**: Tasks must fire within $\le 500\text{ ms}$ of their scheduled execution epoch.
* **Guarantee**: At-least-once delivery with end-to-end idempotency.

### 2. Deep Dive: Sharded Time-Wheel Engine
1. **The Hot-Key Bottleneck**: If 500,000 tasks are scheduled for exactly `12:00:00 UTC`, a single Redis instance will suffer CPU saturation and connection exhaustion.
2. **The Sharding Solution**:
   * We shard the upcoming minute into $K = 64$ slots:
     $$\text{slot\_id} = \text{hash}(\text{task\_id}) \pmod{64}$$
   * Tasks are pushed into key: `wheel:{slot_id}:{minute_epoch}`.
   * A dedicated pool of poller threads pulls tasks via:
     ```redis
     ZRANGEBYSCORE wheel:14:1700000000 0 <current_epoch> LIMIT 0 100
     ```
   * Tasks are deleted via atomic Lua script or `ZPOPMIN`.

### 3. Idempotency & Fault Tolerance
* Each task execution receives an `idempotency_key = sha256(task_id + scheduled_time)`.
* Workers write the key to Redis with a TTL of 24 hours using `SET key token NX PX 86400000`.
* If a worker node crashes mid-execution, the dispatcher heartbeats timeout after 30 seconds, releases the lock, and re-enqueues the job with an incremented `retry_count`.

---

# Architecture 2: Cloud Drive & Enterprise Asset Storage (Google Drive / S3 Scale)

```
[Mobile / Web Client] ──1. POST /files/upload/init (Metadata)──> [Asset API Gateway]
        │                                                               │
        │ <──2. Pre-signed Multipart URLs (Chunks 1..N)─────────────────┘
        │
        ├──3. Parallel Chunk Uploads (HTTP/3 PUT)──> [Object Storage (AWS S3 / GCS)]
        │                                                     │
        ├──4. POST /files/upload/complete──────────────────── │
        │                                                     │
        │ <──5. 200 OK (File Available)                       ▼
        │                                          [Object Created Event]
        │                                                     │
        │                                                     ▼
        │                                           [Kafka: `asset.uploaded`]
        │                                                     │
        │                       ┌─────────────────────────────┼─────────────────────────────┐
        │                       ▼                             ▼                             ▼
        │             [ClamAV / Virus Scanner]       [Thumbnail & Transcode]       [Metadata Indexer]
        │                       │                             │                             │
        ▼                       ▼                             ▼                             ▼
 [Elasticsearch (File Search)] ── Update Status in [PostgreSQL (File Tree & ACLs)]
```

### 1. Requirements & Scale
* 50 Million DAU, 1 Billion files stored.
* File sizes from 10KB to 10GB.
* Must support resume on intermittent mobile connections, virus inspection, and instant deduplication.

### 2. Content-Addressable Storage (CAS) Deduplication
* Client computes the SHA-256 hash of each 4MB chunk and the entire file before uploading.
* When client calls `/files/upload/init`, the server checks the `chunk_hashes` table:
  ```sql
  SELECT chunk_id, storage_uri FROM file_chunks WHERE chunk_hash = :hash;
  ```
* If all chunks already exist in storage (e.g. widely shared corporate PDF), the server immediately creates a metadata reference to the existing blocks and returns `201 Created` with **zero bytes transferred**, saving up to 35% in cloud storage costs.

---

# Architecture 3: Autonomous Multi-Agent AI System (GalaxyONE & Agentic Workflows)

```
[User Specification / Wireframe / Schema Document]
                         │
                         ▼
           ┌────────────────────────────┐
           │     Gateway & Semantic     │
           │      RAG Cache             │ (Checks if identical prompt was solved)
           └─────────────┬──────────────┘
                         │
                         ▼
           ┌────────────────────────────┐
           │      Supervisor Agent      │
           │   (Planner & Task DAG)     │
           └─────────────┬──────────────┘
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
 ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
 │Data Copilot │   │Logic Copilot│   │Layout Copilt│
 │  (Schema)   │   │ (Decisions) │   │ (UI Tree)   │
 └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │ Tool Call Request
                          ▼
           ┌────────────────────────────┐
           │  Tool Orchestration Broker │
           └──────────────┬─────────────┘
                          │
                          ▼
           ┌────────────────────────────┐
           │ Isolated Execution Sandbox │
           │ (Firecracker MicroVM /     │
           │  Docker gVisor)            │
           │  - Run DB Migrations       │
           │  - Run TypeScript/JUnit    │
           │  - Validate JSON Schemas   │
           └──────────────┬─────────────┘
                          │
                          ▼ Execution Results / Lints
           ┌────────────────────────────┐
           │   Reflection & Evaluator   │
           │           Loop             │
           └──────────────┬─────────────┘
                          │
          Passed? ────────┴──────── No ──> [Self-Correction Loop]
            │
           Yes
            ▼
 [Commit to Visual Designers / Codebase]
```

### 1. Key Interview Talking Points for FAANG:
1. **Context Window Optimization**:
   * Instead of dumping an entire 100,000-token enterprise codebase into the prompt, use a **Hierarchical Code Index**:
     * Level 1: File summaries & interface signatures only.
     * Level 2: Specific function implementation retrieved on demand via `view_file` tool call.
2. **Defeating Hallucinations via Grammar-Constrained Decoding**:
   * Use constrained decoding (e.g., GBNF grammars, Pydantic JSON schemas) directly at the token generation level so the model cannot emit invalid syntax.
3. **Multi-Agent Conflict Resolution**:
   * The Supervisor maintains a directed acyclic graph (DAG) of dependencies. If the *Logic Copilot* refers to a table column that does not exist, the Supervisor triggers a validation error back to the *Data Copilot* before executing the UI layer.

---

# Architecture 4: Enterprise Mobile Device Management & Push Engine (Apple MDM / APNs Scale)

```
[Enterprise Admin Console]
             │
             ▼
   [MDM Core API Fleet]
             │
             ├─────────────────────────────────────────────────┐
             ▼ Write Command (`Status: PENDING`)                ▼ Silent Push Notification
   ┌───────────────────┐                             ┌───────────────────┐
   │ PostgreSQL /      │                             │ Apple APNs /      │
   │ Spanner DB        │                             │ Google FCM Hub    │
   └───────────────────┘                             └─────────┬─────────┘
                                                               │
                                                               ▼ Silent Wakeup Push
                                                     ┌───────────────────┐
                                                     │  Managed Device   │
                                                     │ (iOS / Android)   │
                                                     └─────────┬─────────┘
                                                               │
                                                               ▼ Initiates Mutual TLS
   ┌───────────────────────────────────────────────────────────┴─┐
   │                MDM Device Gateway (mTLS Port 443)           │
   │  - Validates Apple Identity Certificate / Device UDID       │
   │  - Fetches Next PENDING Command from DB                     │
   │  - Sends XML / Plist payload                                │
   └─────────────────────────────────────────────────────────────┘
```

### 1. Protocol Deep Dive:
* **Why can't servers push commands directly to phones?**
  * Firewalls, carrier NATs, and device battery optimization terminate incoming socket connections.
* **The APNs Wakeup Protocol**:
  * Server sends a 0-byte payload with device push token to APNs.
  * Device OS receives Apple push packet and wakes up the MDM daemon.
  * Daemon initiates an HTTPS `PUT` request with client identity certificates (`mTLS`) to the server endpoint `/checkin`.
* **Kiosk Lockdown on Android (Device Owner Mode)**:
  * Leveraged `android.app.admin.DevicePolicyManager`.
  * Invoked `setLockTaskPackages()` to restrict device to single launcher.
  * Blocked keyguard, status bar notification shade expansion, and USB file transfer via user restrictions (`DISALLOW_USB_FILE_TRANSFER`).
