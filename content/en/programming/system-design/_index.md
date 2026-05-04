---
title: "System Design"
---

## Chapter 1. Foundations

1. What system design means
2. Requirements and constraints
3. Functional requirements
4. Nonfunctional requirements
5. Latency, throughput, and availability
6. Capacity estimation
7. Back of the envelope math
8. Traffic patterns
9. Read heavy vs write heavy systems
10. State, storage, and computation
11. APIs and contracts
12. Data models
13. Consistency basics
14. Durability basics
15. Fault tolerance basics
16. Scalability basics
17. Observability basics
18. Security basics
19. Cost as a design constraint
20. Simplicity as a design constraint
21. Tradeoffs
22. Failure modes
23. Design review format
24. Design documentation
25. Common interview patterns

## Chapter 2. Networking and Protocols

1. IP, TCP, and UDP
2. DNS resolution
3. HTTP and HTTPS
4. HTTP/1.1, HTTP/2, and HTTP/3
5. TLS termination
6. Reverse proxies
7. Load balancers
8. Connection pooling
9. Keep alive and timeouts
10. Retries and idempotency
11. Rate limits
12. Backpressure
13. WebSockets
14. Server sent events
15. gRPC
16. REST
17. GraphQL
18. Message framing
19. Serialization formats
20. Compression
21. Caching headers
22. CDN behavior
23. Network partitions
24. Network debugging
25. Protocol selection

## Chapter 3. API Design

1. Resource modeling
2. Endpoint design
3. Request and response schemas
4. Pagination
5. Filtering and sorting
6. Partial updates
7. Bulk operations
8. Idempotency keys
9. Error models
10. Status codes
11. Versioning
12. Compatibility
13. Authentication
14. Authorization
15. Rate limiting
16. Quotas
17. Webhooks
18. Long running operations
19. Async APIs
20. SDK design
21. OpenAPI
22. API gateways
23. Contract testing
24. Documentation
25. API evolution

## Chapter 4. Data Modeling

1. Entities and relationships
2. Keys and identifiers
3. Natural keys vs surrogate keys
4. Normalization
5. Denormalization
6. Index design
7. Constraints
8. Foreign keys
9. Time fields
10. Soft deletes
11. Event tables
12. Audit logs
13. Schema migration
14. Backfills
15. Data retention
16. Multitenancy models
17. Ownership boundaries
18. Read models
19. Write models
20. Materialized views
21. Data validation
22. Data quality
23. Metadata
24. Lineage
25. Modeling tradeoffs

## Chapter 5. Storage Systems

1. Filesystems
2. Block storage
3. Object storage
4. Relational databases
5. Key value stores
6. Document databases
7. Wide column stores
8. Time series databases
9. Graph databases
10. Search indexes
11. Vector databases
12. In memory stores
13. Logs as storage
14. Columnar formats
15. Row oriented formats
16. Compression
17. Compaction
18. Replication
19. Partitioning
20. Sharding
21. Indexing
22. Query planning
23. Backup and restore
24. Storage cost
25. Storage selection

## Chapter 6. Relational Database Design

1. Table design
2. Primary keys
3. Secondary indexes
4. Composite indexes
5. Covering indexes
6. Query plans
7. Transactions
8. Isolation levels
9. Locks
10. Deadlocks
11. MVCC
12. Constraints
13. Migrations
14. Online schema changes
15. Read replicas
16. Connection pools
17. Partitioned tables
18. Materialized views
19. Stored procedures
20. Triggers
21. Full text search
22. Analytical queries
23. Backup strategy
24. Failover strategy
25. Operational pitfalls

## Chapter 7. Distributed Data

1. Replication models
2. Leader follower replication
3. Multi leader replication
4. Leaderless replication
5. Quorums
6. Read repair
7. Anti entropy
8. Consistent hashing
9. Range partitioning
10. Hash partitioning
11. Rebalancing
12. Hot partitions
13. Consensus
14. Raft
15. Paxos
16. ZooKeeper style coordination
17. Split brain
18. Fencing tokens
19. Clock skew
20. Logical clocks
21. Vector clocks
22. Conflict resolution
23. CRDTs
24. Distributed transactions
25. CAP and PACELC

