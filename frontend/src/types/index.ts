export type Verdict =
  | "concordant"
  | "explained_difference"
  | "unexplained_contradiction"
  | "invalid_comparison";

export type ConfidenceLevel = "high" | "medium" | "low";

export interface Source {
  id: string;
  workspace_id: string;
  title: string;
  publisher: string | null;
  published_on: string | null;
  url: string | null;
  format: "pdf" | "xlsx" | "csv" | "html";
  status: "uploaded" | "extracting" | "extracted" | "failed";
}

export interface Claim {
  id: string;
  indicator_code: string | null;
  indicator_label_raw: string;
  value: number;
  unit: string | null;
  period_start: string | null;
  period_end: string | null;
  zone_code: string | null;
  population: string | null;
  extraction_confidence: number;
}

export interface Comparison {
  id: string;
  claim_a: Claim;
  claim_b: Claim;
  similarity: number;
  relative_gap: number | null;
  causes: string[];
  verdict: Verdict;
  confidence_level: ConfidenceLevel;
  confidence_reasons: string[];
  explanation: string | null;
}

export interface Evidence {
  source_id: string;
  source_title: string;
  page: number | null;
  table_ref: string | null;
  snippet: string;
}
