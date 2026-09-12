# Reference — Within-Territory Disambiguation Trees

*This file holds the within-territory disambiguation trees consulted by Stage 2 of the pre-routing pipeline. Stage 1 identifies the territory; Stage 2 (this file) disambiguates among modes within the territory once the territory is known. Cross-territory disambiguation — selecting between two adjacent territories that both fit the prompt — lives in `Reference — Cross-Territory Adjacency.md`. The style guide for branch questions is in `Reference — Architecture of Analytical Territories and Modes.md` §5.1–§5.7; this file applies it. Trees reflect the post-Wave-4 mode roster per `Reference — Analytical Territories.md`.*

---

## How to read each tree

The fenced YAML records are the authored routing authority: stable question identity, exact question text, answer phrases, typed destinations, qualifications and an explicit default. A branch may ask another canonical question. Destination lists preserve their written order. Deferred candidates remain visible choices and are reported as deferred; they are never silently replaced by an active mode.

The axis notes and default explanations explain these records. Examples and any generated readable views are illustrative, not additional routing declarations. Any regenerated view must be marked derived from these records. T16 and T20 route directly to their declared defaults. T8 keeps its question because its deferred alternative distinguishes a different operation. Optional follow-up records carry their purpose explicitly; an optional follow-up is not automatically asked after every primary question. A declined or irrelevant optional follow-up preserves the existing selection.

The escalation hooks below are instructions for the human or model conducting the selected analysis after that analysis finishes. Their conditional judgments are not deterministic pre-routing predicates, and this source conversion does not automate post-analysis execution.

```yaml
routing_questions:
  - id: generic_intent
    text: "What are you trying to do: check an argument; understand interests or power; decide; investigate causes; compare explanations; explore futures; examine failure or fragility; map stakeholder conflict; examine paradigms; clarify a concept; map relationships; synthesize knowledge; negotiate; get oriented; evaluate a proposal from a stance; understand a mechanism; map a process; analyze strategic interaction; read a composition; explore an open interest; or execute a project or format material?"
    territories: ["T1","T2","T3","T4","T5","T6","T7","T8","T9","T10","T11","T12","T13","T14","T15","T16","T17","T18","T19","T20","T21"]
    answers:
      - {"phrases":["check whether the argument holds up","argument"],"targets":[{"kind":"territory","id":"T1"}]}
      - {"phrases":["figure out who benefits","interests and power"],"targets":[{"kind":"territory","id":"T2"}]}
      - {"phrases":["decide what to do","decision"],"targets":[{"kind":"territory","id":"T3"}]}
      - {"phrases":["understand why this happened","causes"],"targets":[{"kind":"territory","id":"T4"}]}
      - {"phrases":["weigh competing explanations","hypotheses"],"targets":[{"kind":"territory","id":"T5"}]}
      - {"phrases":["explore future possibilities","futures"],"targets":[{"kind":"territory","id":"T6"}]}
      - {"phrases":["stress-test failure and fragility","risk"],"targets":[{"kind":"territory","id":"T7"}]}
      - {"phrases":["map stakeholders and conflict","stakeholders"],"targets":[{"kind":"territory","id":"T8"}]}
      - {"phrases":["examine assumptions and paradigms","paradigms"],"targets":[{"kind":"territory","id":"T9"}]}
      - {"phrases":["clarify concepts and definitions","concepts"],"targets":[{"kind":"territory","id":"T10"}]}
      - {"phrases":["map relationships among parts","relationships"],"targets":[{"kind":"territory","id":"T11"}]}
      - {"phrases":["integrate knowledge or examine productive tension","synthesis"],"targets":[{"kind":"territory","id":"T12"}]}
      - {"phrases":["prepare negotiation or mediation","negotiation"],"targets":[{"kind":"territory","id":"T13"}]}
      - {"phrases":["orient in an unfamiliar field","orientation"],"targets":[{"kind":"territory","id":"T14"}]}
      - {"phrases":["evaluate a proposal with a stance","proposal evaluation"],"targets":[{"kind":"territory","id":"T15"}]}
      - {"phrases":["explain how something works","mechanism"],"targets":[{"kind":"territory","id":"T16"}]}
      - {"phrases":["map a process or feedback system","process"],"targets":[{"kind":"territory","id":"T17"}]}
      - {"phrases":["analyze strategic interaction or incentive design","strategic interaction"],"targets":[{"kind":"territory","id":"T18"}]}
      - {"phrases":["read spatial composition or visual layout","composition"],"targets":[{"kind":"territory","id":"T19"}]}
      - {"phrases":["explore an open interest","open exploration"],"targets":[{"kind":"territory","id":"T20"}]}
      - {"phrases":["execute a project or format material","execution"],"targets":[{"kind":"territory","id":"T21"}]}
    default: {"targets":[{"kind":"fallback","id":"route-by-intent"}],"qualification":"No territory is inferred without enough intent. Keep the question available when the answer remains ambiguous."}
```

---

## T1 — Argumentative Artifact Examination

```yaml
territory_questions:
  "T1": "t1-primary"
territory_defaults:
  "T1": {"kind":"active","id":"coherence-audit"}
routing_questions:
  - id: t1-primary
    text: "Is the question about whether the argument holds together internally, or about the frame/lens it's using to see the issue, or about both at once?"
    territories: ["T1"]
    optional_questions: ["t1-specificity"]
    answers:
      - {"phrases":["internal logic","holds together internally","coherence"],"targets":[{"kind":"active","id":"coherence-audit"}],"qualification":"Tier-2."}
      - {"phrases":["frame","lens","framing"],"targets":[{"kind":"active","id":"frame-audit"}],"qualification":"Tier-2."}
      - {"phrases":["both","both at once"],"targets":[{"kind":"active","id":"argument-audit"}],"qualification":"Molecular Tier-3; confirm the runtime before execution."}
    default: {"targets":[{"kind":"active","id":"coherence-audit"}]}
  - id: t1-specificity
    text: "Is this an everyday argument, does it look like rhetoric/propaganda where the moves are themselves the issue, or are you tracing where this position came from over time?"
    territories: ["T1"]
    qualification: "Optional specificity follow-up; the selected primary mode remains selected for an everyday argument or an ambiguous answer."
    answers:
      - {"phrases":["rhetoric","propaganda","messaging"],"targets":[{"kind":"active","id":"propaganda-audit"}]}
      - {"phrases":["tracing where this position came from over time","position genealogy"],"targets":[{"kind":"deferred","id":"position-genealogy"}],"qualification":"Deferred per CR-6."}
    default: {"targets":[{"kind":"action","id":"keep-selection"}]}
```

**Axes used.** Depth (Q1: light coherence/frame vs. molecular argument-audit) + specificity (Q2: general vs. propaganda vs. genealogy).

**Default explanation.** `coherence-audit` at Tier-2 when ambiguous, with frame-audit available as an escalation hook (very common pairing — coherence often surfaces a hidden frame question).

