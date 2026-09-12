# Reference — Cross-Territory Adjacency

This file documents the cross-territory disambiguation patterns consulted by Stage 1 of the pre-routing pipeline (filter and territory identification) and by Stage 2 (sufficiency analyzer) when a prompt's signals straddle two territories. For every adjacent territory pair (or triplet), it specifies why the territories sit close, the single plain-language question that distinguishes them, the routing rule for each plausible answer, paired prompt examples, and — where a prompt legitimately fits both — the sequential-dispatch order. Within-territory disambiguation (choosing among modes inside a single territory) is a separate concern and lives in `Reference — Within-Territory Disambiguation Trees.md`.

The fenced YAML questions and answer destinations are the authored routing authority. Their mappings cover every pair declared by the territory adjacency inventory, including each pair in the mechanism/process/structure cluster. An unanswered boundary has an explicit route-by-intent fallback: it remains an unresolved clarification, never an arbitrary territory selection. Ordered destination lists express sequential selection; they do not execute the analysis stages. Qualifications preserve when that sequence is appropriate. Examples and explanatory notes illustrate the records; regenerated readable views must be marked derived. Optional post-analysis follow-ups are judgments for the human or model conducting the analysis, not additional deterministic pre-routing conditions.

---

### T1 ↔ T2 (Argumentative Artifact ↔ Interest and Power)

**Why adjacent.** Both can take a published article, op-ed, memo, or stated position as input. The same artifact can be evaluated for whether the argument holds up (T1) or for whose interests are served if people accept it (T2).

```yaml
cross_territory_questions:
  "T1|T2": "cross-t1-t2"
routing_questions:
  - id: cross-t1-t2
    text: "Are you mostly asking whether the argument itself holds up, or who benefits if people accept it?"
    territories: ["T1","T2"]
    answers:
      - {"phrases":["argument-soundness focus","whether the argument holds up","argument itself"],"targets":[{"kind":"territory","id":"T1"}],"qualification":"Coherence, frame, whole-argument or propaganda examination selected within T1."}
      - {"phrases":["interest-pattern focus","who benefits","interests served"],"targets":[{"kind":"territory","id":"T2"}],"qualification":"Cui Bono, Boundary Critique, Wicked Problems or Decision Clarity selected within T2."}
      - {"phrases":["both","holds up and who benefits"],"targets":[{"kind":"territory","id":"T1"},{"kind":"territory","id":"T2"}],"qualification":"Sequential dispatch: argument soundness first, then the interest pattern."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Is this op-ed on housing policy rigorous?"* → T1.
- *"Whose interests does this op-ed actually serve?"* → T2.
- *"Walk me through whether this argument holds up and also who's behind it."* → T1 + T2 (sequential, T1 first).
- *"This think-tank brief recommends X — is it well-argued, or is it just dressing up someone's agenda?"* → T1 + T2 (sequential, T1 first).

**Sequential dispatch note.** When both fire, T1 runs first because argument-soundness is the lighter, foundational evaluation; T2 then layers interest-pattern analysis on top of an artifact whose internal structure has already been characterized.

### T1 ↔ T5 (Argumentative Artifact ↔ Hypothesis Evaluation)

**Why adjacent.** Competing positions in a debate can be treated either as full arguments-as-artifacts to be audited (T1) or as propositions to be weighed against evidence (T5). The surface form — "two positions, which one wins" — looks similar.

```yaml
cross_territory_questions:
  "T1|T5": "cross-t1-t5"
