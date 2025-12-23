from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class UploadResponse(BaseModel):
    task_id: str
    filename: str
    message: str


# Risk severity and probability enums
class Severity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Probability(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# 1. Executive Analysis
class ExecutiveAnalysis(BaseModel):
    project_name: str = ""
    tagline: str = ""
    core_value_proposition: str = ""
    target_problem: str = ""
    solution_approach: str = ""
    market_positioning: str = ""
    competitive_moat: str = ""


# 2. Technical Deep Dive
class TechnicalDeepDive(BaseModel):
    architecture_overview: str = ""
    design_patterns: List[str] = Field(default_factory=list)
    consensus_mechanism: str = ""
    consensus_details: str = ""
    smart_contract_functionality: str = ""
    smart_contract_limitations: str = ""
    scalability_solutions: List[str] = Field(default_factory=list)
    security_measures: List[str] = Field(default_factory=list)
    audit_status: str = ""
    interoperability: str = ""
    technical_innovation_score: int = 5
    innovation_justification: str = ""


# 3. Tokenomics
class TokenDistribution(BaseModel):
    category: str
    percentage: str
    vesting: str = ""


class TokenFlowNode(BaseModel):
    id: str
    label: str
    type: str  # user, validator, treasury, etc.


class TokenFlowConnection(BaseModel):
    source: str
    target: str
    label: str


class TokenomicsBreakdown(BaseModel):
    token_name: str = ""
    token_symbol: str = ""
    total_supply: str = ""
    utility: List[str] = Field(default_factory=list)
    distribution: List[TokenDistribution] = Field(default_factory=list)
    inflation_mechanism: str = ""
    deflation_mechanism: str = ""
    economic_sustainability: str = ""
    flow_nodes: List[TokenFlowNode] = Field(default_factory=list)
    flow_connections: List[TokenFlowConnection] = Field(default_factory=list)


# 4. Risk Analysis
class RiskItem(BaseModel):
    risk: str
    description: str
    severity: str = "Medium"
    probability: str = "Medium"


class RiskAnalysis(BaseModel):
    technical_risks: List[RiskItem] = Field(default_factory=list)
    market_risks: List[RiskItem] = Field(default_factory=list)
    team_execution_risks: List[RiskItem] = Field(default_factory=list)
    overall_risk_level: str = "Medium"


# 5. Competitive Landscape
class Competitor(BaseModel):
    name: str
    description: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)


class FeatureComparison(BaseModel):
    feature: str
    project_score: str
    competitor_scores: Dict[str, str] = Field(default_factory=dict)


class CompetitiveLandscape(BaseModel):
    direct_competitors: List[Competitor] = Field(default_factory=list)
    feature_comparisons: List[FeatureComparison] = Field(default_factory=list)
    technology_differentiation: str = ""
    alternative_approaches: List[str] = Field(default_factory=list)


# 6. Technology Alternatives
class TechnologyAlternatives(BaseModel):
    current_tech_stack: List[str] = Field(default_factory=list)
    why_chosen: str = ""
    alternatives: List[str] = Field(default_factory=list)
    tradeoffs: str = ""
    emerging_disruptions: List[str] = Field(default_factory=list)
    is_optimal: bool = True
    optimization_reasoning: str = ""


# 7. Roadmap
class Milestone(BaseModel):
    phase: str = ""
    title: str = ""
    description: str = ""
    timeline: str = ""
    status: str = "Planned"  # Completed, In Progress, Planned


class RoadmapAnalysis(BaseModel):
    past_achievements: List[Milestone] = Field(default_factory=list)
    current_phase: str = ""
    future_milestones: List[Milestone] = Field(default_factory=list)
    critical_path: List[str] = Field(default_factory=list)
    roadmap_risk: str = ""


# 8. Team & Partnerships
class TeamMember(BaseModel):
    name: str
    role: str
    experience: str = ""
    linkedin: str = ""


