# Reference — Pre-Routing Pipeline Architecture

*The four-stage routing pipeline that replaces the intent-classification flow of the retired Mode Classification Directory. Each mode owns its identity, display description, selection signals, input contract, default Gear, and analytical instructions. Territory, within-territory, cross-territory, and disambiguation-style canonicals own shared relationships and questions. `orchestrator/routing_sources.py` compiles this complete source set and its lens and molecular references into validated records for the existing process-lifetime loader. The readable Signal Vocabulary Registry, mode catalogues, indexes, aliases, and reverse relationships are generated views; routing never reads them as independently authored policy.*

---

## Architectural Principle: Deep-Mode Default With Friction Reducers

Per Decision 1, the pipeline defaults to **disambiguation by default** — every analytical prompt is offered the disambiguation flow that selects an appropriate mode and depth. **Friction reducers** skip questions the prompt has already answered. The result: routine prompts dispatch with zero clarifying questions because the prompt itself supplied the answers; ambiguous prompts get the disambiguation they need.

This replaces the retired Mode Classification Directory's intent-classification flow, which routed by inferring user intent from a flat 25-mode list. The new flow operates on territories and gradation positions, with disambiguation as a first-class operation rather than a fallback.

The pipeline has four sequential stages. Each stage has a clear input, processing logic, and output. Stage transitions are deterministic (no stage advances on a partial decision; each stage's output is complete before the next stage begins).

The same compiled collection serves automatic selection, explicit and plural mode names, manual/API picker metadata, educational naming, Stage 3 input and lighter-sibling lookup, prompt sections, and source listing/validation. A fresh process reads changed source bytes; there is no persistent routing cache, model-assisted runtime selector, or second authored registry. Invalid declarations, unknown targets, missing lens or molecular references, and unbound operative predicates reject collection loading rather than returning a partial library.

Canonical question records carry stable identity, text, authored answer phrases, typed alternatives, qualifications, follow-up references, and explicit defaults. Active targets may run after input validation; deferred targets are labeled unavailable and are never dispatched as missing mode files; territory targets continue the canonical tree; named fallback/action targets use the finite existing bindings. Equal phrases selecting different destinations remain distinct. Bare T16 and T20 retain their authored defaults, while T8 still asks its authored question despite having one active resident. Genuine no-territory ambiguity asks for intent without excluding a valid territory. A Red Team request without a specific subject uses its owning mode's question. A lighter choice that needs the same missing material preserves the user's selection and asks for that material before execution.

## The Four-Gear Taxonomy (2026-05-24 redesign)

The orchestrator routes each prompt to one of four gears. The gear determines pipeline shape and model selection; pre-routing determines which gear fires.

- **Gear 1 — Direct response.** Greetings, system commands, local facts that need no retrieval, mechanical translations, and explicit analysis opt-outs. Stage 0 strong-bypass triggers and weak-bypass triggers under the short-prompt/no-analytical-vocabulary constraint route to `simple`. Concept RAG, relationship RAG, F-Consult, and deterministic mode tools are skipped; relevant conversation context may still be assembled. The response model resolves from the exact `utility.classification` cell.
- **Gear 2 — Single pass with RAG and tools.** Retrieval-without-judgment requests route to `factual-lookup`; faithful source-to-format transformations route to `structured-output`. Context may include conversation, concept, and relationship RAG, F-Consult, and declared tools. The response model resolves from the exact `utility.gear2_rag_lookup` cell (same-configuration `utility.step1_cleanup` fallback only). There is no adversarial review cascade.
- **Gear 3 — Sequential adversarial pipeline.** Judgment-required prompts that do not trigger a specific Gear 4 mode route to `general-inquiry` or `subjective-inquiry`; open-ended curiosity with no deliverable may route to `passion-exploration`. Exact Gear 3 depth/breadth cells execute analyst → evaluator → claim verification → reviser → unflagged-claim scan → verifier → final quality gate. Gear 3 has no consolidator or formatter and releases only the accepted revised-draft body.
- **Gear 4 — Parallel adversarial pipeline.** The 58 installed deep-analysis modes (cui-bono, ACH, wicked-problems, root-cause-analysis, etc.) explicitly declare Gear 4. Two independent analyst streams feed the evaluator/reviser/verifier/consolidator/formatter cascade with mode-specific depth.

Gear assignment by stage:
- **Stage 0** (raw prompt, pre-Phase-A) — strong or tightly constrained weak bypass → `simple`, Gear 1. Gear 2 RAG dispatch → `factual-lookup`, Gear 2. The two results are mechanically distinct: a retrieval dispatch is never converted into a direct bypass.
- **Stage 1** (operational notation, defensive backup) — same checks as Stage 0; in normal operation silent because Stage 0 already handled the case.
- **Stage 2** (mode disambiguation) — dispatches to a specific analytical mode (Gear 3 or Gear 4 per the mode's `## DEFAULT GEAR` heading).
- **Stage 2 unresolved intent** — asks the canonical intent question, with every analytical territory available. The T0 modes remain selectable through their own declared signals and identity; a lack of evidence is not an automatic T0 dispatch.
- **Default Gear authority** — every installed mode must declare a valid `## DEFAULT GEAR`; an invalid declaration rejects the full source collection. The existing text-helper fallback to Gear 3 applies only to text outside that compiled collection.

The four-gear redesign reclaims Gear 3 from dead code (it existed but no mode dispatched to it pre-2026-05-24) and gives Gear 2 a meaningful single-pass-with-RAG role that the prior architecture lacked.

---

## Stage 0 — Pre-Phase-A Bypass Check

**Purpose.** Catch obvious chitchat / lookup / system-command prompts on the *raw user input* before Phase A runs. Prevents Phase A's expansion of the prompt into operational notation from masking bypass-eligible patterns (the "what time is it" normalised into "REQUEST: current-time" failure) and from false-positive-matching expanded-text substrings ("no analysis" matching inside "cui bono analysis" — the substring-collision failure landed 2026-05-15).

**Input.** Raw user prompt as the user typed it (or as ASR rendered it). No conversation context, no Phase A normalisation.

**Processing logic.**

1. **Strong bypass triggers** — concrete factual lookups that need NO retrieval ("what time is it", "what's today's date"), system-meta references ("what did you just say", "repeat that"), mechanical translation / formatting requests ("translate this", "fix the spelling"), and explicit user opt-outs from the analytical pipeline ("don't analyze", "skip the analysis"). Match → bypass immediately. The list was narrowed 2026-05-24 to remove patterns that may require retrieval ("what is the capital", "remind me of") — those now route to Gear 2 RAG dispatch instead.
2. **Gear 2 RAG dispatch (added 2026-05-24)** — information requests that need retrieval but no judgment: "who is the current president", "weather today", "who won the Super Bowl in 2026", "what is the capital of Burma". The existing detector matches the retrieval cues owned by `factual-lookup` only when no judgment cue owned by `general-inquiry` matches. Match → dispatch to `factual-lookup` mode (Gear 2) immediately, skipping Stage 2 mode disambiguation. The judgment-marker gate ensures that "should I bring an umbrella tomorrow" (retrieval + judgment) routes to Stage 2 rather than Gear 2 lookup.
3. **Weak bypass triggers (constrained)** — greetings and acknowledgements. These bypass only when the prompt is plausibly *just* a greeting: short (≤ 8 normalised words) AND containing no obvious analytical-vocabulary tokens (analyze, evaluate, audit, steelman, compare, cui bono, root cause, etc.). The "Hi! Steelman this op-ed" case correctly falls through to Phase A because the analytical hint disqualifies the weak match.
4. **No match** — fall through to Phase A; the prompt is presumed analytical until later stages prove otherwise.

**Output.**

- If strong / weak bypass fires: `{ bypass_to_direct_response: true, rationale: "<trigger>", stage: "pre-phase-a" }`. Phase A and Stages 1–4 are all skipped. `step1_result.mode` is set to `simple`, Gear 1, and the raw prompt is used as `cleaned_prompt` without expansion. The chat handler intercepts direct-response modes and routes to `_direct_stream`, so bypass cases skip the gear pipeline entirely.
- If Gear 2 RAG dispatch fires: `{ gear2_rag_dispatch: true, dispatched_mode_id: "factual-lookup", rationale: "<trigger>", stage: "pre-phase-a" }`. Phase A and Stage 2 disambiguation are skipped; the pipeline loads `factual-lookup` mode (Gear 2) and runs the single-pass-with-RAG-and-tools dispatch in `_run_pipeline_from_step2`.
- If no match: control passes to Phase A, then to Stage 1.

**Why this exists.** Detector layering is the structural risk. Phase A's job is to expand and normalise; running bypass detectors on the post-expansion text means the detector's input space depends on what Phase A produced for *this* prompt. Substring detectors don't compose cleanly across layers — a phrase legitimate inside the expansion ("Structured cui bono analysis") can contain a substring legitimate as a bypass trigger ("no analysis"). The pre-Phase-A check runs on input the user controls directly, which is the layer where bypass triggers were designed to be evaluated.

**Defensive duplication.** Stage 1 (below) re-runs the strong-bypass scan on the operational notation. The intent is defensive: if Phase A's expansion legitimately reveals a bypass-worthy element the raw prompt didn't carry (a rare but possible case), Stage 1 still catches it. In normal operation Stage 1's bypass branch is silent because the pre-Phase-A check already handled the case.

---

## Stage 1 — Pre-Analysis Filter

**Purpose.** Distinguish prompts that should enter the analytical pipeline from prompts that bypass it (chitchat, simple lookups, conversation continuations, system commands). Runs on Phase A's *operational notation* (the cleaned, expanded form of the prompt). Stage 0 already screened the raw prompt; Stage 1 is the second-pass safety net.

**Input.** Phase A's operational notation plus minimal context (current conversation thread, attached documents if any).

**Processing logic.**

1. **Strong bypass detection (defensive backup).** Same substring scan as Stage 0; silent in normal operation because Stage 0 already caught these. Defensive against the rare case where Phase A's normalization legitimately reveals a bypass-worthy element the raw prompt didn't carry.
2. **Gear 2 RAG dispatch (defensive backup, added 2026-05-24).** Same substring + judgment-marker check as Stage 0; silent in normal operation. Defensive against the rare case where Phase A's normalization legitimately reveals a retrieval-needed pattern the raw prompt didn't carry.
3. **Analytical-artifact signal detection.** Match the signals compiled from each mode's Selection/Activation Guidance. Examples: "analyze," "make the case for," "what could go wrong," "who benefits," "compare these," "is this argument sound," "what are the tradeoffs," "stress-test," "what's missing," "frame this." Case folding, word boundaries, bounded typo matching, negation, and the finite data-shape detectors remain mechanical code. Authored aliases, weights, qualifications, and destinations come from the sources.
4. **Weak bypass detection.** Substring match against bypass triggers: greetings, simple factual questions, system commands, prior-answer references ("what did you say earlier"). Matches with no strong analytical signal → direct response (no analytical pipeline).
5. **Ambiguity handling.** When neither analytical signal nor bypass signal matches, default to **permissive** (let the prompt enter the pipeline). Stage 2 asks for the missing intent rather than inventing an analytical destination.

**Output.**
- `bypass_to_direct_response: true | false`
- `gear2_rag_dispatch: true | false` (when true, also carries `dispatched_mode_id: "factual-lookup"`)
- If neither bypass nor gear2_rag fires: forwarded prompt + initial signal-vocabulary matches as input to Stage 2.

**Detection logic notes.**
- Bounded phrase matching preserves word boundaries, so a short signal does not match inside an unrelated word.
- Case-insensitive.
- Negation handling: a window of ±3 tokens around the trigger is checked for negation markers ("not," "don't," "no," "without").
- Multiple matches accumulate from the compiled mode-owned records; identical words that select different valid destinations remain separate.
- Empty signal-vocabulary match + no bypass match → default permissive (forward to Stage 2).

**Performance characteristic.** Stage 1 runs in O(n × m) where n = prompt length and m = signal-vocabulary size. With m ≈ 100 phrases and n ≈ 500 tokens, this is sub-millisecond on the orchestrator's hot path.

---

## Stage 2 — Prompt Sufficiency Analyzer

**Purpose.** Determine whether the prompt contains enough signal to dispatch to a specific mode without disambiguation, or whether disambiguation questions are needed (and which).

**Input.** Forwarded prompt + Stage 1's signal-vocabulary matches.

**Processing logic.**

### 2.1 Signal-strength classification

Each signal in the prompt is classified as **strong** or **weak** per its owning mode's Selection/Activation Guidance `confidence_weight` field. The generated Signal Vocabulary Registry displays those same compiled records but is not a runtime input:

**Strong signals.**
- Explicit method-name reference (e.g., "steelman this," "do an ACH on these hypotheses," "wicked problem analysis").
- Named artifact-type reference (e.g., "evaluate this op-ed," "analyze this decision," "audit this argument").
- Unambiguous depth/stance/complexity vocabulary (e.g., "quick read," "deep dive," "make the strongest case for," "stress-test").
- Multiple corroborating signals from the same territory.

**Weak signals.**
- Tonal cues (e.g., "I'm worried about this," "what should I think about this").
- Contextual implication (e.g., paste of a document without an explicit question; the document type implies but does not specify the analytical operation).
- Single-territory vocabulary that could match multiple modes within the territory.

### 2.2 Multiple-signal composition

Signals AND together. A complete combination dispatches directly. A partial combination leaves residual disambiguation questions.

**Complete combination examples.**
- "Make the strongest case for this housing policy" → T15 + stance-constructive-strong + artifact-type=proposal → `steelman-construction` directly. No questions asked.
- "Quick read on what could go wrong with this rollout plan" → T6 + stance-adversarial-future + depth-light + artifact-type=action-plan → `pre-mortem-action` (light variant). No questions asked.

**Partial combination examples.**
- "Look at this op-ed" → T1 candidate (artifact-type=argument) + no depth signal + no stance signal → ask depth + stance disambiguation.
- "Help me think about this decision" → T3 candidate (decision-shape) + no complexity signal + no specificity signal → ask complexity disambiguation.

### 2.3 Conflict detection

Contradictory signals trigger surfacing. Examples:
- "Quick deep-dive" → contradictory depth signals → ask user to clarify (Tier-1 vs. Tier-3).
- "Steelman the red-team perspective" → contradictory stance signals → ask user whether to (a) steelman the adversarial argument or (b) red-team a steelman.

When conflict is detected, Stage 2 surfaces a single targeted question via the Disambiguation Style Guide patterns.

### 2.4 Cross-territory adjacency check

Before within-territory disambiguation, Stage 2 consults `Reference — Cross-Territory Adjacency.md`. If signals straddle two territories, the cross-territory disambiguation question fires first. Example: prompt mentions both "argument soundness" (T1) and "who benefits" (T2) → ask the T1↔T2 disambiguating question first; the user's answer narrows to one territory; within-territory disambiguation then proceeds (or skips, if the answer also disambiguates the mode).

A targeted cross-territory question is used only when its declared territories cover every strong territory in the prompt; otherwise Stage 2 asks `generic_intent`, whose full territory choices preserve every valid route.

### 2.5 Within-territory disambiguation

When the territory is identified but the mode is ambiguous, Stage 2 consults `Reference — Within-Territory Disambiguation Trees.md` and asks the relevant tree's question(s) using Disambiguation Style Guide phrasing.

### 2.6 Default-on-ambiguity

When the user's response to a disambiguation question is ambiguous or absent:
- **Tier-2 thorough atomic** by default (per Style Guide §5.6).
- **Neutral stance** when the territory has a stance axis and the user has not signaled.
- **General specificity** when the territory has a specificity axis.

### 2.6a Unresolved intent and T0 modes

When no territory or explicit mode can be selected from the available evidence, Stage 2 asks the authored `generic_intent` question. Its choices include all T1–T21 territories, and its explicit default keeps the question pending. No valid territory is removed merely because the initial prompt supplied no signal.

The two T0 modes remain ordinary source-owned selections: **subjective-inquiry** handles opinion, preference, and aesthetic judgment without objective criteria; **general-inquiry** handles general judgment. Both use Gear 3's sequential adversarial pipeline. Their declared identities and signals can select them, but the absence of a specific dispatch does not silently select either one.

### 2.7 Friction-reducer behavior

When the prompt has supplied an answer to a disambiguation question (via signal vocabulary match), that question is **skipped** automatically. The user does not have to repeat themselves. Example: prompt is "Steelman this op-ed quickly" → both stance ("steelman") and depth ("quickly") supplied → no disambiguation questions; direct dispatch to `steelman-construction` at Tier-1.

**Output.**
- `dispatched_mode_id: <mode_id>` (after disambiguation completes)
- `disambiguation_questions_asked: [<questions>]`
- `disambiguation_answers_received: [<answers>]`
- `confidence: high | medium | low`
- Forwarded to Stage 3 with mode_id and the validated routing context.

---

## Stage 3 — Input Completeness Check

**Purpose.** Verify that the dispatched mode's required inputs are present (per its dual `input_contract`). Surface missing or underspecified inputs and either elicit them or offer graceful-degradation to a sibling mode.

**Input.** Dispatched mode_id + forwarded prompt + any prior-conversation context, attached documents, URLs, prior-answer references, in-prompt examples.

**Processing logic.**

### 3.1 Contract version selection

Stage 3 selects between the mode's `expert_mode` and `accessible_mode` input contracts using the mode spec's `input_contract.detection` rules:

- **Expert signals present** → `expert_mode` contract applies.
- **Accessible signals present** → `accessible_mode` contract applies (default per Decision 3).
- **Neither** → `accessible_mode` (default).

### 3.2 Presence detection

For each `required` field in the selected contract, Stage 3 checks for presence across all input sources:
- Pasted text in the current prompt.
- Attached documents (PDF, image, etc.).
- URLs (if URL fetch is available).
- Prior-conversation references ("the document I shared earlier").
- In-prompt examples ("here's an example: ...").

Presence is a binary check per field. Field-specific detection logic lives in `Reference — Mode Specification Template.md`'s `input_contract.detection` block per mode.

### 3.3 Underspecification detection

A field may be present but underspecified. Example: a mode requires `decision_context` and the prompt mentions "I have a decision" without specifying the decision. Underspecification is detected per-field by mode-spec rules.

### 3.4 Graceful-degradation rules

When a required field is missing or underspecified, Stage 3 consults the mode spec's `input_contract.graceful_degradation` block:

- `on_missing_required` — typically a follow-up question template, possibly suggesting a lighter sibling mode that needs less.
- `on_underspecified` — follow-up question template.

Example: User asks "do a wicked problems analysis" without supplying a problem statement. Stage 3 detects missing `problem_description` and surfaces:
> "I can run a Wicked Problems analysis (*integrated multi-perspective analysis of tangled problems*) — this takes about 10 minutes. Could you describe the problem and any history of attempts to address it? If you'd prefer a quicker read, I can run a lighter Cui Bono (*who-benefits analysis*) on the situation as you describe it."

The graceful-degradation offer pairs the heavier mode (with its time-cost) against a lighter sibling. The user picks one or supplies the missing input.

### 3.5 Accept-and-resume path

When the user supplies the missing input, Stage 3 re-runs the completeness check against the supplied text and actual answers, refreshed eligible conversation history and original attachment-presence facts, without counting presentation labels or inserted paragraph breaks as material. When it passes, Stage 3 forwards to Stage 4. The pause retains each selected mode’s completeness result. When the user opts for the lighter sibling, Stage 3 replaces the mode whose question was shown, preserves the other selections, and re-runs their completeness checks including the new mode's own contract.

**Output.**
- `inputs_complete: true | false`
- `validated_inputs: { <field>: <source-and-value> }`
- If `inputs_complete: false`: dialog turn to user with completeness-check question (per Style Guide §5.8).
- If `inputs_complete: true`: forwarded to Stage 4.

---

## Stage 4 — Mode Execution

**Purpose.** Dispatch to the selected mode against the validated inputs.

**Input.** Validated `dispatched_mode_id` + `validated_inputs` from Stage 3 + the orchestrator's routing context (user, conversation, RAG profile, etc.).

**Processing logic.**

1. **Select the compiled mode record** by `mode_id`. Its source is `~/ora/modes/<mode_id>.md`; the complete mode, territory, lens, and molecular reference collection has already been validated before it becomes available.
2. **Read the mode-owned runtime fields and prompt sections** from that same record. The separate mode runtime-configuration document is retired and is not loaded. Invalid source declarations fail collection loading; they do not silently acquire a default configuration.
3. **Compose dispatch announcement** with educational parenthetical per Decision E:
   > "Plain-language description *(named technique)*"
   The plain-language description comes from the mode's Display Description; the named technique comes from its `educational_name` field.
4. **Execute the existing Gear-specific pipeline** using the selected mode's analytical sections. Gear 3 is sequential; Gear 4 uses parallel analyst streams and consolidation. This source cutover does not change molecular execution or resolve reserved composition/recommendation-policy questions.
5. **Apply the mode-owned configuration**: declared Default Gear, per-stage instruction sections, RAG profile filters, and context budget. Model/configuration authority remains the existing process contract, separate from routing-source ownership.
6. **Output the mode's artifact** per `output_contract`.

**Output.**
- The mode's analytical artifact per its `output_contract`.
- Output format per Decision I/J: territory + mode + residual disambiguation questions if any + completeness gaps if any (richer than current 7-field output).

---

## Manual Mode-Selection Override (server layer)

The four-stage pipeline is the default mode-selection mechanism, not the sole one. The `/chat` and `/chat/multipart` endpoints accept a `manual_mode_selection` field carrying an explicit mode pick. The V3 analysis picker and maintenance scripts send this field. After automatic pre-routing inside Step 1, the server (`server/app.py::_pipeline_stream`) applies the override when **all** of the following hold:

- `manual_mode_selection` is non-empty,
- it names an active mode in the validated compiled collection,
- it differs from the pipeline's dispatched mode, and
- Stage 1 did **not** select bypass-to-direct-response.

When those conditions are met, the manual pick supersedes Stage 2's dispatch and Stage 3 checks the selected mode's own input contract. The server replaces the old pre-routing decision with that selected-mode result. Missing input saves the real question; an explicit Answer to that pending identity rechecks the same selection without reclassification, preserving the pending turn's configuration, model, conversation, and privacy authority. Ordinary chat cannot answer the pending question; Skip uses the separate plain-response fallback. Complete input continues to execution. The override is recorded as `pre_routing.manual_override_applied: true`, with `manual_override_prior_dispatch` holding the superseded Stage 2 pick. The intent-comparison layer likewise treats the manual pick as the winning expressed intent. An optional lens pick is validated against the same compiled mode/lens relationships and retained in the execution context.

**Invalid picks.** A `manual_mode_selection` absent from the compiled active modes is logged server-side and falls through to Stage 2's decision; a deferred candidate is not accepted as a runnable mode.

**Bypass preservation.** A pure chitchat/lookup prompt bypasses to direct response even when a manual pick accompanies it — the override is suppressed whenever Stage 1 chose bypass-to-direct-response.

**Rationale.** Stage 2's signal-vocabulary dispatch is best-effort inference; an explicit user pick is the reliable disambiguator when a prompt's signals overlap across modes.

---

## Baseline Criteria Injection (Cross-Stage ANALYTICAL BRIEF)

Once Stage 4 dispatches a mode into the gear pipeline, every pipeline-step system prompt is assembled by `~/ora/orchestrator/boot.py::build_system_prompt_for_gear(context_package, slot, step, ...)`. Before any role-specific material is added, the function extracts two sections from the dispatched mode file and injects both as **baseline blocks** into the system prompt of **every** pipeline step:

- `## ANALYTICAL BRIEF AND EVALUATION CRITERIA` (legacy fallback during mode propagation: `## EVALUATION CRITERIA`) — injected as `## MODE — <mode name> — Analytical brief and evaluation criteria`.
- `## VERIFICATION CRITERIA` — injected as `## MODE — <mode name> — Verification criteria (PASS gate)`.

"Every pipeline step" means the full `_PIPELINE_STEPS` set: **analyst, evaluator, reviser, verifier, consolidator, formatter**. There is no RAG-planner step in this set — RAG planning happens outside `build_system_prompt_for_gear` and receives no baseline injection.

**The BRIEF is a cross-stage performance contract, not analyst-only context.** The first-pass analyst sees what good looks like before writing — it writes targeting the criteria it will later be graded against. The evaluator and reviser see the same canonical criteria the analyst wrote to, so grading and revision happen against one shared standard rather than each stage's private reconstruction of it. This closes the gap where the first pass wrote blind to the standard it would be graded against.

**Role-specific sections layer ON TOP of this baseline.** The analyst additionally receives `## DEPTH ANALYSIS GUIDANCE` or `## BREADTH ANALYSIS GUIDANCE` (per slot), the reviser receives `## REVISION GUIDANCE`, the consolidator `## CONSOLIDATION GUIDANCE`, and the formatter `## OUTPUT FORMAT GUIDANCE`. The evaluator and verifier receive **no** additional mode-file section — their role framing comes from the universal `f-evaluate.md` / `f-verify.md` scaffolding, and the criteria they apply are already present in the baseline.

**BRIEF vs. VERIFICATION CRITERIA.** The two baseline blocks serve distinct functions. The BRIEF is the shared standard every stage works to: what the analysis is, the procedure, the goal, the evaluation criteria, and the named failure modes. The VERIFICATION CRITERIA section is the mode-specific PASS gate the Step-6 per-stream verifier grades against (layered on `f-verify.md`'s universal floor). Both ride in every step's prompt so no stage is surprised by the gate.

**Gear 1 is structurally exempt.** Gear 1 direct responses do not route through `build_system_prompt_for_gear`, so no injection occurs there.

**Sources.** The injected content lives in the mode files (`~/ora/modes/<mode_id>.md`); the BRIEF's content schema (What this analysis is / Procedure / Goal / Evaluation criteria / Named failure modes) is specified in `Reference — Mode Specification Template.md`; the injection mechanism is `build_system_prompt_for_gear` in `~/ora/orchestrator/boot.py`.

---

## Analyst System Prompt Injection — Analytical Perspectives

Stage 4's gear pipeline composes each role's system prompt via `build_system_prompt_for_gear` (`orchestrator/boot.py`). Every role-specific step receives the same baseline injections — the mode's `## ANALYTICAL BRIEF AND EVALUATION CRITERIA` and `## VERIFICATION CRITERIA` sections (see § Baseline Criteria Injection above). On top of that baseline, the **analyst step** carries analyst-only content injections composed at the same site. This section is the umbrella home for those analyst-prompt injections; the Analytical Perspectives layer is documented here, and future analyst-step injections (e.g. the MCP tool catalog, which both analysts receive) belong as sibling subsections.

### Analytical Perspectives (Breadth analyst only)

**Mode-file source.** `## ANALYTICAL PERSPECTIVES` is a structured, machine-parsed body section in each mode file — every mode file in `~/ora/modes/` carries one (the only `.md` file there without it is the `INDEX.md` inventory, which is not a mode). It is a perspective *allowlist*: the Tier 1 de Bono thinking tools and Tier 3 mental-model lenses appropriate to that mode.

**Parse shape.** Two bullet buckets, each introduced by a bucket-header line:

```markdown
## ANALYTICAL PERSPECTIVES

Thinking tools (always loaded):
- OPV
- KVI
- FGL

Mental models (always loaded):
- nash-equilibrium
- batna
```

The bucket headers are matched case-insensitively by regex: the thinking-tools bucket accepts any header line of the form `Thinking tool(s) …:` or `Tier 1 …:`; the mental-models bucket accepts `Mental model(s) …:`, `Tier 3 …:`, or `Lens(es) …:`. Either bucket may be empty or absent. Bullets without a preceding bucket header are ignored. Within-bucket order is preserved.

**Runtime resolution.** Two module-level registries resolve the listed ids at `build_system_prompt_for_gear` time:

- **Thinking-tool ids** resolve against the `### ` headings of the `## Tier 1 Tool Definitions` section of `~/ora/thinking-tools.md` (loader: `_load_thinking_tools`). The tool id is the heading text up to the em-dash (`AGO — Aims, Goals, Objectives` → `AGO`); for headings without an em-dash the parenthetical alias is stripped (`Provocation (Po)` → `Provocation`); a bare heading (`Concept Fan`) is its own id.
- **Mental-model ids** resolve against the compiled lens collection (loader: `_load_mental_models`) — currently 240 content Lens notes from `~/ora/lenses/`, vault-paired with `Lenses/` (INDEX is not a Lens). The id is the filename without extension (`nash-equilibrium.md` → `nash-equilibrium`); YAML frontmatter is stripped from the projected body.

**Injection target.** The resolved definitions inject into the **Breadth analyst's system prompt only**, as a `## ANALYTICAL PERSPECTIVES — <mode>` block placed ahead of the `## MODE INSTRUCTIONS` section. The Depth analyst is intentionally skipped — depth is already focused; the perspectives layer is a lateral-thinking aid. The evaluator, reviser, verifier, consolidator, and formatter never receive it.

**Optional-injection semantics.** A missing thinking-tool source yields an empty thinking-tool registry plus a stderr log line. Unknown optional perspective ids are skipped with a stderr warning (`[perspective_loader] Unknown …`); an empty or absent `## ANALYTICAL PERSPECTIVES` section is a clean no-op. This does not weaken full routing-source validation: declared mode/lens dependency references must resolve before the compiled collection is exposed.

**Caching.** These process-lifetime projections load once at first use. A fresh process reads changes to `~/ora/thinking-tools.md` and the compiled `~/ora/lenses/` sources; no persistent routing cache is written.

**Distinctions.**

- The `## ANALYTICAL BRIEF AND EVALUATION CRITERIA` baseline injection goes to **all** role-specific pipeline steps; the Analytical Perspectives injection goes to the Breadth analyst only.
- The `lens_dependencies` YAML block (`Reference — Lens Library Specification.md` §5) is a dispatch-gating dependency declaration — it governs whether a mode may dispatch given lens availability. It is not a prompt-content injection; `## ANALYTICAL PERSPECTIVES` is the prompt-content mechanism.

Mode-author guidance for the section lives in `Reference — Mode Specification Template.md` (Locked Template + Template Field Quick Reference).

---

## End-to-End Worked Example

**Prompt.** "give me a quick steelman of this op-ed on housing policy"

**Stage 1 — Pre-Analysis Filter.**
- Signal vocabulary matches: `steelman` (strong, T15), `quick` (depth-Tier-1), `op-ed` (artifact-type=argument).
- No bypass triggers.
- `bypass_to_direct_response: false`.
- Forward to Stage 2 with matches.

**Stage 2 — Prompt Sufficiency Analyzer.**
- `steelman` → T15 + `steelman-construction` mode (strong signal).
- `quick` → Tier-1 depth (strong signal).
- `op-ed` → artifact-type=argument → activates T1 cross-reference for `steelman-construction` (per Decision G re-home).
- Multiple corroborating signals from T15 → complete combination → no disambiguation questions.
- Cross-territory check: T15 home with T1 cross-reference is the configured pattern; not a conflict.
- `dispatched_mode_id: steelman-construction`
- `confidence: high`
- Forward to Stage 3.

**Stage 3 — Input Completeness Check.**
- Mode: `steelman-construction`.
- Contract version: `accessible_mode` (no expert signals).
- Required field: `argument_or_artifact_to_steelman` → present (the op-ed text is in the prompt or attached).
- Underspecification check: passes (op-ed text is concrete content).
- `inputs_complete: true`.
- Forward to Stage 4.

**Stage 4 — Mode Execution.**
- Load `~/ora/modes/steelman-construction.md`.
- Read its compiled Default Gear and analytical prompt sections.
- Compose dispatch announcement: "I'll make the strongest case for this op-ed *(steelman construction)*."
- Execute the mode's Gear-specific pipeline at the requested light depth.
- Output the steelman artifact per `output_contract`.

**Friction-reducer success.** The prompt contained complete signal (mode-name + depth + artifact-type), so no disambiguation questions fired. The pipeline dispatched in one orchestrator turn.

---

## Pipeline Failure Modes and Handling

The pipeline exhibits known failure modes; each has a documented response.

### Failure 1 — Stage 1 false-bypass

**Symptom.** An analytical prompt is mistakenly classified as bypass and routed to direct response.
**Detection.** User repeats the prompt or asks for analysis explicitly.
**Response.** Re-run Stage 1 in permissive mode (skip bypass detection); forward to Stage 2.

### Failure 2 — Stage 2 disambiguation loop

**Symptom.** User's answer to a disambiguation question is itself ambiguous; Stage 2 asks another question; user's answer is again ambiguous; loop.
**Detection.** Same disambiguation context elicits ≥3 ambiguous answers.
**Response.** Apply default-on-ambiguity rules (Tier-2, neutral stance, general specificity). Dispatch to default mode and surface that the default was chosen.

### Failure 3 — Stage 3 missing-input loop

**Symptom.** User does not supply requested missing input (declines, doesn't have it, or doesn't understand the request).
**Detection.** ≥2 missing-input requests for the same field unresolved.
**Response.** Offer graceful-degradation to lightest sibling (which has the smallest required-input contract). If even the lightest sibling cannot run, exit pipeline with explanation.

### Failure 4 — Invalid routing source or reference

**Symptom.** A declaration, target, required source, or bound condition cannot be resolved truthfully.
**Detection.** The compiler rejects the full collection before a partial library reaches routing consumers.
**Response.** Surface the source error and correct the owning canonical and its pair. Do not fabricate a missing mode, silently substitute a Gear, or restore the retired runtime-configuration authority.

### Failure 5 — Mode execution exception

**Symptom.** Mode pipeline stage (e.g., F-Evaluate) raises an exception or produces no output.
**Detection.** Pipeline-stage output is empty or error-typed.
**Response.** Re-run failed stage once with a fresh context. If it fails again, exit with the partial output produced and an explanation.

---

## Architectural Invariants

These invariants hold across all pipeline behavior. They are the bedrock for orchestrator implementation (Phase 9) and for any future revision of the pipeline.

1. **Plain-language disambiguation only.** Every Stage 2 and Stage 3 question uses the Disambiguation Style Guide vocabulary. No mode names, territory labels, methodology jargon, or "atomic vs. molecular" distinctions in the question itself.
2. **Educational parenthetical convention.** Every dispatch announcement uses `"plain language *(named technique)*"`. No bare mode names or bare technique names. Acronyms expanded per Decision E.
3. **Default-on-ambiguity is Tier-2 + neutral + general.** Never Tier-1 by default; never Tier-3 by default; never adversarial by default.
4. **Friction reducer skips answered questions.** A signal already supplied by the prompt does not trigger a disambiguation question on the same content.
5. **Invalid source collections do not partially load.** Routing does not silently substitute defaults for missing declarations or unresolved operative references.
6. **Cross-territory disambiguation precedes within-territory.** When signals straddle two territories, the cross-territory question fires first.
7. **Graceful degradation preserves a real choice.** Stage 3 validates the lighter sibling's own contract and explicitly requests material that it also needs; lighter does not mean runnable without a subject.
8. **Vault canonical and ora runtime stay synchronized.** The compiler reads the paired mode, architecture, lens, and molecular sources; their registered canonical/runtime pairs must stay synchronized.
9. **Explicit user pick supersedes inference.** A valid `manual_mode_selection` from the caller overrides Stage 2's dispatch (except on Stage 1 bypass); the pipeline is authoritative only in the absence of an explicit pick.

---

## Cross-Reference Map

This file is **read by** the orchestrator implementation (Phase 9 reads its ora-runtime pair `~/ora/architecture/pre-routing-pipeline.md`).

The Baseline Criteria Injection (§ above) is **implemented in** `~/ora/orchestrator/boot.py::build_system_prompt_for_gear`; its injected content is sourced from the mode files (`~/ora/modes/<mode_id>.md`).

This file **references**:
- Mode Selection/Activation Guidance (Stage 1 + Stage 2; displayed by the generated `Registry — Signal Vocabulary Registry.md`)
- `Reference — Within-Territory Disambiguation Trees.md` (Stage 2)
- `Reference — Cross-Territory Adjacency.md` (Stage 1 + Stage 2)
- `Reference — Disambiguation Style Guide.md` (Stage 2 + Stage 3 question phrasing)
- `Reference — Mode Specification Template.md` (Stage 3 contract version selection)
- Mode Default Gear, RAG profile, and analytical body sections (Stage 4)
- `Reference — Analytical Territories.md` (territory inventory; consulted across stages)

This file **is referenced from**:
- `Registry — Mode Registry.md` (Phase 7 rewrite — opens with pipeline overview)
- `Reference — Ora Overview and Document Registry.md` (Phase 7 update)
- `~/ora/CLAUDE.md` (Phase 7 update — pairing rules + orchestrator architecture pointer)
- `Framework — Documentation-Code Parity.md` (Phase 1 update — drift correction registry)

*End of Reference — Pre-Routing Pipeline Architecture.*
