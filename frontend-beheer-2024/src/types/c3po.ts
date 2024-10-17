import { FastApiResponse } from '@/types/index'

export interface LanguageRule {
  rule_code: string
  title: string
  description: string
  feedback_message: string
  passed: boolean | null
  result: Result | null
  severity_level: string
}

export interface C3poResponse extends FastApiResponse {
  rules: {
    data: LanguageRule[]
  }
}

interface Result {
  label: string,
  suggestion: string | null,
}