**Escalation hooks.**
- After `coherence-audit` Tier-2: if the audit surfaces a frame-dependent inconsistency, hook upward to `frame-audit` (sideways/sibling escalation).
- After `frame-audit` Tier-2: if multiple competing frames surface and the question is which to adopt, hook upward to `frame-comparison` in T9 (cross-territory escalation).
- After either `coherence-audit` or `frame-audit`: if both findings interact non-trivially, hook upward to `argument-audit` molecular (Tier-3, depth escalation).
- After any T1 mode: if the question becomes "should we accept this proposal?", hook sideways to T15 (`steelman-construction` or `red-team`).

---

## T2 — Interest and Power Analysis

```yaml
territory_questions:
  "T2": "t2-primary"
territory_defaults:
  "T2": {"kind":"active","id":"cui-bono"}
routing_questions:
  - id: t2-primary
    text: "Are you trying to figure out who benefits from this single situation, or map out a landscape of multiple parties with different stakes, or work through something that feels tangled across many dimensions?"
    territories: ["T2"]
    optional_questions: ["t2-stance","t2-output"]
    answers:
      - {"phrases":["this one situation","single situation","who benefits"],"targets":[{"kind":"active","id":"cui-bono"}],"qualification":"Tier-2."}
      - {"phrases":["landscape of parties","multiple parties","stakeholders"],"targets":[{"kind":"active","id":"stakeholder-mapping"}],"qualification":"Tier-2; cross-territory dispatch into T8."}
      - {"phrases":["tangled","wicked","many interacting interests","many dimensions"],"targets":[{"kind":"active","id":"wicked-problems"}],"qualification":"Molecular Tier-3; confirm runtime."}
    default: {"targets":[{"kind":"active","id":"cui-bono"}]}
  - id: t2-stance
    text: "Are you also asking about whose voices are being left out of the picture entirely?"
    territories: ["T2"]
    qualification: "Optional stance follow-up about voices excluded entirely from the picture."
    answers:
      - {"phrases":["yes","voices left out","voices missing","whose voices"],"targets":[{"kind":"active","id":"boundary-critique"}],"qualification":"Ulrich CSH; sideways stance variant."}
    default: {"targets":[{"kind":"action","id":"keep-selection"}]}
  - id: t2-output
    text: "Are you producing a decision-clarity document for someone else (you're the analyst, they're the decision-maker)?"
    territories: ["T2"]
    qualification: "Optional output follow-up when the user is producing analysis for another decision-maker."
    answers:
      - {"phrases":["yes","decision clarity","for someone else","third-party decision-maker","analyst"],"targets":[{"kind":"active","id":"decision-clarity"}],"qualification":"Molecular Tier-3; the user is the analyst and another person is the decision-maker."}
    default: {"targets":[{"kind":"action","id":"keep-selection"}]}
```

**Axes used.** Complexity (Q1: simple → multi-party → systemic) + stance (Q2: descriptive vs. critical) + specificity (Q3: analyst output vs. decision-maker output).

**Default explanation.** `cui-bono` at Tier-2 when ambiguous, with stakeholder-mapping as the most common upward hook.

**Escalation hooks.**
- After `cui-bono` Tier-2: if more than two stakeholder groups surface, hook upward to `stakeholder-mapping` (cross-territory into T8).
- After `stakeholder-mapping`: if interactions among parties surface feedback structure, hook upward to `wicked-problems` molecular.
- After any T2 mode: if the user signals voices may be missing, hook sideways to `boundary-critique`.
- After `cui-bono` or `stakeholder-mapping`: if the user is producing analysis for a third-party decision-maker, hook upward to `decision-clarity`.

---

## T3 — Decision-Making Under Uncertainty

```yaml
territory_questions:
  "T3": "t3-primary"
territory_defaults:
  "T3": {"kind":"active","id":"decision-under-uncertainty"}
routing_questions:
  - id: t3-primary
    text: "Is the environment basically known and you're picking from clear options, or are there real unknowns about how things will play out, or are you weighing several criteria that don't reduce to one number, or are values in tension where the choice is partly about what you stand for?"
    territories: ["T3"]
    optional_questions: ["t3-specificity","t3-depth"]
    answers:
      - {"phrases":["known environment","clear options"],"targets":[{"kind":"active","id":"constraint-mapping"}],"qualification":"Tier-2."}
      - {"phrases":["real unknowns","probability matters","uncertainty"],"targets":[{"kind":"active","id":"decision-under-uncertainty"}],"qualification":"Tier-2."}
      - {"phrases":["many criteria pulling different ways","several criteria","multiple criteria"],"targets":[{"kind":"active","id":"multi-criteria-decision"}],"qualification":"Tier-2."}
      - {"phrases":["values in tension","what I stand for","ethical tradeoff"],"targets":[{"kind":"deferred","id":"ethical-tradeoff"}],"qualification":"Deferred per CR-6."}
    default: {"targets":[{"kind":"active","id":"decision-under-uncertainty"}]}
  - id: t3-specificity
    text: "Is this a one-shot choice, or staged where you can learn between steps?"
    territories: ["T3"]
    qualification: "Optional specificity follow-up about a one-shot choice versus learning between stages."
    answers:
      - {"phrases":["staged","learn between steps"],"targets":[{"kind":"deferred","id":"real-options-decision"}],"qualification":"Deferred per CR-6."}
    default: {"targets":[{"kind":"action","id":"keep-selection"}]}
  - id: t3-depth
    text: "Want me to bring it all together into a decision architecture that tracks the constraints, uncertainties, and criteria in one integrated frame?"
    territories: ["T3"]
    qualification: "Optional depth follow-up when the user wants the integrated decision artifact."
    answers:
      - {"phrases":["yes","bring it all together","integrated decision architecture"],"targets":[{"kind":"active","id":"decision-architecture"}],"qualification":"Molecular Tier-3; integrates constraints, uncertainty and criteria."}
    default: {"targets":[{"kind":"action","id":"keep-selection"}]}
```

**Axes used.** All three: depth (Q3: thorough atomic vs. molecular), complexity (Q1: single criterion vs. multi-criteria), stance (Q1: optimization vs. normative), specificity (Q2: one-shot vs. staged).

**Default explanation.** `decision-under-uncertainty` at Tier-2 when ambiguous (the central mode of the territory; constraint-mapping is the lighter sibling, decision-architecture the molecular sibling).

**Escalation hooks.**
- After `constraint-mapping` Tier-2: if real unknowns surface that change the option set, hook upward to `decision-under-uncertainty`.
- After `decision-under-uncertainty` Tier-2: if multiple non-commensurable criteria are in play, hook sideways to `multi-criteria-decision`.
- After any Tier-2 T3 mode: if the user wants a single integrated artifact tracking all dimensions, hook upward to `decision-architecture` molecular.
- After any T3 mode: if the question shifts from "what should I do" to "how could this fail", hook sideways to T6 `pre-mortem-action` for an action plan or T7 `pre-mortem-fragility` for a system or design.

---

## T4 — Causal Investigation

