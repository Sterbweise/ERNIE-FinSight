import json
import logging
from openai import OpenAI
from typing import Dict, Any
from models.schemas import AnalysisResult

logger = logging.getLogger(__name__)


def _get_json_schema() -> dict:
    """Get the JSON schema for structured AI responses"""
    return {
        "type": "object",
        "properties": {
            "executive_analysis": {
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "tagline": {"type": "string"},
                    "core_value_proposition": {"type": "string"},
                    "target_problem": {"type": "string"},
                    "solution_approach": {"type": "string"},
                    "market_positioning": {"type": "string"},
                    "competitive_moat": {"type": "string"}
                },
                "required": ["project_name", "tagline", "core_value_proposition"]
            },
            "technical_deep_dive": {
                "type": "object",
                "properties": {
                    "architecture_overview": {"type": "string"},
                    "design_patterns": {"type": "array", "items": {"type": "string"}},
                    "consensus_mechanism": {"type": "string"},
                    "consensus_details": {"type": "string"},
                    "smart_contract_functionality": {"type": "string"},
                    "smart_contract_limitations": {"type": "string"},
                    "scalability_solutions": {"type": "array", "items": {"type": "string"}},
                    "security_measures": {"type": "array", "items": {"type": "string"}},
                    "audit_status": {"type": "string"},
                    "interoperability": {"type": "string"},
                    "technical_innovation_score": {"type": "integer", "minimum": 1, "maximum": 10},
                    "innovation_justification": {"type": "string"}
                },
                "required": ["architecture_overview", "consensus_mechanism"]
            },
            "tokenomics": {
                "type": "object",
                "properties": {
                    "token_name": {"type": "string"},
                    "token_symbol": {"type": "string"},
                    "total_supply": {"type": "string"},
                    "utility": {"type": "array", "items": {"type": "string"}},
                    "distribution": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "category": {"type": "string"},
                                "percentage": {"type": "string"},
                                "vesting": {"type": "string"}
                            }
                        }
                    },
                    "inflation_mechanism": {"type": "string"},
                    "deflation_mechanism": {"type": "string"},
                    "economic_sustainability": {"type": "string"}
                },
                "required": ["token_name", "token_symbol"]
            },
            "risk_analysis": {
                "type": "object",
                "properties": {
                    "technical_risks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "risk": {"type": "string"},
                                "description": {"type": "string"},
                                "severity": {"type": "string", "enum": ["Low", "Medium", "High", "Critical"]},
                                "probability": {"type": "string", "enum": ["Low", "Medium", "High"]}
                            }
                        }
                    },
                    "market_risks": {"type": "array"},
                    "team_execution_risks": {"type": "array"},
                    "overall_risk_level": {"type": "string"}
                }
            },
            "financial_analysis": {
                "type": "object",
                "properties": {
                    "funding_raised": {"type": "string"},
                    "funding_allocation": {"type": "object"},
                    "revenue_model": {"type": "string"},
                    "token_value_drivers": {"type": "array", "items": {"type": "string"}},
                    "bull_case": {"type": "string"},
                    "bear_case": {"type": "string"}
                }
            },
            "overall_assessment": {
                "type": "object",
                "properties": {
                    "innovation_score": {"type": "integer", "minimum": 1, "maximum": 10},
                    "technical_viability": {"type": "integer", "minimum": 1, "maximum": 10},
                    "team_capability": {"type": "integer", "minimum": 1, "maximum": 10},
                    "market_opportunity": {"type": "integer", "minimum": 1, "maximum": 10},
                    "risk_adjusted_rating": {"type": "integer", "minimum": 1, "maximum": 10},
                    "investment_recommendation": {"type": "string", "enum": ["Strong Buy", "Buy", "Hold", "Avoid"]},
                    "recommendation_justification": {"type": "string"}
                },
                "required": ["innovation_score", "investment_recommendation"]
            }
        },
        "required": ["executive_analysis", "technical_deep_dive", "tokenomics", "overall_assessment"]
    }


class ERNIEAnalyzer:
    """Service for analyzing whitepapers using ERNIE AI via Novita AI API"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.novita.ai/openai"
        )
        self.model = "baidu/ernie-4.5-vl-28b-a3b-thinking"
        self.json_schema = self._get_json_schema()
    
    def _get_json_schema(self) -> dict:
        """Get the JSON schema for structured AI responses"""
        return _get_json_schema()
    
    def _create_analysis_prompt(self, whitepaper_text: str) -> str:
        prompt = f"""Analyze this crypto whitepaper comprehensively and return ONLY valid JSON. Use web research to find the LATEST 2025-2026 information.

WHITEPAPER:
{whitepaper_text[:18000]}

CRITICAL REQUIREMENTS:
1. DETAILED ANSWERS: Each text field must be 3-5+ sentences with specific data, metrics, and examples
2. CURRENT DATA: Use web research for latest 2025-2026 prices, market caps, TVL, user counts, partnerships, and developments
3. SPECIFIC NUMBERS: Include actual metrics (e.g., "$50M market cap as of Jan 2025", "150K daily users")
4. COMPREHENSIVE: Provide in-depth technical and financial analysis
5. ALL SCORES MUST BE INTEGERS 1-10, NOT STRINGS!
6. Property names MUST be in double quotes. Do NOT truncate any section.

