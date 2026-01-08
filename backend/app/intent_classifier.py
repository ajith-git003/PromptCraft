import re
from typing import Dict, List, Tuple, Optional

class IntentClassifier:
    def __init__(self):
        # Define intent hierarchy with keywords and patterns
        self.intent_patterns = {
            "marketing": {
                "reporting": {
                    "keywords": ["report", "analyze", "analysis", "summarize", "summary", 
                               "performance", "results", "metrics", "dashboard"],
                    "phrases": ["create a report", "from this data", "send to", 
                              "show the results", "performance report", "analyze the data"],
                    "indicators": ["data", "metrics", "numbers", "statistics"]
                },
                "strategy": {
                    "keywords": ["strategy", "plan", "approach", "roadmap", "framework"],
                    "phrases": ["marketing strategy", "strategic plan", "go-to-market"],
                    "indicators": ["how to", "what should", "best approach"]
                },
                "audience_targeting": {
                    "keywords": ["audience", "targeting", "segment", "personas", "demographics"],
                    "phrases": ["target audience", "customer segment", "buyer persona"],
                    "indicators": ["who should", "which audience", "demographic"]
                },
                "campaign_creation": {
                    "keywords": ["campaign", "ad", "advertisement", "creative", "copy"],
                    "phrases": ["create campaign", "launch campaign", "ad copy", "write ad"],
                    "indicators": ["launch", "create", "new campaign"]
                },
                "optimization": {
                    "keywords": ["optimize", "improve", "boost", "increase", "enhance", "reduce", "decrease", "lower"],
                    "phrases": ["how to improve", "increase performance", "optimize campaign", "reduce cost", "lower cpa", "reduce cpc"],
                    "indicators": ["better", "more", "higher", "lower cost", "cpa", "cpc", "roas"]
                }
            },
            "coding": {
                "web_development": {
                    "keywords": ["website", "web", "html", "css", "react", "vue", "angular"],
                    "phrases": ["web app", "web application", "website"],
                    "indicators": ["frontend", "backend", "fullstack"]
                },
                "api_development": {
                    "keywords": ["api", "endpoint", "rest", "graphql", "microservice"],
                    "phrases": ["api endpoint", "rest api", "web service"],
                    "indicators": ["http", "request", "response"]
                },
                "application": {
                    "keywords": ["app", "application", "tool", "calculator", "todo", "tracker"],
                    "phrases": ["build app", "create application", "develop tool"],
                    "indicators": ["functionality", "feature", "implement"]
                },
                "debugging": {
                    "keywords": ["bug", "error", "debug", "fix", "issue", "problem"],
                    "phrases": ["not working", "getting error", "fix bug"],
                    "indicators": ["error message", "exception", "crash"]
                }
            },
            "image": {
                "creative": {
                    "keywords": ["art", "artistic", "creative", "illustration", "painting"],
                    "phrases": ["create art", "artistic style", "digital painting"],
                    "indicators": ["style", "mood", "aesthetic"]
                },
                "photorealistic": {
                    "keywords": ["photo", "realistic", "4k", "8k", "photography"],
                    "phrases": ["photorealistic", "real photo", "high resolution"],
                    "indicators": ["realistic", "detailed", "quality"]
                },
                "design": {
                    "keywords": ["logo", "design", "branding", "icon", "ui"],
                    "phrases": ["design logo", "create design", "brand identity"],
                    "indicators": ["professional", "modern", "clean"]
                }
            },
            "writing": {
                "creative": {
                    "keywords": ["story", "poem", "narrative", "fiction", "novel"],
                    "phrases": ["write story", "creative writing", "tell story"],
                    "indicators": ["character", "plot", "setting"]
                },
                "professional": {
                    "keywords": ["email", "letter", "report", "proposal", "memo"],
                    "phrases": ["business email", "formal letter", "professional writing"],
                    "indicators": ["professional", "formal", "business"]
                },
                "content": {
                    "keywords": ["blog", "article", "content", "post", "copy"],
                    "phrases": ["blog post", "article writing", "content creation"],
                    "indicators": ["seo", "engagement", "readers"]
                }
            }
        }
        
        # Stakeholder detection patterns
        self.stakeholder_patterns = [
            r"send to (\w+)",
            r"for my (\w+)",
            r"present to (\w+)",
            r"share with (\w+)",
            r"to my (\w+)",
            r"for the (\w+)"
        ]
        
        # Data context patterns
        self.data_context_patterns = {
            "has_data": [
                r"from this data",
                r"with this data",
                r"using this data",
                r"based on this data",
                r"here('s| is) the data",
                r"attached data",
                r"the following data",
                r"this dataset"
            ],
            "needs_data": [
                r"what data",
                r"which metrics",
                r"how to collect",
                r"what should I track"
            ]
        }
    
    def classify_intent(self, query: str) -> Dict:
        """
        Classify the intent of the user query
        Returns: {
            'primary_intent': str,
            'sub_intent': str,
            'confidence': float,
            'context': dict
        }
        """
        query_lower = query.lower()
        
        # Detect data context
        data_context = self._detect_data_context(query_lower)
        
        # Detect stakeholder
        stakeholder = self._detect_stakeholder(query_lower)
        
        # Score each sub-intent
        scores = {}
        for primary, sub_intents in self.intent_patterns.items():
            for sub_intent, patterns in sub_intents.items():
                score = self._calculate_intent_score(query_lower, patterns)
                scores[f"{primary}.{sub_intent}"] = score
        
        # Get top intent
        if scores:
            top_intent = max(scores.items(), key=lambda x: x[1])
            if top_intent[1] > 0:  # Only use if we have a positive score
                primary, sub = top_intent[0].split('.')
                confidence = min(top_intent[1] / 10.0, 1.0)  # Normalize to 0-1 range
            else:
                # Fallback to simple primary intent
                primary, sub = self._fallback_intent(query_lower)
                confidence = 0.5
        else:
            primary, sub = "general", "general"
            confidence = 0.3
        
        return {
            'primary_intent': primary,
            'sub_intent': sub,
            'confidence': confidence,
            'context': {
                'has_data': data_context['has_data'],
                'needs_data': data_context['needs_data'],
                'stakeholder': stakeholder,
                'query_length': len(query.split())
            }
        }
    
    def _fallback_intent(self, query: str) -> Tuple[str, str]:
        """Fallback to basic keyword matching for primary intent"""
        # Basic keyword sets for primary intents
        if any(word in query for word in ["code", "python", "script", "function", "app", "calculator", "api"]):
            return "coding", "application"
        if any(word in query for word in ["image", "photo", "picture", "logo", "design", "4k"]):
            return "image", "creative"
        if any(word in query for word in ["write", "story", "essay", "article", "blog"]):
            return "writing", "content"
        if any(word in query for word in ["marketing", "brand", "audience", "campaign", "ad"]):
            return "marketing", "strategy"
        return "general", "general"
    
    def _calculate_intent_score(self, query: str, patterns: Dict) -> float:
        """Calculate score for a specific intent based on keyword and phrase matching"""
        score = 0.0
        
        # Keyword matching (1 point each)
        for keyword in patterns.get('keywords', []):
            if keyword in query:
                score += 1.0
        
        # Phrase matching (3 points each - more weight)
        for phrase in patterns.get('phrases', []):
            if phrase in query:
                score += 3.0
        
        # Indicator matching (2 points each)
        for indicator in patterns.get('indicators', []):
            if indicator in query:
                score += 2.0
        
        return score
    
    def _detect_data_context(self, query: str) -> Dict:
        """Detect if user has data or needs data"""
        has_data = any(re.search(pattern, query) for pattern in self.data_context_patterns['has_data'])
        needs_data = any(re.search(pattern, query) for pattern in self.data_context_patterns['needs_data'])
        
        return {
            'has_data': has_data,
            'needs_data': needs_data
        }
    
    def _detect_stakeholder(self, query: str) -> Optional[str]:
        """Detect stakeholder mentioned in query"""
        for pattern in self.stakeholder_patterns:
            match = re.search(pattern, query)
            if match:
                return match.group(1)
        return None


# Example usage and testing
if __name__ == "__main__":
    classifier = IntentClassifier()
    
    # Test cases
    test_queries = [
        "create a report from this data for meta ads so I can send it to my manager",
        "what's the best marketing strategy for launching a new product",
        "who should be my target audience for fitness supplements",
        "how do I optimize my facebook ad campaign to reduce CPA",
        "analyze the performance metrics from last month's campaign",
        "build a calculator app with React",
        "create a photorealistic image of a sunset over mountains"
    ]
    
    print("Intent Classification Results:\n")
    for query in test_queries:
        result = classifier.classify_intent(query)
        print(f"Query: {query}")
        print(f"Primary Intent: {result['primary_intent']}")
        print(f"Sub Intent: {result['sub_intent']}")
        print(f"Confidence Score: {result['confidence']:.2f}")
        print(f"Has Data: {result['context']['has_data']}")
        print(f"Stakeholder: {result['context']['stakeholder']}")
        print("-" * 80)
