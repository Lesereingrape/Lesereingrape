# Open-source record

**Two halves.** Below, the work I built and the work I landed in other people's projects. Every pull request in the second half is a commit that shipped upstream: a defect I reproduced first, the smallest fix I could defend, and the tests that pin the behaviour. Both halves are rendered from the GitHub API on a schedule, so neither can drift from what is actually public.

**Focus** &middot; AI agent runtimes and their memory subsystems &middot; multi-agent orchestration &middot; MCP and tool plumbing &middot; multimodal agents &middot; Python

<p align="left"> ![OWN LABS 14](https://img.shields.io/badge/OWN__LABS-14-bc8cff?style=flat-square&labelColor=1b1f24&color=bc8cff&logo=flask&logoColor=white) ![MERGED PRs 17](https://img.shields.io/badge/MERGED__PRs-17-4c8bf5?style=flat-square&labelColor=1b1f24&color=4c8bf5&logo=github&logoColor=white) ![UPSTREAM PROJECTS 4](https://img.shields.io/badge/UPSTREAM__PROJECTS-4-3fb950?style=flat-square&labelColor=1b1f24&color=3fb950&logo=package&logoColor=white) ![UPSTREAM STARS 154.2K](https://img.shields.io/badge/UPSTREAM__STARS-154.2K-e3b341?style=flat-square&labelColor=1b1f24&color=e3b341&logo=star&logoColor=white)</p>

## Labs I built

These 14 labs were each built from scratch and run on a laptop CPU. Every one ships a verifier, multi-seed measurements, and a README whose results table is rendered from a committed JSON by a script the CI byte-compares against, so no number in any of them is hand-typed. The descriptions below are pulled live from each repository, so this table cannot rot either.

### Post-training and alignment

| Repository | What it demonstrates |
| --- | --- |
| [align-lab](https://github.com/Lesereingrape/align-lab)<br><sub>CPU-only post-training study: SFT vs DPO vs ORPO vs SimPO on a verifiable digit-addition task. Multi-seed; shows DPO/SimPO win-rate climbing to ~0.99 while real generation accuracy collapses (likelihood displacement).</sub> | Four preference-optimisation objectives on one task and one policy: the pair-wise win-rate is a flattering metric that can rise while generation gets worse. |
| [grpo-repro](https://github.com/Lesereingrape/grpo-repro)<br><sub>A tiny, fully-verifiable GRPO / REINFORCE / DPO comparison lab on a Reverse-Polish-Notation puzzle env. Same policy, same reward, same budget; CPU-measured with per-run wall-clock reported honestly.</sub> | GRPO, REINFORCE and DPO as three arms on identical weights and an identical verifiable reward. With a partial credit given to any legal answer, all three collapse to a degenerate output; the reward shape, not the algorithm, was the bug. |
| [reward-hacking-lab](https://github.com/Lesereingrape/reward-hacking-lab)<br><sub>CPU-only study of reward-model over-optimisation (Goodharting) in RLHF-style rejection-sampling self-improvement: optimise a verifiable reward and accuracy climbs; optimise a learned reward and the proxy climbs while true accuracy collapses.</sub> | Same loop, two rewards: optimise an exact verifier and true accuracy climbs, optimise a learned proxy and the proxy climbs while accuracy falls. Goodhart on demand, measured. |
| [starlab](https://github.com/Lesereingrape/starlab)<br><sub>CPU-reproducible STaR self-improvement: a ~100k-param transformer bootstraps column-addition reasoning from its own verifier-checked chains, with a matched-compute control.</sub> | STaR bootstrap: the model samples its own chains, an exact arithmetic verifier filters them, survivors become next round's training set - reported against a matched-compute control so the gain cannot be mistaken for simply training longer. |
| [data-select-lab](https://github.com/Lesereingrape/data-select-lab)<br><sub>A CPU-only LoRA/PEFT + LESS data-selection study: influence-scored LoRA gradient features pick the few fine-tuning examples that teach a frozen model a held-out capability, with forgetting reported honestly.</sub> | LESS-style LoRA gradient features pick the few dozen examples that teach a frozen model a held-out skill; the same table reports how much of the skill it already had that costs. |

### Self-optimising agents

| Repository | What it demonstrates |
| --- | --- |
| [skill-lab](https://github.com/Lesereingrape/skill-lab)<br><sub>CPU-only, dependency-free study of a Voyager-style self-evolving skill library: a budgeted BFS planner distils reusable first-order skills from its own verified plans and gets measurably cheaper the more it is used.</sub> | Voyager-style skill library distilled from the agent's own verified plans: the budget spent on the next task falls as the library grows, which is the whole claim. |
| [autprompt-lab](https://github.com/Lesereingrape/autprompt-lab)<br><sub>CPU-only study of budgeted automatic prompt optimisation (OPRO / Promptbreeder-style): random vs greedy vs population-evolution search against a frozen tiny transformer on a verifier-scored task, at an equal query budget.</sub> | OPRO / Promptbreeder-style prompt search under an equal query budget - random, greedy and population evolution scored against one frozen policy, so the comparison is about search, not compute. |
| [evolve-lab](https://github.com/Lesereingrape/evolve-lab)<br><sub>A CPU-only, dependency-free self-optimizing agent: evolution rediscovers and blends single-machine dispatching rules purely from an exact tardiness verifier.</sub> | A (mu, lambda) evolution strategy over dispatch rules rediscovers WSPT from an exact tardiness verifier. Dependency-free, and honest that the margin it keeps over WSPT sits inside the seed noise. |

### Agent systems on a tiny LLaMA-style stack

| Repository | What it demonstrates |
| --- | --- |
| [lagent](https://github.com/Lesereingrape/lagent)<br><sub>Local-first ReAct tool-use agent with a measured scaffold ablation: identical behaviour-cloned weights, four harnesses, ground-truth verifier. CPU-only tiny transformer.</sub> | ReAct scaffold ablation on identical behaviour-cloned weights: strip the observation scratchpad and the solve rate collapses. The harness loop is load-bearing machinery, not decoration around the model. |
| [agent-harness-eval](https://github.com/Lesereingrape/agent-harness-eval)<br><sub>Agent Harness Eval: instrument, score, and statistically compare agent rollouts. Paired bootstrap + McNemar, behavior metrics, zero-dependency core.</sub> | Paired bootstrap and McNemar for comparing agent rollouts, because a three-seed difference is not a result and most harness comparisons never check. |
| [hier-memo-agents](https://github.com/Lesereingrape/hier-memo-agents)<br><sub>Hierarchical planner-executor agents with shared blackboard memory, topic-level reuse, and verifiable citation provenance. Zero deps, deterministic, CI-tested.</sub> | Planner and executor agents over a shared blackboard with citation-linked reuse: memory matched by topic rather than by question, so reuse is transfer and not a cache hit. |

### Reasoning and measurement

| Repository | What it demonstrates |
| --- | --- |
| [llama-anatomy](https://github.com/Lesereingrape/llama-anatomy)<br><sub>From-scratch ~100k-parameter LLaMA decoder (RMSNorm, RoPE, SwiGLU, GQA), plus an equal-parameter ablation of each choice, a train-short/test-long probe of RoPE against learned absolute positions, and a parameter-free sweep of RoPE's rotation base. CPU-only, multi-seed; every README number renders from a committed artifact and CI byte-compares it.</sub> | A LLaMA decoder written from the papers at 10^5 parameters, with every component swapped for an equal-parameter control so a difference is never just size. The rotation-base sweep is the one axis that adds no parameters at all, and it separates a floor its seeds agree on from a ceiling they do not. |
| [consistency-lab](https://github.com/Lesereingrape/consistency-lab)<br><sub>Adaptive early-stopping self-consistency: a sequential stopping rule that halts CoT sampling once the vote is statistically decided, measured on the accuracy-vs-compute frontier vs fixed-N self-consistency. CPU-only, verifiable.</sub> | A sequential stopping rule for self-consistency: sample chains until the vote is statistically decided, then spend the chains you saved on the questions that are actually contested. |
| [vlm-distill-bench](https://github.com/Lesereingrape/vlm-distill-bench)<br><sub>Reproducible CPU-only distillation & quantization benchmark for compact vision-language models on procedural mini-CLEVR. Real numbers, committed seeds, no downloads.</sub> | Distillation plus quantisation of a compact vision-language model on procedural mini-CLEVR, including the negative result that temperature-scaled KD can lose to plain cross-entropy at this scale. |

## Pull requests merged upstream

Projects with 1,000+ stars that have merged my pull requests upstream.

| Project | Stars | Merged | Pull requests |
| --- | ---: | ---: | --- |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 83.0K | 9 | [#5555](https://github.com/bytedance/deer-flow/pull/5555) · [#5593](https://github.com/bytedance/deer-flow/pull/5593) · [#5609](https://github.com/bytedance/deer-flow/pull/5609) · [#5586](https://github.com/bytedance/deer-flow/pull/5586) · [#5588](https://github.com/bytedance/deer-flow/pull/5588) · [#5801](https://github.com/bytedance/deer-flow/pull/5801) · [#5821](https://github.com/bytedance/deer-flow/pull/5821) · [#5607](https://github.com/bytedance/deer-flow/pull/5607) · [#5852](https://github.com/bytedance/deer-flow/pull/5852) |
| [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | 32.4K | 2 | [#2754](https://github.com/agentscope-ai/agentscope/pull/2754) · [#2808](https://github.com/agentscope-ai/agentscope/pull/2808) |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 26.6K | 2 | [#12810](https://github.com/deepset-ai/haystack/pull/12810) · [#12905](https://github.com/deepset-ai/haystack/pull/12905) |
| [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | 12.3K | 4 | [#531](https://github.com/mrexodia/ida-pro-mcp/pull/531) · [#529](https://github.com/mrexodia/ida-pro-mcp/pull/529) · [#533](https://github.com/mrexodia/ida-pro-mcp/pull/533) · [#539](https://github.com/mrexodia/ida-pro-mcp/pull/539) |

<details>
<summary><b>Merged per month</b></summary>

```text
2026-09  ######################################## 17
```

</details>

<details>
<summary><b>All merged pull requests</b></summary>

| Merged | Project | Pull request |
| --- | --- | --- |
| 2026-09-25 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5852](https://github.com/bytedance/deer-flow/pull/5852) fix(community): reject bool and fractional web-search max_results like image search does |
| 2026-09-24 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5607](https://github.com/bytedance/deer-flow/pull/5607) fix(memory): reject a Honcho base_url that can never resolve |
| 2026-09-24 | [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | [#12905](https://github.com/deepset-ai/haystack/pull/12905) fix(core): compare Ellipsis callable parameters by return type |
| 2026-09-24 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5821](https://github.com/bytedance/deer-flow/pull/5821) fix(community): fall back to the default SearXNG max_results on an unparseable value |
| 2026-09-24 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5801](https://github.com/bytedance/deer-flow/pull/5801) fix(gateway): treat a blank GATEWAY_HOST/GATEWAY_PORT as unset |
| 2026-09-24 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5588](https://github.com/bytedance/deer-flow/pull/5588) fix(skills): load SKILL.md saved as UTF-8 with a BOM |
| 2026-09-24 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5586](https://github.com/bytedance/deer-flow/pull/5586) fix(memory): keep a zero confidence from scoring as the default |
| 2026-09-24 | [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | [#2808](https://github.com/agentscope-ai/agentscope/pull/2808) fix(formatter): forward the images of collapsed messages in xAI multi-agent history |
| 2026-09-23 | [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | [#12810](https://github.com/deepset-ai/haystack/pull/12810) fix(auth): deserialize listed secrets when recursive is enabled |
| 2026-09-22 | [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | [#539](https://github.com/mrexodia/ida-pro-mcp/pull/539) fix(rpc): treat a blank IDA_MCP_URL as unset for download URLs |
| 2026-09-22 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5609](https://github.com/bytedance/deer-flow/pull/5609) fix(subagents): report an explicit zero batch limit instead of defaulting it |
| 2026-09-22 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5593](https://github.com/bytedance/deer-flow/pull/5593) fix(skills): render an explicit empty allowed-tools as no tools, not as all |
| 2026-09-22 | [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | [#2754](https://github.com/agentscope-ai/agentscope/pull/2754) fix(agent): keep tool-result metadata and timestamps when truncating |
| 2026-09-21 | [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | [#533](https://github.com/mrexodia/ida-pro-mcp/pull/533) fix(idalib): fall back to defaults for blank IDA_MCP_* values |
| 2026-09-21 | [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | [#529](https://github.com/mrexodia/ida-pro-mcp/pull/529) fix(installer): keep IPv6 brackets in generated transport URLs |
| 2026-09-21 | [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | [#531](https://github.com/mrexodia/ida-pro-mcp/pull/531) fix(installer): let --uninstall run when IDA Free is installed |
| 2026-09-20 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5555](https://github.com/bytedance/deer-flow/pull/5555) fix(memory): report malformed backend_config values by key name |

</details>

<details>
<summary><b>In review right now (54 open pull requests)</b></summary>

| Project | Open | Pull requests |
| --- | ---: | --- |
| [agno-agi/agno](https://github.com/agno-agi/agno) | 7 | [#10281](https://github.com/agno-agi/agno/pull/10281) · [#10287](https://github.com/agno-agi/agno/pull/10287) · [#10297](https://github.com/agno-agi/agno/pull/10297) · [#10301](https://github.com/agno-agi/agno/pull/10301) · [#10320](https://github.com/agno-agi/agno/pull/10320) · [#10323](https://github.com/agno-agi/agno/pull/10323) · [#10325](https://github.com/agno-agi/agno/pull/10325) |
| [langflow-ai/langflow](https://github.com/langflow-ai/langflow) | 5 | [#15223](https://github.com/langflow-ai/langflow/pull/15223) · [#15225](https://github.com/langflow-ai/langflow/pull/15225) · [#15227](https://github.com/langflow-ai/langflow/pull/15227) · [#15229](https://github.com/langflow-ai/langflow/pull/15229) · [#15231](https://github.com/langflow-ai/langflow/pull/15231) |
| [TencentCloud/Octop](https://github.com/TencentCloud/Octop) | 5 | [#910](https://github.com/TencentCloud/Octop/pull/910) · [#912](https://github.com/TencentCloud/Octop/pull/912) · [#1146](https://github.com/TencentCloud/Octop/pull/1146) · [#1147](https://github.com/TencentCloud/Octop/pull/1147) · [#1150](https://github.com/TencentCloud/Octop/pull/1150) |
| [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | 4 | [#2741](https://github.com/agentscope-ai/agentscope/pull/2741) · [#2799](https://github.com/agentscope-ai/agentscope/pull/2799) · [#2805](https://github.com/agentscope-ai/agentscope/pull/2805) · [#2834](https://github.com/agentscope-ai/agentscope/pull/2834) |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 4 | [#5838](https://github.com/browser-use/browser-use/pull/5838) · [#5845](https://github.com/browser-use/browser-use/pull/5845) · [#5847](https://github.com/browser-use/browser-use/pull/5847) · [#5849](https://github.com/browser-use/browser-use/pull/5849) |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 4 | [#7610](https://github.com/crewAIInc/crewAI/pull/7610) · [#7612](https://github.com/crewAIInc/crewAI/pull/7612) · [#7615](https://github.com/crewAIInc/crewAI/pull/7615) · [#7617](https://github.com/crewAIInc/crewAI/pull/7617) |
| [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | 4 | [#537](https://github.com/mrexodia/ida-pro-mcp/pull/537) · [#541](https://github.com/mrexodia/ida-pro-mcp/pull/541) · [#542](https://github.com/mrexodia/ida-pro-mcp/pull/542) · [#543](https://github.com/mrexodia/ida-pro-mcp/pull/543) |
| [strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk) | 3 | [#4553](https://github.com/strands-agents/harness-sdk/pull/4553) · [#4554](https://github.com/strands-agents/harness-sdk/pull/4554) · [#4591](https://github.com/strands-agents/harness-sdk/pull/4591) |
| [AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot) | 2 | [#10229](https://github.com/AstrBotDevs/AstrBot/pull/10229) · [#10231](https://github.com/AstrBotDevs/AstrBot/pull/10231) |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 2 | [#5850](https://github.com/bytedance/deer-flow/pull/5850) · [#5864](https://github.com/bytedance/deer-flow/pull/5864) |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 2 | [#12813](https://github.com/deepset-ai/haystack/pull/12813) · [#12907](https://github.com/deepset-ai/haystack/pull/12907) |
| [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | 2 | [#4097](https://github.com/HKUDS/LightRAG/pull/4097) · [#4098](https://github.com/HKUDS/LightRAG/pull/4098) |
| [HKUDS/nanobot](https://github.com/HKUDS/nanobot) | 2 | [#5913](https://github.com/HKUDS/nanobot/pull/5913) · [#5914](https://github.com/HKUDS/nanobot/pull/5914) |
| [livekit/agents](https://github.com/livekit/agents) | 2 | [#7468](https://github.com/livekit/agents/pull/7468) · [#7470](https://github.com/livekit/agents/pull/7470) |
| [QwenLM/Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins) | 2 | [#69](https://github.com/QwenLM/Qwen-MM-Plugins/pull/69) · [#71](https://github.com/QwenLM/Qwen-MM-Plugins/pull/71) |
| [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | 2 | [#3247](https://github.com/zhayujie/CowAgent/pull/3247) · [#3248](https://github.com/zhayujie/CowAgent/pull/3248) |
| [andrewyng/openworker](https://github.com/andrewyng/openworker) | 1 | [#690](https://github.com/andrewyng/openworker/pull/690) |
| [PrefectHQ/prefect](https://github.com/PrefectHQ/prefect) | 1 | [#23190](https://github.com/PrefectHQ/prefect/pull/23190) |

</details>

<sub>Plus 1 merged pull request(s) in 1 smaller repository, below the 1,000 star bar of this table.</sub>

---

<sub>Rendered by [`scripts/build_readme.py`](scripts/build_readme.py) from the GitHub API &mdash; the lab table reads each repository's live description, the PR tables read the search API &mdash; and refreshed by [`.github/workflows/refresh.yml`](.github/workflows/refresh.yml) &middot; record last changed 2026-09-25 17:08 UTC.</sub>