```yaml
territory_questions:
  "T4": "t4-primary"
territory_defaults:
  "T4": {"kind":"active","id":"root-cause-analysis"}
routing_questions:
  - id: t4-primary
    text: "Is the question more like 'what one thing went wrong here', or more like 'what set of things keep producing this', or do you want a formal causal model with arrows you can reason over, or are you tracing how a specific historical event actually unfolded?"
    territories: ["T4"]
    answers:
      - {"phrases":["one thing","chain back to root","root cause"],"targets":[{"kind":"active","id":"root-cause-analysis"}],"qualification":"Tier-2."}
      - {"phrases":["feedback","things reinforcing each other","reinforcing loops"],"targets":[{"kind":"active","id":"systems-dynamics-causal"}],"qualification":"Tier-2; investigates causes."}
      - {"phrases":["formal causal model with arrows","causal graph","causal dag"],"targets":[{"kind":"active","id":"causal-dag"}],"qualification":"Tier-3; Pearl-style."}
      - {"phrases":["specific historical event","step by step","process tracing"],"targets":[{"kind":"active","id":"process-tracing"}],"qualification":"Tier-3; Bennett/Checkel."}
    default: {"targets":[{"kind":"active","id":"root-cause-analysis"}]}
```

**Axes used.** Complexity (single chain → feedback structure) + specificity (general vs. historical-event) + depth (light vs. formal DAG).

**Default explanation.** `root-cause-analysis` at Tier-2 when ambiguous; this is the lightest path and surfaces feedback signals naturally.

**Escalation hooks.**
- After `root-cause-analysis` Tier-2: if the analysis surfaces reinforcing loops or competing causes that interact, hook upward to `systems-dynamics-causal` (the canonical "the structure here looks like there are competing causes that interact" hook from §5.7).
- After `systems-dynamics-causal`: if formalism is needed to share with others, hook upward to `causal-dag`.
- After any T4 mode: if the framing itself appears to be generating the problem, hook sideways to T9 (`paradigm-suspension` or `frame-comparison`).
- After any T4 mode: if the question shifts to "how do the parts produce the whole's behavior", hook sideways to T16 (`mechanism-understanding`).

---

## T5 — Hypothesis Evaluation

```yaml
territory_questions:
  "T5": "t5-primary"
territory_defaults:
  "T5": {"kind":"active","id":"competing-hypotheses"}
routing_questions:
  - id: t5-primary
    text: "Quick read on which explanation fits best, or do you want me to lay out evidence systematically against each candidate, or do you want a probabilistic model with priors?"
    territories: ["T5"]
    answers:
      - {"phrases":["quick","quick read"],"targets":[{"kind":"active","id":"differential-diagnosis"}],"qualification":"Tier-1."}
      - {"phrases":["systematic","systematically","evidence against each candidate"],"targets":[{"kind":"active","id":"competing-hypotheses"}],"qualification":"Tier-2; Heuer ACH."}
      - {"phrases":["probabilistic model with priors","probabilistic model","priors"],"targets":[{"kind":"active","id":"bayesian-hypothesis-network"}],"qualification":"Tier-3."}
    default: {"targets":[{"kind":"active","id":"competing-hypotheses"}]}
```

**Axes used.** Depth — the territory's primary axis. The three resident modes form a clean depth ladder.

**Default explanation.** `competing-hypotheses` at Tier-2 when ambiguous (the canonical Heuer ACH operation; both the quick and the formal are siblings of this baseline).

**Escalation hooks.**
- After `differential-diagnosis` Tier-1: if more than two hypotheses survive the quick read, hook upward to `competing-hypotheses` ("Quick read complete — there's more here than one mode can disentangle, want the longer route?").
- After `competing-hypotheses` Tier-2: if priors materially shift the diagnosis, hook upward to `bayesian-hypothesis-network`.
- After any T5 mode: if the disagreement is really about how to frame the issue rather than which hypothesis fits the evidence, hook sideways to T9 (`paradigm-suspension` or `frame-comparison`).
- After any T5 mode: if each hypothesis is itself a complete argument-as-artifact, hook sideways to T1 (audit each).

---

## T6 — Future Exploration

```yaml
territory_questions:
  "T6": "t6-primary"
territory_defaults:
  "T6": {"kind":"active","id":"consequences-and-sequel"}
routing_questions:
  - id: t6-primary
    text: "Mostly looking forward to anticipate likely consequences, wanting probability estimates, wanting alternative future stories, stress-testing a plan against how it could go wrong, or imagining the success and working backward to today?"
    territories: ["T6"]
    optional_questions: ["t6-depth"]
    answers:
      - {"phrases":["likely consequences","consequences"],"targets":[{"kind":"active","id":"consequences-and-sequel"}],"qualification":"Tier-2."}
      - {"phrases":["probabilities","probability estimates"],"targets":[{"kind":"active","id":"probabilistic-forecasting"}],"qualification":"Tier-2; Tetlock-style."}
      - {"phrases":["alternative stories","alternative futures","scenarios"],"targets":[{"kind":"active","id":"scenario-planning"}],"qualification":"Tier-2; Wack-style."}
      - {"phrases":["what could go wrong with the plan","action plan","stress-testing a plan"],"targets":[{"kind":"active","id":"pre-mortem-action"}],"qualification":"Action-plan variant of pre-mortem; the structural-system variant is pre-mortem-fragility in T7."}
      - {"phrases":["imagining the success and working backward","backcasting"],"targets":[{"kind":"deferred","id":"backcasting"}],"qualification":"Deferred per CR-6."}
    default: {"targets":[{"kind":"active","id":"consequences-and-sequel"}]}
  - id: t6-depth
    text: "Want me to bring it all together — multiple scenarios, probability estimates, and pre-mortems composed into a wicked-future analysis?"
    territories: ["T6"]
    qualification: "Optional depth follow-up about integrated future analysis."
    answers:
      - {"phrases":["yes","bring it all together","wicked future"],"targets":[{"kind":"active","id":"wicked-future"}],"qualification":"Molecular Tier-3; composes scenarios, probabilities and pre-mortems."}
    default: {"targets":[{"kind":"action","id":"keep-selection"}]}
```

**Axes used.** Stance (Q1: neutral forecasting vs. adversarial pre-mortem vs. constructive backcasting) + depth (Q2: thorough atomic vs. molecular).

**Default explanation.** `consequences-and-sequel` at Tier-2 when ambiguous (the lightest forward-projection mode; scenario-planning is the most common upward hook).

**Escalation hooks.**
- After `consequences-and-sequel` Tier-2: if multiple plausible futures diverge, hook upward to `scenario-planning`; if probabilities can be quantified usefully, hook sideways to `probabilistic-forecasting`.
- After `scenario-planning`: if the user wants stress-testing of a chosen path, hook sideways to `pre-mortem-action`; if integrated with probabilities and pre-mortem, hook upward to `wicked-future` molecular.
- After `pre-mortem-action`: if the failure modes are structural rather than action-specific, hook sideways to T7 `pre-mortem-fragility` (cross-territory parse).
- After any T6 mode: if the question is really about choosing among options now rather than exploring futures, hook sideways to T3.