## Chapter 8. Caching

1. Cache use cases
2. Cache aside
3. Read through cache
4. Write through cache
5. Write back cache
6. Refresh ahead
7. TTLs
8. Eviction policies
9. Invalidation
10. Cache stampede
11. Request coalescing
12. Negative caching
13. CDN caching
14. Browser caching
15. Edge caching
16. Distributed caches
17. Local caches
18. Cache consistency
19. Cache warming
20. Hot keys
21. Cache sizing
22. Redis patterns
23. Memcached patterns
24. Observability
25. Failure modes

## Chapter 9. Messaging and Event Systems

1. Queues
2. Pub/sub
3. Logs
4. Message brokers
5. Kafka style systems
6. RabbitMQ style systems
7. SQS style systems
8. Producers
9. Consumers
10. Consumer groups
11. Ordering
12. Delivery guarantees
13. At least once delivery
14. At most once delivery
15. Exactly once semantics
16. Dead letter queues
17. Retries
18. Delayed messages
19. Backpressure
20. Fanout
21. Event schemas
22. Schema registry
23. Outbox pattern
24. Saga pattern
25. Event replay

## Chapter 10. Search, Ranking, and Retrieval

1. Inverted indexes
2. Tokenization
3. Normalization
4. Stemming and lemmatization
5. Term frequency
6. BM25
7. Filters and facets
8. Sorting
9. Pagination
10. Freshness
11. Index updates
12. Shard layout
13. Replication
14. Query routing
15. Highlighting
16. Autocomplete
17. Spell correction
18. Semantic search
19. Vector indexes
20. Hybrid retrieval
21. Ranking pipelines
22. Learning to rank
23. Evaluation metrics
24. Search observability
25. Search failure modes

## Chapter 11. Streaming and Realtime Systems

1. Streams vs batches
2. Event time and processing time
3. Windows
4. Watermarks
5. Late events
6. Stream joins
7. Aggregations
8. Stateful processing
9. Checkpointing
10. Reprocessing
11. Exactly once processing
12. WebSocket fanout
13. Presence systems
14. Live counters
15. Notifications
16. Activity feeds
17. Realtime collaboration
18. Operational transforms
19. CRDT collaboration
20. Realtime analytics
21. Alerting pipelines
22. Stream backpressure
23. Capacity planning
24. Debugging streams
25. Realtime tradeoffs

## Chapter 12. Batch Data Systems

1. Batch processing
2. ETL and ELT
3. Data lakes
4. Warehouses
5. Lakehouse patterns
6. File formats
7. Parquet
8. ORC
9. Avro
10. CSV pitfalls
11. Partitioning
12. Compaction
13. Catalogs
14. Metadata stores
15. Workflow orchestration
16. Scheduling
17. Incremental jobs
18. Backfills
19. Data quality checks
20. Deduplication
21. Slowly changing dimensions
22. Aggregation tables
23. Cost control
24. Data observability
25. Failure recovery

## Chapter 13. Scalability Patterns

1. Vertical scaling
2. Horizontal scaling
3. Stateless services
4. Stateful services
5. Load shedding
6. Backpressure
7. Queue based leveling
8. Partitioning by tenant
9. Partitioning by geography
10. Partitioning by time
11. Fanout on write
12. Fanout on read
13. Precomputation
14. Approximation
15. Sampling
16. Bloom filters
17. Count min sketch
18. Rate limiting algorithms
19. Circuit breakers
20. Bulkheads
21. Graceful degradation
22. Brownout patterns
23. Autoscaling
24. Capacity planning
25. Scaling checklist

## Chapter 14. Reliability and Resilience