class Partnership(BaseModel):
    partner: str
    type: str
    significance: str


class TeamPartnerships(BaseModel):
    team_members: List[TeamMember] = Field(default_factory=list)
    advisors: List[TeamMember] = Field(default_factory=list)
    partnerships: List[Partnership] = Field(default_factory=list)
    community_size: str = ""
    community_engagement: str = ""


# 9. Use Cases & Adoption
class UseCase(BaseModel):
    title: str
    description: str
    example: str = ""


class UseCasesAdoption(BaseModel):
    primary_use_cases: List[UseCase] = Field(default_factory=list)
    target_segments: List[str] = Field(default_factory=list)
    adoption_barriers: List[str] = Field(default_factory=list)
    network_effects: str = ""
    traction_evidence: List[str] = Field(default_factory=list)


# 10. Financial Analysis
class FinancialAnalysis(BaseModel):
    funding_raised: str = ""
    funding_allocation: Optional[Dict[str, Any]] = Field(default_factory=dict)
    revenue_model: Any = ""  # Can be string or list
    token_value_drivers: List[str] = Field(default_factory=list)
    bull_case: str = ""
    bear_case: str = ""


# 11. Visualization Data
class DiagramNode(BaseModel):
    id: str
    label: str
    type: str = ""


class DiagramConnection(BaseModel):
    source: str
    target: str
    label: str = ""


class RadarDataPoint(BaseModel):
    dimension: str
    score: int  # 0-10


class CompetitorPlot(BaseModel):
    name: str
    x: float  # Position on first axis
    y: float  # Position on second axis


class VisualizationData(BaseModel):
    tech_stack_nodes: List[DiagramNode] = Field(default_factory=list)
    tech_stack_connections: List[DiagramConnection] = Field(default_factory=list)
    risk_radar: List[RadarDataPoint] = Field(default_factory=list)
    competitive_matrix_x_axis: str = "Decentralization"
    competitive_matrix_y_axis: str = "Scalability"
    competitive_plots: List[CompetitorPlot] = Field(default_factory=list)


# 12. Overall Assessment
class OverallAssessment(BaseModel):
    innovation_score: int = 5
    technical_viability: int = 5
    team_capability: int = 5
    market_opportunity: int = 5
    risk_adjusted_rating: int = 5
    investment_recommendation: str = "Hold"  # Strong Buy, Buy, Hold, Avoid
    recommendation_justification: str = ""


# Complete Analysis Result
class AnalysisResult(BaseModel):
    executive_analysis: ExecutiveAnalysis = Field(default_factory=ExecutiveAnalysis)
    technical_deep_dive: TechnicalDeepDive = Field(default_factory=TechnicalDeepDive)
    tokenomics: TokenomicsBreakdown = Field(default_factory=TokenomicsBreakdown)
    risk_analysis: RiskAnalysis = Field(default_factory=RiskAnalysis)
    competitive_landscape: CompetitiveLandscape = Field(default_factory=CompetitiveLandscape)
    technology_alternatives: TechnologyAlternatives = Field(default_factory=TechnologyAlternatives)
    roadmap: RoadmapAnalysis = Field(default_factory=RoadmapAnalysis)
    team_partnerships: TeamPartnerships = Field(default_factory=TeamPartnerships)
    use_cases_adoption: UseCasesAdoption = Field(default_factory=UseCasesAdoption)
    financial_analysis: FinancialAnalysis = Field(default_factory=FinancialAnalysis)
    visualization_data: VisualizationData = Field(default_factory=VisualizationData)
    overall_assessment: OverallAssessment = Field(default_factory=OverallAssessment)


class TaskStatusResponse(BaseModel):
    task_id: str
    status: TaskStatus
    message: Optional[str] = None
    progress: Optional[int] = Field(default=0, ge=0, le=100)


class TaskResultResponse(BaseModel):
    task_id: str
    status: TaskStatus
    result: Optional[AnalysisResult] = None
    error: Optional[str] = None
