from typing import Dict, List

class ReportTemplateGenerator:
    def __init__(self):
        self.platform_contexts = {
            "meta": ["facebook", "instagram", "meta ads", "fb ads"],
            "google": ["google ads", "adwords", "google advertising", "gdn"],
            "linkedin": ["linkedin ads", "linkedin advertising"],
            "tiktok": ["tiktok ads", "tiktok advertising"],
            "twitter": ["twitter ads", "x ads"],
            "general": []
        }
        
        self.stakeholder_contexts = {
            "manager": {
                "focus": ["ROI", "budget efficiency", "key insights", "recommendations"],
                "style": "executive summary with highlights"
            },
            "client": {
                "focus": ["results", "value delivered", "goal achievement", "next steps"],
                "style": "professional report with context"
            },
            "team": {
                "focus": ["detailed metrics", "optimization opportunities", "learnings"],
                "style": "detailed analysis with technical insights"
            },
            "executive": {
                "focus": ["business impact", "strategic insights", "high-level trends"],
                "style": "concise executive summary"
            }
        }
    
    def generate_template(self, intent_result: Dict, query: str) -> str:
        """Generate appropriate template based on intent classification"""
        
        sub_intent = intent_result['sub_intent']
        context = intent_result['context']
        
        if sub_intent == "reporting":
            return self._generate_report_template(context, query)
        elif sub_intent == "strategy":
            return self._generate_strategy_template(context, query)
        elif sub_intent == "audience_targeting":
            return self._generate_audience_template(context, query)
        elif sub_intent == "campaign_creation":
            return self._generate_campaign_template(context, query)
        elif sub_intent == "optimization":
            return self._generate_optimization_template(context, query)
        else:
            return self._generate_generic_template(context, query)
    
    def _generate_report_template(self, context: Dict, query: str) -> str:
        """Generate report creation template"""
        
        # Detect platform
        platform = self._detect_platform(query)
        stakeholder = context.get('stakeholder', 'manager')
        has_data = context.get('has_data', False)
        
        # Get platform-specific metrics
        metrics = self._get_platform_metrics(platform)
        
        # Get stakeholder preferences
        stakeholder_prefs = self.stakeholder_contexts.get(
            stakeholder, 
            self.stakeholder_contexts['manager']
        )
        
        template = f"""**Situation**
You need to communicate {platform.title()} Ads performance data to your {stakeholder} in a professional, easy-to-understand format that highlights key metrics and insights.

**Task**
The assistant should create a comprehensive report from {platform.title()} Ads performance data that is formatted professionally and ready to send to a {stakeholder}. The report should present the data clearly with context and actionable insights tailored to what a {stakeholder} needs to see.

**Objective**
Deliver a polished, {stakeholder}-ready report that demonstrates campaign performance, identifies trends, and supports decision-making around {platform.title()} Ads spend and strategy. Focus on: {', '.join(stakeholder_prefs['focus'])}.

**Knowledge**
To create the most effective report, please provide:
- The {platform.title()} Ads performance data including metrics such as:
  {self._format_metrics_list(metrics)}
- The time period the data covers (e.g., last 7 days, last month, Q4 2024)
- Any specific campaigns, ad sets, or accounts included
- Key business goals or KPIs your {stakeholder} cares about most (e.g., ROAS target, CPA goal, conversion volume)
- Budget information (total spend, remaining budget)
- Any context about what you're trying to achieve with these ads (e.g., lead generation, sales, brand awareness, app installs)
- Previous period data for comparison (optional but recommended)

**Output Format**
The report will be structured as a {stakeholder_prefs['style']} including:
- Executive summary with key highlights
- Performance overview with main metrics
- Campaign/Ad set breakdown
- Trends and insights analysis
- Recommendations and next steps
- Visual representation suggestions (charts/graphs)

---
"""
        
        if has_data:
            template += f"\n**Note:** Please share the data now, and I'll structure it into the report immediately."
        else:
            template += f"\n**Note:** Once you provide the data above, I'll create a professional report with clear sections, key takeaways, and actionable recommendations your {stakeholder} needs to see."
        
        return template
    
    def _generate_strategy_template(self, context: Dict, query: str) -> str:
        """Generate marketing strategy template"""
        return """**Situation**
You need to develop a comprehensive marketing strategy to achieve specific business objectives.

**Task**
Create a detailed marketing strategy that outlines target audience, positioning, channels, budget allocation, and success metrics.

**Objective**
Develop an actionable marketing plan that aligns with business goals and maximizes ROI across chosen channels.

**Knowledge**
Please provide:
- Business/product details and unique value proposition
- Target market and audience insights
- Budget range and timeline
- Primary business objectives (brand awareness, lead gen, sales, etc.)
- Competitive landscape
- Current marketing efforts (if any)
- Key constraints or requirements"""
    
    def _generate_audience_template(self, context: Dict, query: str) -> str:
        """Generate audience targeting template"""
        
        # Extract product/service from query
        query_context = query.replace("target audience", "").replace("for", "").strip()
        
        return f"""**Situation**
You are developing a marketing strategy for '{query_context}' and need to identify and define the target audience segments that would be most receptive to your product/service.

**Task**
Identify and describe 3-5 distinct audience segments for '{query_context}', including:
- Demographics (age, gender, location, income level, education)
- Psychographics (interests, values, lifestyle, attitudes)
- Behavioral characteristics (purchasing behaviors, media consumption, brand interactions)
- Pain points and needs that your product addresses
- Primary motivations for engaging with the brand

**Objective**
Create clear, actionable audience profiles that will guide marketing messaging, channel selection, budget allocation, and product positioning to maximize market reach and brand resonance.

**Knowledge**
To provide the most relevant audience analysis, please share:
- Product/service details and key benefits
- Price point or tier (budget, mid-range, premium)
- Industry or category
- Geographic focus (local, national, global)
- Any existing customer data or insights
- B2B vs B2C focus
- Competitive alternatives in the market"""
    
    def _generate_campaign_template(self, context: Dict, query: str) -> str:
        """Generate campaign creation template"""
        platform = self._detect_platform(query)
        
        return f"""**Situation**
You need to create a {platform.title()} advertising campaign that effectively reaches your target audience and achieves specific marketing objectives.

**Task**
Develop a complete campaign structure including objectives, targeting, creative strategy, budget allocation, and success metrics for {platform.title()} Ads.

**Objective**
Launch a well-structured campaign that is optimized for your goals and positioned for measurable success.

**Knowledge**
Please provide:
- Campaign objective (conversions, traffic, awareness, engagement, etc.)
- Target audience details (demographics, interests, behaviors)
- Budget and timeline
- Product/service being promoted
- Key messaging or value propositions
- Creative assets available (images, videos, copy)
- Landing page or destination URL
- Success metrics and KPIs"""
    
    def _generate_optimization_template(self, context: Dict, query: str) -> str:
        """Generate optimization template"""
        return """**Situation**
Your current advertising campaign is running, but you need to improve performance and achieve better results relative to your goals.

**Task**
Analyze current campaign performance and provide specific, actionable optimization recommendations to improve key metrics.

**Objective**
Identify optimization opportunities and implement changes that will improve campaign efficiency and ROI.

**Knowledge**
Please provide:
- Current campaign performance data (metrics, benchmarks)
- Specific issues or underperforming areas
- Campaign settings (targeting, budget, bidding strategy, creative)
- Business goals and KPI targets
- Time period analyzed
- Previous optimization attempts (if any)"""
    
    def _generate_generic_template(self, context: Dict, query: str) -> str:
        """Fallback generic template"""
        return """**Situation**
You have a marketing-related request that requires clarification.

**Task**
Understand your specific needs and provide targeted assistance.

**Objective**
Help you achieve your marketing goals effectively.

**Knowledge**
Please provide more details about:
- What you're trying to accomplish
- Any relevant context or data
- Specific challenges or constraints
- Desired outcomes"""
    
    def _detect_platform(self, query: str) -> str:
        """Detect advertising platform from query"""
        query_lower = query.lower()
        
        for platform, keywords in self.platform_contexts.items():
            if any(keyword in query_lower for keyword in keywords):
                return platform
        
        return "general"
    
    def _get_platform_metrics(self, platform: str) -> List[str]:
        """Get relevant metrics for each platform"""
        platform_metrics = {
            "meta": [
                "Impressions", "Reach", "Clicks", "CTR (Click-Through Rate)",
                "CPC (Cost Per Click)", "CPM (Cost Per 1000 Impressions)",
                "Conversions", "Cost Per Conversion", "ROAS (Return on Ad Spend)",
                "Amount Spent", "Frequency", "Engagement Rate"
            ],
            "google": [
                "Impressions", "Clicks", "CTR", "CPC", "Conversions",
                "Cost Per Conversion", "Conversion Rate", "Quality Score",
                "Impression Share", "ROAS", "Total Spend"
            ],
            "linkedin": [
                "Impressions", "Clicks", "CTR", "CPC", "Conversions",
                "Cost Per Conversion", "Engagement Rate", "Leads",
                "Cost Per Lead", "Total Spend"
            ],
            "general": [
                "Impressions", "Clicks", "CTR", "CPC", "Conversions",
                "Cost Per Conversion", "ROAS", "Total Spend"
            ]
        }
        
        return platform_metrics.get(platform, platform_metrics["general"])
    
    def _format_metrics_list(self, metrics: List[str]) -> str:
        """Format metrics list for template"""
        return "\n  ".join([f"• {metric}" for metric in metrics])


# Example usage
if __name__ == "__main__":
    import sys
    from pathlib import Path
    # Add parent directory to path for imports
    sys.path.insert(0, str(Path(__file__).parent))
    
    from intent_classifier import IntentClassifier
    
    classifier = IntentClassifier()
    template_gen = ReportTemplateGenerator()
    
    # Test query
    query = "create a report from this data for meta ads so I can send it to my manager"
    
    # Classify intent
    intent_result = classifier.classify_intent(query)
    
    # Generate template
    template = template_gen.generate_template(intent_result, query)
    
    print("Generated Template:\n")
    print(template)
