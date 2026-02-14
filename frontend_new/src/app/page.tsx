"use client";

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import {
  BookOpen,
  Zap,
  Loader2,
  CheckCircle2,
  ExternalLink,
  RefreshCcw,
  ChevronRight,
  AlertCircle,
  Database,
  Eye,
  Package,
  Download,
  Table as TableIcon
} from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { motion, AnimatePresence } from "framer-motion";
import confetti from "canvas-confetti";
import Chatbot from "@/components/Chatbot";
import LoadingOverlay from "@/components/LoadingOverlay";

const API_BASE = '/api';

// Character highlighting styles
const CHARACTER_HIGHLIGHTS = {
  "Peter Pandey": { bg: "#20C99730", color: "#20C997", label: "Analyst" },
  "Tony Sharma": { bg: "#3B82F630", color: "#3B82F6", label: "Executive" },
  "Bruce Hariyali": { bg: "#6F53C130", color: "#6F53C1", label: "Owner" }
};

// Difficulty Configuration
const DIFFICULTY_CONFIG = {
  "Easy": { rows: 5000, tables: 5, columns: 15, questions: 5 },
  "Medium": { rows: 10000, tables: 8, columns: 22, questions: 6 },
  "Difficult": { rows: 20000, tables: 12, columns: 30, questions: 7 }
};

const DIFFICULTY_LEVELS = Object.keys(DIFFICULTY_CONFIG) as (keyof typeof DIFFICULTY_CONFIG)[];

// Predefined options
const DOMAINS = [
  "Fast Food Industry", "E-Commerce", "Healthcare", "Banking & Finance",
  "Real Estate", "Retail", "Tourism & Travel", "Education",
  "Logistics & Supply Chain", "Telecom", "Automobile", "Agriculture", "Other"
];

const FUNCTIONS = [
  "Sales & Marketing", "Operations", "Finance & Accounting", "Human Resources",
  "Supply Chain", "Customer Service", "Product Management",
  "Risk & Compliance", "IT & Technology", "Other"
];

// Phase definitions
const PHASES = [
  { id: 1, name: "Research & Problem", icon: Zap },
  { id: 2, name: "Schema", icon: Database },
  { id: 3, name: "Preview", icon: Eye },
  { id: 4, name: "Full Dataset & QA", icon: Package },
  { id: 5, name: "Downloads", icon: Download }
];

interface ResearchSource {
  title: string;
  url: string;
  source_type: string;
  relevance: string;
  is_primary: boolean;
  key_insights: string[];
}

interface ResearchData {
  domain: string;
  function: string;
  sources: ResearchSource[];
  domain_insights: string[];
  identified_kpis: string[];
}

interface ProblemStatementData {
  company_name: string;
  title: string;
  statement: string;
  character_positions: Record<string, number[]>;
  analytical_questions: string[];
}

interface SchemaTable {
  name: string;
  description: string;
  columns: { name: string; datatype: string; description: string }[];
}

interface SchemaData {
  tables: SchemaTable[];
  relationships: any[];
}

interface PreviewTableData {
  table_name: string;
  sample_rows: any[];
  row_count: number;
  column_count: number;
}

