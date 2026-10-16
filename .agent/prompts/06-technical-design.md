# Feature Technical Design Prompt

"Using the Feature/PBI contract, UX/UI, Architecture Baseline and Impact findings, design the smallest technical slice required. Define contracts, data changes, affected components/services, affected repositories, integrations, security, observability, failure behavior and test strategy as applicable. If the baseline is insufficient, trigger Architecture Evolution instead of silently changing it."

Gate context: input = Architecture Baseline approved at gate GA plus the refined PBI; output = Feature Technical Design feeding G3 criterion tech-design-ready. Baseline gaps route to gate GB, never silent change.