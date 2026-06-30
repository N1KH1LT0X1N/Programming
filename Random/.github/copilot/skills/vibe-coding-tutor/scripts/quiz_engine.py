"""
Quiz Engine for Vibe Coding Tutor
Generates pedagogically-sound MCQs following the 4-option pattern.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class DecisionType(Enum):
    """Types of design decisions that trigger MCQs."""
    VALIDATION = "validation"
    ERROR_HANDLING = "error_handling"
    PERFORMANCE = "performance"
    INPUT_TYPE = "input_type"
    OUTPUT_FORMAT = "output_format"
    DEPENDENCY = "dependency"
    ARCHITECTURE = "architecture"
    SECURITY = "security"


class OptionRole(Enum):
    """Role of each MCQ option in the 4-option pattern."""
    BEST_PRACTICE = "best_practice"      # Option A: Industry standard
    NAIVE_MISTAKE = "naive_mistake"       # Option B: Common beginner error
    TRADEOFF = "tradeoff"                 # Option C: Valid but has costs
    CUSTOM = "custom"                     # Option D: Let user specify


@dataclass
class MCQOption:
    """A single MCQ answer option."""
    letter: str           # A, B, C, D
    text: str             # The option text
    role: OptionRole      # Purpose in the pattern
    explanation: str      # Why this is right/wrong
    is_correct: bool      # Whether this is the best answer


@dataclass
class MCQ:
    """A complete Multiple Choice Question."""
    number: int
    topic: str            # Knowledge component tag
    decision_type: DecisionType
    question: str
    options: List[MCQOption]
    correct_index: int    # 0-3 (A-D)
    difficulty: int       # 800-1600 Elo scale
    
    def get_option_texts(self) -> List[str]:
        """Return just the option texts for display."""
        return [opt.text for opt in self.options]
    
    def get_correct_letter(self) -> str:
        """Return the correct answer letter."""
        return chr(65 + self.correct_index)
    
    def validate_answer(self, answer: str) -> tuple[bool, str]:
        """
        Validate user's answer and return feedback.
        
        Args:
            answer: User's answer (A, B, C, D)
            
        Returns:
            Tuple of (is_correct, feedback_text)
        """
        answer_upper = answer.upper().strip()
        if answer_upper not in ["A", "B", "C", "D"]:
            return False, "Please select A, B, C, or D."
        
        answer_index = ord(answer_upper) - 65
        selected_option = self.options[answer_index]
        correct_option = self.options[self.correct_index]
        
        if selected_option.is_correct:
            return True, selected_option.explanation
        else:
            # Provide both why their choice was wrong and why the correct one is right
            feedback = f"{selected_option.explanation} The better choice is {correct_option.letter}: {correct_option.explanation}"
            return False, feedback


@dataclass
class DecisionPoint:
    """A design decision that needs an MCQ."""
    name: str
    decision_type: DecisionType
    context: str          # What the user is trying to build
    constraints: List[str] = field(default_factory=list)


class QuizEngine:
    """
    Generates MCQs for design decisions.
    
    Follows the 4-option pattern:
    - A: Best practice (usually correct)
    - B: Naive mistake (targets common misconception)
    - C: Tradeoff (valid but has costs)
    - D: Custom (let user specify)
    """
    
    # MCQ templates organized by decision type
    MCQ_TEMPLATES: Dict[DecisionType, Dict[str, Any]] = {
        DecisionType.VALIDATION: {
            "question_template": "How strict should the {context} validation be?",
            "options": {
                OptionRole.BEST_PRACTICE: "Use industry-standard validation (comprehensive)",
                OptionRole.NAIVE_MISTAKE: "Basic check only (quick but incomplete)",
                OptionRole.TRADEOFF: "Use a third-party library (adds dependency)",
                OptionRole.CUSTOM: "Custom validation (let me specify rules)",
            },
            "explanations": {
                OptionRole.BEST_PRACTICE: "Industry-standard validation catches edge cases and follows established patterns.",
                OptionRole.NAIVE_MISTAKE: "Basic checks often miss edge cases and can lead to security vulnerabilities.",
                OptionRole.TRADEOFF: "Libraries provide robust validation but add external dependencies to manage.",
                OptionRole.CUSTOM: "Custom rules give full control but require careful implementation.",
            },
            "correct_role": OptionRole.BEST_PRACTICE,
            "difficulty": 1100,
        },
        DecisionType.ERROR_HANDLING: {
            "question_template": "How should errors be handled in {context}?",
            "options": {
                OptionRole.BEST_PRACTICE: "Raise specific exceptions with clear messages",
                OptionRole.NAIVE_MISTAKE: "Return None or False on error",
                OptionRole.TRADEOFF: "Log errors and continue silently",
                OptionRole.CUSTOM: "Custom error handling (let me specify)",
            },
            "explanations": {
                OptionRole.BEST_PRACTICE: "Specific exceptions make debugging easier and force callers to handle errors explicitly.",
                OptionRole.NAIVE_MISTAKE: "Returning None hides errors and can cause subtle bugs downstream.",
                OptionRole.TRADEOFF: "Silent logging keeps the system running but may mask important issues.",
                OptionRole.CUSTOM: "Custom handling can be tailored to your specific needs.",
            },
            "correct_role": OptionRole.BEST_PRACTICE,
            "difficulty": 1200,
        },
        DecisionType.PERFORMANCE: {
            "question_template": "What performance characteristics are needed for {context}?",
            "options": {
                OptionRole.BEST_PRACTICE: "Optimize for readability first, profile later",
                OptionRole.NAIVE_MISTAKE: "Optimize everything upfront",
                OptionRole.TRADEOFF: "Use caching (adds complexity but speeds up)",
                OptionRole.CUSTOM: "Custom performance requirements (let me specify)",
            },
            "explanations": {
                OptionRole.BEST_PRACTICE: "Premature optimization is the root of all evil. Write clean code first, then profile.",
                OptionRole.NAIVE_MISTAKE: "Over-optimizing early wastes time and often optimizes the wrong things.",
                OptionRole.TRADEOFF: "Caching improves speed but adds state management complexity.",
                OptionRole.CUSTOM: "Specific requirements may need targeted optimization strategies.",
            },
            "correct_role": OptionRole.BEST_PRACTICE,
            "difficulty": 1300,
        },
        DecisionType.INPUT_TYPE: {
            "question_template": "What input types should {context} accept?",
            "options": {
                OptionRole.BEST_PRACTICE: "Use type hints with runtime validation",
                OptionRole.NAIVE_MISTAKE: "Accept any input, handle errors later",
                OptionRole.TRADEOFF: "Use strict typing (safer but less flexible)",
                OptionRole.CUSTOM: "Custom input handling (let me specify)",
            },
            "explanations": {
                OptionRole.BEST_PRACTICE: "Type hints document intent and runtime validation catches errors early.",
                OptionRole.NAIVE_MISTAKE: "Accepting any input leads to hard-to-debug type errors at runtime.",
                OptionRole.TRADEOFF: "Strict typing prevents errors but may require more boilerplate.",
                OptionRole.CUSTOM: "Custom handling for specific data formats or protocols.",
            },
            "correct_role": OptionRole.BEST_PRACTICE,
            "difficulty": 1000,
        },
        DecisionType.OUTPUT_FORMAT: {
            "question_template": "What should {context} return?",
            "options": {
                OptionRole.BEST_PRACTICE: "Return a well-defined type with clear semantics",
                OptionRole.NAIVE_MISTAKE: "Return different types depending on success/failure",
                OptionRole.TRADEOFF: "Return a tuple with multiple values",
                OptionRole.CUSTOM: "Custom return format (let me specify)",
            },
            "explanations": {
                OptionRole.BEST_PRACTICE: "Consistent return types make code predictable and easier to use.",
                OptionRole.NAIVE_MISTAKE: "Mixed return types force callers to check types, leading to bugs.",
                OptionRole.TRADEOFF: "Tuples work but can be unclear without good documentation.",
                OptionRole.CUSTOM: "Custom formats for specific API requirements.",
            },
            "correct_role": OptionRole.BEST_PRACTICE,
            "difficulty": 1100,
        },
        DecisionType.DEPENDENCY: {
            "question_template": "Should {context} use external dependencies?",
            "options": {
                OptionRole.BEST_PRACTICE: "Use well-maintained libraries for complex tasks",
                OptionRole.NAIVE_MISTAKE: "Implement everything from scratch",
                OptionRole.TRADEOFF: "Vendor/copy the specific code needed",
                OptionRole.CUSTOM: "Custom dependency strategy (let me specify)",
            },
            "explanations": {
                OptionRole.BEST_PRACTICE: "Quality libraries are tested, maintained, and save development time.",
                OptionRole.NAIVE_MISTAKE: "Reinventing the wheel introduces bugs and wastes time.",
                OptionRole.TRADEOFF: "Vendoring avoids dependency management but misses security updates.",
                OptionRole.CUSTOM: "Specific requirements may need a tailored approach.",
            },
            "correct_role": OptionRole.BEST_PRACTICE,
            "difficulty": 1200,
        },
        DecisionType.ARCHITECTURE: {
            "question_template": "How should {context} be structured?",
            "options": {
                OptionRole.BEST_PRACTICE: "Follow established patterns (MVC, layered, etc.)",
                OptionRole.NAIVE_MISTAKE: "Put everything in one file/function",
                OptionRole.TRADEOFF: "Microservices approach (flexible but complex)",
                OptionRole.CUSTOM: "Custom architecture (let me specify)",
            },
            "explanations": {
                OptionRole.BEST_PRACTICE: "Established patterns are well-understood and make code maintainable.",
                OptionRole.NAIVE_MISTAKE: "Monolithic code becomes unmaintainable and hard to test.",
                OptionRole.TRADEOFF: "Microservices add deployment complexity but improve scalability.",
                OptionRole.CUSTOM: "Specific constraints may require a unique architecture.",
            },
            "correct_role": OptionRole.BEST_PRACTICE,
            "difficulty": 1400,
        },
        DecisionType.SECURITY: {
            "question_template": "How should {context} handle security?",
            "options": {
                OptionRole.BEST_PRACTICE: "Follow OWASP guidelines and validate all inputs",
                OptionRole.NAIVE_MISTAKE: "Trust user input, sanitize on output",
                OptionRole.TRADEOFF: "Use a security library (adds dependency)",
                OptionRole.CUSTOM: "Custom security requirements (let me specify)",
            },
            "explanations": {
                OptionRole.BEST_PRACTICE: "OWASP provides battle-tested security practices. Always validate inputs.",
                OptionRole.NAIVE_MISTAKE: "Trusting user input is the #1 cause of security vulnerabilities.",
                OptionRole.TRADEOFF: "Security libraries handle edge cases but require updates.",
                OptionRole.CUSTOM: "Specific compliance requirements may need custom handling.",
            },
            "correct_role": OptionRole.BEST_PRACTICE,
            "difficulty": 1500,
        },
    }
    
    def __init__(self):
        self.mcq_counter = 0
    
    def extract_decision_points(self, user_request: str) -> List[DecisionPoint]:
        """
        Analyze user request and extract design decisions.
        
        Args:
            user_request: The user's coding request
            
        Returns:
            List of decision points that need MCQs
        """
        decision_points = []
        request_lower = user_request.lower()
        
        # Keyword-based extraction (can be enhanced with LLM)
        keyword_mapping = {
            DecisionType.VALIDATION: ["validate", "check", "verify", "format", "email", "phone", "url"],
            DecisionType.ERROR_HANDLING: ["error", "exception", "handle", "fail", "invalid"],
            DecisionType.INPUT_TYPE: ["input", "parameter", "argument", "accept", "take"],
            DecisionType.OUTPUT_FORMAT: ["return", "output", "result", "format"],
            DecisionType.DEPENDENCY: ["library", "package", "import", "use", "install"],
            DecisionType.PERFORMANCE: ["fast", "performance", "optimize", "cache", "speed"],
            DecisionType.ARCHITECTURE: ["structure", "design", "pattern", "organize", "project"],
            DecisionType.SECURITY: ["security", "auth", "password", "encrypt", "token"],
        }
        
        # Always include these for any code request
        base_decisions = [DecisionType.ERROR_HANDLING, DecisionType.INPUT_TYPE]
        
        detected_types = set(base_decisions)
        
        for decision_type, keywords in keyword_mapping.items():
            for keyword in keywords:
                if keyword in request_lower:
                    detected_types.add(decision_type)
                    break
        
        # Create decision points
        for decision_type in detected_types:
            decision_points.append(DecisionPoint(
                name=decision_type.value.replace("_", " ").title(),
                decision_type=decision_type,
                context=user_request
            ))
        
        return decision_points[:4]  # Limit to 4 MCQs as per PRD
    
    def generate_mcq(
        self,
        decision_point: DecisionPoint,
        user_elo: int = 1200
    ) -> MCQ:
        """
        Generate an MCQ for a decision point.
        
        Args:
            decision_point: The decision that needs an MCQ
            user_elo: User's current Elo rating for difficulty adjustment
            
        Returns:
            A complete MCQ object
        """
        self.mcq_counter += 1
        
        template = self.MCQ_TEMPLATES.get(
            decision_point.decision_type,
            self.MCQ_TEMPLATES[DecisionType.VALIDATION]  # Default fallback
        )
        
        # Format question with context
        context_short = decision_point.context[:50] + "..." if len(decision_point.context) > 50 else decision_point.context
        question = template["question_template"].format(context=context_short)
        
        # Build options in order: A, B, C, D
        role_order = [
            OptionRole.BEST_PRACTICE,
            OptionRole.NAIVE_MISTAKE,
            OptionRole.TRADEOFF,
            OptionRole.CUSTOM
        ]
        
        options = []
        for i, role in enumerate(role_order):
            letter = chr(65 + i)
            is_correct = role == template["correct_role"]
            options.append(MCQOption(
                letter=letter,
                text=template["options"][role],
                role=role,
                explanation=template["explanations"][role],
                is_correct=is_correct
            ))
        
        # Find correct index
        correct_index = role_order.index(template["correct_role"])
        
        # Adjust difficulty based on user Elo (keep within bounds)
        base_difficulty = template["difficulty"]
        adjusted_difficulty = max(800, min(1600, base_difficulty + (user_elo - 1200) // 4))
        
        return MCQ(
            number=self.mcq_counter,
            topic=decision_point.decision_type.value,
            decision_type=decision_point.decision_type,
            question=question,
            options=options,
            correct_index=correct_index,
            difficulty=adjusted_difficulty
        )
    
    def generate_reinforcement_mcq(
        self,
        code_context: str,
        knowledge_tag: str,
        user_elo: int = 1200
    ) -> MCQ:
        """
        Generate a reinforcement MCQ after code is delivered.
        
        Args:
            code_context: The code that was generated
            knowledge_tag: Topic to reinforce
            user_elo: User's Elo for difficulty
            
        Returns:
            An MCQ testing understanding of the generated code
        """
        self.mcq_counter += 1
        
        # Simplified reinforcement question
        question = f"Why did we choose this approach for {knowledge_tag.replace('_', ' ')}?"
        
        options = [
            MCQOption("A", "It follows best practices and handles edge cases", OptionRole.BEST_PRACTICE, "Correct! Best practices exist because they've been tested in production.", True),
            MCQOption("B", "It was the easiest to implement", OptionRole.NAIVE_MISTAKE, "Ease of implementation shouldn't be the primary factor for design decisions.", False),
            MCQOption("C", "It was a tradeoff based on our constraints", OptionRole.TRADEOFF, "While tradeoffs are valid, we specifically chose best practices here.", False),
            MCQOption("D", "I'm not sure, please explain", OptionRole.CUSTOM, "That's okay! Review the decision in .vibe/findings.md for more context.", False),
        ]
        
        return MCQ(
            number=self.mcq_counter,
            topic=knowledge_tag,
            decision_type=DecisionType.ARCHITECTURE,
            question=question,
            options=options,
            correct_index=0,
            difficulty=user_elo
        )
    
    def reset_counter(self) -> None:
        """Reset MCQ counter for a new session."""
        self.mcq_counter = 0