---

## T7 — Risk and Failure Analysis

```yaml
territory_questions:
  "T7": "t7-primary"
territory_defaults:
  "T7": {"kind":"active","id":"pre-mortem-fragility"}
routing_questions:
  - id: t7-primary
    text: "Is the question about an action plan that could fail, a system or design with structural fragilities (where could it break under any pressure), or specifically asymmetric exposure to volatility — what makes it fragile or antifragile?"
    territories: ["T7"]
    optional_questions: ["t7-depth","t7-stance"]
    answers:
      - {"phrases":["action plan","what could go wrong before we commit","plan that could fail"],"targets":[{"kind":"active","id":"pre-mortem-action"}],"qualification":"Action-plan object; cross-territory dispatch to the T6 parsed mode."}
      - {"phrases":["system","design","structural fragilities","structural fragility","where could it break under any pressure"],"targets":[{"kind":"active","id":"pre-mortem-fragility"}],"qualification":"System-or-design object; structural failure under stress."}
      - {"phrases":["asymmetric exposure","fragile versus antifragile","antifragile","talebian","taleb"],"targets":[{"kind":"active","id":"fragility-antifragility-audit"}],"qualification":"Full Talebian asymmetry treatment; the precise variant remains distinct from the structural pre-mortem."}
    default: {"targets":[{"kind":"active","id":"pre-mortem-fragility"}]}
  - id: t7-depth
    text: "Want a quick scan for failure modes, or a thorough fault-tree that traces how component failures propagate?"
    territories: ["T7"]
    qualification: "Optional depth follow-up; ambiguity preserves the primary selection."
    answers:
      - {"phrases":["quick scan","failure modes"],"targets":[{"kind":"deferred","id":"failure-mode-scan"}],"qualification":"Deferred per CR-6."}
      - {"phrases":["thorough fault tree","fault tree","component failures propagate"],"targets":[{"kind":"deferred","id":"fault-tree"}],"qualification":"Deferred per CR-6."}
    default: {"targets":[{"kind":"action","id":"keep-selection"}]}
  - id: t7-stance
    text: "Are you specifically modeling an adversary trying to defeat this, or asking where it could break under any pressure (no adversary required)?"
    territories: ["T7"]
    qualification: "Optional stance follow-up; an adversarial actor differs from structural pressure."
    answers:
      - {"phrases":["adversary modeling","adversary trying to defeat this"],"question":"t15-red-team-operation","qualification":"Cross-territory red-team dispatch to T15; distinguish own-decision assessment from external-use advocacy."}
      - {"phrases":["any pressure","no adversary needed","no adversary required"],"targets":[{"kind":"action","id":"keep-selection"}],"qualification":"Stay with the T7 selection."}
    default: {"targets":[{"kind":"action","id":"keep-selection"}]}
```

**Axes used.** Specificity (Q1: action-plan vs. structural-system) + depth (Q2: light scan vs. thorough fault tree) + stance (Q3: adversarial-actor vs. structural-fragility — also the T7↔T15 cross-territory disambiguator).

**Default explanation.** `pre-mortem-fragility` at Tier-2 when ambiguous (the lighter atomic mode; `fragility-antifragility-audit` is the heavier sibling with the full Talebian asymmetry treatment).

**Escalation hooks.**
- After `pre-mortem-fragility` Tier-2: if the failure modes surfaced are structural and asymmetric rather than action-specific, hook upward to `fragility-antifragility-audit`.
- After either T7 mode: if an adversary is genuinely in the picture, hook sideways to T15 `red-team` per the §5.6 stance disambiguator.
- After either T7 mode: if the failure has already happened and the question is now causal, hook sideways to T4.
- After either T7 mode: if the failure is a strategic-interaction failure, hook sideways to T18.

---

## T8 — Stakeholder Conflict

```yaml
territory_questions:
  "T8": "t8-primary"
territory_defaults:
  "T8": {"kind":"active","id":"stakeholder-mapping"}
routing_questions:
  - id: t8-primary
    text: "Are you mapping the parties and how their interests align or diverge, or is the conflict structure itself wicked (parties, sub-parties, shifting coalitions)?"
    territories: ["T8"]
    qualification: "Ask this question even with one currently active resident: the deferred conflict-structure alternative remains a real choice."
    answers:
      - {"phrases":["mapping parties and interests","mapping parties","mapping interests","stakeholder mapping"],"targets":[{"kind":"active","id":"stakeholder-mapping"}],"qualification":"Tier-2."}
      - {"phrases":["wicked","shifting","sub-coalitions","conflict structure"],"targets":[{"kind":"deferred","id":"conflict-structure"}],"qualification":"Deferred per CR-6; do not substitute wicked-problems, which performs a different operation."}
    default: {"targets":[{"kind":"active","id":"stakeholder-mapping"}]}
```

**Axes used.** Complexity (single mapping vs. systemic conflict structure) — partial because the second mode is deferred.

**Default explanation.** `stakeholder-mapping` at Tier-2 — this is effectively the territory founder; `conflict-structure` is deferred per CR-6.

**Escalation hooks.**
- After `stakeholder-mapping` Tier-2: if the user is moving from descriptive mapping into active negotiation guidance, hook sideways to T13 (`interest-mapping` or `principled-negotiation`).
- After `stakeholder-mapping`: if the question is fundamentally about who benefits and where power sits rather than about the conflict shape, hook sideways to T2 (`cui-bono` or `boundary-critique`).
- After `stakeholder-mapping`: if the conflict has feedback structure across multiple sub-coalitions and the deferred `conflict-structure` mode is needed, surface the deferred-mode flag rather than substituting `wicked-problems` from T2 (different operations).

**Singleton note.** T8 currently has one resident mode (`stakeholder-mapping`). Expansion candidate `conflict-structure` is deferred per CR-6. If T8 invocations consistently produce composition-with-T13 patterns, that suggests `conflict-structure` should be promoted ahead of CR-6 review.

---

## T9 — Paradigm and Assumption Examination

