"""
Research-driven problem statement generation with brand character integration.
Uses 6-source research aggregator and Groq AI to generate realistic problem statements.
"""
import json
import logging
import re
from typing import List, Dict, Tuple
from datetime import datetime
from groq import Groq

from config import GROQ_API_KEY, AI_MODEL, DIFFICULTY_CONFIG
from models import (
    ChallengeInput, ResearchResult, ResearchSource, ProblemStatement,
    Difficulty
)
from research_service import ResearchAggregator

logger = logging.getLogger(__name__)

# Brand characters that MUST appear in problem statements
BRAND_CHARACTERS = {
    "Peter Pandey": {
        "role": "Data Analyst",
        "description": "The humble learner navigating the data world",
        "color": "#20C997"
    },
    "Tony Sharma": {
        "role": "VP/Senior Executive",
        "description": "Helpful senior guiding through professional challenges",
        "color": "#3B82F6"
    },
    "Bruce Hariyali": {
        "role": "Business Owner/Stakeholder",
        "description": "Decision-maker identifying business problems",
        "color": "#6F53C1"
    }
}


class ProblemGenerator:
    """Generate research-backed problem statements with brand character integration."""

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = AI_MODEL
        self.research_aggregator = ResearchAggregator()

    def conduct_research(self, domain: str, function: str) -> ResearchResult:
        """
        Conduct domain-specific research using 6 parallel APIs.
        """
        logger.info(f"Conducting research for {domain} - {function}")

        try:
            # Aggregated research from 6 sources
            research_sources = self.research_aggregator.aggregate_research(domain, function)

            if not research_sources:
                logger.warning("No research sources found. Using fallback.")
                return self._create_fallback_research(domain, function)

            # Extract insights and KPIs
            domain_insights = self._extract_insights(research_sources)
            identified_kpis = self._extract_kpis(domain, function, research_sources)
            industry_challenges = self._extract_challenges(research_sources)

            research_result = ResearchResult(
                session_id="temp",
                domain=domain,
                function=function,
                sources=research_sources,
                domain_insights=domain_insights,
                identified_kpis=identified_kpis,
                industry_challenges=industry_challenges,
                generated_at=datetime.now()
            )

            logger.info(f"Research completed: {len(research_sources)} sources found")
            return research_result

        except Exception as e:
            logger.error(f"Research failed: {e}. Using fallback.")
            return self._create_fallback_research(domain, function)

    def generate_problem_statement(
        self,
        session_id: str,
        input_data: ChallengeInput,
        research: ResearchResult
    ) -> ProblemStatement:
        """
        Generate a research-backed problem statement with brand characters.
        """
        logger.info(f"Generating problem statement for session {session_id}")

        prompt = self._build_generation_prompt(input_data, research)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_generation_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            parsed = self._parse_generation_response(content, input_data, research)

            # Find character positions in generated statement
            char_positions = self._find_character_positions(parsed["statement"])

            problem_statement = ProblemStatement(
                session_id=session_id,
                company_name=parsed["company_name"],
                title=parsed["title"],
                statement=parsed["statement"],
                character_positions=char_positions,
                analytical_questions=parsed["questions"],
                research_id=str(f"RESEARCH_{session_id}"), 
                difficulty=input_data.difficulty,
                generated_at=datetime.now()
            )

            logger.info(f"Problem statement generated with {len(char_positions)} character mentions")
            return problem_statement

        except Exception as e:
            logger.error(f"Problem generation failed: {e}")
            raise

    def _build_generation_prompt(self, input_data: ChallengeInput, research: ResearchResult) -> str:
        """Build detailed prompt for problem statement generation."""

        # Get config based on difficulty
        diff_config = DIFFICULTY_CONFIG.get(input_data.difficulty.value, DIFFICULTY_CONFIG["Medium"])
        question_count = diff_config["questions"]

        kpis_text = "\n".join([f"- {kpi}" for kpi in research.identified_kpis[:5]])
        challenges_text = "\n".join([f"- {ch}" for ch in research.industry_challenges[:4]])
        
        # Identify primary case study if available
        primary_source_text = ""
        for source in research.sources:
            if source.is_primary:
                primary_source_text = f"Based on real-world case: {source.title} ({source.url})"
                break

        return f"""Create a compelling data challenge problem statement for:

**Domain:** {input_data.domain}
**Business Function:** {input_data.function}
**Difficulty:** {input_data.difficulty.value}
{primary_source_text}

**Research Context:**
Key KPIs in this space:
{kpis_text}

Industry challenges:
{challenges_text}

**Brand Characters (MUST ALL APPEAR IN STATEMENT):**
1. **Peter Pandey** - Data Analyst (the humble learner)
2. **Tony Sharma** - VP/Senior Executive (the helpful mentor)
3. **Bruce Hariyali** - Business Owner/Stakeholder (the demand creator)

**Requirements:**
1. Create a fictional company name (domain-appropriate, NOT real)
2. Write 300-400 word problem statement that:
   - Includes ALL three brand characters with realistic roles
   - Presents a quantified business problem (e.g., "X% decline in retention", "$2M revenue loss", "30% dip in CSAT"). 
   - Use specific numbers, percentages, and dollar values to make the story compelling and data-driven.
   - References the research insights naturally
   - Ends with: "Imagine yourself as Peter Pandey..."
3. Generate {question_count} analytical questions that:
   - Can be answered with SQL/analytics on {input_data.dataset_size:,} rows
   - Build on each other logically
   - Address the business problem

**User Context (if provided):**
{input_data.problem_statement}

Return valid JSON with structure:
{{
    "company_name": "...",
    "title": "...",
    "statement": "...(300-400 words including all 3 characters)...",
    "questions": ["Q1", "Q2", "..."]
}}
"""

    def _get_generation_system_prompt(self) -> str:
        """System prompt for problem statement generation."""
        return """You are a data challenge designer creating realistic, engaging business scenarios for analytics learners.

Your role:
1. Craft compelling narratives around real business problems
2. Integrate brand characters naturally into scenarios
3. Ensure all analytical questions are solvable with the specified dataset
4. Balance realism with learning objectives

CRITICAL CONSTRAINT:
- Your problem statement MUST include all three brand characters:
  * Peter Pandey (as the Data Analyst/learner)
  * Tony Sharma (as VP or senior executive)
  * Bruce Hariyali (as business owner or stakeholder)
- Characters must have realistic roles within the company context
- Statement must end with: "Imagine yourself as Peter Pandey..."
"""

    def _parse_generation_response(self, content: str, input_data: ChallengeInput, research: ResearchResult) -> Dict:
        """Parse AI response into structured problem statement."""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
            else:
                parsed = json.loads(content)

            return {
                "company_name": parsed.get("company_name", "DataCorp Industries"),
                "title": parsed.get("title", f"{input_data.domain} Analytics Challenge"),
                "statement": parsed.get("statement", ""),
                "questions": parsed.get("questions", [])
            }
        except (json.JSONDecodeError, AttributeError) as e:
            logger.error(f"Failed to parse generation response: {e}")
            raise ValueError("Invalid response format from AI")

    def _find_character_positions(self, text: str) -> Dict[str, List[int]]:
        """Find positions of brand characters in text (case-insensitive)."""
        positions = {}
        text_lower = text.lower()

        for character in BRAND_CHARACTERS.keys():
            char_lower = character.lower()
            positions[character] = []

            start = 0
            while True:
                pos = text_lower.find(char_lower, start)
                if pos == -1:
                    break
                positions[character].append(pos)
                start = pos + 1

        return positions

    def _extract_insights(self, sources: List[ResearchSource]) -> List[str]:
        """Extract key insights from research sources."""
        insights = []
        for source in sources[:3]:
            insights.extend(source.key_insights[:2])
        return insights[:5]

    def _extract_kpis(self, domain: str, function: str, sources: List[ResearchSource]) -> List[str]:
        """Extract KPIs from research."""
        # Simple extraction logic + fallback defaults
        defaults = [
            "Revenue Growth", "Cost Efficiency", "Customer Satisfaction", 
            "Market Share", "Operational Performance"
        ]
        
        # In a real implementation, we might parse these from the source text
        # For now, return defaults as placeholder or implement simple keyword matching
        return defaults

    def _extract_challenges(self, sources: List[ResearchSource]) -> List[str]:
        """Extract industry challenges from research sources."""
        challenges = []
        for source in sources:
            for insight in source.key_insights:
                if any(word in insight.lower() for word in ['challenge', 'problem', 'risk', 'declining', 'issue']):
                    challenges.append(insight)
        
        if not challenges:
            return ["Increasing competition", "Cost optimization pressures", "Data quality issues", "Changing consumer behavior"]
            
        return challenges[:5]

    def _create_fallback_research(self, domain: str, function: str) -> ResearchResult:
        """Create fallback research when web search fails."""
        logger.info(f"Creating fallback research for {domain} - {function}")

        return ResearchResult(
            session_id="temp",
            domain=domain,
            function=function,
            sources=[
                ResearchSource(
                    title=f"Industry Best Practices: {domain}",
                    url="https://example.com/research",
                    relevance="high",
                    key_insights=[
                        f"Data-driven {function} is critical for success",
                        f"Real-time analytics enhance decision-making"
                    ],
                    publication_date=datetime.now().isoformat()
                )
            ],
            domain_insights=[f"{domain} sector experiencing rapid transformation"],
            identified_kpis=["Revenue Growth", "Customer Retention", "Operational Efficiency"],
            industry_challenges=["Data quality", "Talent shortage", "Cost optimization"],
            generated_at=datetime.now()
        )
