# Open-source record

**Two halves.** Below, the work I built and the work I landed in other people's projects. Every pull request in the second half is a commit that shipped upstream: a defect I reproduced first, the smallest fix I could defend, and the tests that pin the behaviour. Both halves are rendered from the GitHub API on a schedule, so neither can drift from what is actually public.

**Focus** &middot; AI agent runtimes and their memory subsystems &middot; multi-agent orchestration &middot; MCP and tool plumbing &middot; multimodal agents &middot; Python

<p align="left"> ![OWN LABS 16](https://img.shields.io/badge/OWN__LABS-16-bc8cff?style=flat-square&labelColor=1b1f24&color=bc8cff&logo=flask&logoColor=white) ![MERGED PRs 80](https://img.shields.io/badge/MERGED__PRs-80-4c8bf5?style=flat-square&labelColor=1b1f24&color=4c8bf5&logo=github&logoColor=white) ![COMPANY PROJECTS 10](https://img.shields.io/badge/COMPANY__PROJECTS-10-3fb950?style=flat-square&labelColor=1b1f24&color=3fb950&logo=building&logoColor=white) ![UPSTREAM STARS 396.1K](https://img.shields.io/badge/UPSTREAM__STARS-396.1K-e3b341?style=flat-square&labelColor=1b1f24&color=e3b341&logo=star&logoColor=white)</p>

## Labs I built

These 16 labs were each built from scratch and run on a laptop CPU. Every one is deterministic, offline and CI-tested, and every figure its README reports is re-derived by a test - from a committed artifact, or by re-running the CLI and byte-comparing the transcript - so no headline number in any of them is hand-typed; the measurement labs run several seeds and print the spread instead of a best run. The descriptions below are pulled live from each repository, so this table cannot rot either.

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
| [research-relay-lab](https://github.com/Lesereingrape/research-relay-lab)<br><sub>CPU-only, multi-seed measurement of where a deep-research pipeline loses the evidence it found: one frozen 142k-parameter policy run through six researcher-to-reporter harnesses on a task with an exact verifier, with every README number rendered from a committed artifact.</sub> | A deer-flow-shaped Planner / Research Team / Reporter pipeline measured at the step nobody evaluates: the reporter handed raw search hits loses no facts at all and still lands near chance, and one notebook slot short of the chain every report cites more hops than its own notebook holds. |

### Reasoning and measurement

| Repository | What it demonstrates |
| --- | --- |
| [llama-anatomy](https://github.com/Lesereingrape/llama-anatomy)<br><sub>From-scratch ~100k-parameter LLaMA decoder (RMSNorm, RoPE, SwiGLU, GQA), plus an equal-parameter ablation of each choice, a train-short/test-long probe of RoPE against learned absolute positions, and a parameter-free sweep of RoPE's rotation base. CPU-only, multi-seed; every README number renders from a committed artifact and CI byte-compares it.</sub> | A LLaMA decoder written from the papers at 10^5 parameters, with every component swapped for an equal-parameter control so a difference is never just size. The rotation-base sweep is the one axis that adds no parameters at all, and it separates a floor its seeds agree on from a ceiling they do not. |
| [consistency-lab](https://github.com/Lesereingrape/consistency-lab)<br><sub>Adaptive early-stopping self-consistency: a sequential stopping rule that halts CoT sampling once the vote is statistically decided, measured on the accuracy-vs-compute frontier vs fixed-N self-consistency. CPU-only, verifiable.</sub> | A sequential stopping rule for self-consistency: sample chains until the vote is statistically decided, then spend the chains you saved on the questions that are actually contested. |
| [vlm-distill-bench](https://github.com/Lesereingrape/vlm-distill-bench)<br><sub>Reproducible CPU-only distillation & quantization benchmark for compact vision-language models on procedural mini-CLEVR. Real numbers, committed seeds, no downloads.</sub> | Distillation plus quantisation of a compact vision-language model on procedural mini-CLEVR, including the negative result that temperature-scaled KD can lose to plain cross-entropy at this scale. |
| [system-one-lab](https://github.com/Lesereingrape/system-one-lab)<br><sub>CPU-only, multi-seed measurement of what an agent decision layer is sensitive to: a typed Choice/Score/Noul judge vs a prose judge vs a prompt-flattened control, on synthetic findings with an exact verifier.</sub> | Three judges over the same findings, separated only by what they can read: the control that is handed the evidence in its prompt still changes its answer when only the wording moves, and one global temperature turn makes the pooled error smaller by making the honest slice worse. |

## Merged into company-backed projects

Repositories run by a company or product organisation, each with 10,000+ stars, that have merged my pull requests upstream.

| Project | Stars | Merged | Pull requests |
| --- | ---: | ---: | --- |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 83.6K | 20 | [#5555](https://github.com/bytedance/deer-flow/pull/5555) · [#5593](https://github.com/bytedance/deer-flow/pull/5593) · [#5609](https://github.com/bytedance/deer-flow/pull/5609) · [#5586](https://github.com/bytedance/deer-flow/pull/5586) · [#5588](https://github.com/bytedance/deer-flow/pull/5588) · [#5801](https://github.com/bytedance/deer-flow/pull/5801) · [#5821](https://github.com/bytedance/deer-flow/pull/5821) · [#5607](https://github.com/bytedance/deer-flow/pull/5607) · [#5852](https://github.com/bytedance/deer-flow/pull/5852) · [#5864](https://github.com/bytedance/deer-flow/pull/5864) · [#5883](https://github.com/bytedance/deer-flow/pull/5883) · [#5850](https://github.com/bytedance/deer-flow/pull/5850) · [#5960](https://github.com/bytedance/deer-flow/pull/5960) · [#6067](https://github.com/bytedance/deer-flow/pull/6067) · [#6174](https://github.com/bytedance/deer-flow/pull/6174) · [#6175](https://github.com/bytedance/deer-flow/pull/6175) · [#6252](https://github.com/bytedance/deer-flow/pull/6252) · [#6253](https://github.com/bytedance/deer-flow/pull/6253) · [#6274](https://github.com/bytedance/deer-flow/pull/6274) · [#6338](https://github.com/bytedance/deer-flow/pull/6338) |
| [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | 33.0K | 3 | [#2754](https://github.com/agentscope-ai/agentscope/pull/2754) · [#2808](https://github.com/agentscope-ai/agentscope/pull/2808) · [#2805](https://github.com/agentscope-ai/agentscope/pull/2805) |
| [locustio/locust](https://github.com/locustio/locust) | 28.2K | 5 | [#3528](https://github.com/locustio/locust/pull/3528) · [#3534](https://github.com/locustio/locust/pull/3534) · [#3536](https://github.com/locustio/locust/pull/3536) · [#3538](https://github.com/locustio/locust/pull/3538) · [#3530](https://github.com/locustio/locust/pull/3530) |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 26.7K | 3 | [#12810](https://github.com/deepset-ai/haystack/pull/12810) · [#12905](https://github.com/deepset-ai/haystack/pull/12905) · [#12907](https://github.com/deepset-ai/haystack/pull/12907) |
| [modelscope/FunASR](https://github.com/modelscope/FunASR) | 20.6K | 2 | [#3758](https://github.com/modelscope/FunASR/pull/3758) · [#3760](https://github.com/modelscope/FunASR/pull/3760) |
| [modelscope/ms-swift](https://github.com/modelscope/ms-swift) | 15.8K | 5 | [#10245](https://github.com/modelscope/ms-swift/pull/10245) · [#10248](https://github.com/modelscope/ms-swift/pull/10248) · [#10247](https://github.com/modelscope/ms-swift/pull/10247) · [#10250](https://github.com/modelscope/ms-swift/pull/10250) · [#10246](https://github.com/modelscope/ms-swift/pull/10246) |
| [livekit/agents](https://github.com/livekit/agents) | 14.7K | 1 | [#7468](https://github.com/livekit/agents/pull/7468) |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | 14.0K | 2 | [#8787](https://github.com/microsoft/agent-framework/pull/8787) · [#8974](https://github.com/microsoft/agent-framework/pull/8974) |
| [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent) | 13.3K | 1 | [#3722](https://github.com/The-PR-Agent/pr-agent/pull/3722) |
| [neuml/txtai](https://github.com/neuml/txtai) | 13.0K | 2 | [#1325](https://github.com/neuml/txtai/pull/1325) · [#1323](https://github.com/neuml/txtai/pull/1323) |

**Also merged, kept off the featured tables:** 36 pull requests across 8 projects &mdash; `zhayujie/CowAgent`, `AstrBotDevs/AstrBot`, `andrewyng/openworker`, `StarTrail-org/LEANN`, `mrexodia/ida-pro-mcp`, `TencentCloud/Octop`, `QwenLM/Qwen-MM-Plugins`, `iot-hackathon-2026-teamESGenius/iot_hackathon_2026_mannings`. Company-backed work above 10,000 stars is what this page features; this line exists so the totals still add up.


<details>
<summary><b>Merged per month</b></summary>

```text
2026-02  #                                        1
2026-09  ######################################## 53
2026-10  ####################                     26
```

</details>

<details>
<summary><b>All merged pull requests</b></summary>

| Merged | Project | Pull request |
| --- | --- | --- |
| 2026-10-09 | [StarTrail-org/LEANN](https://github.com/StarTrail-org/LEANN) | [#430](https://github.com/StarTrail-org/LEANN/pull/430) fix(core): keep index metadata when MCP status counts passages |
| 2026-10-09 | [StarTrail-org/LEANN](https://github.com/StarTrail-org/LEANN) | [#428](https://github.com/StarTrail-org/LEANN/pull/428) fix(core): let update_index choose passage IDs for unclaimed chunks |
| 2026-10-08 | [modelscope/FunASR](https://github.com/modelscope/FunASR) | [#3760](https://github.com/modelscope/FunASR/pull/3760) fix(frontend): stop cmvn readers from crashing on blank lines or returning empty statistics |
| 2026-10-08 | [modelscope/FunASR](https://github.com/modelscope/FunASR) | [#3758](https://github.com/modelscope/FunASR/pull/3758) fix(auto): skip blank lines in wav.scp and jsonl file lists |
| 2026-10-05 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#6338](https://github.com/bytedance/deer-flow/pull/6338) fix(discord): read allowed_guilds as IDs and deny every guild on an unreadable allowlist |
| 2026-10-05 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#6274](https://github.com/bytedance/deer-flow/pull/6274) fix(extensions): measure the team response size gate in UTF-8 bytes |
| 2026-10-05 | [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | [#8974](https://github.com/microsoft/agent-framework/pull/8974) Python: Search() keeps a falsy value instead of treating it as Blank |
| 2026-10-05 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3514](https://github.com/zhayujie/CowAgent/pull/3514) fix(artifact): keep a relative artifact path POSIX on Windows |
| 2026-10-04 | [neuml/txtai](https://github.com/neuml/txtai) | [#1323](https://github.com/neuml/txtai/pull/1323) Keep 0 and False in concat merge outputs |
| 2026-10-04 | [neuml/txtai](https://github.com/neuml/txtai) | [#1325](https://github.com/neuml/txtai/pull/1325) Fix DuckDB bind parameters followed by a non-word character not being converted |
| 2026-10-04 | [locustio/locust](https://github.com/locustio/locust) | [#3530](https://github.com/locustio/locust/pull/3530) Do not modify the headers dict the caller passed in |
| 2026-10-04 | [locustio/locust](https://github.com/locustio/locust) | [#3538](https://github.com/locustio/locust/pull/3538) Reject a negative spawn_rate in /swarm instead of reporting a successful start |
| 2026-10-04 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#6253](https://github.com/bytedance/deer-flow/pull/6253) fix(gateway): read uvicorn's WEB_CONCURRENCY in the remaining worker-count readers |
| 2026-10-04 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#6252](https://github.com/bytedance/deer-flow/pull/6252) fix(gateway): read uvicorn's WEB_CONCURRENCY in the multi-worker safety gates |
| 2026-10-03 | [locustio/locust](https://github.com/locustio/locust) | [#3536](https://github.com/locustio/locust/pull/3536) Fix format_duration() truncating each timestamp before subtracting |
| 2026-10-03 | [locustio/locust](https://github.com/locustio/locust) | [#3534](https://github.com/locustio/locust/pull/3534) Reject a non-positive rate in constant_throughput() |
| 2026-10-03 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3450](https://github.com/zhayujie/CowAgent/pull/3450) fix(memory): add missing artifact columns to databases created before pin/rename |
| 2026-10-03 | [locustio/locust](https://github.com/locustio/locust) | [#3528](https://github.com/locustio/locust/pull/3528) Reject a non-positive spawn_rate in new_dispatch() |
| 2026-10-02 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#6175](https://github.com/bytedance/deer-flow/pull/6175) fix(community): normalize max_results before handing it to Firecrawl and fastCRW |
| 2026-10-02 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#6174](https://github.com/bytedance/deer-flow/pull/6174) fix(telegram): measure the rich-message cap in UTF-16 code units |
| 2026-10-02 | [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | [#8787](https://github.com/microsoft/agent-framework/pull/8787) Python: Accept the registered audio/mpeg media type for MP3 input content |
| 2026-10-01 | [QwenLM/Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins) | [#71](https://github.com/QwenLM/Qwen-MM-Plugins/pull/71) fix(api): bound transcribe_audio's ffmpeg calls with QWEN_MM_FFMPEG_TIMEOUT |
| 2026-10-01 | [QwenLM/Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins) | [#69](https://github.com/QwenLM/Qwen-MM-Plugins/pull/69) fix(blender,freecad): keep a blank port in the config from killing the server |
| 2026-10-01 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3344](https://github.com/zhayujie/CowAgent/pull/3344) fix(env_config): refuse entries that would split into extra .env lines |
| 2026-10-01 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3332](https://github.com/zhayujie/CowAgent/pull/3332) fix(knowledge): keep graph node paths slash-separated on Windows |
| 2026-10-01 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#6067](https://github.com/bytedance/deer-flow/pull/6067) fix(channels): split Telegram messages by UTF-16 code units, not code points |
| 2026-09-30 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5960](https://github.com/bytedance/deer-flow/pull/5960) fix(agents): anchor agent-name validation against a trailing newline |
| 2026-09-30 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5850](https://github.com/bytedance/deer-flow/pull/5850) fix(config): guard the recovered stream cleanup delay like its heartbeat sibling |
| 2026-09-30 | [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | [#12907](https://github.com/deepset-ai/haystack/pull/12907) fix: render every content part of ChatPromptBuilder message templates |
| 2026-09-30 | [andrewyng/openworker](https://github.com/andrewyng/openworker) | [#690](https://github.com/andrewyng/openworker/pull/690) fix(mentions): a corrupt mention_threads.json must not brick server startup |
| 2026-09-30 | [livekit/agents](https://github.com/livekit/agents) | [#7468](https://github.com/livekit/agents/pull/7468) fix(voice): treat a non-list record_keyterms argument as no change |
| 2026-09-29 | [StarTrail-org/LEANN](https://github.com/StarTrail-org/LEANN) | [#427](https://github.com/StarTrail-org/LEANN/pull/427) fix(core): honour an explicit passage ID of 0 and key the offset map by string |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3325](https://github.com/zhayujie/CowAgent/pull/3325) fix(cli): remove the temp dir when a repo archive cannot be extracted |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3319](https://github.com/zhayujie/CowAgent/pull/3319) fix(cli): overlay the live roster when restoring a backup |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3321](https://github.com/zhayujie/CowAgent/pull/3321) fix(wechatmp): upload a local video reply instead of crashing on its path |
| 2026-09-29 | [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent) | [#3722](https://github.com/The-PR-Agent/pr-agent/pull/3722) fix(azure): do not resolve a comment thread after a swallowed tool failure |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3316](https://github.com/zhayujie/CowAgent/pull/3316) fix(channel): cancel queued work under the agent-scoped session key |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3314](https://github.com/zhayujie/CowAgent/pull/3314) fix(plugins): normalize a damaged plugins.json entry instead of losing every plugin |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3312](https://github.com/zhayujie/CowAgent/pull/3312) fix(wechatcom): read a locally generated image instead of fetching it |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3305](https://github.com/zhayujie/CowAgent/pull/3305) fix(godcmd): answer when #model is given more than one argument |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3303](https://github.com/zhayujie/CowAgent/pull/3303) fix(godcmd): answer when the plugin priority is not a number |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3296](https://github.com/zhayujie/CowAgent/pull/3296) fix(role): answer when the customize command has no description |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3299](https://github.com/zhayujie/CowAgent/pull/3299) fix(feishu,dingtalk): upload local video replies instead of dropping them |
| 2026-09-29 | [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | [#2805](https://github.com/agentscope-ai/agentscope/pull/2805) fix(message): keep a copy of the usage appended to a message |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3293](https://github.com/zhayujie/CowAgent/pull/3293) fix(dingtalk): route text-only richText to the agent instead of dropping it |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3291](https://github.com/zhayujie/CowAgent/pull/3291) fix(linkai): reply when the midjourney image index is not a number |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3289](https://github.com/zhayujie/CowAgent/pull/3289) fix(discord): upload local video replies instead of printing the file:// path |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3282](https://github.com/zhayujie/CowAgent/pull/3282) fix(dingtalk): deliver ERROR and INFO replies instead of dropping them |
| 2026-09-29 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3284](https://github.com/zhayujie/CowAgent/pull/3284) fix(dingtalk): skip group messages outside the whitelist instead of crashing |
| 2026-09-28 | [modelscope/ms-swift](https://github.com/modelscope/ms-swift) | [#10246](https://github.com/modelscope/ms-swift/pull/10246) fix(utils): treat a blank or non-numeric LOCAL_RANK as unset |
| 2026-09-28 | [modelscope/ms-swift](https://github.com/modelscope/ms-swift) | [#10250](https://github.com/modelscope/ms-swift/pull/10250) fix(infer): raise the intended ValueError when tool_choice names an unknown tool |
| 2026-09-28 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5883](https://github.com/bytedance/deer-flow/pull/5883) fix(community): normalize InfoQuest timeout config values like the sibling providers do |
| 2026-09-28 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3248](https://github.com/zhayujie/CowAgent/pull/3248) fix(wechat_kf): keep a server-supplied file name inside the tmp dir |
| 2026-09-28 | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | [#3247](https://github.com/zhayujie/CowAgent/pull/3247) fix(telegram): keep a sender-chosen document name inside the tmp dir |
| 2026-09-27 | [AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot) | [#10248](https://github.com/AstrBotDevs/AstrBot/pull/10248) fix(platform): keep the Satori heartbeat and reconnect delays from being disabled by a cleared field |
| 2026-09-27 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | [#5864](https://github.com/bytedance/deer-flow/pull/5864) fix(models): skip credential files whose access token is not a string |
| 2026-09-27 | [AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot) | [#10231](https://github.com/AstrBotDevs/AstrBot/pull/10231) fix(respond): keep an unusable segmented-reply log base from dropping the reply |
| 2026-09-27 | [AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot) | [#10229](https://github.com/AstrBotDevs/AstrBot/pull/10229) fix(weixin_oc): keep a cleared timeout field from disabling the HTTP timeout |
| 2026-09-26 | [modelscope/ms-swift](https://github.com/modelscope/ms-swift) | [#10247](https://github.com/modelscope/ms-swift/pull/10247) fix(metrics): score only sequences that carry a supervised label in seq_acc |
| 2026-09-26 | [modelscope/ms-swift](https://github.com/modelscope/ms-swift) | [#10248](https://github.com/modelscope/ms-swift/pull/10248) fix(cli): stringify list values from a YAML/JSON config before building argv |
| 2026-09-26 | [TencentCloud/Octop](https://github.com/TencentCloud/Octop) | [#1150](https://github.com/TencentCloud/Octop/pull/1150) fix(config): bound OCTOP_PORT and --port to a bindable range |
| 2026-09-26 | [modelscope/ms-swift](https://github.com/modelscope/ms-swift) | [#10245](https://github.com/modelscope/ms-swift/pull/10245) fix(utils): fall back to INFO for a blank or unknown LOG_LEVEL |
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
| 2026-02-12 | [iot-hackathon-2026-teamESGenius/iot_hackathon_2026_mannings](https://github.com/iot-hackathon-2026-teamESGenius/iot_hackathon_2026_mannings) | [#1](https://github.com/iot-hackathon-2026-teamESGenius/iot_hackathon_2026_mannings/pull/1) feat(routing): enhance robust optimizer with learning strategy |

</details>

## In review right now

45 open pull requests of mine are waiting on a maintainer (9 more held back as draft). Only company-backed projects above 10,000 stars are listed here; the rest are counted in the line below.

| Project | Stars | Open | Pull requests |
| --- | ---: | ---: | --- |
| [langflow-ai/langflow](https://github.com/langflow-ai/langflow) | 155.5K | 4 | [#15223](https://github.com/langflow-ai/langflow/pull/15223) · [#15225](https://github.com/langflow-ai/langflow/pull/15225) · [#15227](https://github.com/langflow-ai/langflow/pull/15227) · [#15229](https://github.com/langflow-ai/langflow/pull/15229) |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 117.5K | 4 | [#5838](https://github.com/browser-use/browser-use/pull/5838) · [#5845](https://github.com/browser-use/browser-use/pull/5845) · [#5847](https://github.com/browser-use/browser-use/pull/5847) · [#5849](https://github.com/browser-use/browser-use/pull/5849) |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 59.5K | 4 | [#7610](https://github.com/crewAIInc/crewAI/pull/7610) · [#7612](https://github.com/crewAIInc/crewAI/pull/7612) · [#7615](https://github.com/crewAIInc/crewAI/pull/7615) · [#7617](https://github.com/crewAIInc/crewAI/pull/7617) |
| [MemPalace/mempalace](https://github.com/MemPalace/mempalace) | 59.5K | 1 | [#2674](https://github.com/MemPalace/mempalace/pull/2674) |
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | 52.5K | 2 | [#23244](https://github.com/run-llama/llama_index/pull/23244) · [#23248](https://github.com/run-llama/llama_index/pull/23248) |
| [agno-agi/agno](https://github.com/agno-agi/agno) | 42.6K | 7 | [#10281](https://github.com/agno-agi/agno/pull/10281) · [#10287](https://github.com/agno-agi/agno/pull/10287) · [#10297](https://github.com/agno-agi/agno/pull/10297) · [#10301](https://github.com/agno-agi/agno/pull/10301) · [#10320](https://github.com/agno-agi/agno/pull/10320) · [#10323](https://github.com/agno-agi/agno/pull/10323) · [#10325](https://github.com/agno-agi/agno/pull/10325) |
| [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | 33.0K | 2 | [#2741](https://github.com/agentscope-ai/agentscope/pull/2741) · [#2799](https://github.com/agentscope-ai/agentscope/pull/2799) |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 26.7K | 1 | [#12813](https://github.com/deepset-ai/haystack/pull/12813) |
| [PrefectHQ/prefect](https://github.com/PrefectHQ/prefect) | 24.0K | 2 | [#23190](https://github.com/PrefectHQ/prefect/pull/23190) · [#23277](https://github.com/PrefectHQ/prefect/pull/23277) |
| [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | 18.7K | 2 | [#3377](https://github.com/confident-ai/deepeval/pull/3377) · [#3406](https://github.com/confident-ai/deepeval/pull/3406) |
| [modelscope/ms-swift](https://github.com/modelscope/ms-swift) | 15.8K | 3 | [#10251](https://github.com/modelscope/ms-swift/pull/10251) · [#10264](https://github.com/modelscope/ms-swift/pull/10264) · [#10266](https://github.com/modelscope/ms-swift/pull/10266) |
| [livekit/agents](https://github.com/livekit/agents) | 14.7K | 2 | [#7470](https://github.com/livekit/agents/pull/7470) · [#7619](https://github.com/livekit/agents/pull/7619) |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | 14.0K | 1 | [#8965](https://github.com/microsoft/agent-framework/pull/8965) |

**Also open, kept off the featured tables:** 10 pull requests across 4 projects &mdash; `HKUDS/nanobot`, `AstrBotDevs/AstrBot`, `HKUDS/LightRAG`, `mrexodia/ida-pro-mcp`. Company-backed work above 10,000 stars is what this page features; this line exists so the totals still add up.


---

<sub>Rendered by [`scripts/build_readme.py`](scripts/build_readme.py) from the GitHub API &mdash; the lab table reads each repository's live description, the PR tables read the search API &mdash; and refreshed by [`.github/workflows/refresh.yml`](.github/workflows/refresh.yml) &middot; record last changed 2026-10-10 09:46 UTC.</sub>