```yaml
territory_questions:
  "T9": "t9-primary"
territory_defaults:
  "T9": {"kind":"active","id":"paradigm-suspension"}
routing_questions:
  - id: t9-primary
    text: "Are you trying to suspend the current frame to see what it's hiding, compare two or more frames against each other, or build out the full landscape of how different worldviews see this?"
    territories: ["T9"]
    optional_questions: ["t9-depth"]
    answers:
      - {"phrases":["suspend the current frame","suspend","assumptions"],"targets":[{"kind":"active","id":"paradigm-suspension"}],"qualification":"Tier-2."}
      - {"phrases":["compare frames","compare","different frames"],"targets":[{"kind":"active","id":"frame-comparison"}],"qualification":"Tier-2."}
      - {"phrases":["full worldview landscape","worldviews","landscape"],"targets":[{"kind":"active","id":"worldview-cartography"}],"qualification":"Molecular Tier-3; confirm runtime."}
    default: {"targets":[{"kind":"active","id":"paradigm-suspension"}]}
  - id: t9-depth
    text: "Want a single-frame surfacing on this one artifact (atomic), or a sustained walk through how multiple frames build and constrain each other (molecular)?"
    territories: ["T9"]
    qualification: "Optional depth follow-up; the single-artifact answer preserves the primary selection."
    answers:
      - {"phrases":["single-frame on one artifact","single frame","atomic"],"targets":[{"kind":"action","id":"keep-selection"}]}
      - {"phrases":["sustained molecular walk","molecular","sustained walk"],"targets":[{"kind":"active","id":"worldview-cartography"}],"qualification":"Depth escalation to molecular cartography."}
    default: {"targets":[{"kind":"action","id":"keep-selection"}]}
```

**Axes used.** Stance (Q1: suspending vs. comparing vs. mapping) + depth (Q2: atomic surfacing vs. molecular cartography).

**Default explanation.** `paradigm-suspension` at Tier-2 when ambiguous (the lightest atomic; the comparing and cartography variants are sideways/upward escalations).

**Escalation hooks.**
- After `paradigm-suspension` Tier-2: if multiple frames surface that need explicit comparison, hook upward to `frame-comparison`.
- After `frame-comparison`: if the comparison expands into a full landscape of worldviews, hook upward to `worldview-cartography` molecular.
- After any T9 mode: if the question collapses back into within-frame argumentation, hook sideways to T1 (`frame-audit` for a single-artifact frame surface).
- After any T9 mode: if the question becomes "integrate across these paradigms" rather than "examine the differences", hook sideways to T12 (`synthesis` or `dialectical-analysis`).

---

## T10 — Conceptual Clarification

```yaml
territory_questions:
  "T10": "t10-primary"
territory_defaults:
  "T10": {"kind":"active","id":"deep-clarification"}
routing_questions:
  - id: t10-primary
    text: "Are you trying to clarify what the concept already means in current usage, engineer it toward what it should mean (sometimes called ameliorative work), or examine why it is essentially contested across users with no single right meaning?"
    territories: ["T10"]
    answers:
      - {"phrases":["clarify current usage","current usage","what it means"],"targets":[{"kind":"active","id":"deep-clarification"}],"qualification":"Tier-2; ordinary-language."}
      - {"phrases":["engineer toward what it should mean","what it should mean","ameliorative"],"targets":[{"kind":"active","id":"conceptual-engineering"}],"qualification":"Tier-2; Cappelen/Plunkett."}
      - {"phrases":["essentially contested","no single right meaning","contested across users"],"targets":[{"kind":"deferred","id":"definitional-dispute"}],"qualification":"Deferred per CR-6; Gallie."}
    default: {"targets":[{"kind":"active","id":"deep-clarification"}]}
```

**Axes used.** Stance — the territory's primary axis (descriptive vs. ameliorative vs. essentially-contested).

**Default explanation.** `deep-clarification` at Tier-2 when ambiguous (the descriptive baseline; ameliorative and essentially-contested variants are stance escalations).

**Escalation hooks.**
- After `deep-clarification` Tier-2: if clarification reveals the concept is doing normative work that needs revision, hook sideways to `conceptual-engineering`.
- After `conceptual-engineering`: if the engineered version cannot be agreed because users' values diverge, hook sideways to `definitional-dispute` (deferred — surface the flag).
- After any T10 mode: if the concept-clarification is a precursor to argument evaluation, hook sideways to T1.
- After any T10 mode: if the concept is embedded in a paradigm dispute, hook sideways to T9.

---

## T11 — Structural Relationship Mapping

```yaml
territory_questions:
  "T11": "t11-primary"
territory_defaults:
  "T11": {"kind":"active","id":"relationship-mapping"}
routing_questions:
  - id: t11-primary
    text: "Is your input a textual description of entities and their relationships, or a visual diagram, network, or schema where the question is what relations the picture asserts (or where relations are missing)?"
    territories: ["T11"]
    answers:
      - {"phrases":["textual description","list of entities and relations","text","entities and relationships"],"targets":[{"kind":"active","id":"relationship-mapping"}],"qualification":"Tier-2; general textual input."}
      - {"phrases":["visual diagram","network","schema","diagram","picture"],"targets":[{"kind":"active","id":"spatial-reasoning"}],"qualification":"Tier-2; specificity-visual-input; reads asserted or missing relations."}
    default: {"targets":[{"kind":"active","id":"relationship-mapping"}]}
```

**Axes used.** Specificity — the territory's primary axis (general vs. visual-input).

**Default explanation.** `relationship-mapping` at Tier-2 when ambiguous (the general atomic; `spatial-reasoning` is the visual-input specificity variant doing the same operation on diagrammatic input).

**Escalation hooks.**
- After `relationship-mapping` Tier-2: if the input becomes visual mid-conversation, switch sideways to `spatial-reasoning`.
- After `spatial-reasoning`: if the question shifts from "what relations does this diagram assert" to "what is the layout itself doing", hook sideways to T19 (`compositional-dynamics` or `ma-reading`) — this is the canonical T11↔T19 cross-territory disambiguator.
- After either T11 mode: if the question becomes "how does this work" rather than "how are the parts related", hook sideways to T16 (`mechanism-understanding`).
- After either T11 mode: if the question becomes "how does this flow over time", hook sideways to T17 (`process-mapping`).

---

## T12 — Cross-Domain and Knowledge Synthesis

```yaml
territory_questions:
  "T12": "t12-primary"
territory_defaults:
  "T12": {"kind":"active","id":"synthesis"}
routing_questions:
  - id: t12-primary
    text: "Are you trying to integrate two or more bodies of knowledge into a unified picture, hold a thesis and an antithesis in productive tension to see what new understanding emerges, or find a structural analogy across very different domains?"
    territories: ["T12"]
    answers:
      - {"phrases":["integrate into unified picture","unified picture","integrate","synthesis"],"targets":[{"kind":"active","id":"synthesis"}],"qualification":"Tier-2."}
      - {"phrases":["thesis and antithesis in tension","thesis","antithesis","productive tension"],"targets":[{"kind":"active","id":"dialectical-analysis"}],"qualification":"Tier-2."}
      - {"phrases":["structural analogy across very different domains","structural analogy","analogy"],"targets":[{"kind":"deferred","id":"cross-domain-analogical"}],"qualification":"Deferred per CR-6."}
    default: {"targets":[{"kind":"active","id":"synthesis"}]}
```

**Axes used.** Stance — the territory's primary axis (integrative vs. thesis-antithesis vs. analogical).

**Default explanation.** `synthesis` at Tier-2 when ambiguous (the integrative baseline; dialectical is the productive-tension variant).

