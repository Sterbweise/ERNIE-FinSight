import { useState, useCallback, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Upload as UploadIcon,
  FileText,
  Sparkles,
  AlertCircle,
  Zap,
  Shield,
  Brain,
  TrendingUp,
  Clock,
  CheckCircle2,
} from "lucide-react";
import { apiService } from "../services/api";

type UploadState = "idle" | "uploading" | "processing" | "error";

function getCurrentProcessStep(progress: number): string {
  if (progress < 10) return "Preparing upload...";
  if (progress < 20) return "Uploading PDF document...";
  if (progress < 30) return "Validating document format...";
  if (progress < 40) return "Extracting text content...";
  if (progress < 50) return "Initializing ERNIE AI analysis...";
  if (progress < 60) return "Analyzing tokenomics structure...";
  if (progress < 70) return "Evaluating technical architecture...";
  if (progress < 80) return "Assessing market risks...";
  if (progress < 90) return "Generating investment insights...";
  if (progress < 95) return "Compiling comprehensive report...";
  return "Finalizing analysis results...";
}

function Upload() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [uploadState, setUploadState] = useState<UploadState>("idle");
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string>("");
  const [isDragging, setIsDragging] = useState(false);
  const [particles, setParticles] = useState<Array<{ id: number; left: number; delay: number }>>([]);

  // Create floating particles effect
  useEffect(() => {
    const createParticles = () => {
      const newParticles = Array.from({ length: 20 }, (_, i) => ({
        id: i,
        left: Math.random() * 100,
        delay: Math.random() * 6,
      }));
      setParticles(newParticles);
    };

    createParticles();
    const interval = setInterval(createParticles, 6000);
    return () => clearInterval(interval);
  }, []);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === "application/pdf") {
      setFile(droppedFile);
      setError("");
    } else {
      setError("Please upload a PDF file");
    }
  }, []);

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFile = e.target.files?.[0];
      if (selectedFile) {
        if (selectedFile.type === "application/pdf") {
          setFile(selectedFile);
          setError("");
        } else {
          setError("Please upload a PDF file");
        }
      }
    },
    []
  );

  const handleUpload = async () => {
    if (!file) return;

    try {
      setUploadState("uploading");
      setProgress(20);
      setError("");

      const uploadResponse = await apiService.uploadWhitepaper(file);
      setProgress(40);
      setUploadState("processing");

      await apiService.pollTaskStatus(uploadResponse.task_id, (status) => {
        setProgress(status.progress || 50);
      });

      navigate(`/results/${uploadResponse.task_id}`);
    } catch (err: any) {
      setUploadState("error");
      setError(
        err.response?.data?.detail ||
          "Failed to analyze whitepaper. Please try again."
      );
      setProgress(0);
    }
  };

  return (
    <div className="min-h-screen relative">
      {/* Zed.dev inspired background */}
      <div className="zed-background">
        <div className="zed-grid"></div>
        <div className="zed-orbs">
          <div className="zed-orb zed-orb-1"></div>
          <div className="zed-orb zed-orb-2"></div>
          <div className="zed-orb zed-orb-3"></div>
        </div>
      </div>

      {/* Floating particles */}
      <div className="particles-container">
        {particles.map((particle) => (
          <div
            key={particle.id}
            className="particle"
            style={{
              left: `${particle.left}%`,
              animationDelay: `${particle.delay}s`,
            }}
          />
        ))}
      </div>

      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-6 pt-20 pb-12 relative z-10">
        <div className="text-center mb-16">
          {/* Enhanced FinSight Title */}
          <h1 className="text-6xl md:text-7xl lg:text-8xl finsight-title mb-4 tracking-tight relative">
            FinSight
          </h1>
          
          <p className="text-sm text-blue-zed/80 mb-6 font-medium">
            Hackathon Project • Powered by ERNIE AI
          </p>
          
          <p className="text-xl md:text-2xl text-gray-400 max-w-3xl mx-auto font-light mb-8">
            AI-powered whitepaper analysis for crypto projects
          </p>
          
          <p className="text-base text-gray-500 max-w-2xl mx-auto">
            Decode complex whitepapers in seconds with advanced AI. Get
            comprehensive insights on tokenomics, technology, roadmaps, and
            risks.
          </p>
        </div>

        {/* Enhanced Upload Section */}
        <div className="glass-premium rounded-2xl p-8 md:p-12 mb-20 relative overflow-hidden">
          <AnimatePresence mode="wait">
            {uploadState === "idle" && (
              <div key="idle">
                <div
                  onDragEnter={handleDragEnter}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  className={`upload-zone relative border-2 border-dashed rounded-xl p-16 text-center transition-all duration-200 ${
                    isDragging
                      ? "upload-zone-active"
                      : "border-white/10 hover:border-white/20 hover:bg-white/[0.02]"
                  }`}
                >
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileInput}
                    className="hidden"
                    id="file-upload"
                  />

                  {!file ? (
                    <div>
                      <motion.div
                        animate={{ 
                          y: [0, -6, 0],
                        }}
                        transition={{ 
                          duration: 2,
                          repeat: Infinity,
                          ease: "easeInOut"
                        }}
                      >
                        <UploadIcon className="w-12 h-12 text-gray-500 mx-auto mb-4" />
                      </motion.div>
                      <h3 className="text-xl font-medium text-white mb-2">
                        Drop your whitepaper here
                      </h3>
                      <p className="text-gray-500 mb-6">or click to browse</p>
                      <label
                        htmlFor="file-upload"
                        className="inline-block px-6 py-3 btn-zed text-sm font-medium rounded-lg cursor-pointer hover:scale-105 transition-transform duration-100"
                      >
                        Select PDF File
                      </label>
                      <p className="text-xs text-gray-600 mt-4">
                        PDF format • Max 10MB
                      </p>
                    </div>
                  ) : (
                    <div>
                      <FileText className="w-12 h-12 text-blue-zed mx-auto mb-4" />
                      <h3 className="text-lg font-medium text-white mb-1">
                        {file.name}
                      </h3>
                      <p className="text-gray-500 mb-6">
                        {(file.size / (1024 * 1024)).toFixed(2)} MB
                      </p>
                      <div className="flex gap-3 justify-center">
                        <button
                          onClick={handleUpload}
                          className="px-6 py-3 btn-zed-blue text-sm font-medium rounded-lg hover:scale-105 transition-transform duration-100"
                        >
                          Analyze Whitepaper
                        </button>
                        <button
                          onClick={() => setFile(null)}
                          className="px-6 py-3 btn-zed-outline text-sm font-medium rounded-lg hover:scale-105 transition-transform duration-100"
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                {error && (
                  <div className="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-lg flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
                    <p className="text-red-300 text-sm">{error}</p>
                  </div>
                )}
              </div>
            )}

            {(uploadState === "uploading" || uploadState === "processing") && (
              <div
                key="processing"
                className="text-center py-8"
              >
                {/* Simple loading spinner */}
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="w-12 h-12 mx-auto mb-6 border-2 border-white/20 border-t-blue-zed rounded-full"
                />

                <h3 className="text-xl font-medium text-white mb-2">
                  {uploadState === "uploading" ? "Uploading..." : "Analyzing Document"}
                </h3>
                
                <p className="text-gray-400 mb-6 text-sm">
                  {getCurrentProcessStep(progress)}
                </p>

                {/* Progress bar */}
                <div className="relative w-full max-w-md mx-auto h-2 bg-white/10 rounded-full mb-4 overflow-hidden">
                  <div
                    className="absolute top-0 left-0 h-full bg-blue-zed rounded-full transition-all duration-300 ease-out"
                    style={{ width: `${progress}%` }}
                  />
                </div>

                <p className="text-gray-500 text-sm">{progress}% Complete</p>
              </div>
            )}

            {uploadState === "error" && (
              <div
                key="error"
                className="text-center py-8"
              >
                <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
                <h3 className="text-xl font-medium text-white mb-2">
                  Analysis Failed
                </h3>
                <p className="text-gray-400 mb-6 text-sm">{error}</p>
                <button
                  onClick={() => {
                    setUploadState("idle");
                    setFile(null);
                    setError("");
                  }}
                  className="px-6 py-3 btn-zed text-sm font-medium rounded-lg hover:scale-105 transition-transform duration-100"
                >
                  Try Again
                </button>
              </div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Why Section */}
      <div className="border-t border-white/5 relative z-10">
        <div className="max-w-6xl mx-auto px-6 py-20">
          <div>
            <h2 className="text-3xl md:text-4xl font-semibold text-white mb-4 text-center">
              Why FinSight?
            </h2>
            <p className="text-gray-400 text-center max-w-2xl mx-auto mb-16">
              Reading crypto whitepapers is time-consuming and complex. We make
              it simple.
            </p>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  icon: <Clock className="w-6 h-6" />,
                  title: "Save Time",
                  description: "Analyze 50+ page whitepapers in under 60 seconds instead of spending hours reading.",
                },
                {
                  icon: <Brain className="w-6 h-6" />,
                  title: "Deep Insights", 
                  description: "Extract tokenomics, roadmap, risks, and competitive advantages automatically.",
                },
                {
                  icon: <TrendingUp className="w-6 h-6" />,
                  title: "Better Decisions",
                  description: "Make informed investment decisions with comprehensive risk analysis and assessments.",
                }
              ].map((item, index) => (
                <div key={index} className="hover:-translate-y-1 transition-transform duration-200">
                  <InfoCard {...item} />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Model Section */}
      <div className="border-t border-white/5 relative z-10">
        <div className="max-w-6xl mx-auto px-6 py-20">
          <div>
            <h2 className="text-3xl md:text-4xl font-semibold text-white mb-4 text-center">
              Powered by ERNIE 4.5
            </h2>
            <p className="text-gray-400 text-center max-w-2xl mx-auto mb-16">
              Advanced AI model from Baidu with 28 billion parameters
            </p>

            <div className="grid md:grid-cols-2 gap-8">
              <div className="glass-premium p-8 rounded-xl hover:scale-[1.01] transition-transform duration-200">
                <h3 className="text-xl font-medium text-white mb-4">
                  Model Capabilities
                </h3>
                <ul className="space-y-3">
                  {[
                    "Multimodal understanding of complex documents",
                    "Advanced natural language processing", 
                    "Contextual analysis and reasoning",
                    "Structured data extraction"
                  ].map((text, index) => (
                    <div key={index}>
                      <Feature text={text} />
                    </div>
                  ))}
                </ul>
              </div>

              <div className="glass-premium p-8 rounded-xl hover:scale-[1.01] transition-transform duration-200">
                <h3 className="text-xl font-medium text-white mb-4">
                  Technical Details
                </h3>
                <ul className="space-y-3">
                  {[
                    "Model: baidu/ernie-4.5-vl-28b-a3b-thinking",
                    "API Provider: Novita AI",
                    "Context window: 15,000+ characters",
                    "Response format: Structured JSON"
                  ].map((text, index) => (
                    <div key={index}>
                      <Feature text={text} />
                    </div>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* What We Analyze */}
      <div className="border-t border-white/5 relative z-10">
        <div className="max-w-6xl mx-auto px-6 py-20">
          <div>
            <h2 className="text-3xl md:text-4xl font-semibold text-white mb-4 text-center">
              12-Point Deep Analysis
            </h2>
            <p className="text-gray-400 text-center max-w-2xl mx-auto mb-16">
              Comprehensive institutional-grade research in seconds
            </p>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                { title: "Executive Analysis", description: "Value proposition, market positioning, competitive moat" },
                { title: "Technical Deep Dive", description: "Architecture, consensus, scalability, security audit" },
                { title: "Tokenomics", description: "Distribution, vesting, inflation/deflation, token flow" },
                { title: "Risk Matrix", description: "Technical, market, team risks with severity scores" },
                { title: "Competitive Landscape", description: "Direct competitors, feature comparison, differentiation" },
                { title: "Tech Alternatives", description: "Why this stack? Trade-offs and emerging disruptions" },
                { title: "Roadmap Analysis", description: "Milestones, critical path, execution feasibility" },
                { title: "Team & Partnerships", description: "Core team, advisors, strategic alliances" },
                { title: "Adoption Potential", description: "Use cases, target segments, network effects" },
                { title: "Financial Analysis", description: "Funding, revenue model, bull/bear cases" },
                { title: "Visualization Data", description: "Charts, diagrams, risk radar for visual insights" },
                { title: "Investment Rating", description: "1-10 scores and Buy/Hold/Avoid recommendation" }
              ].map((item, index) => (
                <div
                  key={index}
                  className="hover:-translate-y-1 hover:scale-[1.01] transition-transform duration-200"
                >
                  <AnalysisCard {...item} />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="border-t border-white/5 relative z-10">
        <div className="max-w-6xl mx-auto px-6 py-20">
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                icon: <Zap className="w-5 h-5" />,
                title: "Lightning Fast",
                description: "Complete analysis in under 60 seconds",
              },
              {
                icon: <Shield className="w-5 h-5" />,
                title: "Secure",
                description: "Files are processed and deleted immediately",
              },
              {
                icon: <Sparkles className="w-5 h-5" />,
                title: "Beautiful UI",
                description: "Clean, modern interface for easy reading",
              }
            ].map((item, index) => (
              <div
                key={index}
                className="hover:-translate-y-1 transition-transform duration-200"
              >
                <FeatureCard {...item} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="glass-premium p-6 rounded-xl hover:border-white/15 transition-all duration-150 group">
      <div className="text-gray-400 mb-3 group-hover:text-blue-zed group-hover:scale-105 transition-all duration-100">
        {icon}
      </div>
      <h4 className="text-white font-medium text-sm mb-1 group-hover:text-blue-zed transition-colors duration-150">
        {title}
      </h4>
      <p className="text-gray-500 text-xs">{description}</p>
    </div>
  );
}

function InfoCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="text-center group">
      <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-blue-zed/10 text-blue-zed mb-4 group-hover:scale-105 group-hover:bg-blue-zed/20 transition-all duration-150">
        {icon}
      </div>
      <h3 className="text-xl font-medium text-white mb-2 group-hover:text-blue-zed transition-colors duration-150">
        {title}
      </h3>
      <p className="text-gray-500 text-sm">{description}</p>
    </div>
  );
}

function AnalysisCard({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="glass-premium p-6 rounded-xl hover:border-white/15 transition-all duration-150 group">
      <h4 className="text-white font-medium mb-2 group-hover:text-blue-zed transition-colors duration-150">
        {title}
      </h4>
      <p className="text-gray-500 text-sm">{description}</p>
    </div>
  );
}

function Feature({ text }: { text: string }) {
  return (
    <li className="flex items-start gap-2 hover:translate-x-1 transition-transform duration-100">
      <div className="hover:scale-110 transition-transform duration-100">
        <CheckCircle2 className="w-4 h-4 text-blue-zed flex-shrink-0 mt-0.5" />
      </div>
      <span className="text-gray-400 text-sm">{text}</span>
    </li>
  );
}

export default Upload;
