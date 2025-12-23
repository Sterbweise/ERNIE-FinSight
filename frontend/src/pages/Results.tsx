import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  Loader2,
  AlertTriangle,
  Sparkles,
  Cpu,
  Coins,
  Shield,
  Users,
  Target,
  TrendingUp,
  Calendar,
  BarChart3,
  Layers,
  Zap,
  CheckCircle2,
  XCircle,
  AlertCircle,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { apiService } from "../services/api";

interface AnalysisResult {
  executive_analysis: any;
  technical_deep_dive: any;
  tokenomics: any;
  risk_analysis: any;
  competitive_landscape: any;
  technology_alternatives: any;
  roadmap: any;
  team_partnerships: any;
  use_cases_adoption: any;
  financial_analysis: any;
  visualization_data: any;
  overall_assessment: any;
}

function Results() {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");
  const [activeSection, setActiveSection] = useState<string>("executive");

  useEffect(() => {
    const fetchResult = async () => {
      if (!taskId) return;

      try {
        setLoading(true);
        const response = await apiService.getTaskResult(taskId);

        if (response.status === "failed") {
          setError(response.error || "Analysis failed");
        } else if (response.status === "completed" && response.result) {
          setResult(response.result as any);
        } else {
          setError("No results available");
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || "Failed to fetch results");
      } finally {
        setLoading(false);
      }
    };

    fetchResult();
  }, [taskId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-zed animate-spin mx-auto mb-4" />
          <p className="text-white text-lg">Loading analysis...</p>
        </div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="glass-dark rounded-2xl p-12 text-center max-w-md">
          <AlertTriangle className="w-12 h-12 text-red-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-white mb-4">Error</h2>
          <p className="text-gray-400 mb-6">{error || "No results found"}</p>
          <button
            onClick={() => navigate("/")}
            className="px-6 py-3 btn-zed text-sm font-medium rounded-lg"
          >
            Analyze Another
          </button>
        </div>
      </div>
    );
  }

  const sections = [
    { id: "executive", label: "Executive", icon: Sparkles },
    { id: "technical", label: "Technical", icon: Cpu },
    { id: "tokenomics", label: "Tokenomics", icon: Coins },
    { id: "risks", label: "Risks", icon: Shield },
    { id: "competitive", label: "Competitive", icon: Target },
    { id: "technology", label: "Tech Stack", icon: Layers },
    { id: "roadmap", label: "Roadmap", icon: Calendar },
    { id: "team", label: "Team", icon: Users },
    { id: "adoption", label: "Adoption", icon: TrendingUp },
    { id: "financial", label: "Financial", icon: BarChart3 },
    { id: "assessment", label: "Assessment", icon: Zap },
  ];

  return (
    <div className="min-h-screen">
      {/* Header */}
      <div className="border-b border-white/5 sticky top-0 bg-dark-950/90 backdrop-blur-lg z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate("/")}
              className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back
            </button>
            <h1 className="text-lg font-medium text-white">
              {result.executive_analysis?.project_name || "Analysis Results"}
            </h1>
            <div className="w-20" />
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="max-w-7xl mx-auto px-6 overflow-x-auto">
          <div className="flex gap-1 pb-2">
            {sections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`flex items-center gap-1.5 px-3 py-2 text-sm rounded-lg whitespace-nowrap transition-all ${
                  activeSection === section.id
                    ? "bg-white/10 text-white"
                    : "text-gray-500 hover:text-gray-300"
                }`}
              >
                <section.icon className="w-4 h-4" />
                {section.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <motion.div
          key={activeSection}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          {activeSection === "executive" && (
            <ExecutiveSection data={result.executive_analysis} />
          )}
          {activeSection === "technical" && (
            <TechnicalSection data={result.technical_deep_dive} />
          )}
          {activeSection === "tokenomics" && (
            <TokenomicsSection data={result.tokenomics} />
          )}
          {activeSection === "risks" && (
            <RiskSection data={result.risk_analysis} />
          )}
          {activeSection === "competitive" && (
            <CompetitiveSection data={result.competitive_landscape} />
          )}
          {activeSection === "technology" && (
            <TechnologySection data={result.technology_alternatives} />
          )}
          {activeSection === "roadmap" && (
            <RoadmapSection data={result.roadmap} />
          )}
          {activeSection === "team" && (
            <TeamSection data={result.team_partnerships} />
          )}
          {activeSection === "adoption" && (
            <AdoptionSection data={result.use_cases_adoption} />
          )}
          {activeSection === "financial" && (
            <FinancialSection data={result.financial_analysis} />
          )}
          {activeSection === "assessment" && (
            <AssessmentSection
              data={result.overall_assessment}
              visualization={result.visualization_data}
            />
          )}
        </motion.div>
      </div>
    </div>
  );
}

// Section Components
function ExecutiveSection({ data }: { data: any }) {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Executive Analysis"
        subtitle="High-level overview and strategic positioning"
      />

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-medium text-white mb-1">
            {data?.project_name || "Unknown Project"}
          </h3>
          <p className="text-gray-500 text-sm mb-4">{data?.tagline}</p>
          <div className="space-y-4">
            <InfoBlock
              label="Core Value Proposition"
              value={data?.core_value_proposition}
            />
            <InfoBlock label="Target Problem" value={data?.target_problem} />
            <InfoBlock
              label="Solution Approach"
              value={data?.solution_approach}
            />
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-medium text-white mb-4">
            Market Position
          </h3>
          <div className="space-y-4">
            <InfoBlock
              label="Market Positioning"
              value={data?.market_positioning}
            />
            <InfoBlock
              label="Competitive Moat"
              value={data?.competitive_moat}
            />
          </div>
        </Card>
      </div>
    </div>
  );
}

