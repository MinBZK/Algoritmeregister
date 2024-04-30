import { FastApiResponse } from '@/types/index'

export interface C3poResults {
  rules: RuleResults[]
}

export interface RuleResults {
  rule_code: string
  description: string
  feedback_message: string
  result: boolean | null
}

export interface Rule {
  rule_code: string
  rule_variant: string
  description: string
  severity_level: string
}

export interface RuleSet {
  code: string
  rules: Rule[]
}

export interface C3poRequestBody {
  text: string
  ruleSet: string
}

export interface C3poPostResponse extends FastApiResponse {
  data: C3poResults
}

export interface C3poRulesResponse extends FastApiResponse {
  data: RuleSet[]
}