1. Availability targets
2. SLOs and SLIs
3. Error budgets
4. Redundancy
5. Failover
6. Disaster recovery
7. Backup verification
8. Health checks
9. Timeouts
10. Retries
11. Circuit breakers
12. Load shedding
13. Bulkheads
14. Chaos testing
15. Incident response
16. Postmortems
17. Runbooks
18. Dependency failure
19. Partial outages
20. Regional outages
21. Data corruption
22. Recovery time objective
23. Recovery point objective
24. Reliability testing
25. Resilience tradeoffs

## Chapter 15. Observability

1. Logs
2. Metrics
3. Traces
4. Events
5. Correlation IDs
6. Structured logging
7. RED metrics
8. USE metrics
9. High cardinality data
10. Sampling
11. Dashboards
12. Alerts
13. Alert fatigue
14. SLO dashboards
15. Distributed tracing
16. Profiling
17. Error tracking
18. Synthetic checks
19. Real user monitoring
20. Business metrics
21. Data observability
22. Cost observability
23. Debugging production
24. Observability pipelines
25. Instrumentation checklist

## Chapter 16. Security and Privacy

1. Threat modeling
2. Authentication
3. Authorization
4. Sessions
5. Tokens
6. OAuth
7. API keys
8. Password storage
9. Secrets management
10. Encryption in transit
11. Encryption at rest
12. Key management
13. Network isolation
14. Input validation
15. Injection attacks
16. SSRF
17. XSS
18. CSRF
19. Rate limiting for abuse
20. Audit logging
21. Privacy by design
22. Data minimization
23. Retention and deletion
24. Compliance basics
25. Security review checklist

## Chapter 17. Deployment and Operations

1. Build pipelines
2. Release strategies
3. Blue green deployment
4. Canary deployment
5. Feature flags
6. Rollbacks
7. Configuration
8. Environment separation
9. Containers
10. Kubernetes
11. Serverless
12. Service discovery
13. Service meshes
14. Infrastructure as code
15. Secrets in deployment
16. Database migrations
17. Operational readiness
18. Runbooks
19. On call handoff
20. Incident drills
21. Cost monitoring
22. Capacity reviews
23. Dependency reviews
24. Production checklists
25. Operational maturity

## Chapter 18. Cost and Capacity Engineering

1. Unit economics
2. Cost drivers
3. Compute pricing
4. Storage pricing
5. Network egress
6. Database cost
7. Cache cost
8. Queue cost
9. Search cost
10. Observability cost
11. Overprovisioning
12. Autoscaling economics
13. Reserved capacity
14. Spot capacity
15. Multi cloud cost
16. Build vs buy
17. Cost allocation
18. Tenant level cost
19. FinOps basics
20. Capacity forecasts
21. Load testing
22. Benchmarking
23. Cost regression tests
24. Architecture cost review
25. Cost reduction playbook

## Chapter 19. Common System Designs

1. URL shortener
2. Pastebin
3. File storage service
4. Photo sharing service
5. Video streaming service
6. News feed
7. Chat system
8. Notification system
9. Rate limiter
10. Search engine
11. Web crawler
12. Payment system
13. Booking system
14. Ride hailing system
15. Food delivery system
16. Ecommerce marketplace
17. Inventory system
18. Logging platform
19. Metrics platform
20. Feature flag service
21. Recommendation system
22. Collaborative editor
23. CDN
24. Analytics platform
25. Multi tenant SaaS

## Chapter 20. Design Review and Case Studies

1. Reading a design prompt
2. Asking clarifying questions
3. Defining scope
4. Estimating load
5. Sketching APIs
6. Choosing storage
7. Choosing consistency
8. Designing data flow
9. Identifying bottlenecks
10. Identifying failure modes
11. Security review
12. Privacy review
13. Cost review
14. Operational review
15. Scaling plan
16. Migration plan
17. Tradeoff table
18. Design document template
19. Review checklist
20. Interview walkthrough
21. Production design walkthrough
22. Startup scale case study
23. Enterprise scale case study
24. Global scale case study
25. Final system design rubric
