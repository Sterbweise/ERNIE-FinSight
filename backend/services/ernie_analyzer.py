import json
import logging
from openai import OpenAI
from typing import Dict, Any
from models.schemas import AnalysisResult

logger = logging.getLogger(__name__)


class ERNIEAnalyzer:
    """Service for analyzing whitepapers using ERNIE AI via Novita AI API"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.novita.ai/openai"
        )
        self.model = "baidu/ernie-4.5-vl-28b-a3b-thinking"
    
    def _create_analysis_prompt(self, whitepaper_text: str) -> str:
        prompt = f"""You are an expert cryptocurrency analyst, blockchain architect, and financial analyst. Perform a comprehensive deep-dive analysis of this whitepaper.

WHITEPAPER TEXT:
{whitepaper_text[:20000]}

CRITICAL INSTRUCTIONS FOR MISSING INFORMATION:
- If team information is not available, use: "Information not available in whitepaper"
- If tokenomics details are missing, use: "Not specified in whitepaper" 
- If financial information is not disclosed, use: "Not disclosed in whitepaper"
- For missing partnerships, use: "Partnership information not available"
- NEVER leave fields empty - always provide a descriptive fallback value
- ENSURE the JSON is complete and properly formatted - do not truncate the response

Analyze this whitepaper and return a detailed JSON response with the following structure. Be thorough, specific, and critical in your analysis:

{{
  "executive_analysis": {{
    "project_name": "Official project/token name",
    "tagline": "One-line description or tagline",
    "core_value_proposition": "2-3 sentences on what makes this unique",
    "target_problem": "The specific problem being solved",
    "solution_approach": "How the project solves this problem",
    "market_positioning": "Where it fits in the market",
    "competitive_moat": "What protects it from competition"
  }},
  
  "technical_deep_dive": {{
    "architecture_overview": "High-level architecture description",
    "design_patterns": ["List of architectural patterns used"],
    "consensus_mechanism": "PoW/PoS/DPoS/etc",
    "consensus_details": "Detailed explanation of consensus",
    "smart_contract_functionality": "What smart contracts can do",
    "smart_contract_limitations": "Known limitations",
    "scalability_solutions": ["Layer 2", "Sharding", etc.],
    "security_measures": ["List of security implementations"],
    "audit_status": "Audit status and auditors",
    "interoperability": "Cross-chain capabilities",
    "technical_innovation_score": 7,
    "innovation_justification": "Why this score"
  }},
  
  "tokenomics": {{
    "token_name": "Token name",
    "token_symbol": "TOKEN",
    "total_supply": "1,000,000,000",
    "utility": ["Staking", "Governance", "Gas fees", etc.],
    "distribution": [
      {{"category": "Public Sale", "percentage": "40%", "vesting": "None"}},
      {{"category": "Team", "percentage": "20%", "vesting": "4 years linear"}},
      {{"category": "Ecosystem", "percentage": "25%", "vesting": "None"}},
      {{"category": "Investors", "percentage": "15%", "vesting": "2 years cliff"}}
    ],
    "inflation_mechanism": "Describe inflation if any",
    "deflation_mechanism": "Describe burn/deflation if any",
    "economic_sustainability": "Assessment of long-term economics",
    "flow_nodes": [
      {{"id": "users", "label": "Users", "type": "actor"}},
      {{"id": "validators", "label": "Validators", "type": "actor"}},
      {{"id": "treasury", "label": "Treasury", "type": "storage"}}
    ],
    "flow_connections": [
      {{"source": "users", "target": "validators", "label": "Stake"}},
      {{"source": "validators", "target": "treasury", "label": "Fees"}}
    ]
  }},
  
  "risk_analysis": {{
    "technical_risks": [
      {{"risk": "Smart Contract Vulnerabilities", "description": "Details...", "severity": "High", "probability": "Medium"}},
      {{"risk": "Centralization Points", "description": "Details...", "severity": "Medium", "probability": "High"}}
    ],
    "market_risks": [
      {{"risk": "Competition Intensity", "description": "Details...", "severity": "High", "probability": "High"}},
      {{"risk": "Regulatory Exposure", "description": "Details...", "severity": "Medium", "probability": "Medium"}}
    ],
    "team_execution_risks": [
      {{"risk": "Roadmap Feasibility", "description": "Details...", "severity": "Medium", "probability": "Medium"}},
      {{"risk": "Funding Runway", "description": "Details...", "severity": "Low", "probability": "Low"}}
    ],
    "overall_risk_level": "Medium"
  }},
  
  "competitive_landscape": {{
    "direct_competitors": [
      {{
        "name": "Competitor 1",
        "description": "Brief description",
        "strengths": ["Strength 1", "Strength 2"],
        "weaknesses": ["Weakness 1", "Weakness 2"]
      }}
    ],
    "feature_comparisons": [
      {{"feature": "TPS", "project_score": "10,000", "competitor_scores": {{"Ethereum": "15", "Solana": "65,000"}}}}
    ],
    "technology_differentiation": "What makes the tech unique",
    "alternative_approaches": ["Other ways to solve the same problem"]
  }},
  
  "technology_alternatives": {{
    "current_tech_stack": ["Technology 1", "Technology 2"],
    "why_chosen": "Reasoning for tech choices",
    "alternatives": ["Alternative 1", "Alternative 2"],
    "tradeoffs": "Analysis of tradeoffs made",
    "emerging_disruptions": ["Emerging tech that could disrupt"],
    "is_optimal": true,
    "optimization_reasoning": "Why optimal or not"
  }},
  
  "roadmap": {{
    "past_achievements": [
      {{"phase": "Phase 1", "title": "Mainnet Launch", "description": "Details", "timeline": "Q1 2024", "status": "Completed"}}
    ],
    "current_phase": "Phase 2 - Ecosystem Expansion",
    "future_milestones": [
      {{"phase": "Phase 3", "title": "DEX Launch", "description": "Details", "timeline": "Q3 2024", "status": "Planned"}}
    ],
    "critical_path": ["Key dependencies and blockers"],
    "roadmap_risk": "Assessment of roadmap achievability"
  }},
  
  "team_partnerships": {{
    "team_members": [
      {{"name": "John Doe", "role": "CEO", "experience": "10 years in blockchain", "linkedin": ""}}
    ],
    "advisors": [
      {{"name": "Jane Smith", "role": "Advisor", "experience": "Former Coinbase", "linkedin": ""}}
    ],
    "partnerships": [
      {{"partner": "Partner Name", "type": "Strategic", "significance": "Why important"}}
    ],
    "community_size": "100,000+ Discord members",
    "community_engagement": "Assessment of engagement level"
  }},
  
  "use_cases_adoption": {{
    "primary_use_cases": [
      {{"title": "DeFi Lending", "description": "How it works", "example": "Real-world example"}}
    ],
    "target_segments": ["Retail investors", "Institutions", "Developers"],
    "adoption_barriers": ["Complexity", "Competition", "Regulation"],
    "network_effects": "Analysis of network effects potential",
    "traction_evidence": ["TVL of $X", "Y active users", "Z transactions/day"]
  }},
  
  "financial_analysis": {{
    "funding_raised": "$50M across 3 rounds",
    "funding_allocation": {{"Development": "40%", "Marketing": "30%", "Operations": "30%"}},
    "revenue_model": "Transaction fees, staking rewards",
    "token_value_drivers": ["Utility demand", "Staking lockup", "Burns"],
    "bull_case": "Best case scenario analysis",
    "bear_case": "Worst case scenario analysis"
  }},
  
  "visualization_data": {{
    "tech_stack_nodes": [
      {{"id": "consensus", "label": "Consensus Layer", "type": "core"}},
      {{"id": "execution", "label": "Execution Layer", "type": "core"}},
      {{"id": "application", "label": "Application Layer", "type": "app"}}
    ],
    "tech_stack_connections": [
      {{"source": "application", "target": "execution", "label": "Transactions"}},
      {{"source": "execution", "target": "consensus", "label": "Blocks"}}
    ],
    "risk_radar": [
      {{"dimension": "Technical Risk", "score": 6}},
      {{"dimension": "Market Risk", "score": 7}},
      {{"dimension": "Team Risk", "score": 4}},
      {{"dimension": "Regulatory Risk", "score": 5}},
      {{"dimension": "Competition Risk", "score": 8}},
      {{"dimension": "Execution Risk", "score": 5}}
    ],
    "competitive_matrix_x_axis": "Decentralization",
    "competitive_matrix_y_axis": "Scalability",
    "competitive_plots": [
      {{"name": "This Project", "x": 7, "y": 8}},
      {{"name": "Ethereum", "x": 9, "y": 3}},
      {{"name": "Solana", "x": 4, "y": 9}}
    ]
  }},
  
  "overall_assessment": {{
    "innovation_score": 7,
    "technical_viability": 8,
    "team_capability": 6,
    "market_opportunity": 7,
    "risk_adjusted_rating": 6,
    "investment_recommendation": "Buy",
    "recommendation_justification": "3 sentences explaining the recommendation with key factors considered."
  }}
}}

