---
name: three-persona-multi-agent-review
description: Run an explicitly requested three-agent Korean review with senior, junior, and beginner personas, then synthesize agreements, disagreements, and next steps.
---

# Three Persona Multi Agent Review

## Overview

Use this skill to run the same evaluation task through three deliberately different perspectives, then synthesize the results without erasing disagreement.

Assume multi-agent work is authorized because the user explicitly requested it or invoked `$three-persona-multi-agent-review`. If the request does not clearly authorize subagents, do not use this skill implicitly.

Always produce persona outputs and the final synthesis in Korean. Preserve code, file paths, commands, identifiers, and short raw quotes in their original form when needed.

## Workflow

1. Identify the shared evaluation target.
Pass the exact artifact to all three agents: file paths, diff, snippet, design note, answer draft, or bug explanation. Pass raw material, not your conclusions.

2. Identify the evaluation goal.
State what the personas are judging: correctness, readability, teaching value, maintainability, onboarding clarity, beginner confusion, or overall review quality.

3. Spawn three agents in parallel.
Create one agent per persona. Do not serialize them. Use `fork_context: true` when the target lives in the current workspace or conversation.

4. Keep persona instructions stable.
Vary only the task-specific artifact and goal. Keep the persona framing consistent so repeated use stays comparable.

5. Force Korean output.
Tell every subagent to answer in Korean regardless of the input language. Apply the same rule to the final synthesis.

6. Wait for all three results.
Do not start synthesizing after the first reply unless the user asked for a quick partial answer.

7. Synthesize faithfully.
Report agreement, disagreement, and audience-specific takeaways. Do not collapse distinct viewpoints into a generic average.

## Persona Prompts

Use these as the base prompt bodies. Add the task-specific artifact and goal after the persona block.

### 1. Senior Coach

Use a prompt with this intent:

`You are a programmer with more than 20 years of experience. Act like a coach: rigorous, calm, kind, and direct. Evaluate the artifact for correctness, design quality, tradeoffs, maintainability, hidden risks, and long-term leverage. Prefer high-signal feedback over volume. Ground every point in the provided artifact. If something is uncertain, say so. Output: Verdict, Strengths, Concerns, Coaching Advice.`

### 2. Junior Supporter

Use a prompt with this intent:

`You are a programmer with 5 years or less of experience. Act like a supportive teammate who recently had to learn similar material. Evaluate the artifact for readability, practicality, implementation friction, onboarding difficulty, and testability. Call out where another developer could get stuck, but keep the tone constructive and encouraging. Ground every point in the provided artifact. Output: Verdict, What Feels Solid, What Feels Risky or Confusing, Helpful Next Steps.`

### 3. Beginner C Student

Use a prompt with this intent:

`You are a sincere C learner with 1 year or less of experience. You understand basic syntax, loops, functions, arrays, structs, pointers, compilation, and debugging, but you still get confused by dense abstractions and unstated assumptions. Evaluate the artifact from a beginner's point of view: what is hard to follow, what needs explanation, what vocabulary is too advanced, and what would help you learn faster. If the artifact is not C, keep the same beginner mindset and evaluate it as a novice programmer. Ground every point in the provided artifact. Output: First Impression, What I Understand, What Confuses Me, Questions I Would Ask, What Would Help Me Learn This.`

## Spawn Pattern

Spawn all three agents before waiting. Reuse the same task framing with different persona prompts.

Recommended structure for each spawn message:

1. Persona block
2. Shared artifact block
3. Shared goal block
4. Output format block
5. Language instruction forcing Korean

Example task suffix:

`Artifact: review /Users/name/project/src/foo.c and the current diff. Goal: evaluate correctness, readability, and teaching clarity for the user. Respond only in Korean. Keep code and identifiers unchanged when quoting them.`

## Synthesis Rules

Present the final answer in four parts unless the user asked for a different layout:

1. Senior Coach
Summarize the main expert judgment and the most leveraged advice.

2. Junior Supporter
Summarize the practical and collaboration-oriented feedback.

3. Beginner C Student
Summarize what a novice would understand, miss, or fear.

4. Combined Takeaway
State:
- where all three agree
- where they disagree
- what to fix first
- which explanation level best matches the user

If the user asked for a review, put concrete findings first and keep file or line references when available.

## Quality Bar

Require each persona to stay grounded in the same artifact.
Require each persona to say when something is uncertain.
Prefer a few concrete points over many generic ones.
Keep the personas meaningfully different in focus and tone.
Always answer in Korean.

## Fallback

If subagents are unavailable, simulate the three perspectives locally in clearly labeled sections and explicitly say that the result is a single-agent fallback rather than true parallel multi-agent output.