**Escalation hooks.**
- After `synthesis` Tier-2: if irreducible tensions remain that resist integration, hook sideways to `dialectical-analysis` (the productive-tension variant is appropriate when integration is forced).
- After `dialectical-analysis`: if a synthesis emerges from the tension and can be articulated, loop back to `synthesis` for the unified output.
- After either T12 mode: if the analysis is really about which paradigm to adopt rather than how to integrate them, hook sideways to T9 (`frame-comparison` or `worldview-cartography`).
- After either T12 mode: if the work is generative rather than integrative, hook sideways to T20 (`passion-exploration`).

---

## T13 — Negotiation and Conflict Resolution

```yaml
territory_questions:
  "T13": "t13-primary"
territory_defaults:
  "T13": {"kind":"active","id":"principled-negotiation"}
routing_questions:
  - id: t13-primary
    text: "Want a quick interest-mapping pass to see what each side actually wants, or the full structured walk through interests, options, and objective criteria (sometimes called principled negotiation)?"
    territories: ["T13"]
    optional_questions: ["t13-specificity"]
    answers:
      - {"phrases":["quick interest-mapping","quick","interest mapping"],"targets":[{"kind":"active","id":"interest-mapping"}],"qualification":"Tier-1; Fisher/Ury light."}
      - {"phrases":["full structured walk","full","structured negotiation"],"targets":[{"kind":"active","id":"principled-negotiation"}],"qualification":"Tier-2; Fisher/Ury full."}
    default: {"targets":[{"kind":"active","id":"principled-negotiation"}]}
  - id: t13-specificity
    text: "Are you a party to this negotiation, or are you advising as a neutral third side (mediator stance)?"
    territories: ["T13"]
    qualification: "Optional specificity follow-up about the user’s role in the negotiation."
    answers:
      - {"phrases":["I'm a party","party","participant"],"targets":[{"kind":"action","id":"keep-selection"}],"qualification":"Party stance; keep the selected depth."}
      - {"phrases":["third side","mediator","neutral","mediation"],"targets":[{"kind":"active","id":"third-side"}],"qualification":"Ury; multi-party mediator stance."}
    default: {"targets":[{"kind":"action","id":"keep-selection"}]}
```

**Axes used.** Depth (Q1: light interest-mapping vs. thorough principled-negotiation) + specificity (Q2: negotiation-as-party vs. negotiation-as-mediator).

**Default explanation.** `principled-negotiation` at Tier-2 when ambiguous (the central full-Fisher/Ury treatment; interest-mapping is the lighter sibling, third-side is the mediator-stance variant).

**Escalation hooks.**
- After `interest-mapping` Tier-1: if the mapped interests reveal substantial integrative possibilities, hook upward to `principled-negotiation` ("Quick interest-mapping complete; the structure here looks like there's room for an integrative option, want the longer route?").
- After `principled-negotiation`: if the user's role is more facilitator than party, hook sideways to `third-side`.
- After any T13 mode: if the question is really about descriptive stakeholder mapping rather than active negotiation, hook sideways to T8.
- After any T13 mode: if the negotiation is best modeled as a strategic-interaction game with formal payoffs, hook sideways to T18 (`strategic-interaction`).

---

## T14 — Orientation in Unfamiliar Territory

```yaml
territory_questions:
  "T14": "t14-primary"
territory_defaults:
  "T14": {"kind":"active","id":"terrain-mapping"}
routing_questions:
  - id: t14-primary
    text: "Want a quick lay of the land — main landmarks, common pitfalls, where to start — or a thorough terrain map with the major sub-areas and their relationships, or a full induction that walks you in from first principles?"
    territories: ["T14"]
    answers:
      - {"phrases":["quick lay of the land","quick","landmarks"],"targets":[{"kind":"active","id":"quick-orientation"}],"qualification":"Tier-1."}
      - {"phrases":["thorough terrain map","terrain map","major sub-areas"],"targets":[{"kind":"active","id":"terrain-mapping"}],"qualification":"Tier-2."}
      - {"phrases":["full induction from first principles","full induction","first principles"],"targets":[{"kind":"active","id":"domain-induction"}],"qualification":"Molecular Tier-3; confirm runtime."}
    default: {"targets":[{"kind":"active","id":"terrain-mapping"}]}
```

**Axes used.** Depth — the territory's primary axis. The three modes form a clean depth ladder (light triplet pattern per the spec note).

**Default explanation.** `terrain-mapping` at Tier-2 when ambiguous (the central thorough mode; quick-orientation is the lighter sibling, domain-induction the heavier molecular).

**Escalation hooks.**
- After `quick-orientation` Tier-1: if the user wants to actually settle into the domain rather than just reconnoiter, hook upward to `terrain-mapping`.
- After `terrain-mapping` Tier-2: if the user wants induction into the domain's reasoning patterns rather than just its layout, hook upward to `domain-induction` molecular.
- After any T14 mode: if orientation surfaces a generative interest the user wants to explore, hook sideways to T20 (`passion-exploration`).
- After any T14 mode: if the orientation produces a relationship map as a side-effect that the user wants to elaborate, hook sideways to T11 (`relationship-mapping`).

---

## T15 — Artifact Evaluation by Stance

```yaml
territory_questions:
  "T15": "t15-primary"
territory_defaults:
  "T15": {"kind":"active","id":"balanced-critique"}
routing_questions:
  - id: t15-primary
    text: "Want the strongest case for it, the strongest case against it, a balanced look weighted toward positives, a neutral look at both sides, or a quick devil's advocate (not a full hostile-actor stress test)?"
    territories: ["T15"]
    answers:
      - {"phrases":["for it","strongest possible case","strongest case for","steelman"],"targets":[{"kind":"active","id":"steelman-construction"}],"qualification":"T15 home; consult the T1 cross-reference when the artifact is itself an argument."}
      - {"phrases":["against it","hostile actor stress test","strongest case against","red team"],"question":"t15-red-team-operation","qualification":"Adversarial actor modeling; ask the secondary operation question."}
      - {"phrases":["balanced positives weighted","positives weighted","benefits"],"targets":[{"kind":"active","id":"benefits-analysis"}]}
      - {"phrases":["balanced neutral","neutral","both sides","weigh both"],"targets":[{"kind":"active","id":"balanced-critique"}]}
      - {"phrases":["quick devil's advocate","not full hostile actor","devils advocate lite"],"targets":[{"kind":"deferred","id":"devils-advocate-lite"}],"qualification":"Deferred per CR-6."}
    default: {"targets":[{"kind":"active","id":"balanced-critique"}]}
  - id: t15-red-team-operation
    text: "want adversarial — for own decision (assessment) or for external use (advocate)?"
    territories: ["T15"]
    answers:
      - {"phrases":["for own decision","what's wrong","fix list","assessment","fix vulnerabilities"],"targets":[{"kind":"active","id":"red-team-assessment"}],"qualification":"Default own-decision operation; prioritize vulnerabilities for repair."}
      - {"phrases":["argue against","ammunition","debate prep","external use","advocate"],"targets":[{"kind":"active","id":"red-team-advocate"}],"qualification":"External-use case against the artifact."}
    default: {"targets":[{"kind":"active","id":"red-team-assessment"}]}
```

