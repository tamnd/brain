---
title: "Lean"
description: "A guided introduction to Lean for theorem proving, formalization, and proof engineering."
tags: ["lean", "proof-assistant", "type-theory"]
---

#### Chapter 1. Core Language and Environment

1. Installation and toolchain
2. Project structure with Lean and Lake
3. Files, namespaces, and modules
4. Basic syntax and expressions
5. Definitions with `def`
6. Theorems with `theorem` and `lemma`
7. Types and universes
8. Functions and lambda abstraction
9. Implicit and explicit arguments
10. Notation and infix operators
11. Comments and documentation
12. Evaluation with `#eval`
13. Checking types with `#check`
14. Simple rewriting
15. Pattern matching basics
16. Inductive types introduction
17. Structures and records
18. Basic tactic mode
19. Term mode vs tactic mode
20. Holes and goals
21. Error messages and debugging
22. Imports and dependencies
23. Interactive development workflow
24. Editor integration (VSCode)
25. Minimal working examples

###### Chapter 2. Propositions and Proofs

1. Propositions as types
2. Implication and functions
3. Conjunction
4. Disjunction
5. Negation
6. False and contradiction
7. True and trivial proofs
8. Equality basics
9. Rewriting with equality
10. Symmetry and transitivity
11. Existential quantifiers
12. Universal quantifiers
13. Classical vs constructive logic
14. Proof by contradiction
15. Case analysis
16. Introduction and elimination rules
17. Proof structuring patterns
18. Naming conventions
19. Local context management
20. Using assumptions effectively
21. Forward reasoning
22. Backward reasoning
23. Combining tactics and terms
24. Small proof refactoring
25. Proof readability patterns

#### Chapter 3. Tactic Framework

1. The `intro` tactic
2. The `apply` tactic
3. The `exact` tactic
4. The `assumption` tactic
5. The `rw` tactic
6. The `simp` tactic
7. The `simp` set control
8. The `cases` tactic
9. The `induction` tactic
10. The `constructor` tactic
11. The `have` tactic
12. The `let` tactic
13. The `show` tactic
14. The `refine` tactic
15. The `calc` block
16. The `conv` tactic
17. The `change` tactic
18. The `generalize` tactic
19. The `revert` tactic
20. The `clear` tactic
21. The `rename` tactic
22. The `simp_all` tactic
23. The `aesop` tactic
24. Combining tactics
25. Debugging tactic scripts

#### Chapter 4. Equality and Rewriting

1. Definitional equality
2. Propositional equality
3. The `rfl` proof
4. Congruence lemmas
5. Rewriting direction control
6. Chained rewriting
7. Rewriting under binders
8. Rewriting with hypotheses
9. Dependent rewriting
10. Substitution patterns
11. Transport across equality
12. Heterogeneous equality
13. `simp` normalization
14. Custom simp lemmas
15. Avoiding rewrite loops
16. Controlled rewriting strategies
17. Equality in inductive types
18. Equality of functions
19. Extensionality
20. Proof irrelevance
21. Decidable equality
22. Boolean equality bridges
23. Rewriting with equivalences
24. Rewriting in structures
25. Common pitfalls

#### Chapter 5. Inductive Types

1. Defining inductive types
2. Constructors and recursion
3. Pattern matching deep dive
4. Structural recursion
5. Well-founded recursion
6. Induction principles
7. Custom induction schemes
8. Mutual inductive types
9. Nested inductive types
10. Indexed families
11. Finite types
12. Enumerations
13. Trees and recursion
14. Lists and sequences
15. Options and sums
16. Products and pairs
17. Proofs by induction
18. Eliminators
19. Recursors
20. Dependent pattern matching
21. Inductive propositions
22. Encoding logical rules
23. Proof objects
24. Design patterns
25. Performance considerations

#### Chapter 6. Structures and Typeclasses

1. Structures definition
2. Field access
3. Instances
4. Typeclass basics
5. Instance search
6. Coercions
7. Inheritance patterns
8. Bundled vs unbundled
9. Algebraic structures
10. Custom instances
11. Overlapping instances
12. Priority control
13. Local instances
14. Deriving mechanisms
15. Reusable interfaces
16. Notation with structures
17. Canonical structures
18. Class inference debugging
19. Mixins
20. Parametric structures
21. Typeclass design patterns
22. Automation via classes
23. Interoperability
24. Extending libraries
25. Pitfalls