routing_questions:
  - id: cross-t1-t5
    text: "Are the competing positions each a complete argument you want me to audit, or are they propositions you want weighed against evidence?"
    territories: ["T1","T5"]
    answers:
      - {"phrases":["argument-as-artifact","complete argument","structured argument","audit each"],"targets":[{"kind":"active","id":"argument-audit"}],"qualification":"Audit each full argument as an artifact in T1."}
      - {"phrases":["proposition-against-evidence","propositions","candidate explanation","weighed against evidence"],"targets":[{"kind":"territory","id":"T5"}],"qualification":"Choose the depth of hypothesis evaluation within T5."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Two op-eds disagree about minimum wage — which has the stronger argument?"* → T1 (audit each).
- *"Two explanations for the company's revenue dip — which fits the evidence better?"* → T5 (ACH or differential).
- *"Critics offer three frames for what went wrong; help me evaluate them."* → If frames are full arguments → T1; if they are causal hypotheses → T5.

### T1 ↔ T9 (Argumentative Artifact ↔ Paradigm and Assumption Examination)

**Why adjacent.** Both engage with frames. T1's Frame Audit operates on a single artifact's frame; T9 operates on the comparison or examination of paradigms across artifacts or positions.

```yaml
cross_territory_questions:
  "T1|T9": "cross-t1-t9"
routing_questions:
  - id: cross-t1-t9
    text: "Are you evaluating this single argument's frame, or comparing different paradigms that frame the issue differently?"
    territories: ["T1","T9"]
    answers:
      - {"phrases":["single-artifact frame","single argument","this article","single frame"],"targets":[{"kind":"active","id":"frame-audit"}],"qualification":"Surface the frame of the single argumentative artifact in T1."}
      - {"phrases":["multi-paradigm","different paradigms","compare paradigms","across artifacts"],"targets":[{"kind":"territory","id":"T9"}],"qualification":"Examine, compare or map paradigms within T9."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"What frame is this article smuggling in?"* → T1 (Frame Audit on the single article).
- *"How do progressives and conservatives frame this issue differently?"* → T9 (Frame Comparison).
- *"Map the major worldviews in this debate."* → T9 (Worldview Cartography).

### T1 ↔ T10 (Argumentative Artifact ↔ Conceptual Clarification)

**Why adjacent.** When an argument hinges on a contested concept, the same prompt can be heard as either "audit the argument" (T1) or "clarify the concept first" (T10).

```yaml
cross_territory_questions:
  "T1|T10": "cross-t1-t10"
routing_questions:
  - id: cross-t1-t10
    text: "Is the issue with how the argument deploys a specific concept (clarify the concept first), or with how the argument coheres given any reasonable reading of the concept?"
    territories: ["T1","T10"]
    answers:
      - {"phrases":["concept-precision","definitional slippage","clarify the concept first","concept"],"targets":[{"kind":"territory","id":"T10"}],"qualification":"Clarify or engineer the concept first."}
      - {"phrases":["argument-coherence","structural problems","coheres","premises"],"targets":[{"kind":"territory","id":"T1"}],"qualification":"Evaluate argument coherence regardless of reasonable concept interpretation."}
      - {"phrases":["both","clarify first then audit","concept first then argument"],"targets":[{"kind":"territory","id":"T10"},{"kind":"territory","id":"T1"}],"qualification":"When concept clarification is needed before the argument audit can proceed, clarify first and audit the now-clarified version second."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"What does the author even mean by 'freedom' here?"* → T10.
- *"Does the author's argument actually follow from their premises?"* → T1.
- *"The whole piece rests on 'merit' — is that doing real work?"* → T10 first, then optionally T1.

**Sequential dispatch note.** When concept clarification is needed before argument audit can proceed, T10 runs first; T1 follows on the now-clarified version.

### T1 ↔ T15 (Argumentative Artifact ↔ Artifact Evaluation by Stance — Steelman cross-territory case)

**Why adjacent.** Both can evaluate an argument. T1 evaluates the argument *as an argument* for soundness; T15 evaluates it *as a proposal* by adopting a defined stance (steelman / push back / weigh both). The Steelman mode is the canonical cross-territory case.

```yaml
cross_territory_questions:
  "T1|T15": "cross-t1-t15"
routing_questions:
  - id: cross-t1-t15
    text: "Want me to evaluate the argument's soundness (does it hold up?), or evaluate the proposal with a particular stance (steelman / push back / weigh both)?"
    territories: ["T1","T15"]
    answers:
      - {"phrases":["soundness","does it hold up","argument as an argument"],"targets":[{"kind":"territory","id":"T1"}],"qualification":"Evaluate argument soundness."}
      - {"phrases":["evaluate the proposal","particular stance","steelman","push back","weigh both"],"targets":[{"kind":"territory","id":"T15"}],"qualification":"T15 owns stance-bearing proposal evaluation; an argument being steelmanned retains its T1 cross-reference without acquiring a second home territory."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Steelman cross-territory disposition (per Decision G).** Steelman's home is T15 (its primary work is stance-bearing artifact evaluation — constructing the strongest version of a proposal). When the artifact under steelmanning is itself an argument, the T1 cross-reference activates so that argument-coherence considerations inform the steelmanned reconstruction. The mode is *not* dual-citizened — home is T15; T1 is consulted as cross-reference.

**Examples.**
- *"Does this argument hold up?"* → T1.
- *"Steelman this proposal — make the strongest version of it."* → T15.
- *"Steelman this argument."* → T15 (home), with T1 cross-reference active because the artifact is an argument.
- *"Push back hard on this plan."* → T15 (Red Team or Balanced Critique).
- *"Weigh both sides of this proposal."* → T15 (Balanced Critique).

### T2 ↔ T8 (Interest and Power ↔ Stakeholder Conflict)

**Why adjacent.** Both involve multiple parties whose interests diverge. T2 asks who benefits and who has power; T8 asks how the conflict among parties is structured and what integrative possibilities exist.

```yaml
cross_territory_questions:
  "T2|T8": "cross-t2-t8"
routing_questions:
  - id: cross-t2-t8
    text: "Mostly asking who benefits or has power, or asking how the parties' competing claims can be worked through?"
    territories: ["T2","T8"]
    answers:
      - {"phrases":["power","who benefits","has power","interest analysis"],"targets":[{"kind":"territory","id":"T2"}],"qualification":"Descriptive power and interest analysis."}
      - {"phrases":["conflict structure","competing claims","positions map","stakeholders"],"targets":[{"kind":"territory","id":"T8"}],"qualification":"Map the parties and their conflict structure."}
      - {"phrases":["both","interest landscape and positions"],"targets":[{"kind":"territory","id":"T2"},{"kind":"territory","id":"T8"}],"qualification":"When interest analysis grounds conflict mapping, analyze interests first."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Whose interests are being served by this zoning policy?"* → T2.
- *"Who are all the stakeholders in this dispute and how do their positions map?"* → T8.
- *"Three parties want different things — what's the underlying interest landscape, and how do their positions relate?"* → T2 + T8 (sequential, T2 first when interest analysis grounds the conflict structure).

**Sequential dispatch note.** When both fire, T2 typically runs first because interest analysis grounds the descriptive conflict mapping that T8 produces.

### T2 ↔ T13 (Interest and Power ↔ Negotiation and Conflict Resolution)

**Why adjacent.** Both engage with multi-party situations. T2 maps the interest landscape descriptively; T13 produces guidance for active negotiation or mediation.

```yaml
cross_territory_questions:
  "T2|T13": "cross-t2-t13"
routing_questions:
  - id: cross-t2-t13
    text: "Are you mapping the interest landscape, or are you about to negotiate (or advise a negotiation)?"
    territories: ["T2","T13"]
    answers:
      - {"phrases":["mapping","interest landscape","descriptive"],"targets":[{"kind":"territory","id":"T2"}],"qualification":"Map interests descriptively."}
      - {"phrases":["active negotiation","negotiate","advise a negotiation","mediation","mediator"],"targets":[{"kind":"territory","id":"T13"}],"qualification":"Active guidance; mediator stance selects Third-Side within T13."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Who has power in this negotiation and what do they want?"* → T2.
- *"I'm walking into this negotiation tomorrow — help me think through interests and BATNA."* → T13.
- *"As a mediator, how should I structure this conflict?"* → T13 (Third-Side).

### T3 ↔ T6 (Decision-Making Under Uncertainty ↔ Future Exploration)

**Why adjacent.** Decisions are forward-looking and engage uncertainty about future states; future exploration sometimes serves a pending decision. The two can blur when the decision is inseparable from how the future might unfold.

```yaml
cross_territory_questions:
  "T3|T6": "cross-t3-t6"
routing_questions:
  - id: cross-t3-t6
    text: "Are you choosing among options now, or exploring how the future might unfold (irrespective of what you do)?"
    territories: ["T3","T6"]
    answers:
      - {"phrases":["choice-now","choosing among options now","choose","decision"],"targets":[{"kind":"territory","id":"T3"}],"qualification":"Alternatives, criteria and constraints inform a choice now."}
      - {"phrases":["future-shape","future might unfold","scenarios","future"],"targets":[{"kind":"territory","id":"T6"}],"qualification":"Explore projections and possibility spaces irrespective of the immediate choice."}
      - {"phrases":["both","scenarios first then choose","future first then decision"],"targets":[{"kind":"territory","id":"T6"},{"kind":"territory","id":"T3"}],"qualification":"When the future must be explored before framing the decision, map scenarios first and choose second."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Should I take this job offer or stay where I am?"* → T3.
- *"What does the next decade of remote work look like?"* → T6.
- *"I'm deciding whether to invest in this market — paint me the scenarios first, then we'll choose."* → T6 + T3 (sequential, T6 first to map the possibility space, T3 to choose).

**Sequential dispatch note.** When the future must be explored before the decision can be framed, T6 runs first; T3 then operates on the scenarios T6 produces.

### T3 ↔ T7 (Decision-Making Under Uncertainty ↔ Risk and Failure Analysis)

**Why adjacent.** Decisions involve risk as one input; risk analysis sometimes serves a pending decision. The disambiguator is whether the user wants a balanced choice procedure or a focused failure investigation.

```yaml
cross_territory_questions:
  "T3|T7": "cross-t3-t7"
routing_questions:
  - id: cross-t3-t7
    text: "Choosing among options where risk is one input among several, or specifically stress-testing how things could fail?"
    territories: ["T3","T7"]
    answers:
      - {"phrases":["multi-input choice","choosing among options","risk is one input","choice"],"targets":[{"kind":"territory","id":"T3"}],"qualification":"Risk is one input to a balanced choice procedure."}
      - {"phrases":["failure-focused","stress-testing","how things could fail","failure"],"targets":[{"kind":"territory","id":"T7"}],"qualification":"Within T7 distinguish the examined object: an action plan dispatches pre-mortem-action in T6; a system or design dispatches pre-mortem-fragility; precise asymmetric exposure selects fragility-antifragility-audit."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Should we launch in Q3 or Q4 — risk is a factor."* → T3.
- *"Stress-test our launch plan — what could break it?"* → the risk question, then `pre-mortem-action` in T6 because the examined object is an action plan.
- *"What are the worst-case scenarios for this strategy?"* → T7 (Fragility) or T6 (Wicked Future) depending on scope.

### T3 ↔ T8 (Decision-Making Under Uncertainty ↔ Stakeholder Conflict)

**Why adjacent.** Decisions sometimes involve multiple parties. The disambiguator is whether the user owns the decision (parties as inputs) or whether the parties' conflict itself is the analytical object.

```yaml
cross_territory_questions:
  "T3|T8": "cross-t3-t8"
routing_questions:
  - id: cross-t3-t8
    text: "Is this fundamentally your decision to make (with the parties as inputs), or is it a situation where the parties' conflict itself is what needs to be worked through first?"
    territories: ["T3","T8"]
    answers:
      - {"phrases":["your-decision","my decision","your decision","parties as inputs","make a call"],"targets":[{"kind":"territory","id":"T3"}],"qualification":"The user owns the decision; the parties are inputs."}
      - {"phrases":["parties' conflict first","conflict itself","conflict first","understand the conflict"],"targets":[{"kind":"territory","id":"T8"}],"qualification":"The conflict among parties is the analytical object."}
      - {"phrases":["both","conflict first then decision","map positions before deciding"],"targets":[{"kind":"territory","id":"T8"},{"kind":"territory","id":"T3"}],"qualification":"Characterize conflict before framing the decision when the positions are not yet mapped."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"My team wants A, my boss wants B, the client wants C — I have to decide."* → T3.
- *"My team wants A, my boss wants B, the client wants C — help me understand the conflict before I touch it."* → T8.
- *"The board is split three ways on the strategic direction — I need to make a call but I don't yet know how the positions even relate."* → T8 first, then T3.

**Sequential dispatch note.** When the conflict structure must be characterized before the decision can be framed, T8 runs first; T3 follows once the parties and their positions are mapped.

### T4 ↔ T9 (Causal Investigation ↔ Paradigm and Assumption Examination)

**Why adjacent.** Both ask "why" — but at different levels. T4 traces causes within the assumed frame; T9 asks whether the frame itself is generating the apparent problem.

```yaml
cross_territory_questions:
  "T4|T9": "cross-t4-t9"
routing_questions:
  - id: cross-t4-t9
    text: "Looking for the causes within how the problem is currently framed, or stepping back to ask whether the framing itself is generating the problem?"
    territories: ["T4","T9"]
    answers:
      - {"phrases":["within-frame","causes within","causes","currently framed"],"targets":[{"kind":"territory","id":"T4"}],"qualification":"Investigate causes within the assumed frame."}
      - {"phrases":["frame-as-cause","framing itself","frame","paradigm"],"targets":[{"kind":"territory","id":"T9"}],"qualification":"Examine whether the frame generates the apparent problem; a T4 follow-up may become useful after resetting the frame."}
      - {"phrases":["reset the frame then trace causes","frame first then causes"],"targets":[{"kind":"territory","id":"T9"},{"kind":"territory","id":"T4"}],"qualification":"Optional T4 follow-up follows the frame reset when causal investigation is still needed."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Why does our hiring funnel keep narrowing?"* → T4 (within-frame).
- *"Why does every solution to this problem keep failing?"* → T9 (signal of frame-issue), possibly with T4 follow-up once the frame is reset.
- *"What's causing the engagement drop?"* → T4.
- *"Why do we keep having the same fight in different forms?"* → T9 (the recurrence pattern signals frame-as-cause).

### T4 ↔ T16 (Causal Investigation ↔ Mechanism Understanding)

**Why adjacent.** Both engage with how things produce outcomes. T4 traces backward from outcome to cause; T16 explains how the parts of a phenomenon work together to produce its behavior.

```yaml
cross_territory_questions:
  "T4|T16": "cross-t4-t16"
routing_questions:
  - id: cross-t4-t16
    text: "Tracing back to causes, or explaining how the parts produce the behavior?"
    territories: ["T4","T16"]
    answers:
      - {"phrases":["backward-to-causes","tracing back","causes","why did"],"targets":[{"kind":"territory","id":"T4"}],"qualification":"Trace from outcome back to cause."}
      - {"phrases":["how-it-works","how it works","parts produce the behavior","mechanism"],"targets":[{"kind":"territory","id":"T16"}],"qualification":"Explain the working principle producing the behavior."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Why did the rollout fail?"* → T4.
- *"How does this recommendation algorithm actually work?"* → T16.
- *"What caused the market shift?"* → T4.
- *"How does fiscal policy translate into household spending?"* → T16.

### T4 ↔ T17 (Causal Investigation ↔ Process and System Analysis)

**Why adjacent.** Both can engage with workflows or systems. T4 asks why a pattern recurs; T17 maps the process as it currently is, identifying components, flows, and bottlenecks.

```yaml
cross_territory_questions:
  "T4|T17": "cross-t4-t17"
routing_questions:
  - id: cross-t4-t17
    text: "Why does this keep happening (causes), or how does this currently work (process map)?"
    territories: ["T4","T17"]
    answers:
      - {"phrases":["causal investigation","why does this keep happening","causes","why"],"targets":[{"kind":"territory","id":"T4"}],"qualification":"Explain why the pattern recurs."}
      - {"phrases":["process mapping","how does this currently work","process map","workflow"],"targets":[{"kind":"territory","id":"T17"}],"qualification":"Map current components, flows and bottlenecks."}
      - {"phrases":["both","map the process then investigate causes","process first then causes"],"targets":[{"kind":"territory","id":"T17"},{"kind":"territory","id":"T4"}],"qualification":"When causal investigation requires a process map first, characterize the workflow before asking why it stalls."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Why does our deployment process keep producing outages?"* → T4.
- *"Walk me through our deployment process as it currently runs."* → T17.
- *"Map the workflow."* → T17.
- *"Why does the workflow keep stalling at the same step?"* → T4 (with T17 likely as upstream input).

**Sequential dispatch note.** When causal investigation requires a process map first (you can't ask why the workflow stalls without knowing what the workflow is), T17 runs first; T4 follows.

### T5 ↔ T9 (Hypothesis Evaluation ↔ Paradigm and Assumption Examination)

**Why adjacent.** Both engage with competing explanations. T5 weighs them within a shared frame; T9 asks whether the disagreement is really about how to see the issue rather than which proposition is true.

```yaml
cross_territory_questions:
  "T5|T9": "cross-t5-t9"
routing_questions:
  - id: cross-t5-t9
    text: "Are you weighing competing explanations within a shared understanding of the problem, or are the explanations using such different frames that the disagreement is really about how to see the issue?"
    territories: ["T5","T9"]
    answers:
      - {"phrases":["within-frame hypothesis comparison","shared understanding","competing explanations","same frame"],"targets":[{"kind":"territory","id":"T5"}],"qualification":"Weigh candidate explanations within a shared frame."}
      - {"phrases":["inter-frame disagreement","different frames","different paradigms","how to see the issue"],"targets":[{"kind":"territory","id":"T9"}],"qualification":"Examine how the frames differ before treating the disagreement as competing propositions."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Three theories explain the data — which fits best?"* → T5.
- *"The economists and the sociologists disagree — but they're not even asking the same question."* → T9.
- *"Doctor A says it's X, doctor B says it's Y — same evidence."* → T5.
- *"Doctor A and the homeopath disagree — but they're operating from different paradigms entirely."* → T9.

### T6 ↔ T7 (Future Exploration ↔ Risk and Failure Analysis — Pre-Mortem parse)

**Why adjacent.** Both adopt an adversarial-future stance — imagining what could go wrong. The Pre-Mortem operation appears to fit both, but per Decision D's parsing principle the candidate mode is split rather than dual-citizened.

**Disposition per Decision D (parse, not dual citizenship).** Pre-Mortem is parsed into two modes that share the `klein-pre-mortem` lens but differ in operation:
- `pre-mortem-action` (T6): adversarial-future stance applied to *the action plan* — what could go wrong with this plan as it unfolds.
- `pre-mortem-fragility` (T7): adversarial-future stance applied to *the system or design* — what failure modes does this structure exhibit under stress.

```yaml
cross_territory_questions:
  "T6|T7": "cross-t6-t7"
routing_questions:
  - id: cross-t6-t7
    text: "Is this about an action plan that could fail, or about a system or design with structural fragilities?"
    territories: ["T6","T7"]
    answers:
      - {"phrases":["action-plan focus","action plan","plan","rollout","initiative rollout"],"targets":[{"kind":"active","id":"pre-mortem-action"}],"qualification":"T6 parsed mode: the plan unfolds in time; investigate what could derail it."}
      - {"phrases":["system-or-design fragility focus","system","design","structural fragilities","architecture"],"targets":[{"kind":"active","id":"pre-mortem-fragility"}],"qualification":"T7 parsed mode: examine structural failure under stress. Both parsed modes remain; they share the klein-pre-mortem lens."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"We're launching this campaign next month — pre-mortem it."* → T6 (Pre-Mortem Action: the plan unfolds in time, what derails it).
- *"This architecture is going into production — pre-mortem it."* → T7 (Pre-Mortem Fragility: the system is structural, where does it break).
- *"Run a pre-mortem on this initiative."* → ambiguous; sufficiency analyzer asks whether the focus is the rollout (T6) or the design (T7).

### T7 ↔ T15 (Risk and Failure Analysis ↔ Artifact Evaluation by Stance — Red Team case)

**Why adjacent.** Both stress-test artifacts. T15's Red Team modes (`red-team-assessment` / `red-team-advocate` — both) model an adversarial actor trying to defeat the artifact; T7's Fragility Audit looks at structural weaknesses regardless of any actor.

```yaml
cross_territory_questions:
  "T7|T15": "cross-t7-t15"
routing_questions:
  - id: cross-t7-t15
    text: "Adversarial-actor stress test (someone is trying to defeat this), or structural-fragility audit (where could this break under any pressure)?"
    territories: ["T7","T15"]
    answers:
      - {"phrases":["actor-modeling","adversarial actor","someone is trying to defeat this","adversary"],"question":"t15-red-team-operation","qualification":"T15 red-team branch: own-decision assessment is the default; external-use advocacy remains a distinct choice."}
      - {"phrases":["structural fragility","any pressure","no adversary","where could this break"],"targets":[{"kind":"territory","id":"T7"}],"qualification":"Structural failure does not require an adversarial actor; select the appropriate T7 method."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"How would a competitor attack this strategy?"* → T15 Red Team Assessment (own-decision framing).
- *"Where would this strategy break under market stress regardless of who's pushing on it?"* → T7 Fragility Audit.
- *"How would a hostile reviewer pick apart this paper?"* → T15 Red Team Assessment if the goal is to fix vulnerabilities before submission; Red Team Advocate if the goal is to prepare a brief against the paper for an actual hostile reviewer.
- *"What are the load-bearing assumptions in this paper that would crack first?"* → T7 Fragility Audit.

### T8 ↔ T13 (Stakeholder Conflict ↔ Negotiation and Conflict Resolution)

**Why adjacent.** Both engage with multi-party conflict situations. T8 is descriptive (mapping the conflict structure); T13 is active (guiding negotiation or mediation).

```yaml
cross_territory_questions:
  "T8|T13": "cross-t8-t13"
routing_questions:
  - id: cross-t8-t13
    text: "Mapping the conflict structure, or guiding active negotiation?"
    territories: ["T8","T13"]
    answers:
      - {"phrases":["mapping","conflict structure","descriptive"],"targets":[{"kind":"territory","id":"T8"}],"qualification":"Describe and map the conflict structure."}
      - {"phrases":["active","negotiation","mediation","guiding"],"targets":[{"kind":"territory","id":"T13"}],"qualification":"Guide negotiation or mediation."}
      - {"phrases":["both","understand before intervening","map conflict then negotiate"],"targets":[{"kind":"territory","id":"T8"},{"kind":"territory","id":"T13"}],"qualification":"When negotiation is needed but conflict structure is not mapped, mapping precedes active guidance."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Lay out who's on what side and why."* → T8.
- *"I'm sitting down with them tomorrow — help me prepare."* → T13.
- *"As mediator I need to understand the conflict before I intervene."* → T8 first, then T13.

**Sequential dispatch note.** When active negotiation guidance is needed but the conflict structure is not yet mapped, T8 runs first; T13 follows.

### T9 ↔ T12 (Paradigm and Assumption Examination ↔ Cross-Domain and Knowledge Synthesis)

**Why adjacent.** Both engage with multiple frames or knowledge bodies. T9 examines paradigms (suspending, comparing, critiquing them); T12 integrates across them.

```yaml
cross_territory_questions:
  "T9|T12": "cross-t9-t12"
routing_questions:
  - id: cross-t9-t12
    text: "Stepping back to examine the paradigms, or integrating across paradigms?"
    territories: ["T9","T12"]
    answers:
      - {"phrases":["examining","examine the paradigms","compare paradigms","worldview"],"targets":[{"kind":"territory","id":"T9"}],"qualification":"Suspend, compare or critique paradigms."}
      - {"phrases":["integrating","integrating across paradigms","integrate","synthesis"],"targets":[{"kind":"territory","id":"T12"}],"qualification":"Integrate across knowledge bodies, hold productive tension or identify a structural analogy."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Compare how economics and sociology frame this."* → T9.
- *"Integrate what economics and sociology each contribute here."* → T12.
- *"What worldview is each side bringing?"* → T9.
- *"Hold thesis and antithesis in productive tension."* → T12 (Dialectical Analysis).

### T11 ↔ T16 ↔ T17 (Mechanism / Process / Structure cluster)

**Why adjacent.** These three cluster tightly because they all engage with how something works internally — but they ask different questions about it. T16 asks how the gears interlock to produce behavior; T17 asks how the flow runs in sequence; T11 asks how the parts relate as a structure.

```yaml
cross_territory_questions:
  "T11|T16": "cross-t11-t16-t17"
  "T11|T17": "cross-t11-t16-t17"
  "T16|T17": "cross-t11-t16-t17"
routing_questions:
  - id: cross-t11-t16-t17
    text: "Is the question about how this works (the gears), about the flow or process (sequence), or about how the parts relate (structure)?"
    territories: ["T11","T16","T17"]
    answers:
      - {"phrases":["how","gears","mechanism","working principle"],"targets":[{"kind":"territory","id":"T16"}],"qualification":"Explain how the parts produce behavior."}
      - {"phrases":["flow","process","sequence","procedural"],"targets":[{"kind":"territory","id":"T17"}],"qualification":"Map the sequence or lived flow."}
      - {"phrases":["structure","parts relate","relations","formal relationships"],"targets":[{"kind":"territory","id":"T11"}],"qualification":"Map the relations among parts."}
      - {"phrases":["structure and process","relations and flow"],"targets":[{"kind":"territory","id":"T11"},{"kind":"territory","id":"T17"}],"qualification":"When both are needed, structure precedes process."}
      - {"phrases":["structure and mechanism","relations and how it works"],"targets":[{"kind":"territory","id":"T11"},{"kind":"territory","id":"T16"}],"qualification":"When both are needed, structure precedes mechanism."}
      - {"phrases":["process and mechanism","flow and working principle"],"targets":[{"kind":"territory","id":"T17"},{"kind":"territory","id":"T16"}],"qualification":"When both are needed, process precedes mechanism."}
      - {"phrases":["all three","structure process and mechanism"],"targets":[{"kind":"territory","id":"T11"},{"kind":"territory","id":"T17"},{"kind":"territory","id":"T16"}],"qualification":"Lighter structure first, process second, mechanism third; each builds on the prior."}
      - {"phrases":["both"],"targets":[{"kind":"action","id":"sequential-selection"}],"territory_order":["T11","T17","T16"],"qualification":"Select the two territories actually implicated by the prompt; order T11 before T17 before T16. Do not add the unrequested third territory. Keep the canonical question pending if exactly two cannot be identified."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"How does this engine actually produce torque?"* → T16.
- *"Map the production workflow from raw material to finished product."* → T17.
- *"Show me how these departments relate to each other."* → T11.
- *"How does our org chart actually function — what's the real flow?"* → T17 (process focus) or T11 (structural focus) depending on whether the user wants the lived flow or the formal relations.
- *"How does the algorithm work, step by step?"* → T17 if procedural; T16 if the user wants the underlying mechanism.

**Sequential dispatch note.** When two of the three fire on the same input (e.g., "explain how this works and map who reports to whom"), the lighter framing typically runs first: T11 (structure) before T17 (process) before T16 (mechanism), because each successive territory builds on the prior.

### T11 ↔ T19 (Structural Relationship Mapping ↔ Spatial Composition)

**Why adjacent.** Same input — a diagram or visual artifact — answers different questions. T11 reads the diagram as notation: what relations are asserted among elements. T19 reads the diagram as composition: what the layout itself is doing.

```yaml
cross_territory_questions:
  "T11|T19": "cross-t11-t19"
routing_questions:
  - id: cross-t11-t19
    text: "Is the question about what relations the diagram asserts among elements, or about what the layout or composition itself is doing?"
    territories: ["T11","T19"]
    answers:
      - {"phrases":["relation-extraction","relations asserted","notation","who is connected to whom"],"targets":[{"kind":"territory","id":"T11"}],"qualification":"Read the diagram as notation; extract its asserted relations."}
      - {"phrases":["layout-doing","layout","composition","what the layout does"],"targets":[{"kind":"territory","id":"T19"}],"qualification":"Read what the composition itself is doing."}
      - {"phrases":["both","relations and layout","asserts and layout"],"targets":[{"kind":"territory","id":"T11"},{"kind":"territory","id":"T19"}],"qualification":"Extract the more determinate relations first; compositional reading builds on that characterized artifact."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"What does this org chart say about reporting lines?"* → T11.
- *"What is this org chart's layout doing — why does it feel hierarchical even where the lines say it isn't?"* → T19.
- *"Read this network diagram for me — who's connected to whom?"* → T11.
- *"This network diagram is dense in the middle and sparse at the edges — what is that doing to the reader?"* → T19.
- *"Both: tell me what the diagram asserts and what the layout is doing."* → T11 + T19 (sequential, T11 first).

**Sequential dispatch note.** When both legitimately fire on the same input, T11 runs first because relation-extraction is the lighter, more determinate operation; T19 layers compositional reading on top of an artifact whose asserted relations have already been characterized.

### T14 ↔ T20 (Orientation in Unfamiliar Territory ↔ Open Exploration)

**Why adjacent.** Both engage with unfamiliar or open spaces. T14 is analytical — what's here, what's the lay of the land. T20 is generative — what could be, what opens up.

```yaml
cross_territory_questions:
  "T14|T20": "cross-t14-t20"
routing_questions:
  - id: cross-t14-t20
    text: "Trying to orient in an unfamiliar space (what's here), or generating in an open space (what could be)?"
    territories: ["T14","T20"]
    answers:
      - {"phrases":["orienting","orient","what is here","lay of the land"],"targets":[{"kind":"territory","id":"T14"}],"qualification":"Analytical orientation in an unfamiliar space."}
      - {"phrases":["generating","generate","what could be","open exploration"],"targets":[{"kind":"territory","id":"T20"}],"qualification":"Generative exploration of what could open up."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"I'm new to this codebase — give me the lay of the land."* → T14.
- *"I'm interested in this area — help me explore where it might go."* → T20.
- *"What are the major positions in this field?"* → T14.
- *"What questions could I be asking here?"* → T20 (Research Question Generation).

### T19 ↔ T20 (Spatial Composition ↔ Open Exploration on aesthetic input)

**Why adjacent.** Aesthetic inputs (paintings, gardens, scenes) can be read analytically (T19 — defeasible operations on what the composition does) or explored open-endedly (T20 — what the work opens up for the viewer).

```yaml
cross_territory_questions:
  "T19|T20": "cross-t19-t20"
routing_questions:
  - id: cross-t19-t20
    text: "Are you asking for analytical reading of the composition, or for open-ended exploration of what it opens up?"
    territories: ["T19","T20"]
    answers:
      - {"phrases":["analytical reading","composition","read compositionally","layout"],"targets":[{"kind":"territory","id":"T19"}],"qualification":"Perform defeasible analysis of the composition."}
      - {"phrases":["open exploration","what it opens up","explore","fascinates me"],"targets":[{"kind":"territory","id":"T20"}],"qualification":"Open-ended exploration of what the work opens up for the viewer."}
      - {"phrases":["both","read it and let me explore"],"targets":[{"kind":"territory","id":"T19"},{"kind":"territory","id":"T20"}],"qualification":"Analytical reading first grounds the open exploration that follows."}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

**Examples.**
- *"Read this painting compositionally — what is the layout doing?"* → T19.
- *"This painting fascinates me — help me explore why."* → T20.
- *"Walk me through the gestalt of this image."* → T19.
- *"What does this scene open up for me?"* → T20.
- *"Both — read it and let me explore."* → T19 + T20 (sequential, T19 first to ground the exploration).

**Sequential dispatch note.** When both fire on aesthetic input, T19 typically runs first because the analytical reading grounds the open exploration that T20 then carries.

### T2 ↔ T18 (Interest and Power ↔ Strategic Interaction)

**Why adjacent.** T2 maps who benefits and who holds power; T18 analyzes the moves, information and incentives through which strategic players respond to one another.

```yaml
cross_territory_questions:
  "T2|T18": "cross-t2-t18"
routing_questions:
  - id: cross-t2-t18
    text: "Are you asking who benefits and where power sits, or how the players will respond to one another and what incentives shape their choices?"
    territories: ["T2","T18"]
    answers:
      - {"phrases":["who benefits","where power sits","interests","power"],"targets":[{"kind":"territory","id":"T2"}]}
      - {"phrases":["players respond","equilibrium","strategic moves","incentives"],"targets":[{"kind":"territory","id":"T18"}]}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

### T9 ↔ T10 (Paradigm Examination ↔ Conceptual Clarification)

**Why adjacent.** A concept can be embedded in a paradigm dispute. T10 clarifies or revises the meaning of the concept; T9 examines the wider frame that organizes the issue.

```yaml
cross_territory_questions:
  "T9|T10": "cross-t9-t10"
routing_questions:
  - id: cross-t9-t10
    text: "Is the question about what a particular concept means or should mean, or about the wider paradigm through which the issue is understood?"
    territories: ["T9","T10"]
    answers:
      - {"phrases":["particular concept","meaning","definition","what it should mean"],"targets":[{"kind":"territory","id":"T10"}]}
      - {"phrases":["wider paradigm","frame","worldview","assumptions"],"targets":[{"kind":"territory","id":"T9"}]}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

### T2 ↔ T3 (Interest and Power ↔ Decision Under Uncertainty)

**Why adjacent.** Decision Clarity in T2 is the analyst’s document for a third-party decision-maker. T3 works through the user’s choice among alternatives, constraints, uncertainty and criteria.

```yaml
cross_territory_questions:
  "T2|T3": "cross-t2-t3"
routing_questions:
  - id: cross-t2-t3
    text: "Are you analyzing interests and power or preparing decision clarity for another decision-maker, or working through the choice you need to make?"
    territories: ["T2","T3"]
    answers:
      - {"phrases":["interests and power","who benefits"],"targets":[{"kind":"territory","id":"T2"}]}
      - {"phrases":["decision clarity for another decision-maker","for someone else","analyst document"],"targets":[{"kind":"active","id":"decision-clarity"}],"qualification":"The user is the analyst; another person owns the decision."}
      - {"phrases":["my choice","my decision","choose among alternatives","choice I need to make"],"targets":[{"kind":"territory","id":"T3"}]}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

### T7 ↔ T18 (Risk and Failure ↔ Strategic Interaction)

**Why adjacent.** A strategic interaction can be examined for its moves and equilibrium (T18) or for where its structure could fail (T7).

```yaml
cross_territory_questions:
  "T7|T18": "cross-t7-t18"
routing_questions:
  - id: cross-t7-t18
    text: "Are you analyzing the players’ strategic responses, or examining where this strategic structure could fail under pressure?"
    territories: ["T7","T18"]
    answers:
      - {"phrases":["strategic responses","moves","equilibrium","players"],"targets":[{"kind":"territory","id":"T18"}]}
      - {"phrases":["could fail","under pressure","fragility","failure"],"targets":[{"kind":"territory","id":"T7"}]}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

### T13 ↔ T18 (Negotiation ↔ Strategic Interaction)

**Why adjacent.** T13 guides an actual negotiation or mediation. T18 models strategic interaction, including formal payoffs and incentive structures.

```yaml
cross_territory_questions:
  "T13|T18": "cross-t13-t18"
routing_questions:
  - id: cross-t13-t18
    text: "Do you need guidance for conducting a negotiation or mediation, or a model of the strategic game, payoffs and incentives?"
    territories: ["T13","T18"]
    answers:
      - {"phrases":["negotiation guidance","conduct negotiation","mediation","mediator"],"targets":[{"kind":"territory","id":"T13"}]}
      - {"phrases":["strategic game","formal payoffs","equilibrium","incentive structure"],"targets":[{"kind":"territory","id":"T18"}]}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

### T12 ↔ T20 (Knowledge Synthesis ↔ Open Exploration)

**Why adjacent.** T12 integrates existing knowledge bodies or works through their tensions. T20 explores what an open interest could become.

```yaml
cross_territory_questions:
  "T12|T20": "cross-t12-t20"
routing_questions:
  - id: cross-t12-t20
    text: "Are you integrating existing knowledge or working through its tensions, or exploring new directions an open interest could take?"
    territories: ["T12","T20"]
    answers:
      - {"phrases":["integrate existing knowledge","synthesis","tensions","knowledge bodies"],"targets":[{"kind":"territory","id":"T12"}]}
      - {"phrases":["explore new directions","open interest","generative","what could be"],"targets":[{"kind":"territory","id":"T20"}]}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

### T11 ↔ T14 (Relationship Mapping ↔ Orientation)

**Why adjacent.** Orientation in T14 can produce a relationship map as a side-effect. T11 elaborates the relations among particular entities when those relations themselves are the object.

```yaml
cross_territory_questions:
  "T11|T14": "cross-t11-t14"
routing_questions:
  - id: cross-t11-t14
    text: "Do you need the lay of the land in an unfamiliar domain, or a map of how particular entities relate to one another?"
    territories: ["T11","T14"]
    answers:
      - {"phrases":["lay of the land","unfamiliar domain","orientation","terrain"],"targets":[{"kind":"territory","id":"T14"}]}
      - {"phrases":["particular entities","relationships","relations","map how parts relate"],"targets":[{"kind":"territory","id":"T11"}]}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

### T16 ↔ T19 (Mechanism Understanding ↔ Spatial Composition)

**Why adjacent.** T16 explains the mechanism that produces behavior. T19 reads what the spatial arrangement itself makes possible or impossible.

```yaml
cross_territory_questions:
  "T16|T19": "cross-t16-t19"
routing_questions:
  - id: cross-t16-t19
    text: "Are you asking how the mechanism produces its behavior, or what the spatial composition and layout are doing?"
    territories: ["T16","T19"]
    answers:
      - {"phrases":["mechanism","how it works","produces behavior","working principle"],"targets":[{"kind":"territory","id":"T16"}]}
      - {"phrases":["spatial composition","layout","composition","arrangement"],"targets":[{"kind":"territory","id":"T19"}]}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

### T17 ↔ T19 (Process Analysis ↔ Spatial Composition)

**Why adjacent.** T17 maps process, flow and feedback over time. T19 reads the effects of spatial arrangement and composition.

```yaml
cross_territory_questions:
  "T17|T19": "cross-t17-t19"
routing_questions:
  - id: cross-t17-t19
    text: "Is the question about the process, sequence or feedback over time, or about what the spatial layout and composition are doing?"
    territories: ["T17","T19"]
    answers:
      - {"phrases":["process","sequence","feedback","flow over time"],"targets":[{"kind":"territory","id":"T17"}]}
      - {"phrases":["spatial layout","composition","arrangement","layout"],"targets":[{"kind":"territory","id":"T19"}]}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"The boundary remains unresolved without enough intent; retain clarification rather than picking a territory by roster order."}
```

---

*End of Reference — Cross-Territory Adjacency.*