export default function Home() {
  // Current phase (0 is config/start, 1-5 are logic)
  const [currentPhase, setCurrentPhase] = useState<number>(0);
  const [phaseStatus, setPhaseStatus] = useState<Record<number, 'pending' | 'approved' | 'rejected'>>({});

  // Form data (Initial Configuration)
  const [formData, setFormData] = useState({
    domain: '',
    customDomain: '',
    function: '',
    customFunction: '',
    difficulty: 'Medium' as keyof typeof DIFFICULTY_CONFIG,
    problem_statement: '',
    dataset_size: '10000',
    data_structure: 'Normalized'
  });

  // API data
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [research, setResearch] = useState<ResearchData | null>(null);
  const [problem, setProblem] = useState<ProblemStatementData | null>(null);
  const [schema, setSchema] = useState<SchemaData | null>(null);
  const [previewData, setPreviewData] = useState<PreviewTableData[] | null>(null);
  const [qaResults, setQaResults] = useState<any | null>(null);
  const [downloadInfo, setDownloadInfo] = useState<any | null>(null);

  // UI state
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [genProgress, setGenProgress] = useState<{ stage: string, percent: number, message: string } | null>(null);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatInput, setChatInput] = useState('');

  // Auto-adjust dataset size based on difficulty
  useEffect(() => {
    const config = DIFFICULTY_CONFIG[formData.difficulty];
    if (config) {
      setFormData(prev => ({ ...prev, dataset_size: config.rows.toString() }));
    }
  }, [formData.difficulty]);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const getEffectiveDomain = () => formData.domain === 'Other' ? formData.customDomain : formData.domain;
  const getEffectiveFunction = () => formData.function === 'Other' ? formData.customFunction : formData.function;

  const isPhase0Valid = () => {
    const domain = getEffectiveDomain();
    const func = getEffectiveFunction();
    return domain.length >= 3 && func.length >= 3;
  };

  // --- API HANDLERS ---

  const handleStartChallenge = async () => {
    setLoading(true);
    setError(null);
    try {
      const payload = {
        domain: getEffectiveDomain(),
        function: getEffectiveFunction(),
        problem_statement: formData.problem_statement || `We need to conduct research and generate a comprehensive data challenge for the ${getEffectiveDomain()} domain, focusing on ${getEffectiveFunction()}. The goal is to identify key industry trends and metrics to build a realistic dataset for analytical testing and learning purposes.`,
        difficulty: formData.difficulty,
        dataset_size: parseInt(formData.dataset_size),
        data_structure: formData.data_structure,
        primary_questions: ''
      };
      const response = await fetch(`${API_BASE}/challenge/phase1/research`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!response.ok) throw new Error('Research failed');
      const data = await response.json();
      setSessionId(data.session_id);
      setResearch(data.research);
      setCurrentPhase(1);
      setTimeout(() => generateProblemStatement(data.session_id), 1000);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateProblemStatement = async (sid: string) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/challenge/phase1/generate-problem?session_id=${sid}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          domain: getEffectiveDomain(),
          function: getEffectiveFunction(),
          problem_statement: formData.problem_statement || `We need to conduct research and generate a comprehensive data challenge for the ${getEffectiveDomain()} domain, focusing on ${getEffectiveFunction()}. The goal is to identify key industry trends and metrics to build a realistic dataset for analytical testing and learning purposes.`,
          difficulty: formData.difficulty,
          dataset_size: parseInt(formData.dataset_size),
          data_structure: formData.data_structure,
          primary_questions: ''
        })
      });
      if (!response.ok) throw new Error('Problem generation failed');
      const data = await response.json();
      setProblem(data.problem_statement);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleApproveProblem = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/challenge/phase1/approve?session_id=${sessionId}`, { method: 'POST' });
      if (!response.ok) throw new Error('Approval failed');
      setPhaseStatus(prev => ({ ...prev, 1: 'approved' }));
      setCurrentPhase(2);
      generateSchema(sessionId!);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateSchema = async (sid: string) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/challenge/phase2/generate-schema?session_id=${sid}`, { method: 'POST' });
      if (!response.ok) throw new Error('Schema generation failed');
      const data = await response.json();
      setSchema(data.schema);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleApproveSchema = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/challenge/phase2/approve?session_id=${sessionId}`, { method: 'POST' });
      if (!response.ok) throw new Error('Schema approval failed');
      setPhaseStatus(prev => ({ ...prev, 2: 'approved' }));
      setCurrentPhase(3);
      generatePreview(sessionId!);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generatePreview = async (sid: string) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/challenge/phase3/generate-preview?session_id=${sid}`, { method: 'POST' });
      if (!response.ok) throw new Error('Preview failed');
      const data = await response.json();
      setPreviewData(data.preview_data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleApprovePreview = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/challenge/phase3/approve?session_id=${sessionId}`, { method: 'POST' });
      if (!response.ok) throw new Error('Preview approval failed');
      setPhaseStatus(prev => ({ ...prev, 3: 'approved' }));
      setCurrentPhase(4);
      startFullGeneration(sessionId!);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const startFullGeneration = async (sid: string) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/challenge/phase4/generate-full?session_id=${sid}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dataset_size: parseInt(formData.dataset_size) })
      });
      if (!response.ok) throw new Error('Full generation failed');
      const data = await response.json();
      pollStatus(sid);
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  const pollStatus = (sid: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE}/challenge/phase4/status/${sid}`);
        if (!response.ok) return;
        const data = await response.json();
        if (data.progress) setGenProgress(data.progress);
        if (data.status === 'completed') {
          clearInterval(interval);
          setQaResults(data.qa_results);
          setLoading(false);
          setPhaseStatus(prev => ({ ...prev, 4: 'approved' }));
          setCurrentPhase(5);
          prepareDownloads(sid);

          // Trigger success confetti
          confetti({
            particleCount: 150,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#2563eb', '#9333ea', '#10b981']
          });
        } else if (data.status === 'failed') {
          clearInterval(interval);
          setError(data.error);
          setLoading(false);
        }
      } catch (e) {
        console.error("Polling error", e);
      }
    }, 2000);
  };

  const prepareDownloads = async (sid: string) => {
    try {
      const response = await fetch(`${API_BASE}/challenge/phase5/prepare/${sid}`);
      if (!response.ok) throw new Error('Package preparation failed');
      const data = await response.json();
      setDownloadInfo(data);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleReset = () => {
    setCurrentPhase(0);
    setSessionId(null);
    setResearch(null);
    setProblem(null);
    setSchema(null);
    setPreviewData(null);
    setQaResults(null);
    setDownloadInfo(null);
    setError(null);
    setPhaseStatus({});
    setFormData({
      domain: '', customDomain: '', function: '', customFunction: '',
      difficulty: 'Medium', problem_statement: '', dataset_size: '10000', data_structure: 'Normalized'
    });
  };

  // --- HELPERS ---

  const renderHighlightedText = (text: string, positions: Record<string, number[]>) => {
    const segments: { text: string; character?: string }[] = [];
    let lastPos = 0;
    const allMentions: { pos: number; character: string }[] = [];
    Object.entries(positions).forEach(([char, posArray]) => {
      posArray.forEach(pos => { allMentions.push({ pos, character: char }); });
    });
    allMentions.sort((a, b) => a.pos - b.pos);
    allMentions.forEach(mention => {
      if (mention.pos > lastPos) segments.push({ text: text.slice(lastPos, mention.pos) });
      segments.push({ text: text.slice(mention.pos, mention.pos + mention.character.length), character: mention.character });
      lastPos = mention.pos + mention.character.length;
    });
    if (lastPos < text.length) segments.push({ text: text.slice(lastPos) });

    return segments.map((seg, idx) => {
      if (!seg.character) return seg.text;
      const highlight = CHARACTER_HIGHLIGHTS[seg.character as keyof typeof CHARACTER_HIGHLIGHTS];
      return <span key={idx} style={{ backgroundColor: highlight.bg, color: highlight.color, fontWeight: 700, padding: '2px 6px', borderRadius: '4px' }} title={highlight.label}>{seg.text}</span>;
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      {/* Header */}
      <div className="bg-white border-b shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Image src="/logo.png" alt="Codebasics Logo" width={50} height={50} className="object-contain" />
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Codebasics Data Challenge Generator</h1>
                <p className="text-sm text-slate-600 mt-1">Research-driven data challenges with quality validation</p>
              </div>
            </div>
            {currentPhase > 0 && <Button variant="outline" size="sm" onClick={handleReset}><RefreshCcw size={14} className="mr-2" />Start Over</Button>}
          </div>
        </div>
      </div>

      {/* Progress */}
      {currentPhase > 0 && (
        <div className="bg-white border-b sticky top-0 z-20 shadow-sm">
          <div className="max-w-6xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              {PHASES.map((phase, idx) => {
                const Icon = phase.icon;
                const isActive = currentPhase === phase.id;
                const isCompleted = phaseStatus[phase.id] === 'approved' || currentPhase > phase.id;
                return (
                  <React.Fragment key={phase.id}>
                    <div className="flex flex-col items-center">
                      <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm transition-all ${isActive ? 'bg-blue-600 text-white shadow-lg scale-110' : isCompleted ? 'bg-green-600 text-white' : 'bg-slate-200 text-slate-500'}`}>
                        {isCompleted ? <CheckCircle2 size={20} /> : <Icon size={20} />}
                      </div>
                      <div className={`text-xs font-medium mt-2 text-center ${isActive ? 'text-blue-600' : 'text-slate-600'}`}>{phase.name}</div>
                    </div>
                    {idx < PHASES.length - 1 && <div className={`flex-1 h-1 mx-2 mb-8 rounded transition-all ${isCompleted ? 'bg-green-400' : 'bg-slate-200'}`} />}
                  </React.Fragment>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Content */}
      <div className="max-w-6xl mx-auto px-4 py-8">
        {error && <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3"><AlertCircle className="text-red-600 mt-0.5" size={20} /><div><strong className="text-red-800">Error:</strong><p className="text-red-700 mt-1">{error}</p></div></div>}

        <AnimatePresence mode="wait">
          {/* Phase 0: Info */}
          {currentPhase === 0 && (
            <motion.div
              key="phase0"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Card className="border-blue-200 border-2 shadow-xl">
                <CardHeader className="bg-gradient-to-r from-blue-50 to-purple-50">
                  <CardTitle className="flex items-center gap-2 text-blue-900"><BookOpen className="text-blue-600" size={24} />Initial Configuration</CardTitle>
                  <CardDescription>Define your data challenge requirements</CardDescription>
                </CardHeader>
                <CardContent className="pt-6 space-y-5">
                  <LoadingOverlay isLoading={loading && currentPhase === 0} messages={[
                    "Analyzing " + (formData.domain || "industry") + " domain...",
                    "Searching for relevant problem statements...",
                    "Evaluating best matches...",
                    "Finalizing results..."
                  ]} />
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div className="space-y-2">
                      <label className="text-sm font-semibold">Domain *</label>
                      <Select value={formData.domain} onValueChange={v => handleInputChange('domain', v)}><SelectTrigger><SelectValue placeholder="Select domain..." /></SelectTrigger><SelectContent>{DOMAINS.map(d => <SelectItem key={d} value={d}>{d}</SelectItem>)}</SelectContent></Select>
                      {formData.domain === 'Other' && <Input placeholder="Custom Domain..." value={formData.customDomain} onChange={e => handleInputChange('customDomain', e.target.value)} className="mt-2" />}
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-semibold">Business Function *</label>
                      <Select value={formData.function} onValueChange={v => handleInputChange('function', v)}><SelectTrigger><SelectValue placeholder="Select function..." /></SelectTrigger><SelectContent>{FUNCTIONS.map(f => <SelectItem key={f} value={f}>{f}</SelectItem>)}</SelectContent></Select>
                      {formData.function === 'Other' && <Input placeholder="Custom Function..." value={formData.customFunction} onChange={e => handleInputChange('customFunction', e.target.value)} className="mt-2" />}
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-semibold">Difficulty Level *</label>
                      <Select value={formData.difficulty} onValueChange={v => handleInputChange('difficulty', v as any)}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="Easy">Easy (5 tables)</SelectItem><SelectItem value="Medium">Medium (8 tables)</SelectItem><SelectItem value="Difficult">Difficult (12 tables)</SelectItem></SelectContent></Select>
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-semibold">Auto-Configuration</label>
                      <div className="p-2 bg-blue-50 border rounded-md flex justify-around items-center h-10">
                        <Badge variant="outline" className="bg-white"><Database size={12} className="mr-1" />{DIFFICULTY_CONFIG[formData.difficulty].tables} Tables</Badge>
                        <Badge variant="outline" className="bg-white"><Eye size={12} className="mr-1" />{DIFFICULTY_CONFIG[formData.difficulty].columns} Columns</Badge>
                        <Badge variant="outline" className="bg-white"><Zap size={12} className="mr-1" />{DIFFICULTY_CONFIG[formData.difficulty].questions} Questions</Badge>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-semibold">Data Structure *</label>
                      <Select value={formData.data_structure} onValueChange={v => handleInputChange('data_structure', v)}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="Normalized">Normalized</SelectItem><SelectItem value="Denormalized">Denormalized</SelectItem></SelectContent></Select>
                    </div>
                  </div>
                  <div className="space-y-2"><label className="text-sm font-semibold">Context (Optional)</label><Textarea placeholder="Describe requirements..." value={formData.problem_statement} onChange={e => handleInputChange('problem_statement', e.target.value)} rows={4} maxLength={2000} /></div>
                </CardContent>
                <CardFooter className="bg-slate-50 border-t p-6 flex justify-end"><Button onClick={handleStartChallenge} className="bg-gradient-to-r from-blue-600 to-purple-600 text-white gap-2 px-8 shadow-lg" disabled={!isPhase0Valid() || loading}>{loading ? <><Loader2 size={16} className="animate-spin" />Starting...</> : <><Zap size={16} />Start Creation</>}</Button></CardFooter>
              </Card>
            </motion.div>
          )}

          {/* Phase 1: Research & Problem */}
          {currentPhase === 1 && (
            <motion.div
              key="phase1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="space-y-6 relative"
            >
              <LoadingOverlay isLoading={loading} messages={[
                "Analyzing research findings...",
                "Generating problem statement...",
                "Integrating brand characters...",
                "Creating analytical questions..."
              ]} />
              {research && (
                <Card className="border-purple-200 border-2 shadow-xl">
                  <CardHeader className="bg-gradient-to-r from-purple-50 to-blue-50"><CardTitle className="flex items-center gap-2"><BookOpen className="text-purple-600" size={24} />Research Findings</CardTitle></CardHeader>
                  <CardContent className="pt-6 space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="p-4 bg-purple-50 rounded-lg border">
                        <div className="text-2xl font-bold">{research.sources.length}</div>
                        <div className="text-sm">Sources</div>
                      </div>
                      <div className="p-4 bg-blue-50 rounded-lg border">
                        <div className="text-2xl font-bold">{research.identified_kpis.length}</div>
                        <div className="text-sm">KPIs</div>
                      </div>
                      <div className="p-4 bg-green-50 rounded-lg border">
                        <div className="text-2xl font-bold">{research.domain_insights.length}</div>
                        <div className="text-sm">Insights</div>
                      </div>
                    </div>
                    <div className="space-y-4">
                      {research.sources.map((s, i) => (
                        <div key={i} className={`p-4 border-l-4 rounded-lg hover:shadow-md transition-all ${s.is_primary ? 'border-yellow-500 bg-yellow-50/30' : 'border-purple-500 bg-white'}`}>
                          <div className="flex justify-between items-start mb-2">
                            <div>
                              <div className="flex items-center gap-2">
                                <h5 className="font-bold text-slate-900">{s.title}</h5>
                                {s.is_primary && <Badge className="bg-yellow-100 text-yellow-800 text-[10px]">PRIMARY</Badge>}
                              </div>
                              <div className="flex items-center gap-2 text-xs text-slate-500"><Badge variant="outline" className="text-[9px] h-4">{s.source_type}</Badge><a href={s.url} target="_blank" className="hover:underline flex items-center gap-1">{s.url} <ExternalLink size={10} /></a></div>
                            </div>
                            <Badge className={s.relevance === 'high' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}>{s.relevance}</Badge>
                          </div>
                          <ul className="text-xs text-slate-600 space-y-1">{s.key_insights.slice(0, 3).map((ins, j) => <li key={j}>• {ins}</li>)}</ul>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
              {problem ? (
                <Card className="border-green-200 border-2 shadow-xl">
                  <CardHeader><CardTitle className="text-green-900">{problem.company_name}: {problem.title}</CardTitle></CardHeader>
                  <CardContent className="space-y-6">
                    <div className="whitespace-pre-wrap text-slate-700 leading-relaxed">{renderHighlightedText(problem.statement, problem.character_positions)}</div>
                    <div className="space-y-2"><h4 className="font-bold">Analytics Tasks:</h4><ol className="list-decimal list-inside text-sm space-y-1">{problem.analytical_questions.map((q, i) => <li key={i}>{q}</li>)}</ol></div>
                  </CardContent>
                  <CardFooter className="flex justify-between bg-slate-50 border-t p-4">
                    <div className="flex gap-2">
                      <Button variant="outline" onClick={() => generateProblemStatement(sessionId!)}>Quick Regenerate</Button>
                      <Button variant="outline" onClick={() => {
                        setChatOpen(true);
                        setChatInput("I'd like to refine the problem statement. Please change...");
                      }}>Refine w/ AI</Button>
                    </div>
                    <Button onClick={handleApproveProblem} className="bg-blue-600">Approve & Generate Schema</Button>
                  </CardFooter>
                </Card>
              ) : <Card className="p-12 text-center"><Loader2 className="animate-spin mx-auto mb-4 text-blue-600" size={40} /><p>Synthesizing problem statement...</p></Card>}
            </motion.div>
          )}

          {/* Phase 2: Schema */}
          {currentPhase === 2 && (
            <motion.div
              key="phase2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="space-y-6 relative"
            >
              <LoadingOverlay isLoading={loading} messages={[
                "Designing database schema...",
                "Defining table relationships...",
                "Optimizing data types...",
                "Validating normalization..."
              ]} />
              {schema ? (
                <Card className="border-blue-200 border-2 shadow-xl">
                  <CardHeader className="bg-blue-50"><CardTitle className="flex items-center gap-2"><Database className="text-blue-600" />Generated Database Schema</CardTitle></CardHeader>
                  <CardContent className="pt-6 relative">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {schema.tables.map((t, i) => (
                        <div key={i} className="p-0 border-2 rounded-xl bg-white shadow-lg overflow-hidden transition-all hover:border-blue-400 group">
                          <div className="bg-slate-50 border-b p-3 flex items-center justify-between">
                            <h5 className="font-bold text-blue-900 flex items-center gap-2"><TableIcon size={18} className="text-blue-600" />{t.name}</h5>
                            <Badge variant="outline" className="text-[10px] group-hover:bg-blue-100">{t.columns.length} Fields</Badge>
                          </div>
                          <div className="p-3">
                            <p className="text-[11px] text-slate-500 mb-4 line-clamp-2 italic">{t.description}</p>
                            <div className="space-y-1">{t.columns.slice(0, 10).map((c, j) => (
                              <div key={j} className="flex justify-between text-[11px] font-medium border-b border-slate-50 py-1 hover:bg-slate-50 rounded px-1 group/row">
                                <span className="flex items-center gap-1">
                                  {c.name.includes('_id') && <Zap size={10} className="text-yellow-500" />}
                                  {c.name}
                                </span>
                                <span className="text-slate-400 text-[10px] uppercase font-bold">{c.datatype}</span>
                              </div>
                            ))}</div>
                            {t.columns.length > 10 && <div className="text-[10px] text-center mt-3 p-1 bg-slate-50 rounded text-slate-400 font-bold tracking-wider">+{t.columns.length - 10} MORE FIELDS</div>}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-between bg-slate-50 border-t p-4">
                    <div className="flex gap-2">
                      <Button variant="outline" onClick={() => generateSchema(sessionId!)}>Quick Regenerate</Button>
                      <Button variant="outline" onClick={() => {
                        setChatOpen(true);
                        setChatInput("I'd like to adjust the schema. Can you help me change...");
                      }}>Refine w/ AI</Button>
                    </div>
                    <Button onClick={handleApproveSchema} className="bg-blue-600 font-bold">Approve & Preview Data</Button>
                  </CardFooter>
                </Card>
              ) : <Card className="p-12 text-center"><Loader2 className="animate-spin mx-auto mb-4 text-blue-600" size={40} /><p>Engineering database architecture...</p></Card>}
            </motion.div>
          )}

          {/* Phase 3: Preview */}
          {currentPhase === 3 && (
            <motion.div
              key="phase3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="space-y-6 relative"
            >
              <LoadingOverlay isLoading={loading} messages={[
                "Generating fake data...",
                "Maintaining referential integrity...",
                "Creating preview samples...",
                "Validating constraints..."
              ]} />
              {previewData ? (
                <Card className="border-emerald-200 border-2 shadow-xl">
                  <CardHeader className="bg-emerald-50"><CardTitle className="flex items-center gap-2 text-emerald-900"><Eye className="text-emerald-600" />Data Preview (Sample)</CardTitle></CardHeader>
                  <CardContent className="pt-6 space-y-8">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                      {previewData.map((table, i) => (
                        <div key={i} className="space-y-3 bg-white p-4 rounded-xl shadow-md border animate-in fade-in slide-in-from-bottom-2">
                          <div className="flex justify-between items-center">
                            <h5 className="font-bold flex items-center gap-2 text-slate-800"><TableIcon size={18} className="text-emerald-600" /> {table.table_name}</h5>
                            <div className="flex gap-2">
                              <Badge className="bg-emerald-100 text-emerald-800">{table.row_count} Preview Rows</Badge>
                              <Badge className="bg-slate-100 text-slate-800">{table.column_count} Columns</Badge>
                            </div>
                          </div>
                          <div className="overflow-x-auto border rounded-lg scrollbar-hide">
                            <table className="w-full text-[11px] text-left">
                              <thead className="bg-slate-50 border-b sticky top-0"><tr>{table.sample_rows[0] && Object.keys(table.sample_rows[0]).map(k => <th key={k} className="p-3 font-black text-slate-500 uppercase tracking-tighter">{k}</th>)}</tr></thead>
                              <tbody className="divide-y">{table.sample_rows.slice(0, 8).map((row, j) => <tr key={j} className="hover:bg-slate-50 transition-colors">{Object.values(row).map((v: any, k) => <td key={k} className="p-3 truncate max-w-[120px] font-medium text-slate-600">{String(v)}</td>)}</tr>)}</tbody>
                            </table>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="p-4 bg-emerald-50 border border-emerald-100 rounded-xl flex items-center justify-center gap-6">
                      <div className="text-center">
                        <div className="text-lg font-bold text-emerald-800">{previewData.length}</div>
                        <div className="text-[10px] text-emerald-600 font-bold uppercase">Total Tables</div>
                      </div>
                      <div className="w-px h-8 bg-emerald-200" />
                      <div className="text-center text-sm text-slate-500 italic">... the schema relationship integrity is holding 100% across all generated preview rows.</div>
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-between bg-slate-50 border-t p-4">
                    <div className="flex gap-2">
                      <Button variant="outline" onClick={() => generatePreview(sessionId!)}>Quick Regenerate</Button>
                      <Button variant="outline" onClick={() => {
                        setChatOpen(true);
                        setChatInput("The data preview needs adjustment. Please update...");
                      }}>Refine w/ AI</Button>
                    </div>
                    <Button onClick={handleApprovePreview} className="bg-emerald-600 text-white font-bold">Looks Good! Generate Full Dataset</Button>
                  </CardFooter>
                </Card>
              ) : <Card className="p-12 text-center"><Loader2 className="animate-spin mx-auto mb-4 text-emerald-600" size={40} /><p>Synthesizing sample data rows...</p></Card>}
            </motion.div>
          )}

          {/* Phase 4: Full Gen & QA */}
          {currentPhase === 4 && (
            <motion.div
              key="phase4"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.05 }}
              transition={{ duration: 0.4 }}
            >
              <Card className="border-blue-200 border-2 shadow-xl overflow-hidden">
                <CardHeader className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
                  <CardTitle className="flex items-center gap-2"><Package size={24} />Final Generation Pipeline</CardTitle>
                </CardHeader>
                <CardContent className="p-12 text-center space-y-6">
                  <div className="relative w-48 h-48 mx-auto">
                    <div className="absolute inset-0 border-4 border-blue-100 rounded-full" />
                    <div className="absolute inset-0 border-4 border-blue-600 rounded-full border-t-transparent animate-spin" />
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className="text-4xl font-bold text-blue-600">{genProgress?.percent || 0}%</span>
                      <span className="text-xs uppercase text-slate-400 font-bold">Progress</span>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-xl font-bold">{(genProgress?.stage || "STARTING").replace('_', ' ').toUpperCase()}</h3>
                    <p className="text-slate-500">{genProgress?.message || "Preparing engines..."}</p>
                  </div>
                  <Progress value={genProgress?.percent || 0} className="h-2 w-full max-w-md mx-auto" />
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Phase 5: Downloads */}
          {currentPhase === 5 && (
            <motion.div
              key="phase5"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, type: "spring" }}
            >
              <Card className="border-green-200 border-2 shadow-xl">
                <CardHeader className="bg-green-50"><CardTitle className="flex items-center gap-2 text-green-900"><CheckCircle2 className="text-green-600" />Challenge Ready for Download!</CardTitle></CardHeader>
                <CardContent className="pt-8 space-y-6">
                  {qaResults && (
                    <div className="p-6 bg-slate-900 text-white rounded-xl flex items-center justify-between">
                      <div>
                        <div className="text-sm uppercase text-slate-400 font-bold mb-1">Overall Quality Score</div>
                        <div className="text-5xl font-black text-green-400">{qaResults.overall_score.toFixed(1)}<span className="text-lg text-slate-500 font-normal">/10</span></div>
                      </div>
                      <div className="text-right">
                        <Badge className="bg-green-500 mb-2">{qaResults.status}</Badge>
                        <div className="text-xs text-slate-400">Verified by Data Factory QA Enginer</div>
                      </div>
                    </div>
                  )}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-6 border-2 border-dashed rounded-xl space-y-4">
                      <h4 className="font-bold flex items-center gap-2"><TableIcon className="text-blue-600" /> CSV Datasets</h4>
                      <p className="text-sm text-slate-500">Full dataset in CSV format, ready for any analysis tool.</p>
                      <Button className="w-full bg-blue-600" asChild><a href={downloadInfo?.download_url}><Download className="mr-2" size={16} /> Download Full Bundle (.zip)</a></Button>
                    </div>
                    <div className="p-6 border-2 border-dashed rounded-xl space-y-4">
                      <h4 className="font-bold flex items-center gap-2"><Eye className="text-purple-600" /> Solution Report</h4>
                      <p className="text-sm text-slate-500">Excel solution with charts and PDF quality audit report.</p>
                      <div className="flex gap-2">
                        <Button variant="outline" className="flex-1" asChild><a href={downloadInfo?.download_url}><Download size={14} className="mr-2" /> Excel</a></Button>
                        <Button variant="outline" className="flex-1" asChild><a href={downloadInfo?.download_url}><Download size={14} className="mr-2" /> Quality PDF</a></Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
                <CardFooter className="justify-center border-t bg-slate-50 p-6"><Button variant="ghost" onClick={handleReset} className="text-blue-600">Create Another Challenge</Button></CardFooter>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <Chatbot
        sessionId={sessionId}
        currentPhase={currentPhase}
        isOpen={chatOpen}
        setIsOpen={setChatOpen}
        initialInput={chatInput}
      />
    </div>
  );
}