**Axes used.** Stance — the territory's primary and defining axis (constructive-strong → constructive-balanced → neutral → adversarial-light → adversarial-actor-modeling).

**Default explanation.** `balanced-critique` at Tier-2 when ambiguous (per §5.6 the neutral stance is the default when the user has not signaled).

**Escalation hooks.**
- After `steelman-construction`: if the user wants the opposite-stance counterpoint, hook sideways to `red-team-assessment` (own-decision) or `red-team-advocate` (external-use).
- After `red-team-assessment`: if the user wants the constructive counterpoint, hook sideways to `steelman-construction`. If the user shifts from own-decision framing to building a case against the artifact for external use, hook sideways to `red-team-advocate`.
- After `red-team-advocate`: if the user wants the constructive counterpoint, hook sideways to `steelman-construction`. If the user shifts back to wanting their own vulnerabilities surfaced for fix-prioritisation, hook sideways to `red-team-assessment`.
- After `benefits-analysis`: if drawbacks need fuller treatment, hook sideways to `balanced-critique` or `red-team-assessment` (default) / `red-team-advocate` (external use).
- After `balanced-critique`: if the user wants either pole pushed harder, hook sideways to `steelman-construction` or `red-team-assessment` / `red-team-advocate`.
- After any T15 mode: if the artifact is itself an argument and the question becomes argument-soundness rather than proposal-evaluation, hook sideways to T1 (`coherence-audit` or `frame-audit`).
- After either red-team mode: if the question is really about structural fragility rather than an adversary trying to defeat this, hook sideways to T7 (`fragility-antifragility-audit`) per the §5.6 T7↔T15 disambiguator.

---

## T16 — Mechanism Understanding

```yaml
territory_defaults:
  "T16": {"kind":"active","id":"mechanism-understanding"}
```

**Axes used.** Depth (founder mode at thorough atomic depth). Specificity axis grows as domain-specific mechanism modes are added (currently none).

**Default explanation.** `mechanism-understanding` at Tier-2 — singleton at current population. No within-territory disambiguation needed.

**Escalation hooks.**
- After `mechanism-understanding`: if the question becomes "why does this happen" (causal investigation) rather than "how does it work", hook sideways to T4 (`root-cause-analysis` or `systems-dynamics-causal`).
- After `mechanism-understanding`: if the question becomes "how does this flow over time as a process", hook sideways to T17 (`process-mapping`).
- After `mechanism-understanding`: if the question becomes "how do the parts relate structurally" (topology rather than working-principle), hook sideways to T11 (`relationship-mapping`).

**Singleton note.** T16 currently has one resident mode (`mechanism-understanding`, Wave 3 founder). Domain-specific mechanism variants are deferred per CR-6 — they would expand the specificity axis as Ora encounters domain-specific mechanism work that the founder mode handles inadequately.

---

## T17 — Process and System Analysis

```yaml
territory_questions:
  "T17": "t17-primary"
territory_defaults:
  "T17": {"kind":"active","id":"process-mapping"}
routing_questions:
  - id: t17-primary
    text: "Is the system you're mapping a market or economy (prices, supply and demand, competition, network effects), a feedback structure (loops, reinforcing or balancing dynamics), a process flow (sequenced steps, inputs producing outputs), or an organizational structure of formal reporting and roles?"
    territories: ["T17"]
    answers:
      - {"phrases":["a market or economy","market","economy","prices","supply and demand","competition","network effects"],"targets":[{"kind":"active","id":"market-dynamics"}],"qualification":"Tier-2; describes market behavior. Designing a mechanism or contract routes to T18 mechanism-design."}
      - {"phrases":["feedback structure","loops","reinforcing or balancing dynamics","feedback"],"targets":[{"kind":"active","id":"systems-dynamics-structural"}],"qualification":"Tier-2; maps structure. The parsed causal variant lives in T4."}
      - {"phrases":["process flow","sequenced steps","process","workflow"],"targets":[{"kind":"active","id":"process-mapping"}],"qualification":"Tier-2."}
      - {"phrases":["organizational structure","formal reporting and roles","reporting and roles"],"targets":[{"kind":"deferred","id":"organizational-structure"}],"qualification":"Deferred per CR-6."}
    default: {"targets":[{"kind":"active","id":"process-mapping"}]}
```

**Axes used.** Specificity — the territory's primary axis (process flow vs. feedback structure vs. organizational structure).

**Default explanation.** `process-mapping` at Tier-2 when ambiguous (the lightest of the resident modes; systems-dynamics-structural is the feedback-specific sibling).

**Escalation hooks.**
- After `process-mapping` Tier-2: if the process map surfaces feedback loops that account for the system's behavior, hook sideways to `systems-dynamics-structural`.
- After `systems-dynamics-structural`: if the question becomes "why does this keep happening" (causal rather than structural), hook sideways to T4 `systems-dynamics-causal` (the parsed sibling per Decision D).
- After either T17 mode: if the question becomes "how do the parts produce the whole's behavior at the principle level", hook sideways to T16 (`mechanism-understanding`).
- After either T17 mode: if the question becomes "what relations does the system assert among its parts", hook sideways to T11 (`relationship-mapping`).

---

## T18 — Strategic Interaction

```yaml
territory_questions:
  "T18": "t18-primary"
territory_defaults:
  "T18": {"kind":"active","id":"strategic-interaction"}
routing_questions:
  - id: t18-primary
    text: "Is the crux observable moves between players (what will they do, what's the equilibrium), or hidden information / hidden action and the incentive structure (who privately knows or does what; designing rules so agents behave)?"
    territories: ["T18"]
    answers:
      - {"phrases":["observable moves","equilibrium","what will they do if we do X","moves between players"],"targets":[{"kind":"active","id":"strategic-interaction"}],"qualification":"Tier-2; territory founder."}
      - {"phrases":["hidden information","hidden action","adverse selection","moral hazard","design the incentives","contract","auction","incentive structure"],"targets":[{"kind":"active","id":"mechanism-design"}],"qualification":"Tier-2; information or incentive design is the crux."}
    default: {"targets":[{"kind":"active","id":"strategic-interaction"}]}
```

**Axes used.** Complexity — the territory's primary axis (observable-move game vs. information-and-incentive structure / mechanism design). Signaling-game variant remains deferred per CR-6.

**Default explanation.** `strategic-interaction` at Tier-2 when ambiguous (the founder mode); `mechanism-design` when hidden information, hidden action, or incentive/contract design is the crux.

**Escalation hooks.**
- After `strategic-interaction`: if the question becomes about hidden information / hidden action or designing rules under which agents will produce a desired outcome, hook sideways to `mechanism-design` (now resident).
- After `strategic-interaction`: if the question becomes specifically about signaling-game dynamics (asymmetric information, costly signals), hook sideways to `signaling` (deferred — surface the flag).
- After `strategic-interaction`: if the question shifts from analyzing the game to actually negotiating it, hook sideways to T13 (`principled-negotiation` or `third-side`).
- After `strategic-interaction`: if the question shifts to "where could this strategic structure fail", hook sideways to T7 (`pre-mortem-fragility` or `fragility-antifragility-audit`).
- After `strategic-interaction`: if the question is really about who benefits and who has power rather than equilibrium analysis, hook sideways to T2 (`cui-bono`).

