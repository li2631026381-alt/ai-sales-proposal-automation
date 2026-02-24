# proposal_engine.py
import json
from presets import INDUSTRY_PRESETS

def build_payload(
    industry: str,
    company_size: str,
    pain_points: list[str],
    workflow: str,
    budget: str,
    objective: str,
    timeline: str,
) -> dict:
    preset = INDUSTRY_PRESETS.get(industry, {})
    merged_pain_points = list(dict.fromkeys(pain_points + preset.get("common_pain_points", [])))

    return {
        "industry": industry,
        "company_size": company_size,
        "pain_points": merged_pain_points[:6],
        "current_workflow": workflow,
        "budget_range": budget,
        "project_objective": objective,
        "timeline": timeline,
        "suggested_modules": preset.get("solution_modules", []),
    }

def generate_proposal_offline(payload: dict) -> dict:
    # 不用API也能先跑通：给一个结构完整的输出
    industry = payload["industry"]
    modules = payload.get("suggested_modules", [])
    pp = payload.get("pain_points", [])

    return {
        "executive_summary": f"This proposal outlines an AI automation solution for a {payload['company_size']} {industry} client to improve efficiency, reduce manual work, and accelerate response time.",
        "pain_point_analysis": "\n".join([f"- {x}" for x in pp]) or "- Manual work causes delays and errors.",
        "proposed_ai_solution": {
            "input": "Customer requests / internal documents / process forms",
            "processing": "LLM-assisted drafting, workflow rules, and automation triggers",
            "output": "Standardized proposal deck, ROI summary, and sales email draft",
            "modules": modules or ["Proposal drafting automation", "ROI calculator", "Email generator"],
        },
        "implementation_plan": [
            {"phase": "Phase 1 (Week 1-2)", "items": ["Discovery workshop", "Define proposal template & data fields", "ROI model assumptions"]},
            {"phase": "Phase 2 (Week 3-5)", "items": ["Build automation workflow", "Integrate generation prompts", "Internal testing"]},
            {"phase": "Phase 3 (Week 6-8)", "items": ["Pilot rollout", "Refine templates", "Training & handover"]},
        ],
        "roi_estimation_notes": "Assumes proposal preparation time reduced from 3h to 1h per proposal; adjust parameters in ROI calculator for client-specific estimation.",
        "pricing_structure": [
            {"tier": "Basic", "price_note": "HKD 20k–40k", "includes": ["Standard proposal template", "Email draft", "Basic ROI summary"]},
            {"tier": "Standard", "price_note": "HKD 50k–90k", "includes": ["Industry presets", "Implementation roadmap", "Advanced ROI calculator"]},
            {"tier": "Premium", "price_note": "HKD 100k+", "includes": ["Multi-team workflow automation", "Custom integrations", "Governance & analytics"]},
        ],
        "risks_mitigations": [
            {"risk": "Data quality / inconsistent inputs", "mitigation": "Use standardized intake form + validation rules"},
            {"risk": "User adoption", "mitigation": "Provide training + template library + quick-start guide"},
            {"risk": "Security concerns", "mitigation": "Role-based access + redaction + logging"},
        ],
        "next_steps": ["Confirm client stakeholders", "Run 60-minute discovery call", "Finalize scope & success metrics", "Start pilot"],
        "sales_email_draft": {
            "en": "Subject: Proposal for AI Automation to Improve Sales Proposal Efficiency\n\nHi [Name],\n\nBased on our discussion, attached is a proposal outlining an AI-assisted workflow to reduce proposal preparation time and standardize deliverables. Happy to walk you through the ROI assumptions and implementation plan.\n\nBest regards,\n[Your Name]",
            "zh": "主题：AI自动化提升销售提案效率方案\n\n您好 [姓名]：\n\n根据我们沟通的需求，附件为AI辅助销售提案自动化方案，包含实施计划与ROI测算假设。方便的话我们可以约时间逐项讲解。\n\n此致\n[你的名字]",
        },
    }

# 以后你要接API，就在这里加一个 generate_proposal_llm(payload, api_key) 返回同样结构的dict