CRITICAL INSTRUCTIONS:
1. Return ONLY valid JSON, no markdown or additional text
2. Be specific and detailed - use actual data from the whitepaper
3. For missing information, make reasonable inferences or use "Not specified"
4. Scores should be 1-10 with proper justification
5. Risk severity: Low/Medium/High/Critical; Probability: Low/Medium/High
6. Investment recommendation: Strong Buy/Buy/Hold/Avoid
7. Be critical and objective - identify real weaknesses
8. Include at least 3-5 items in each list where applicable
9. Ensure all visualization data is properly structured for charts
10. ENSURE ALL STRING VALUES ARE PROPERLY ESCAPED - use \\" for quotes inside strings
11. DO NOT include trailing commas before closing braces or brackets
12. ENSURE THE JSON IS COMPLETE - do not truncate the response

Return the comprehensive JSON analysis:"""
        
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
                            "content": "You are an expert blockchain analyst and financial advisor. Provide comprehensive, detailed analysis in JSON format only. Be thorough, critical, and specific. ENSURE the JSON is complete and properly formatted."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=12000,
                )
                
                analysis_text = response.choices[0].message.content
                logger.info(f"Received response from ERNIE: {len(analysis_text)} characters")
                
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
            quote_count = line.count('"')
            if quote_count % 2 != 0 and ':' in line:
                # If line has unclosed string, try to close it
                if line.rstrip().endswith(','):
                    line = line.rstrip(',') + '",'
                else:
                    line = line + '"'
            
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