REQUIRED JSON STRUCTURE (expand each field to 3-5+ detailed sentences with metrics):
{{
  "executive_analysis": {{
    "project_name": "Full project name",
    "tagline": "Compelling 1-sentence description", 
    "core_value_proposition": "DETAILED 3-5 sentences explaining unique value, target users, key benefits, and why it matters. Include specific use cases and quantifiable advantages.",
    "target_problem": "DETAILED 3-5 sentences describing the problem, its scale ($X market, Y users affected), current pain points, and why existing solutions fail. Include market research data from 2024-2025.",
    "solution_approach": "DETAILED 3-5 sentences explaining the technical solution, how it works, key innovations, and implementation strategy. Include architecture overview and differentiation.",
    "market_positioning": "DETAILED 3-5 sentences on target market segments, competitive positioning, pricing strategy, and go-to-market approach. Include current market share data (2025) if available.",
    "competitive_moat": "DETAILED 3-5 sentences on sustainable competitive advantages: network effects, technical barriers, partnerships, brand, etc. Explain why competitors can't easily replicate."
  }},
  "technical_deep_dive": {{
    "architecture_overview": "DETAILED 4-6 sentences explaining the complete technical architecture: layers, components, data flow, and how they interact. Include diagrams concepts and specific technologies used.",
    "design_patterns": ["List 3-5 specific design patterns with brief explanations: e.g., 'Microservices architecture for modular scalability'"],
    "consensus_mechanism": "Name of consensus (PoW/PoS/DPoS/BFT/etc.)",
    "consensus_details": "DETAILED 3-5 sentences explaining how the consensus works, its parameters (block time, validator count, stake requirements), strengths, and tradeoffs vs alternatives.", 
    "smart_contract_functionality": "DETAILED 3-5 sentences on smart contract capabilities, supported languages, VM used, gas model, and key contract features. Include examples of what can be built.",
    "smart_contract_limitations": "DETAILED 2-4 sentences on current limitations: gas costs, throughput, complexity constraints, security considerations. Include specific numbers if available.",
    "scalability_solutions": ["List 3-5 scalability approaches with details: e.g., 'Layer 2 rollups processing 10,000+ TPS', 'Sharding for parallel processing'"],
    "security_measures": ["List 4-6 security features with specifics: e.g., 'Multi-signature treasury with 5/9 threshold', 'Bug bounty program: $500K max payout'"],
    "audit_status": "DETAILED status: which firms (CertiK, Trail of Bits, etc.), when (Q4 2024), findings (X critical, Y high), remediation status. Include links if available.",
    "interoperability": "DETAILED 3-4 sentences on cross-chain capabilities, bridges, supported chains, and integration standards (IBC, LayerZero, etc.). Include current bridge TVL if available.",
    "technical_innovation_score": 7,
    "innovation_justification": "DETAILED 3-5 sentences justifying the score: what's innovative, what's standard, comparisons to state-of-art, and potential impact."
  }},
  "tokenomics": {{
    "token_name": "Full token name",
    "token_symbol": "TICKER", 
    "total_supply": "X tokens (or 'Uncapped' with inflation rate). Search for current circulating supply and market cap as of Dec 2024/Jan 2025.",
    "utility": ["List 4-6 utilities with specifics: e.g., 'Governance: 1 token = 1 vote on protocol upgrades', 'Staking: Earn 8-12% APY', 'Fee discounts: 25% reduction'"],
    "distribution": [{{"category": "Team", "percentage": "20%", "vesting": "4-year linear vest, 1-year cliff starting Jan 2024"}}],
    "inflation_mechanism": "DETAILED 2-3 sentences: Emission schedule, annual inflation rate %, distribution of new tokens, how it changes over time. Include current inflation rate (2025).",
    "deflation_mechanism": "DETAILED 2-3 sentences: Token burn mechanisms (% of fees burned, buyback programs), actual burn amounts to date, impact on supply. Search for latest burn data (2024-2025).",
    "economic_sustainability": "DETAILED 3-4 sentences: Long-term token economics viability, balance of inflation/deflation, value capture mechanisms, alignment of incentives. Analysis of whether tokenomics supports growth.",
    "flow_nodes": [{{"id": "node1", "label": "Users", "type": "participant"}}, {{"id": "node2", "label": "Staking Pool", "type": "contract"}}],
    "flow_connections": [{{"source": "node1", "target": "node2", "label": "Stake tokens for 10% APY"}}]
  }},
  "risk_analysis": {{
    "technical_risks": [{{"risk": "string", "description": "string", "severity": "High", "probability": "Medium"}}],
    "market_risks": [{{"risk": "string", "description": "string", "severity": "Medium", "probability": "High"}}],
    "team_execution_risks": [{{"risk": "string", "description": "string", "severity": "Low", "probability": "Medium"}}],
    "overall_risk_level": "Medium"
  }},
  "competitive_landscape": {{
    "direct_competitors": [{{"name": "Competitor name", "description": "2-3 sentences with current 2025 metrics: market cap, TVL, users, TPS", "strengths": ["3-5 specific strengths with data"], "weaknesses": ["3-5 specific weaknesses with data"]}}],
    "feature_comparisons": [{{"feature": "Transaction speed", "project_score": "5000 TPS", "competitor_scores": {{"Ethereum": "15 TPS", "Solana": "65000 TPS", "Arbitrum": "40000 TPS"}}}}],
    "technology_differentiation": "DETAILED 4-5 sentences explaining unique technical advantages vs competitors. Include specific architectural differences, performance benchmarks, and why it matters to users. Use 2025 comparison data.",
    "alternative_approaches": ["List 3-4 alternative approaches competitors take: e.g., 'Optimistic rollups (Optimism) vs ZK-rollups (zkSync) for Layer 2 scaling'"]
  }},
  "technology_alternatives": {{
    "current_tech_stack": ["array"],
    "why_chosen": "string",
    "alternatives": ["array"], 
    "tradeoffs": "string",
    "emerging_disruptions": ["array"],
    "is_optimal": true,
    "optimization_reasoning": "string"
  }},
  "roadmap": {{
    "past_achievements": [{{"phase": "Phase name (e.g., 'Mainnet Launch')", "title": "Milestone title", "description": "2-3 sentences with specifics and impact", "timeline": "Q3 2023 or specific date", "status": "Completed/Delayed/etc."}}],
    "current_phase": "DETAILED 2-3 sentences: What's being built right now (Dec 2024 - Q1 2025), progress %, blockers, expected completion. Search for latest development updates.",
    "future_milestones": [{{"phase": "Future phase", "title": "Upcoming milestone", "description": "2-3 sentences on goals, requirements, expected impact", "timeline": "Q2 2025, Q3 2025, etc.", "status": "Planned/In Progress"}}],
    "critical_path": ["List 3-5 critical milestones that determine project success: e.g., 'Mainnet launch Q2 2025', 'Secure 3 tier-1 exchange listings by Q3 2025'"],
    "roadmap_risk": "DETAILED 3-4 sentences: Likelihood of delays, dependencies, resource constraints, market timing risks. Reference past delivery track record. Search for GitHub/blog updates on progress."
  }},
  "team_partnerships": {{
    "team_members": [{{"name": "Full name", "role": "Title/Position", "experience": "2-3 sentences: Previous companies (Google, Meta, etc.), years of experience, notable achievements, relevant expertise", "linkedin": "URL if found via search"}}],
    "advisors": [{{"name": "Full name", "role": "Advisor type", "experience": "2-3 sentences: Credentials, other projects advised, industry reputation", "linkedin": "URL if found"}}],
    "partnerships": [{{"partner": "Company/Protocol name", "type": "Strategic/Technical/Marketing/etc.", "significance": "2-3 sentences: What the partnership enables, expected impact, announcement date. Search for 2024-2025 partnership announcements."}}],
    "community_size": "DETAILED with current 2025 numbers: Twitter followers (X), Discord members (Y), Telegram (Z), GitHub stars (W). Search social media for latest counts.",
    "community_engagement": "DETAILED 2-3 sentences: Activity levels, engagement rates, community-led initiatives, sentiment analysis. Include recent metrics like daily active Discord users, GitHub contributions/month."
  }},
  "use_cases_adoption": {{
    "primary_use_cases": [{{"title": "Use case name", "description": "3-4 sentences explaining the use case, who it serves, how it works, and value delivered", "example": "Real example: 'Acme Corp uses this for X, processing Y transactions/day, saving Z%'"}}],
    "target_segments": ["List 3-5 specific user segments with size estimates: e.g., 'DeFi traders (5M+ globally)', 'NFT creators ($40B market)'"],
    "adoption_barriers": ["List 4-6 specific barriers with context: e.g., 'High gas fees: $50+ per transaction vs $0.50 on competitors', 'Steep learning curve: 6+ hours to onboard'"],
    "network_effects": "DETAILED 3-4 sentences: Types of network effects (direct, indirect, data), current network size, tipping points, moat strength. Explain how growth accelerates with adoption.",
    "traction_evidence": ["List 5-8 concrete metrics from 2024-2025: e.g., '50,000 daily active users (up 300% YoY)', '$500M TVL as of Dec 2024', '200+ dApps built', 'Listed on Binance, Coinbase'"]
  }},
  "financial_analysis": {{
    "funding_raised": "DETAILED: Total amount raised, rounds (Seed: $X in DATE, Series A: $Y in DATE), investors (name tier-1 VCs), current valuation if known. Search for latest 2024-2025 funding news.",
    "funding_allocation": {{"Development": "40%", "Marketing": "25%", "Operations": "20%", "Reserves": "15%"}},
    "revenue_model": "DETAILED 3-5 sentences: How does the project generate revenue? (transaction fees, subscriptions, token burns, etc.) Include specific fee structures, current revenue (ARR/MRR if available), and projections. Search for 2025 financial disclosures.",
    "token_value_drivers": ["List 4-6 specific drivers: e.g., 'Staking yields: 8-12% APY', 'Token burns: 2% of tx fees', 'Governance rights over $50M treasury'"],
    "bull_case": "DETAILED 4-6 sentences: Best-case scenario with specific targets: market adoption (X users by 2026), token price ($Y with Z market cap), partnerships, technological breakthroughs. Include probability and catalysts. Use current 2025 metrics as baseline.",
    "bear_case": "DETAILED 4-6 sentences: Worst-case scenario: competition risks, regulatory threats, technological failures, market conditions. Include potential price impact and probability. Reference 2024-2025 market context."
  }},
  "visualization_data": {{
    "tech_stack_nodes": [{{"id": "string", "label": "string", "type": "string"}}],
    "tech_stack_connections": [{{"source": "string", "target": "string", "label": "string"}}],
    "risk_radar": [{{"dimension": "string", "score": 7}}],
    "competitive_matrix_x_axis": "string", 
    "competitive_matrix_y_axis": "string",
    "competitive_plots": [{{"name": "string", "x": 7, "y": 8}}]
  }},
  "overall_assessment": {{
    "innovation_score": 7,
    "technical_viability": 8,
    "team_capability": 6,
    "market_opportunity": 7,
    "risk_adjusted_rating": 6,
    "investment_recommendation": "Strong Buy",
    "recommendation_justification": "DETAILED 5-7 sentences: Comprehensive investment thesis considering: technical innovation, team execution, market timing (2025 context), competitive position, tokenomics, risk/reward profile, and catalysts. Include price targets if relevant (e.g., 'potential 3-5x in 12-18 months if mainnet delivers'). Reference current market conditions (Dec 2024/Jan 2025)."
  }}
}}

