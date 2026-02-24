# proposal_engine.py
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
    industry = payload["industry"]
    modules = payload.get("suggested_modules", [])
    pp = payload.get("pain_points", [])

    return {
        "executive_summary": (
            f"This proposal outlines an AI automation solution for a {payload['company_size']} "
            f"{industry} client to improve efficiency, reduce manual work, and accelerate response time."
        ),
        "pain_point_analysis": "\n".join([f"- {x}" for x in pp]) or "- Manual work causes delays and errors.",
        "proposed_ai_solution": {
            "input": "Client requirements + existing proposal assets + internal knowledge",
            "processing": "Structured drafting + quality checks + reusable templates",
            "output": "Proposal (PPT/DOCX), ROI summary, and sales email draft",
            "modules": modules or ["Proposal drafting automation", "ROI calculator", "Email generator"],
        },
        "implementation_plan": [
            {"phase": "Phase 1 (Week 1-2)", "items": ["Discovery workshop", "Define templates & fields", "ROI assumptions"]},
            {"phase": "Phase 2 (Week 3-5)", "items": ["Build workflow", "Validate outputs", "Internal testing"]},
            {"phase": "Phase 3 (Week 6-8)", "items": ["Pilot rollout", "Refine templates", "Training & handover"]},
        ],
        "roi_estimation_notes": "ROI is calculated using the built-in ROI calculator (assumptions adjustable).",
        "pricing_structure": [
            {"tier": "Basic", "price_note": "HKD 20k–40k", "includes": ["Standard template", "Email draft", "Basic ROI summary"]},
            {"tier": "Standard", "price_note": "HKD 50k–90k", "includes": ["Industry presets", "Roadmap", "Advanced ROI modeling"]},
            {"tier": "Premium", "price_note": "HKD 100k+", "includes": ["Custom integrations", "Governance", "Analytics & enablement"]},
        ],
        "risks_mitigations": [
            {"risk": "Inconsistent inputs", "mitigation": "Use standardized intake form + validation rules"},
            {"risk": "Adoption issues", "mitigation": "Provide training + template library + quick-start guide"},
            {"risk": "Security concerns", "mitigation": "Role-based access + redaction + logging"},
        ],
        "next_steps": ["Confirm stakeholders", "Run discovery call", "Finalize scope & success metrics", "Start pilot"],
        "sales_email_draft": {
            "en": (
                "Subject: Proposal – AI Sales Proposal Automation\n\n"
                "Hi [Name],\n\n"
                "Attached is a proposal outlining an AI-assisted workflow to reduce proposal preparation time "
                "and standardize deliverables. Happy to walk through the ROI assumptions and roadmap.\n\n"
                "Best regards,\n[Your Name]"
            ),
            "zh": (
                "主题：AI销售提案自动化方案\n\n"
                "您好 [姓名]：\n\n"
                "附件为AI辅助销售提案自动化方案，包含实施计划与ROI测算假设。"
                "我们可以约时间逐项讲解并确认范围与目标。\n\n"
                "谢谢\n[你的名字]"
            ),
        },
    }