function TechnicalSection({ data }: { data: any }) {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Technical Deep Dive"
        subtitle="Architecture, consensus, and technical innovations"
      />

      <div className="grid lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <h3 className="text-lg font-medium text-white mb-4">
            Architecture Overview
          </h3>
          <p className="text-gray-400 text-sm mb-4">
            {data?.architecture_overview}
          </p>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <h4 className="text-sm font-medium text-gray-300 mb-2">
                Design Patterns
              </h4>
              <div className="flex flex-wrap gap-2">
                {data?.design_patterns?.map((pattern: string, i: number) => (
                  <Tag key={i}>{pattern}</Tag>
                ))}
              </div>
            </div>
            <div>
              <h4 className="text-sm font-medium text-gray-300 mb-2">
                Scalability Solutions
              </h4>
              <div className="flex flex-wrap gap-2">
                {data?.scalability_solutions?.map((sol: string, i: number) => (
                  <Tag key={i}>{sol}</Tag>
                ))}
              </div>
            </div>
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-medium text-white mb-4">
            Innovation Score
          </h3>
          <div className="text-5xl font-bold text-blue-zed mb-2">
            {data?.technical_innovation_score || 0}/10
          </div>
          <p className="text-gray-500 text-sm">
            {data?.innovation_justification}
          </p>
        </Card>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-medium text-white mb-4">Consensus</h3>
          <div className="space-y-3">
            <InfoBlock label="Mechanism" value={data?.consensus_mechanism} />
            <InfoBlock label="Details" value={data?.consensus_details} />
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-medium text-white mb-4">
            Smart Contracts
          </h3>
          <div className="space-y-3">
            <InfoBlock
              label="Functionality"
              value={data?.smart_contract_functionality}
            />
            <InfoBlock
              label="Limitations"
              value={data?.smart_contract_limitations}
            />
          </div>
        </Card>
      </div>

      <Card>
        <h3 className="text-lg font-medium text-white mb-4">
          Security & Interoperability
        </h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div>
            <h4 className="text-sm font-medium text-gray-300 mb-2">
              Security Measures
            </h4>
            <ul className="space-y-1">
              {data?.security_measures?.map((measure: string, i: number) => (
                <li
                  key={i}
                  className="text-gray-400 text-sm flex items-start gap-2"
                >
                  <CheckCircle2 className="w-4 h-4 text-green-400 flex-shrink-0 mt-0.5" />
                  {measure}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-300 mb-2">
              Audit Status
            </h4>
            <p className="text-gray-400 text-sm">{data?.audit_status}</p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-300 mb-2">
              Interoperability
            </h4>
            <p className="text-gray-400 text-sm">{data?.interoperability}</p>
          </div>
        </div>
      </Card>
    </div>
  );
}

function TokenomicsSection({ data }: { data: any }) {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Tokenomics Breakdown"
        subtitle="Token utility, distribution, and economic model"
      />

      <div className="grid lg:grid-cols-3 gap-6">
        <Card>
          <h3 className="text-lg font-medium text-white mb-4">Token Info</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-500">Name</span>
              <span className="text-white">{data?.token_name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Symbol</span>
              <span className="text-white font-mono">{data?.token_symbol}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Total Supply</span>
              <span className="text-white">{data?.total_supply}</span>
            </div>
          </div>
        </Card>

        <Card className="lg:col-span-2">
          <h3 className="text-lg font-medium text-white mb-4">Token Utility</h3>
          <div className="flex flex-wrap gap-2">
            {data?.utility?.map((util: string, i: number) => (
              <Tag key={i} color="blue">
                {util}
              </Tag>
            ))}
          </div>
        </Card>
      </div>

      <Card>
        <h3 className="text-lg font-medium text-white mb-4">Distribution</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          {data?.distribution?.map((item: any, i: number) => (
            <div key={i} className="bg-white/5 rounded-lg p-4">
              <div className="text-2xl font-bold text-blue-zed mb-1">
                {item.percentage}
              </div>
              <div className="text-white text-sm font-medium">
                {item.category}
              </div>
              <div className="text-gray-500 text-xs mt-1">{item.vesting}</div>
            </div>
          ))}
        </div>
      </Card>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-medium text-white mb-4">
            Economic Mechanisms
          </h3>
          <div className="space-y-3">
            <InfoBlock label="Inflation" value={data?.inflation_mechanism} />
            <InfoBlock label="Deflation" value={data?.deflation_mechanism} />
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-medium text-white mb-4">
            Sustainability Assessment
          </h3>
          <p className="text-gray-400 text-sm">
            {data?.economic_sustainability}
          </p>
        </Card>
      </div>
    </div>
  );
}

function RiskSection({ data }: { data: any }) {
  const getSeverityColor = (severity: string) => {
    switch (severity?.toLowerCase()) {
      case "critical":
        return "bg-red-500/20 text-red-400 border-red-500/30";
      case "high":
        return "bg-orange-500/20 text-orange-400 border-orange-500/30";
      case "medium":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30";
      case "low":
        return "bg-green-500/20 text-green-400 border-green-500/30";
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30";
    }
  };

  return (
    <div className="space-y-6">
      <SectionHeader
        title="Risk Analysis"
        subtitle="Comprehensive risk assessment across all dimensions"
      />

      <Card>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-medium text-white">Overall Risk Level</h3>
          <div
            className={`px-4 py-2 rounded-lg border ${getSeverityColor(
              data?.overall_risk_level
            )}`}
          >
            {data?.overall_risk_level || "Medium"}
          </div>
        </div>
      </Card>

      <div className="space-y-6">
        <RiskCategory
          title="Technical Risks"
          icon={<Cpu className="w-5 h-5" />}
          risks={data?.technical_risks}
        />
        <RiskCategory
          title="Market Risks"
          icon={<TrendingUp className="w-5 h-5" />}
          risks={data?.market_risks}
        />
        <RiskCategory
          title="Team & Execution Risks"
          icon={<Users className="w-5 h-5" />}
          risks={data?.team_execution_risks}
        />
      </div>
    </div>
  );
}

function RiskCategory({
  title,
  icon,
  risks,
}: {
  title: string;
  icon: React.ReactNode;
  risks: any[];
}) {
  const [expanded, setExpanded] = useState(true);

  const getSeverityColor = (severity: string) => {
    switch (severity?.toLowerCase()) {
      case "critical":
        return "text-red-400";
      case "high":
        return "text-orange-400";
      case "medium":
        return "text-yellow-400";
      case "low":
        return "text-green-400";
      default:
        return "text-gray-400";
    }
  };

  return (
    <Card>
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between"
      >
        <div className="flex items-center gap-3">
          <div className="text-gray-400">{icon}</div>
          <h3 className="text-lg font-medium text-white">{title}</h3>
          <span className="text-gray-500 text-sm">({risks?.length || 0})</span>
        </div>
        {expanded ? (
          <ChevronUp className="w-5 h-5 text-gray-400" />
        ) : (
          <ChevronDown className="w-5 h-5 text-gray-400" />
        )}
      </button>

      {expanded && risks && risks.length > 0 && (
        <div className="mt-4 space-y-3">
          {risks.map((risk: any, i: number) => (
            <div
              key={i}
              className="bg-white/5 rounded-lg p-4 border border-white/5"
            >
              <div className="flex items-start justify-between mb-2">
                <h4 className="text-white font-medium">{risk.risk}</h4>
                <div className="flex gap-2">
                  <span
                    className={`text-xs px-2 py-1 rounded ${getSeverityColor(
                      risk.severity
                    )}`}
                  >
                    {risk.severity}
                  </span>
                  <span className="text-xs px-2 py-1 rounded text-gray-400 bg-white/5">
                    {risk.probability}
                  </span>
                </div>
              </div>
              <p className="text-gray-400 text-sm">{risk.description}</p>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}

function CompetitiveSection({ data }: { data: any }) {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Competitive Landscape"
        subtitle="Market positioning and competitor analysis"
      />

      <Card>
        <h3 className="text-lg font-medium text-white mb-4">
          Direct Competitors
        </h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data?.direct_competitors?.map((comp: any, i: number) => (
            <div key={i} className="bg-white/5 rounded-lg p-4">
              <h4 className="text-white font-medium mb-2">{comp.name}</h4>
              <p className="text-gray-500 text-sm mb-3">{comp.description}</p>
              <div className="space-y-2">
                <div>
                  <span className="text-xs text-gray-400">Strengths</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {comp.strengths?.map((s: string, j: number) => (
                      <span
                        key={j}
                        className="text-xs bg-green-500/10 text-green-400 px-2 py-0.5 rounded"
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <span className="text-xs text-gray-400">Weaknesses</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {comp.weaknesses?.map((w: string, j: number) => (
                      <span
                        key={j}
                        className="text-xs bg-red-500/10 text-red-400 px-2 py-0.5 rounded"
                      >
                        {w}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      <Card>
        <h3 className="text-lg font-medium text-white mb-4">
          Technology Differentiation
        </h3>
        <p className="text-gray-400 text-sm mb-4">
          {data?.technology_differentiation}
        </p>
        <h4 className="text-sm font-medium text-gray-300 mb-2">
          Alternative Approaches
        </h4>
        <ul className="space-y-1">
          {data?.alternative_approaches?.map((approach: string, i: number) => (
            <li
              key={i}
              className="text-gray-400 text-sm flex items-start gap-2"
            >
              <span className="text-gray-500">•</span>
              {approach}
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}

function TechnologySection({ data }: { data: any }) {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Technology Stack Analysis"
        subtitle="Tech choices, alternatives, and trade-offs"
      />

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-medium text-white mb-4">
            Current Tech Stack
          </h3>
          <div className="flex flex-wrap gap-2 mb-4">
            {data?.current_tech_stack?.map((tech: string, i: number) => (
              <Tag key={i} color="blue">
                {tech}
              </Tag>
            ))}
          </div>
          <InfoBlock label="Why Chosen" value={data?.why_chosen} />
        </Card>

        <Card>
          <h3 className="text-lg font-medium text-white mb-4">
            Is This Optimal?
          </h3>
          <div className="flex items-center gap-3 mb-4">
            {data?.is_optimal ? (
              <CheckCircle2 className="w-8 h-8 text-green-400" />
            ) : (
              <XCircle className="w-8 h-8 text-red-400" />
            )}
            <span className="text-xl font-medium text-white">
              {data?.is_optimal ? "Yes" : "No"}
            </span>
          </div>
          <p className="text-gray-400 text-sm">
            {data?.optimization_reasoning}
          </p>
        </Card>
      </div>

      <Card>
        <h3 className="text-lg font-medium text-white mb-4">
          Alternatives & Trade-offs
        </h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-sm font-medium text-gray-300 mb-2">
              Alternative Technologies
            </h4>
            <div className="flex flex-wrap gap-2">
              {data?.alternatives?.map((alt: string, i: number) => (
                <Tag key={i}>{alt}</Tag>
              ))}
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-300 mb-2">
              Emerging Disruptions
            </h4>
            <div className="flex flex-wrap gap-2">
              {data?.emerging_disruptions?.map((e: string, i: number) => (
                <Tag key={i} color="orange">
                  {e}
                </Tag>
              ))}
            </div>
          </div>
        </div>
        <div className="mt-4">
          <InfoBlock label="Trade-offs Analysis" value={data?.tradeoffs} />
        </div>
      </Card>
    </div>
  );
}

function RoadmapSection({ data }: { data: any }) {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Roadmap & Milestones"
        subtitle="Past achievements, current progress, and future plans"
      />

      <Card>
        <div className="flex items-center gap-3 mb-4">
          <div className="w-3 h-3 rounded-full bg-blue-zed" />
          <h3 className="text-lg font-medium text-white">Current Phase</h3>
        </div>
        <p className="text-gray-400">{data?.current_phase}</p>
      </Card>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-medium text-white mb-4">
            Past Achievements
          </h3>
          <div className="space-y-3">
            {data?.past_achievements?.map((milestone: any, i: number) => (
              <MilestoneItem key={i} milestone={milestone} status="completed" />
            ))}
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-medium text-white mb-4">
            Future Milestones
          </h3>
          <div className="space-y-3">
            {data?.future_milestones?.map((milestone: any, i: number) => (
              <MilestoneItem key={i} milestone={milestone} status="planned" />
            ))}
          </div>
        </Card>
      </div>

      <Card>
        <h3 className="text-lg font-medium text-white mb-4">
          Critical Path & Risks
        </h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-sm font-medium text-gray-300 mb-2">
              Critical Dependencies
            </h4>
            <ul className="space-y-1">
              {data?.critical_path?.map((item: string, i: number) => (
                <li
                  key={i}
                  className="text-gray-400 text-sm flex items-start gap-2"
                >
                  <AlertCircle className="w-4 h-4 text-yellow-400 flex-shrink-0 mt-0.5" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-300 mb-2">
              Roadmap Risk Assessment
            </h4>
            <p className="text-gray-400 text-sm">{data?.roadmap_risk}</p>
          </div>
        </div>
      </Card>
    </div>
  );
}

function MilestoneItem({
  milestone,
  status,
}: {
  milestone: any;
  status: string;
}) {
  return (
    <div className="bg-white/5 rounded-lg p-4 border-l-2 border-blue-zed">
      <div className="flex items-start justify-between mb-1">
        <h4 className="text-white font-medium">{milestone.title}</h4>
        <span className="text-xs text-gray-500">{milestone.timeline}</span>
      </div>
      <p className="text-gray-400 text-sm">{milestone.description}</p>
    </div>
  );
}

function TeamSection({ data }: { data: any }) {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Team & Partnerships"
        subtitle="Core team, advisors, and strategic alliances"
      />

      <Card>
        <h3 className="text-lg font-medium text-white mb-4">Core Team</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data?.team_members?.map((member: any, i: number) => (
            <div key={i} className="bg-white/5 rounded-lg p-4">
              <h4 className="text-white font-medium">{member.name}</h4>
              <p className="text-blue-zed text-sm">{member.role}</p>
              <p className="text-gray-500 text-xs mt-2">{member.experience}</p>
            </div>
          ))}
        </div>
      </Card>

      {data?.advisors && data.advisors.length > 0 && (
        <Card>
          <h3 className="text-lg font-medium text-white mb-4">Advisors</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {data.advisors.map((advisor: any, i: number) => (
              <div key={i} className="bg-white/5 rounded-lg p-4">
                <h4 className="text-white font-medium text-sm">
                  {advisor.name}
                </h4>
                <p className="text-gray-500 text-xs">{advisor.experience}</p>
              </div>
            ))}
          </div>
        </Card>
      )}

      <Card>
        <h3 className="text-lg font-medium text-white mb-4">Partnerships</h3>
        <div className="space-y-3">
          {data?.partnerships?.map((p: any, i: number) => (
            <div key={i} className="bg-white/5 rounded-lg p-4">
              <div className="flex items-center justify-between mb-1">
                <h4 className="text-white font-medium">{p.partner}</h4>
                <Tag>{p.type}</Tag>
              </div>
              <p className="text-gray-400 text-sm">{p.significance}</p>
            </div>
          ))}
        </div>
      </Card>

      <Card>
        <h3 className="text-lg font-medium text-white mb-4">Community</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <InfoBlock label="Community Size" value={data?.community_size} />
          <InfoBlock label="Engagement" value={data?.community_engagement} />
        </div>
      </Card>
    </div>
  );
}

function AdoptionSection({ data }: { data: any }) {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Use Cases & Adoption"
        subtitle="Real-world applications and market traction"
      />

      <Card>
        <h3 className="text-lg font-medium text-white mb-4">
          Primary Use Cases
        </h3>
        <div className="grid md:grid-cols-2 gap-4">
          {data?.primary_use_cases?.map((uc: any, i: number) => (
            <div key={i} className="bg-white/5 rounded-lg p-4">
              <h4 className="text-white font-medium mb-2">{uc.title}</h4>
              <p className="text-gray-400 text-sm mb-2">{uc.description}</p>
              {uc.example && (
                <p className="text-gray-500 text-xs italic">
                  Example: {uc.example}
                </p>
              )}
            </div>
          ))}
        </div>
      </Card>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-medium text-white mb-4">
            Target Segments
          </h3>
          <div className="flex flex-wrap gap-2">
            {data?.target_segments?.map((seg: string, i: number) => (
              <Tag key={i}>{seg}</Tag>
            ))}
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-medium text-white mb-4">
            Adoption Barriers
          </h3>
          <ul className="space-y-1">
            {data?.adoption_barriers?.map((barrier: string, i: number) => (
              <li
                key={i}
                className="text-gray-400 text-sm flex items-start gap-2"
              >
                <XCircle className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" />
                {barrier}
              </li>
            ))}
          </ul>
        </Card>
      </div>

      <Card>
        <h3 className="text-lg font-medium text-white mb-4">
          Traction Evidence
        </h3>
        <div className="grid md:grid-cols-3 gap-4">
          {data?.traction_evidence?.map((evidence: string, i: number) => (
            <div key={i} className="bg-white/5 rounded-lg p-4 text-center">
              <p className="text-gray-400 text-sm">{evidence}</p>
            </div>
          ))}
        </div>
        <div className="mt-4">
          <InfoBlock label="Network Effects" value={data?.network_effects} />
        </div>
      </Card>
    </div>
  );
}

function FinancialSection({ data }: { data: any }) {
  return (
    <div className="space-y-6">
      <SectionHeader
        title="Financial Analysis"
        subtitle="Funding, revenue model, and investment thesis"
      />

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-medium text-white mb-4">Funding</h3>
          <div className="text-3xl font-bold text-blue-zed mb-4">
            {data?.funding_raised || "Not disclosed"}
          </div>
          <h4 className="text-sm font-medium text-gray-300 mb-2">Allocation</h4>
          <div className="space-y-2">
            {Object.entries(data?.funding_allocation || {}).map(
              ([key, value]: any, i: number) => (
                <div key={i} className="flex justify-between">
                  <span className="text-gray-500">{key}</span>
                  <span className="text-white">{value}</span>
                </div>
              )
            )}
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-medium text-white mb-4">Revenue Model</h3>
          <p className="text-gray-400 text-sm mb-4">{data?.revenue_model}</p>
          <h4 className="text-sm font-medium text-gray-300 mb-2">
            Token Value Drivers
          </h4>
          <div className="flex flex-wrap gap-2">
            {data?.token_value_drivers?.map((driver: string, i: number) => (
              <Tag key={i} color="green">
                {driver}
              </Tag>
            ))}
          </div>
        </Card>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <Card>
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-green-400" />
            <h3 className="text-lg font-medium text-white">Bull Case</h3>
          </div>
          <p className="text-gray-400 text-sm">{data?.bull_case}</p>
        </Card>

        <Card>
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-red-400 rotate-180" />
            <h3 className="text-lg font-medium text-white">Bear Case</h3>
          </div>
          <p className="text-gray-400 text-sm">{data?.bear_case}</p>
        </Card>
      </div>
    </div>
  );
}

function AssessmentSection({
  data,
  visualization,
}: {
  data: any;
  visualization: any;
}) {
  const getRecommendationColor = (rec: string) => {
    switch (rec?.toLowerCase()) {
      case "strong buy":
        return "bg-green-500 text-white";
      case "buy":
        return "bg-green-500/20 text-green-400 border border-green-500/30";
      case "hold":
        return "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30";
      case "avoid":
        return "bg-red-500/20 text-red-400 border border-red-500/30";
      default:
        return "bg-gray-500/20 text-gray-400";
    }
  };

  return (
    <div className="space-y-6">
      <SectionHeader
        title="Overall Assessment"
        subtitle="Final scores and investment recommendation"
      />

      <Card>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-medium text-white">
            Investment Recommendation
          </h3>
          <div
            className={`px-6 py-3 rounded-lg font-bold text-lg ${getRecommendationColor(
              data?.investment_recommendation
            )}`}
          >
            {data?.investment_recommendation || "Hold"}
          </div>
        </div>
        <p className="text-gray-400">{data?.recommendation_justification}</p>
      </Card>

      <div className="grid md:grid-cols-5 gap-4">
        <ScoreCard label="Innovation" score={data?.innovation_score} />
        <ScoreCard label="Technical" score={data?.technical_viability} />
        <ScoreCard label="Team" score={data?.team_capability} />
        <ScoreCard label="Market" score={data?.market_opportunity} />
        <ScoreCard
          label="Risk-Adjusted"
          score={data?.risk_adjusted_rating}
          highlight
        />
      </div>

      {visualization?.risk_radar && visualization.risk_radar.length > 0 && (
        <Card>
          <h3 className="text-lg font-medium text-white mb-4">Risk Radar</h3>
          <div className="grid md:grid-cols-3 lg:grid-cols-6 gap-4">
            {visualization.risk_radar.map((item: any, i: number) => (
              <div key={i} className="text-center">
                <div className="text-2xl font-bold text-blue-zed mb-1">
                  {item.score}/10
                </div>
                <div className="text-gray-500 text-xs">{item.dimension}</div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}

function ScoreCard({
  label,
  score,
  highlight,
}: {
  label: string;
  score: number;
  highlight?: boolean;
}) {
  return (
    <div
      className={`rounded-lg p-4 text-center ${
        highlight ? "bg-blue-zed/20 border border-blue-zed/30" : "bg-white/5"
      }`}
    >
      <div
        className={`text-3xl font-bold mb-1 ${
          highlight ? "text-blue-zed" : "text-white"
        }`}
      >
        {score || 0}
      </div>
      <div className="text-gray-500 text-xs">{label}</div>
    </div>
  );
}

// Utility Components
function SectionHeader({
  title,
  subtitle,
}: {
  title: string;
  subtitle: string;
}) {
  return (
    <div className="mb-6">
      <h2 className="text-2xl font-semibold text-white mb-1">{title}</h2>
      <p className="text-gray-500">{subtitle}</p>
    </div>
  );
}

function Card({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={`glass-dark rounded-xl p-6 ${className}`}>{children}</div>
  );
}

function InfoBlock({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <span className="text-gray-500 text-xs uppercase tracking-wider">
        {label}
      </span>
      <p className="text-gray-300 text-sm mt-1">{value || "Not specified"}</p>
    </div>
  );
}

function Tag({
  children,
  color = "default",
}: {
  children: React.ReactNode;
  color?: "default" | "blue" | "green" | "orange";
}) {
  const colors = {
    default: "bg-white/10 text-gray-300",
    blue: "bg-blue-zed/20 text-blue-zed-light",
    green: "bg-green-500/20 text-green-400",
    orange: "bg-orange-500/20 text-orange-400",
  };

  return (
    <span className={`text-xs px-2 py-1 rounded ${colors[color]}`}>
      {children}
    </span>
  );
}

export default Results;