MANDATORY RULES:
1. DETAIL LEVEL: Every string field MUST contain 3-5+ complete sentences with:
   - Specific metrics and numbers (market cap, TVL, user counts, transaction volumes)
   - Real examples and use cases
   - Technical specifications
   - Comparative analysis where relevant
   - Latest 2025-2026 data from web research

2. WEB RESEARCH REQUIRED: Search for and include:
   - Current token price, market cap, and 24h volume (2025-2026 data)
   - Recent partnerships and integrations announced in 2024-2025
   - Latest GitHub activity and development updates
   - Current TVL, user base, and adoption metrics
   - Recent news, controversies, or major developments
   - Competitor comparisons with current market data

3. FORMATTING:
   - Return ONLY valid JSON, no markdown code blocks
   - ALL property names in double quotes
   - Complete ALL sections - do not truncate or abbreviate
   - ALL SCORES are INTEGERS 1-10 (not strings): innovation_score, technical_viability, team_capability, market_opportunity, risk_adjusted_rating, technical_innovation_score
   - Severity/Probability: "Low"/"Medium"/"High"
   - Recommendation: "Strong Buy"/"Buy"/"Hold"/"Avoid"
   - ALL numeric values in competitor_scores must be strings: "15" not 15

4. NO GENERIC ANSWERS: 
   - Do NOT use: "Not specified in whitepaper" 
   - Instead search the web and provide: "Based on current data (Dec 2024): [detailed findings]"
   - If truly no data exists: "Information not publicly available after thorough research (checked: official website, GitHub, social media, crypto data aggregators)"

