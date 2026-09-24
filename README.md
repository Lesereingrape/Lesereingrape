# Open-source record

Every pull request below is a commit that landed in someone else's repository: a defect I reproduced first, the smallest fix I could defend, and the tests that pin the behaviour. This page is rendered from the GitHub search API on a schedule, so it cannot drift from what is actually merged.

**Focus** &middot; AI agent runtimes and their memory subsystems &middot; multi-agent orchestration &middot; MCP and tool plumbing &middot; multimodal agents &middot; Python

<p align="left"> ![MERGED PRs 16](https://img.shields.io/badge/MERGED__PRs-16-4c8bf5?style=flat-square&labelColor=1b1f24&color=4c8bf5&logo=github&logoColor=white) ![PROJECTS 4](https://img.shields.io/badge/PROJECTS-4-3fb950?style=flat-square&labelColor=1b1f24&color=3fb950&logo=package&logoColor=white) ![UPSTREAM STARS 154.1K](https://img.shields.io/badge/UPSTREAM__STARS-154.1K-e3b341?style=flat-square&labelColor=1b1f24&color=e3b341&logo=star&logoColor=white)</p>

Projects with 1,000+ stars that have merged my pull requests upstream.

| Project | Stars | Merged | Pull requests |
| --- | ---: | ---: | --- |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 82.9K | 8 | [#5555](https://github.com/bytedance/deer-flow/pull/5555) · [#5593](https://github.com/bytedance/deer-flow/pull/5593) · [#5609](https://github.com/bytedance/deer-flow/pull/5609) · [#5586](https://github.com/bytedance/deer-flow/pull/5586) · [#5588](https://github.com/bytedance/deer-flow/pull/5588) · [#5801](https://github.com/bytedance/deer-flow/pull/5801) · [#5821](https://github.com/bytedance/deer-flow/pull/5821) · [#5607](https://github.com/bytedance/deer-flow/pull/5607) |
| [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | 32.3K | 2 | [#2754](https://github.com/agentscope-ai/agentscope/pull/2754) · [#2808](https://github.com/agentscope-ai/agentscope/pull/2808) |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 26.6K | 2 | [#12810](https://github.com/deepset-ai/haystack/pull/12810) · [#12905](https://github.com/deepset-ai/haystack/pull/12905) |
| [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | 12.3K | 4 | [#531](https://github.com/mrexodia/ida-pro-mcp/pull/531) · [#529](https://github.com/mrexodia/ida-pro-mcp/pull/529) · [#533](https://github.com/mrexodia/ida-pro-mcp/pull/533) · [#539](https://github.com/mrexodia/ida-pro-mcp/pull/539) |

<details>
<summary><b>Merged per month</b></summary>

```text
2026-09  ######################################## 16
```

</details>

<details>
<summary><b>All merged pull requests</b></summary>

| Merged | Project | Pull request |
| --- | --- | --- |
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
<summary><b>In review right now (39 open pull requests)</b></summary>

| Project | Open | Pull requests |
| --- | ---: | --- |
| [agno-agi/agno](https://github.com/agno-agi/agno) | 7 | [#10281](https://github.com/agno-agi/agno/pull/10281) · [#10287](https://github.com/agno-agi/agno/pull/10287) · [#10297](https://github.com/agno-agi/agno/pull/10297) · [#10301](https://github.com/agno-agi/agno/pull/10301) · [#10320](https://github.com/agno-agi/agno/pull/10320) · [#10323](https://github.com/agno-agi/agno/pull/10323) · [#10325](https://github.com/agno-agi/agno/pull/10325) |
| [langflow-ai/langflow](https://github.com/langflow-ai/langflow) | 5 | [#15223](https://github.com/langflow-ai/langflow/pull/15223) · [#15225](https://github.com/langflow-ai/langflow/pull/15225) · [#15227](https://github.com/langflow-ai/langflow/pull/15227) · [#15229](https://github.com/langflow-ai/langflow/pull/15229) · [#15231](https://github.com/langflow-ai/langflow/pull/15231) |
| [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | 4 | [#2741](https://github.com/agentscope-ai/agentscope/pull/2741) · [#2799](https://github.com/agentscope-ai/agentscope/pull/2799) · [#2805](https://github.com/agentscope-ai/agentscope/pull/2805) · [#2834](https://github.com/agentscope-ai/agentscope/pull/2834) |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 4 | [#5838](https://github.com/browser-use/browser-use/pull/5838) · [#5845](https://github.com/browser-use/browser-use/pull/5845) · [#5847](https://github.com/browser-use/browser-use/pull/5847) · [#5849](https://github.com/browser-use/browser-use/pull/5849) |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 4 | [#7610](https://github.com/crewAIInc/crewAI/pull/7610) · [#7612](https://github.com/crewAIInc/crewAI/pull/7612) · [#7615](https://github.com/crewAIInc/crewAI/pull/7615) · [#7617](https://github.com/crewAIInc/crewAI/pull/7617) |
| [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | 4 | [#537](https://github.com/mrexodia/ida-pro-mcp/pull/537) · [#541](https://github.com/mrexodia/ida-pro-mcp/pull/541) · [#542](https://github.com/mrexodia/ida-pro-mcp/pull/542) · [#543](https://github.com/mrexodia/ida-pro-mcp/pull/543) |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 2 | [#12813](https://github.com/deepset-ai/haystack/pull/12813) · [#12907](https://github.com/deepset-ai/haystack/pull/12907) |
| [PrefectHQ/prefect](https://github.com/PrefectHQ/prefect) | 2 | [#23190](https://github.com/PrefectHQ/prefect/pull/23190) · [#23191](https://github.com/PrefectHQ/prefect/pull/23191) |
| [QwenLM/Qwen-MM-Plugins](https://github.com/QwenLM/Qwen-MM-Plugins) | 2 | [#69](https://github.com/QwenLM/Qwen-MM-Plugins/pull/69) · [#71](https://github.com/QwenLM/Qwen-MM-Plugins/pull/71) |
| [strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk) | 2 | [#4553](https://github.com/strands-agents/harness-sdk/pull/4553) · [#4554](https://github.com/strands-agents/harness-sdk/pull/4554) |
| [TencentCloud/Octop](https://github.com/TencentCloud/Octop) | 2 | [#910](https://github.com/TencentCloud/Octop/pull/910) · [#912](https://github.com/TencentCloud/Octop/pull/912) |
| [andrewyng/openworker](https://github.com/andrewyng/openworker) | 1 | [#682](https://github.com/andrewyng/openworker/pull/682) |

</details>

<sub>Plus 1 merged pull request(s) in 1 smaller repository, below the 1,000 star bar of this table.</sub>

---

<sub>Rendered by [`scripts/build_readme.py`](scripts/build_readme.py) from the GitHub search API and refreshed by [`.github/workflows/refresh.yml`](.github/workflows/refresh.yml) &middot; record last changed 2026-09-24 17:07 UTC.</sub>