**Population note.** T18 has two resident modes: `strategic-interaction` (founder) and `mechanism-design` (added 2026-06-01, un-deferring the CR-6 expansion candidate). The `signaling`-game variant remains deferred per CR-6.

---

## T19 — Spatial Composition

```yaml
territory_questions:
  "T19": "t19-primary"
territory_defaults:
  "T19": {"kind":"active","id":"compositional-dynamics"}
routing_questions:
  - id: t19-primary
    text: "Is this a contemplative reading of a composition where what matters is what the empty spaces and the still moments do (often aesthetic input — painting, garden, room, page), or an analytical reading of a composition where the question is what the layout's structure makes possible or impossible (often applied input — dashboard, urban scene, information graphic), or a deep place-reading where the question is what the place itself is (genius loci, image of the place), or specifically about how densely the composition packs information without losing legibility?"
    territories: ["T19"]
    answers:
      - {"phrases":["contemplative reading","aesthetic","what the voids and stillness do","empty spaces"],"targets":[{"kind":"active","id":"ma-reading"}],"qualification":"Wave 2; Japanese aesthetics."}
      - {"phrases":["universal compositional principles","what the layout does","analytical reading","composition"],"targets":[{"kind":"active","id":"compositional-dynamics"}],"qualification":"Wave 2; Gestalt and Arnheim."}
      - {"phrases":["deep place-reading","what the place itself is","genius loci","place character"],"targets":[{"kind":"active","id":"place-reading-genius-loci"}],"qualification":"Wave 3; Alexander and Norberg-Schulz."}
      - {"phrases":["information density","how densely the composition packs information","legibility"],"targets":[{"kind":"active","id":"information-density"}],"qualification":"Wave 3; Tufte and Bertin."}
    default: {"targets":[{"kind":"active","id":"compositional-dynamics"}]}
```

**Axes used.** Stance (contemplative vs. analytical-applied vs. deep-evaluative) + specificity (aesthetic-experiential vs. universal-perceptual vs. operational-applied vs. information-graphic). T19 carries five open debates at the territory level per Decision G — see `Reference — Analytical Territories.md` T19 entry.

**Default explanation.** `compositional-dynamics` at Tier-2 when ambiguous (the universal-perceptual mode that applies across both aesthetic and applied inputs; ma-reading is the contemplative-aesthetic sibling, place-reading-genius-loci the deep-place sibling, information-density the applied-information-graphic sibling).

**Escalation hooks.**
- After `compositional-dynamics`: if the input is genuinely aesthetic and the user wants the contemplative mode that articulates what the voids and stillness do, hook sideways to `ma-reading`.
- After `ma-reading`: if the user wants an analytical/predictive complement to the contemplative reading, hook sideways to `compositional-dynamics`.
- After any of {`ma-reading`, `compositional-dynamics`}: if the question is fundamentally about *what this place is* (deep place-character), hook sideways to `place-reading-genius-loci`.
- After any T19 mode on a dashboard or chart: if the question is specifically chart-encoding-misfit rather than generic compositional critique, hook sideways to `information-density`.
- After any T19 mode on a network diagram: if the question is "what relations does this assert" rather than "what is the layout doing", hook sideways to T11 `spatial-reasoning` per the canonical T11↔T19 disambiguator.
- After any T19 mode: if the prompt is really open-ended exploration of what the composition opens up rather than analytical reading, hook sideways to T20 (`passion-exploration`).

**Reserved-mode note.** A fifth candidate — Information-Graphic Visual-Hierarchy Analysis — is held in reserve. Promotion threshold is recorded in `Reference — Analytical Territories.md` T19 entry. Below threshold, route information-graphic inputs through `compositional-dynamics` with Tufte/Bertin/Cleveland citations.

---

## T20 — Open Exploration (Generative)

```yaml
territory_defaults:
  "T20": {"kind":"active","id":"passion-exploration"}
```

**Axes used.** Specificity (founder mode at personal-interest specificity). Idea-development and research-question-generation variants are deferred per CR-6.

**Default explanation.** `passion-exploration` at Tier-2 — singleton at current population. No within-territory disambiguation needed.

**Escalation hooks.**
- After `passion-exploration`: if the exploration crystallizes into a creative work the user wants to actually develop, hook upward to `idea-development` (deferred — surface the flag).
- After `passion-exploration`: if the exploration crystallizes into a research question the user wants to pursue, hook upward to `research-question-generation` (deferred — surface the flag).
- After `passion-exploration`: if the exploration crystallizes into a specifiable project (Crystallization Detection per Decision M), hand off to T21 (`project-mode`).
- After `passion-exploration`: if the exploration is really an orientation question in an unfamiliar space, hook sideways to T14 (`quick-orientation` or `terrain-mapping`).
- After `passion-exploration`: if the exploration is really a synthesis-across-domains operation, hook sideways to T12 (`synthesis` or `dialectical-analysis`).

**Singleton note.** T20 currently has one resident mode (`passion-exploration`). Expansion candidates `idea-development` and `research-question-generation` are deferred per CR-6. Crystallization Detection lives within this territory's documentation and within `passion-exploration`'s mode spec rather than as a separate meta-architectural mode (per Decision M).

---

## T21 — Execution / Project Mode (Non-Analytical)

```yaml
territory_questions:
  "T21": "t21-primary"
territory_defaults:
  "T21": {"kind":"active","id":"project-mode"}
routing_questions:
  - id: t21-primary
    text: "Are you executing a defined project (walk through the steps), or formatting material under a structural template?"
    territories: ["T21"]
    answers:
      - {"phrases":["execute a defined project","walk through the steps","execute","project"],"targets":[{"kind":"active","id":"project-mode"}],"qualification":"Defined project-execution shape."}
      - {"phrases":["format material under a template","format","formatting","template","structured output"],"targets":[{"kind":"active","id":"structured-output"}],"qualification":"Explicitly supplied material to be formatted under a structural template."}
    default: {"targets":[{"kind":"active","id":"project-mode"}]}
```

**Axes used.** Specificity — the territory's primary axis (per execution type).

**Default explanation.** `project-mode` when ambiguous and the input has any project-execution shape; `structured-output` when the input is explicitly material to be formatted.

**Escalation hooks.** None within the analytical routing tree — T21 sits outside it. T21 modes do not escalate into analytical territories; if analytical work is needed, that surfaces as a new top-level routing decision.

**Singleton-style note.** T21 has two resident modes but they are non-analytical (no "— Analysis" suffix per Decision L). The territory exists for completeness and to mark execution as outside the analytical routing tree.

---

*End of Reference — Within-Territory Disambiguation Trees.*