5. ARRAY MINIMUM: Each array should have at least 3-5 meaningful items with detailed descriptions

Return the complete, comprehensive JSON now:"""
        
        return prompt
    
    def analyze_whitepaper(self, whitepaper_text: str, max_retries: int = 2) -> AnalysisResult:
        """Analyze whitepaper using ERNIE AI with retry logic"""
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"Sending whitepaper to ERNIE for comprehensive analysis (attempt {attempt + 1}/{max_retries + 1})...")
                
                prompt = self._create_analysis_prompt(whitepaper_text)
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a senior blockchain analyst with 10+ years of experience in crypto investments, technical due diligence, and market research. 

CRITICAL INSTRUCTIONS:
1. DEPTH: Provide institutional-grade analysis with 3-5+ sentences per field
2. CURRENT DATA: Always search the web for latest 2025-2026 information (prices, market caps, partnerships, developments)
3. SPECIFICITY: Include concrete numbers, metrics, dates, and examples
4. RESEARCH: Use CoinGecko, CoinMarketCap, GitHub, Twitter, official websites, news articles
5. FORMAT: Return ONLY valid JSON with ALL property names in double quotes - NO markdown, NO code blocks, NO tool calls, JUST the raw JSON object starting with {
6. COMPLETENESS: Never truncate - complete every single field thoroughly

DO NOT use tool calls or function calls. Return the JSON directly in your response.
Your analysis will be used for investment decisions - be thorough, critical, and data-driven."""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=32000,
                )
                
                analysis_text = response.choices[0].message.content
                logger.info(f"Received response from ERNIE: {len(analysis_text)} characters")
                
                # Clean XML/tool call tags that the model might add
                if "<tool_call>" in analysis_text or "</tool_call>" in analysis_text:
                    # Remove tool call wrappers
                    import re
                    analysis_text = re.sub(r'<tool_call>.*?</tool_call>', '', analysis_text, flags=re.DOTALL)
                    analysis_text = re.sub(r'<tool_call>.*', '', analysis_text, flags=re.DOTALL)
                    logger.warning("Removed tool_call tags from response")
                
                # Clean JSON from markdown
                if "```json" in analysis_text:
                    analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
                elif "```" in analysis_text:
                    analysis_text = analysis_text.split("```")[1].split("```")[0].strip()
                
                # Additional cleaning - remove any trailing text after the JSON
                analysis_text = analysis_text.strip()
                
                # Find the JSON boundaries more carefully
                if analysis_text.startswith('{'):
                    # Find the matching closing brace
                    brace_count = 0
                    json_end = -1
                    for i, char in enumerate(analysis_text):
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                json_end = i + 1
                                break
                    
                    if json_end > 0:
                        analysis_text = analysis_text[:json_end]
                
                logger.info(f"Cleaned JSON length: {len(analysis_text)} characters")
                
                try:
                    analysis_dict = json.loads(analysis_text)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing failed at position {e.pos}")
                    logger.error(f"Context around error: {analysis_text[max(0, e.pos-100):e.pos+100]}")
                    
                    # Try to fix common JSON issues
                    try:
                        analysis_text = self._fix_common_json_issues(analysis_text)
                        analysis_dict = json.loads(analysis_text)
                    except json.JSONDecodeError as e2:
                        logger.error(f"JSON still malformed after fix attempt: {str(e2)}")
                        
                        # Try more aggressive JSON repair
                        try:
                            analysis_text = self._aggressive_json_repair(analysis_text)
                            analysis_dict = json.loads(analysis_text)
                        except json.JSONDecodeError as e3:
                            logger.error(f"JSON still malformed after aggressive repair: {str(e3)}")
                            if attempt < max_retries:
                                logger.info(f"Retrying analysis due to JSON parsing error (attempt {attempt + 1})")
                                last_error = e3
                                continue
                            else:
                                # If JSON is completely broken on final attempt, return a minimal valid structure
                                logger.warning("Returning minimal analysis structure due to JSON parsing failure")
                                analysis_dict = self._get_minimal_analysis_structure()
                
                # Ensure all required fields exist with defaults
                analysis_dict = self._ensure_defaults(analysis_dict)
                
                # Validate the analysis result before creating the Pydantic model
                analysis_dict = self._validate_analysis_completeness(analysis_dict)
                
                result = AnalysisResult(**analysis_dict)
                
                logger.info("Successfully parsed comprehensive analysis result")
                return result
                
            except json.JSONDecodeError as e:
                last_error = e
                if attempt < max_retries:
                    logger.warning(f"JSON parsing failed on attempt {attempt + 1}, retrying...")
                    continue
                else:
                    logger.error(f"Failed to parse JSON response after {max_retries + 1} attempts: {str(e)}")
                    logger.error(f"Final response text: {analysis_text[:1000] if 'analysis_text' in locals() else 'No response'}")
                    raise Exception(f"Failed to parse AI response as JSON after {max_retries + 1} attempts: {str(e)}")
            
            except Exception as e:
                last_error = e
                if attempt < max_retries:
                    logger.warning(f"Analysis failed on attempt {attempt + 1}, retrying: {str(e)}")
                    continue
                else:
                    logger.error(f"Analysis failed after {max_retries + 1} attempts: {str(e)}")
                    raise Exception(f"Failed to analyze whitepaper after {max_retries + 1} attempts: {str(e)}")
        
        # This should never be reached, but just in case
        raise Exception(f"Failed to analyze whitepaper: {str(last_error)}")
    
    def _fix_common_json_issues(self, json_text: str) -> str:
        """Fix common JSON formatting issues"""
        import re
        
        # Remove any trailing commas before closing braces/brackets
        json_text = re.sub(r',(\s*[}\]])', r'\1', json_text)
        
        # Fix incomplete JSON by finding the last complete object
        if json_text.count('{') > json_text.count('}'):
            # Find the last complete closing brace
            brace_count = 0
            last_complete = -1
            for i, char in enumerate(json_text):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        last_complete = i + 1
            
            if last_complete > 0:
                json_text = json_text[:last_complete]
            else:
                # No complete objects found, try to close what we have
                missing_braces = json_text.count('{') - json_text.count('}')
                if missing_braces > 0:
                    json_text += '}' * missing_braces
        
        # Fix incomplete arrays by closing them properly
        if json_text.count('[') > json_text.count(']'):
            missing_brackets = json_text.count('[') - json_text.count(']')
            json_text += ']' * missing_brackets
        
        # Fix truncated strings by closing them
        lines = json_text.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Check for unclosed strings (odd number of quotes)
            # Count unescaped quotes only
            escaped_line = line.replace('\\"', '')  # Remove escaped quotes for counting
            quote_count = escaped_line.count('"')
            
            if quote_count % 2 != 0 and ':' in line:
                # If line has unclosed string, try to close it
                line_stripped = line.rstrip()
                if line_stripped.endswith(','):
                    line = line_stripped[:-1] + '",'
                elif line_stripped.endswith('}') or line_stripped.endswith(']'):
                    line = line_stripped[:-1] + '"' + line_stripped[-1]
                else:
                    line = line_stripped + '"'
            
            # Fix unescaped quotes in strings
            if ':' in line and '"' in line:
                # Split on colon to separate key from value
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key_part = parts[0]
                    value_part = parts[1].strip()
                    
                    # If value starts and ends with quotes but has unescaped quotes inside
                    if (value_part.startswith('"') and 
                        value_part.rstrip(',').endswith('"') and 
                        value_part.count('"') > 2):
                        # Extract the content between quotes
                        content = value_part[1:value_part.rstrip(',').rfind('"')]
                        # Escape internal quotes
                        content = content.replace('"', '\\"')
                        # Reconstruct the line
                        trailing_comma = ',' if value_part.rstrip().endswith(',') else ''
                        line = f'{key_part}: "{content}"{trailing_comma}'
            
            fixed_lines.append(line)
        
        json_text = '\n'.join(fixed_lines)
        
        # Remove any remaining trailing commas
        json_text = re.sub(r',(\s*[}\]])', r'\1', json_text)
        
        # Ensure the JSON ends properly
        json_text = json_text.strip()
        if not json_text.endswith('}') and json_text.startswith('{'):
            # Count braces to see how many we need to close
            open_braces = json_text.count('{')
            close_braces = json_text.count('}')
            missing_braces = open_braces - close_braces
            
            if missing_braces > 0:
                json_text += '}' * missing_braces
        
        return json_text
    
    def _aggressive_json_repair(self, json_text: str) -> str:
        """More aggressive JSON repair for severely malformed JSON"""
        import re
        
        # Remove control characters that can break JSON
        json_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_text)
        
        # Fix common issues with missing quotes around property names
        # Pattern: word followed by colon (property name without quotes)
        # But avoid fixing already quoted properties
        lines = json_text.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Fix unquoted property names like: description: "text" -> "description": "text"
            # Look for word characters followed by colon, not already in quotes
            if ':' in line:
                # Check if this looks like a property definition
                match = re.match(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.+)$', line)
                if match:
                    indent = match.group(1)
                    prop_name = match.group(2)
                    value = match.group(3)
                    # Only fix if property name is not already quoted
                    if not line.strip().startswith('"'):
                        line = f'{indent}"{prop_name}": {value}'
            
            fixed_lines.append(line)
        
        json_text = '\n'.join(fixed_lines)
        
        # Try to extract valid JSON sections by parsing line by line
        lines = json_text.split('\n')
        valid_lines = []
        brace_count = 0
        bracket_count = 0
        in_string = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line would break JSON structure
            temp_brace_count = brace_count
            temp_bracket_count = bracket_count
            temp_in_string = in_string
            line_valid = True
            
            i = 0
            while i < len(line):
                char = line[i]
                
                if char == '"' and (i == 0 or line[i-1] != '\\'):
                    temp_in_string = not temp_in_string
                elif not temp_in_string:
                    if char == '{':
                        temp_brace_count += 1
                    elif char == '}':
                        temp_brace_count -= 1
                        if temp_brace_count < 0:
                            line_valid = False
                            break
                    elif char == '[':
                        temp_bracket_count += 1
                    elif char == ']':
                        temp_bracket_count -= 1
                        if temp_bracket_count < 0:
                            line_valid = False
                            break
                i += 1
            
            if line_valid:
                # Fix incomplete strings in this line
                if temp_in_string and not line.endswith('"'):
                    line += '"'
                    temp_in_string = False
                
                valid_lines.append(line)
                brace_count = temp_brace_count
                bracket_count = temp_bracket_count
                in_string = temp_in_string
            else:
                # Stop at first structurally invalid line
                break
        
        repaired_json = '\n'.join(valid_lines)
        
        # Close any remaining open structures
        if bracket_count > 0:
            repaired_json += ']' * bracket_count
        if brace_count > 0:
            repaired_json += '}' * brace_count
        
        # Remove trailing commas
        repaired_json = re.sub(r',(\s*[}\]])', r'\1', repaired_json)
        
        return repaired_json
    
    def _validate_analysis_completeness(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Final validation to ensure analysis completeness"""
        
        # Ensure all main sections exist
        required_sections = [
            "executive_analysis", "technical_deep_dive", "tokenomics", "risk_analysis",
            "competitive_landscape", "technology_alternatives", "roadmap", "team_partnerships",
            "use_cases_adoption", "financial_analysis", "visualization_data", "overall_assessment"
        ]
        
        for section in required_sections:
            if section not in data or data[section] is None:
                logger.warning(f"Missing section {section}, adding default")
                data[section] = {}
        
        # Validate team_partnerships has meaningful data
        tp = data.get("team_partnerships", {})
        if not tp.get("team_members") or (len(tp["team_members"]) == 1 and tp["team_members"][0].get("name") == ""):
            tp["team_members"] = [{
                "name": "Team information not disclosed",
                "role": "Information not available in whitepaper",
                "experience": "",
                "linkedin": ""
            }]
        
        # Validate tokenomics has meaningful data
        tok = data.get("tokenomics", {})
        if not tok.get("token_name") or tok["token_name"] == "":
            tok["token_name"] = "Token name not specified"
        if not tok.get("token_symbol") or tok["token_symbol"] == "":
            tok["token_symbol"] = "N/A"
        
        # Validate financial_analysis has meaningful data
        fa = data.get("financial_analysis", {})
        if not fa.get("funding_allocation") or len(fa["funding_allocation"]) == 0:
            fa["funding_allocation"] = {"Information": "Not disclosed in whitepaper"}
        
        # Fix overall_assessment scores - ensure all scores are integers
        oa = data.get("overall_assessment", {})
        data["overall_assessment"] = oa  # Ensure it exists
        
        score_fields = [
            "innovation_score", "technical_viability", "team_capability", 
            "market_opportunity", "risk_adjusted_rating"
        ]
        
        for field in score_fields:
            print(f"DEBUG: Checking field {field}, current value: {oa.get(field)}, type: {type(oa.get(field))}")
            if field in oa:
                # If it's a string or not a valid integer, set default score
                current_value = oa[field]
                if not isinstance(current_value, int) or current_value < 1 or current_value > 10:
                    print(f"DEBUG: Setting {field} to 5")
                    oa[field] = 5  # Default middle score
            else:
                print(f"DEBUG: Field {field} missing, setting to 5")
                oa[field] = 5  # Default if missing
        
        # Ensure recommendation is valid
        valid_recommendations = ["Strong Buy", "Buy", "Hold", "Avoid"]
        if "investment_recommendation" not in oa or oa["investment_recommendation"] not in valid_recommendations:
            oa["investment_recommendation"] = "Hold"
        
        if "recommendation_justification" not in oa:
            oa["recommendation_justification"] = "Analysis completed with limited information available"
        
        # Fix technical_deep_dive scores
        td = data.get("technical_deep_dive", {})
        data["technical_deep_dive"] = td  # Ensure it exists
        
        if "technical_innovation_score" in td:
            if not isinstance(td["technical_innovation_score"], int) or td["technical_innovation_score"] < 1 or td["technical_innovation_score"] > 10:
                td["technical_innovation_score"] = 5
        else:
            td["technical_innovation_score"] = 5
        
        # Fix visualization_data scores
        vd = data.get("visualization_data", {})
        data["visualization_data"] = vd  # Ensure it exists
        
        if "risk_radar" in vd and isinstance(vd["risk_radar"], list):
            for item in vd["risk_radar"]:
                if isinstance(item, dict) and "score" in item:
                    if not isinstance(item["score"], int) or item["score"] < 0 or item["score"] > 10:
                        item["score"] = 5
        
        return data
    
    def _get_minimal_analysis_structure(self) -> dict:
        """Return a minimal valid analysis structure when JSON parsing fails"""
        return {
            "executive_analysis": {
                "project_name": "Analysis Failed",
                "tagline": "Unable to parse AI response",
                "core_value_proposition": "JSON parsing error occurred",
                "target_problem": "Not available due to parsing error",
                "solution_approach": "Not available due to parsing error",
                "market_positioning": "Not available due to parsing error",
                "competitive_moat": "Not available due to parsing error"
            },
            "technical_deep_dive": {
                "architecture_overview": "Not available due to parsing error",
                "design_patterns": [],
                "consensus_mechanism": "Unknown",
                "consensus_details": "Not available due to parsing error",
                "smart_contract_functionality": "Not available due to parsing error",
                "smart_contract_limitations": "Not available due to parsing error",
                "scalability_solutions": [],
                "security_measures": [],
                "audit_status": "Not available due to parsing error",
                "interoperability": "Not available due to parsing error",
                "technical_innovation_score": 5,
                "innovation_justification": "Unable to assess due to parsing error"
            },
            "tokenomics": {
                "token_name": "Unknown",
                "token_symbol": "UNK",
                "total_supply": "Unknown",
                "utility": [],
                "distribution": [],
                "inflation_mechanism": "Not available due to parsing error",
                "deflation_mechanism": "Not available due to parsing error",
                "economic_sustainability": "Not available due to parsing error",
                "flow_nodes": [],
                "flow_connections": []
            },
            "risk_analysis": {
                "technical_risks": [
                    {
                        "risk": "Analysis Incomplete",
                        "description": "Unable to complete risk analysis due to JSON parsing error",
                        "severity": "High",
                        "probability": "High"
                    }
                ],
                "market_risks": [],
                "team_execution_risks": [],
                "overall_risk_level": "High"
            },
            "competitive_landscape": {
                "direct_competitors": [],
                "feature_comparisons": [],
                "technology_differentiation": "Not available due to parsing error",
                "alternative_approaches": []
            },
            "technology_alternatives": {
                "current_tech_stack": [],
                "why_chosen": "Not available due to parsing error",
                "alternatives": [],
                "tradeoffs": "Not available due to parsing error",
                "emerging_disruptions": [],
                "is_optimal": False,
                "optimization_reasoning": "Unable to assess due to parsing error"
            },
            "roadmap": {
                "past_achievements": [],
                "current_phase": "Unknown",
                "future_milestones": [],
                "critical_path": [],
                "roadmap_risk": "High"
            },
            "team_partnerships": {
                "team_members": [],
                "advisors": [],
                "partnerships": [],
                "community_size": "Unknown",
                "community_engagement": "Unknown"
            },
            "use_cases_adoption": {
                "primary_use_cases": [],
                "target_segments": [],
                "adoption_barriers": ["Analysis incomplete due to parsing error"],
                "network_effects": "Not available due to parsing error",
                "traction_evidence": []
            },
            "financial_analysis": {
                "funding_raised": "Unknown",
                "funding_allocation": {},
                "revenue_model": "Not available due to parsing error",
                "token_value_drivers": [],
                "bull_case": "Not available due to parsing error",
                "bear_case": "Not available due to parsing error"
            },
            "visualization_data": {
                "tech_stack_nodes": [],
                "tech_stack_connections": [],
                "risk_radar": [
                    {"dimension": "Analysis Risk", "score": 10}
                ],
                "competitive_matrix_x_axis": "Unknown",
                "competitive_matrix_y_axis": "Unknown",
                "competitive_plots": []
            },
            "overall_assessment": {
                "innovation_score": 1,
                "technical_viability": 1,
                "team_capability": 1,
                "market_opportunity": 1,
                "risk_adjusted_rating": 1,
                "investment_recommendation": "Avoid",
                "recommendation_justification": "Analysis could not be completed due to JSON parsing error. Please try again."
            }
        }
    
    def _ensure_list(self, obj: Dict, field: str) -> None:
        """Ensure a field is a list, converting strings to empty lists"""
        if field not in obj or obj[field] is None or isinstance(obj[field], str):
            obj[field] = []
    
    def _ensure_dict(self, obj: Dict, field: str) -> None:
        """Ensure a field is a dict, converting strings to empty dicts"""
        if field not in obj or obj[field] is None or isinstance(obj[field], str):
            obj[field] = {}
    
    def _ensure_defaults(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure all required fields have default values"""
        
        defaults = {
            "executive_analysis": {},
            "technical_deep_dive": {},
            "tokenomics": {},
            "risk_analysis": {},
            "competitive_landscape": {},
            "technology_alternatives": {},
            "roadmap": {},
            "team_partnerships": {},
            "use_cases_adoption": {},
            "financial_analysis": {},
            "visualization_data": {},
            "overall_assessment": {}
        }
        
        for key, default in defaults.items():
            if key not in data or data[key] is None or isinstance(data[key], str):
                data[key] = default
        
        # Fix risk_analysis lists
        if "risk_analysis" in data and isinstance(data["risk_analysis"], dict):
            ra = data["risk_analysis"]
            for risk_type in ["technical_risks", "market_risks", "team_execution_risks"]:
                self._ensure_list(ra, risk_type)
        
        # Fix tokenomics lists
        if "tokenomics" in data and isinstance(data["tokenomics"], dict):
            tok = data["tokenomics"]
            for field in ["utility", "distribution", "flow_nodes", "flow_connections"]:
                self._ensure_list(tok, field)
            
            # Add default values for missing tokenomics information
            if not tok.get("token_name"):
                tok["token_name"] = "Not specified in whitepaper"
            
            if not tok.get("token_symbol"):
                tok["token_symbol"] = "N/A"
            
            if not tok.get("total_supply"):
                tok["total_supply"] = "Not specified in whitepaper"
            
            if not tok.get("utility"):
                tok["utility"] = ["Token utility not specified in whitepaper"]
            
            if not tok.get("distribution"):
                tok["distribution"] = [{
                    "category": "Information not available",
                    "percentage": "Not disclosed",
                    "vesting": "Not specified"
                }]
            
            if not tok.get("inflation_mechanism"):
                tok["inflation_mechanism"] = "Not specified in whitepaper"
            
            if not tok.get("deflation_mechanism"):
                tok["deflation_mechanism"] = "Not specified in whitepaper"
            
            if not tok.get("economic_sustainability"):
                tok["economic_sustainability"] = "Economic sustainability analysis not provided in whitepaper"
        
        # Fix competitive_landscape lists
        if "competitive_landscape" in data and isinstance(data["competitive_landscape"], dict):
            cl = data["competitive_landscape"]
            for field in ["direct_competitors", "feature_comparisons", "alternative_approaches"]:
                self._ensure_list(cl, field)
            # Fix competitor nested data
            if cl.get("direct_competitors"):
                for comp in cl["direct_competitors"]:
                    if isinstance(comp, dict):
                        self._ensure_list(comp, "strengths")
                        self._ensure_list(comp, "weaknesses")
            
            # Fix feature_comparisons - convert dict to list if needed
            if "feature_comparisons" in cl:
                if isinstance(cl["feature_comparisons"], dict):
                    # Convert dict like {"Transaction speed": {"project_score": "X", "competitor_scores": {...}}}
                    # to list like [{"feature": "Transaction speed", "project_score": "X", "competitor_scores": {...}}]
                    comparisons_list = []
                    for feature_name, feature_data in cl["feature_comparisons"].items():
                        if isinstance(feature_data, dict):
                            comparison_obj = {
                                "feature": feature_name,
                                "project_score": feature_data.get("project_score", "N/A"),
                                "competitor_scores": feature_data.get("competitor_scores", {})
                            }
                            comparisons_list.append(comparison_obj)
                    cl["feature_comparisons"] = comparisons_list
                
                # Ensure competitor_scores values are strings
                if isinstance(cl["feature_comparisons"], list):
                    for comparison in cl["feature_comparisons"]:
                        if isinstance(comparison, dict) and "competitor_scores" in comparison:
                            if isinstance(comparison["competitor_scores"], dict):
                                # Convert integer values to strings
                                for key, value in comparison["competitor_scores"].items():
                                    if isinstance(value, (int, float)):
                                        comparison["competitor_scores"][key] = str(value)
        
        # Fix roadmap lists
        if "roadmap" in data and isinstance(data["roadmap"], dict):
            rm = data["roadmap"]
            for field in ["past_achievements", "future_milestones", "critical_path"]:
                self._ensure_list(rm, field)
            # Fix milestone nested fields
            for field in ["past_achievements", "future_milestones"]:
                if rm.get(field) and isinstance(rm[field], list):
                    for milestone in rm[field]:
                        if isinstance(milestone, dict):
                            if "title" not in milestone:
                                milestone["title"] = milestone.get("phase", "")
                            if "description" not in milestone:
                                milestone["description"] = ""
                            if "phase" not in milestone:
                                milestone["phase"] = ""
        
        # Fix visualization_data lists
        if "visualization_data" in data and isinstance(data["visualization_data"], dict):
            vd = data["visualization_data"]
            for field in ["tech_stack_nodes", "tech_stack_connections", "risk_radar", "competitive_plots"]:
                self._ensure_list(vd, field)
        
        # Fix financial_analysis
        if "financial_analysis" in data and isinstance(data["financial_analysis"], dict):
            fa = data["financial_analysis"]
            # Fix funding_allocation - convert list to dict if needed
            if "funding_allocation" in fa:
                if isinstance(fa["funding_allocation"], list):
                    # Convert list like ['Development: 50%', 'Marketing: 20%'] to dict
                    allocation_dict = {}
                    for item in fa["funding_allocation"]:
                        if isinstance(item, str) and ":" in item:
                            key, value = item.split(":", 1)
                            allocation_dict[key.strip()] = value.strip()
                    fa["funding_allocation"] = allocation_dict
                elif not isinstance(fa["funding_allocation"], dict):
                    fa["funding_allocation"] = {}
            else:
                self._ensure_dict(fa, "funding_allocation")
            
            self._ensure_list(fa, "token_value_drivers")
            if "revenue_model" in fa and isinstance(fa["revenue_model"], list):
                fa["revenue_model"] = ", ".join(fa["revenue_model"])
            
            # Add default values for missing financial information
            if not fa.get("funding_raised"):
                fa["funding_raised"] = "Not disclosed in whitepaper"
            
            if not fa.get("funding_allocation") or len(fa["funding_allocation"]) == 0:
                fa["funding_allocation"] = {
                    "Information": "Not available in whitepaper"
                }
            
            if not fa.get("revenue_model"):
                fa["revenue_model"] = "Revenue model not specified in whitepaper"
            
            if not fa.get("token_value_drivers"):
                fa["token_value_drivers"] = ["Token value drivers not specified in whitepaper"]
            
            if not fa.get("bull_case"):
                fa["bull_case"] = "Bull case scenario not provided in whitepaper"
            
            if not fa.get("bear_case"):
                fa["bear_case"] = "Bear case scenario not provided in whitepaper"
        
        # Fix team_partnerships lists
        if "team_partnerships" in data and isinstance(data["team_partnerships"], dict):
            tp = data["team_partnerships"]
            for field in ["team_members", "advisors"]:
                if field in tp and isinstance(tp[field], list):
                    # Convert string entries to proper TeamMember objects
                    fixed_members = []
                    for member in tp[field]:
                        if isinstance(member, str):
                            # Parse string like "Satoshi Nakamoto (pseudonymous)" into proper object
                            name = member.split(" (")[0] if " (" in member else member
                            role = member.split(" (")[1].rstrip(")") if " (" in member else "Team Member"
                            fixed_members.append({
                                "name": name,
                                "role": role,
                                "experience": "",
                                "linkedin": ""
                            })
                        elif isinstance(member, dict):
                            # Ensure all required fields exist
                            if "name" not in member:
                                member["name"] = ""
                            if "role" not in member:
                                member["role"] = "Team Member"
                            if "experience" not in member:
                                member["experience"] = ""
                            if "linkedin" not in member:
                                member["linkedin"] = ""
                            fixed_members.append(member)
                    tp[field] = fixed_members
                else:
                    self._ensure_list(tp, field)
            
            # Fix partnerships
            if "partnerships" in tp and isinstance(tp["partnerships"], list):
                fixed_partnerships = []
                for partnership in tp["partnerships"]:
                    if isinstance(partnership, str):
                        # Parse string like "Bitcoin Foundation" or "Coinbase (early exchange)" into proper object
                        if " (" in partnership and partnership.endswith(")"):
                            partner_name = partnership.split(" (")[0]
                            partner_type = partnership.split(" (")[1].rstrip(")")
                        else:
                            partner_name = partnership
                            partner_type = "Strategic"
                        fixed_partnerships.append({
                            "partner": partner_name,
                            "type": partner_type,
                            "significance": "Key partnership"
                        })
                    elif isinstance(partnership, dict):
                        # Ensure all required fields exist
                        if "partner" not in partnership:
                            partnership["partner"] = ""
                        if "type" not in partnership:
                            partnership["type"] = "Strategic"
                        if "significance" not in partnership:
                            partnership["significance"] = ""
                        fixed_partnerships.append(partnership)
                tp["partnerships"] = fixed_partnerships
            else:
                self._ensure_list(tp, "partnerships")
            
            # Add default values for missing team information
            if not tp.get("team_members"):
                tp["team_members"] = [{
                    "name": "Information not available",
                    "role": "Team information not disclosed in whitepaper",
                    "experience": "",
                    "linkedin": ""
                }]
            
            if not tp.get("advisors"):
                tp["advisors"] = [{
                    "name": "Information not available", 
                    "role": "Advisor information not disclosed in whitepaper",
                    "experience": "",
                    "linkedin": ""
                }]
            
            if not tp.get("partnerships"):
                tp["partnerships"] = [{
                    "partner": "Information not available",
                    "type": "Not disclosed",
                    "significance": "Partnership information not available in whitepaper"
                }]
            
            if not tp.get("community_size"):
                tp["community_size"] = "Not specified in whitepaper"
            
            if not tp.get("community_engagement"):
                tp["community_engagement"] = "Not specified in whitepaper"
        
        # Fix use_cases_adoption lists
        if "use_cases_adoption" in data and isinstance(data["use_cases_adoption"], dict):
            uca = data["use_cases_adoption"]
            for field in ["primary_use_cases", "target_segments", "adoption_barriers", "traction_evidence"]:
                self._ensure_list(uca, field)
        
        # Fix technology_alternatives lists
        if "technology_alternatives" in data and isinstance(data["technology_alternatives"], dict):
            ta = data["technology_alternatives"]
            for field in ["current_tech_stack", "alternatives", "emerging_disruptions"]:
                self._ensure_list(ta, field)
                # Extract strings from dicts if needed
                if ta.get(field) and isinstance(ta[field], list):
                    cleaned = []
                    for item in ta[field]:
                        if isinstance(item, dict):
                            # Extract the value from dict (e.g., {"alternative": "text"})
                            cleaned.append(item.get("alternative") or item.get("name") or str(item))
                        elif isinstance(item, str):
                            cleaned.append(item)
                    ta[field] = cleaned
        
        # Fix technical_deep_dive lists
        if "technical_deep_dive" in data and isinstance(data["technical_deep_dive"], dict):
            td = data["technical_deep_dive"]
            for field in ["design_patterns", "scalability_solutions", "security_measures"]:
                self._ensure_list(td, field)
        
        return data