#### Chapter 7. Functions and Recursion

1. Function definitions
2. Higher-order functions
3. Currying and uncurrying
4. Recursion basics
5. Tail recursion
6. Termination checking
7. Measure functions
8. Structural recursion patterns
9. Partial functions
10. Option-returning functions
11. Error handling
12. Monadic style
13. Dependent functions
14. Function extensionality
15. Mapping and folding
16. Composition patterns
17. Lazy evaluation patterns
18. Efficiency concerns
19. Memoization ideas
20. Rewriting recursive definitions
21. Equational reasoning
22. Proofs about functions
23. Parametricity
24. Abstraction patterns
25. Refactoring functions

#### Chapter 8. Lists and Collections

1. Lists basics
2. List recursion
3. Mapping
4. Filtering
5. Folding
6. Zipping
7. Concatenation
8. Membership
9. Sublist relations
10. Permutations
11. Sorting
12. Multisets
13. Arrays
14. Finite sets
15. Maps and dictionaries
16. Indexing
17. Iterators
18. Collection proofs
19. Algebraic properties
20. Complexity reasoning
21. Efficient representations
22. Custom containers
23. Interoperability
24. Common lemmas
25. Design patterns

#### Chapter 9. Arithmetic and Algebra

1. Natural numbers
2. Integers
3. Rational numbers
4. Real numbers interface
5. Arithmetic tactics
6. Ring reasoning
7. Linear arithmetic
8. Inequalities
9. Divisibility
10. Modular arithmetic
11. Algebraic identities
12. Polynomial reasoning
13. Structures (semigroup, monoid)
14. Groups
15. Rings
16. Fields
17. Homomorphisms
18. Algebraic rewriting
19. Canonical forms
20. Decision procedures
21. Automation
22. Custom algebraic tactics
23. Proof patterns
24. Optimization
25. Integration with libraries

#### Chapter 10. Logic Engineering

1. Encoding syntax
2. Encoding semantics
3. Abstract syntax trees
4. Evaluation functions
5. Substitution
6. Variable binding
7. De Bruijn indices
8. Alpha equivalence
9. Beta reduction
10. Small-step semantics
11. Big-step semantics
12. Proof systems
13. Soundness
14. Completeness
15. Decidability
16. Normalization
17. Encoding inference rules
18. Automated reasoning
19. Reflection
20. Verified interpreters
21. Verified compilers
22. Logical frameworks
23. DSL design
24. Meta-theory proofs
25. Case studies

#### Chapter 11. Metaprogramming

1. The `Lean` metaprogramming model
2. Syntax trees
3. Elaborator basics
4. Tactic writing
5. Custom tactics
6. Macros
7. Attributes
8. Environment inspection
9. Quotation
10. Anti-quotation
11. Reflection
12. Code generation
13. Custom commands
14. Interactive tools
15. Debugging meta code
16. Performance tuning
17. Automation pipelines
18. Proof search
19. Custom simplifiers
20. Domain-specific tactics
21. Integrating with libraries
22. Tooling extensions
23. Safe metaprogramming
24. Testing meta code
25. Design patterns

#### Chapter 12. Automation

1. Simplification strategies
2. Rewriting automation
3. Decision procedures
4. Search-based tactics
5. Heuristic design
6. Controlling search
7. Custom simp sets
8. Combining automation
9. Proof reconstruction
10. External solvers
11. SMT integration
12. Arithmetic automation
13. Logic automation
14. Rewriting engines
15. Performance tuning
16. Debugging automation
17. Domain-specific automation
18. Automation boundaries
19. Proof minimization
20. Trusted kernels
21. Reliability concerns
22. Incremental automation
23. Benchmarking
24. Scaling automation
25. Case studies

#### Chapter 13. Formalizing Mathematics

1. Sets and functions
2. Relations
3. Orders
4. Topology basics
5. Analysis basics
6. Algebra formalization
7. Category theory basics
8. Combinatorics formalization
9. Graph theory
10. Probability basics
11. Number theory
12. Linear algebra
13. Abstract structures
14. Reusable lemmas
15. Naming conventions
16. Library navigation
17. Documentation patterns
18. Bridging informal to formal
19. Formal proof strategies
20. Refactoring libraries
21. Dependency management
22. Cross-domain reuse
23. Collaboration workflows
24. Review processes
25. Case studies

#### Chapter 14. Large Projects

1. Project architecture
2. Module boundaries
3. Naming systems
4. Dependency graphs
5. Build performance
6. Incremental compilation
7. Testing strategies
8. Continuous integration
9. Documentation systems
10. Versioning
11. Refactoring large codebases
12. Code review practices
13. Style guides
14. Collaboration models
15. Packaging
16. Distribution
17. Benchmarking
18. Profiling
19. Debugging large systems
20. Error isolation
21. Scaling proofs
22. Automation pipelines
23. Library evolution
24. Migration strategies
25. Case studies

#### Chapter 15. Interoperability

1. Calling external code
2. FFI basics
3. Data exchange
4. Serialization
5. JSON handling
6. Interfacing with C
7. Interfacing with Rust
8. Interfacing with Python
9. Command line tools
10. File IO
11. Network IO
12. External solvers
13. Database interaction
14. Embedding Lean
15. Extracting programs
16. Verified pipelines
17. Toolchain integration
18. Build system bridges
19. Testing interoperability
20. Performance concerns
21. Security considerations
22. Sandboxing
23. Deployment
24. Monitoring
25. Case studies

#### Chapter 16. Performance and Optimization

1. Evaluation model
2. Memory usage
3. Lazy vs strict
4. Profiling tools
5. Bottleneck analysis
6. Optimizing recursion
7. Efficient data structures
8. Avoiding recomputation
9. Caching
10. Parallelism concepts
11. Compilation strategies
12. Kernel performance
13. Tactic performance
14. Simplifier tuning
15. Instance search tuning
16. Reducing proof size
17. Code generation efficiency
18. Benchmarking
19. Micro-optimizations
20. Macro-optimizations
21. Trade-offs
22. Regression testing
23. Performance metrics
24. Scaling strategies
25. Case studies

#### Chapter 17. Debugging and Diagnostics

1. Reading error messages
2. Type mismatch diagnosis
3. Unification failures
4. Missing instances
5. Infinite loops
6. Tactic failures
7. Simplifier issues
8. Trace tools
9. Logging
10. Inspecting goals
11. Context inspection
12. Stepwise debugging
13. Binary search debugging
14. Minimizing examples
15. Reproducing bugs
16. Fix strategies
17. Testing fixes
18. Debugging meta code
19. Debugging automation
20. Performance debugging
21. Tooling support
22. Editor features
23. Reporting issues
24. Common pitfalls
25. Debugging checklist

#### Chapter 18. Proof Patterns

1. Direct proofs
2. Contradiction
3. Contrapositive
4. Induction patterns
5. Case splits
6. Invariants
7. Structural recursion proofs
8. Algebraic proofs
9. Combinatorial proofs
10. Constructive proofs
11. Classical proofs
12. Equational reasoning
13. Diagram chasing
14. Reduction arguments
15. Encoding arguments
16. Abstraction patterns
17. Layered proofs
18. Reusable lemmas
19. Proof compression
20. Proof expansion
21. Readability patterns
22. Naming patterns
23. Refactoring proofs
24. Anti-patterns
25. Case studies

#### Chapter 19. Domain-Specific Libraries

1. Mathlib overview
2. Navigating mathlib
3. Extending mathlib
4. Custom libraries
5. DSL construction
6. Domain modeling
7. Interfaces
8. Reuse strategies
9. Version compatibility
10. Documentation
11. Testing
12. Benchmarking
13. Distribution
14. Collaboration
15. Review processes
16. Stability
17. Deprecation
18. Migration
19. Tooling
20. Packaging
21. Publication
22. Community standards
23. Maintenance
24. Governance
25. Case studies

#### Chapter 20. End-to-End Case Studies

1. Verified arithmetic library
2. Verified data structure
3. Verified parser
4. Verified interpreter
5. Verified compiler
6. Verified algorithm
7. Formal combinatorics project
8. Formal algebra project
9. Formal logic system
10. DSL implementation
11. Automation pipeline
12. Custom tactic suite
13. Large proof development
14. Library extension
15. Interoperability project
16. Performance optimization
17. Debugging case study
18. Refactoring case study
19. Collaboration case study
20. Teaching example
21. Research prototype
22. Industrial application
23. Deployment scenario
24. Maintenance workflow
25. Lessons learned
