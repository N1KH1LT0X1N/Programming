"""
Feedback Generator for Vibe Coding Tutor
Provides immediate, explanatory feedback after MCQ answers.
"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class FeedbackType(Enum):
    """Type of feedback to provide."""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIAL = "partial"
    TEACHING = "teaching"


@dataclass
class Feedback:
    """
    Complete feedback for an MCQ answer.
    
    Follows research-based patterns:
    - Explanatory over corrective
    - Scaffolded for incorrect answers
    - Actionable next steps
    """
    feedback_type: FeedbackType
    is_correct: bool
    
    # Why the correct answer is correct
    why_correct: str
    
    # Why their chosen answer was right/wrong (if different from correct)
    why_chosen: Optional[str]
    
    # Concrete next step
    next_step: str
    
    # Optional link to documentation
    remediation_link: Optional[str]
    
    # Bridge question for wrong answers (scaffolded learning)
    bridge_question: Optional[str]
    
    def format_for_user(self) -> str:
        """Format feedback for display to user."""
        if self.is_correct:
            lines = [
                f"✅ **Correct!** {self.why_correct}",
                "",
                f"💡 **Next step**: {self.next_step}"
            ]
        else:
            lines = [
                f"❌ **Not quite.** {self.why_chosen}",
                "",
                f"✓ **Better choice**: {self.why_correct}",
            ]
            
            if self.bridge_question:
                lines.extend([
                    "",
                    f"🤔 **Think about it**: {self.bridge_question}"
                ])
            
            lines.extend([
                "",
                f"💡 **Next step**: {self.next_step}"
            ])
        
        if self.remediation_link:
            lines.append(f"📚 **Learn more**: {self.remediation_link}")
        
        return "\n".join(lines)


class FeedbackGenerator:
    """
    Generates pedagogically-sound feedback for MCQ answers.
    
    Design principles:
    1. Explanatory over corrective (explain WHY)
    2. Scaffolded feedback (bridge questions for wrong answers)
    3. Actionable remediation (concrete next steps)
    """
    
    # Bridge questions for common misconceptions
    BRIDGE_QUESTIONS = {
        "validation": "What could go wrong if we only check for the most obvious cases?",
        "error_handling": "How would a caller know something went wrong if we return None?",
        "performance": "Is it better to spend 2 hours optimizing code that runs once, or 2 hours writing clear code?",
        "input_type": "What happens when unexpected data types reach your function?",
        "output_format": "How easy would it be to use this function if it returned different types?",
        "dependency": "How much time would it take to implement this from scratch vs using a library?",
        "architecture": "How would a new team member understand this code?",
        "security": "What could a malicious user do with unrestricted input?",
    }
    
    # Next step suggestions by topic
    NEXT_STEPS = {
        "validation": "Implement validation with comprehensive test cases for edge cases.",
        "error_handling": "Define specific exception classes for different error scenarios.",
        "performance": "Write clean, readable code first. Profile if performance becomes an issue.",
        "input_type": "Add type hints and consider using a validation library like Pydantic.",
        "output_format": "Document the return type clearly in the docstring.",
        "dependency": "Check the library's maintenance status and security history.",
        "architecture": "Draw a simple diagram of how components interact.",
        "security": "Review OWASP guidelines for this type of functionality.",
    }
    
    # Documentation links by topic
    DOCS_LINKS = {
        "validation": "https://docs.python.org/3/library/re.html",
        "error_handling": "https://docs.python.org/3/tutorial/errors.html",
        "performance": "https://docs.python.org/3/library/profile.html",
        "input_type": "https://docs.python.org/3/library/typing.html",
        "security": "https://owasp.org/www-project-top-ten/",
    }
    
    def generate_feedback(
        self,
        topic: str,
        user_answer: str,
        correct_answer: str,
        user_explanation: str,
        correct_explanation: str,
        user_level: str = "beginner"
    ) -> Feedback:
        """
        Generate comprehensive feedback for an MCQ answer.
        
        Args:
            topic: Knowledge component tag
            user_answer: User's selected option (A, B, C, D)
            correct_answer: Correct option letter
            user_explanation: Why user's choice is good/bad
            correct_explanation: Why correct choice is best
            user_level: User's skill level for tailored feedback
            
        Returns:
            Complete Feedback object
        """
        is_correct = user_answer.upper() == correct_answer.upper()
        
        if is_correct:
            return self._generate_correct_feedback(
                topic=topic,
                explanation=correct_explanation,
                user_level=user_level
            )
        else:
            return self._generate_incorrect_feedback(
                topic=topic,
                why_chosen=user_explanation,
                why_correct=correct_explanation,
                user_level=user_level
            )
    
    def _generate_correct_feedback(
        self,
        topic: str,
        explanation: str,
        user_level: str
    ) -> Feedback:
        """Generate feedback for correct answer."""
        next_step = self.NEXT_STEPS.get(topic, "Proceed to the next decision point.")
        
        # Beginners get more encouragement
        if user_level == "beginner":
            why = f"{explanation} Great job recognizing the best practice!"
        else:
            why = explanation
        
        return Feedback(
            feedback_type=FeedbackType.CORRECT,
            is_correct=True,
            why_correct=why,
            why_chosen=None,
            next_step=next_step,
            remediation_link=None,
            bridge_question=None
        )
    
    def _generate_incorrect_feedback(
        self,
        topic: str,
        why_chosen: str,
        why_correct: str,
        user_level: str
    ) -> Feedback:
        """Generate scaffolded feedback for incorrect answer."""
        next_step = self.NEXT_STEPS.get(topic, "Review the explanation and try to understand why.")
        bridge = self.BRIDGE_QUESTIONS.get(topic)
        docs_link = self.DOCS_LINKS.get(topic)
        
        # Beginners get gentler feedback
        if user_level == "beginner":
            why_chosen_formatted = f"This is a common choice, but: {why_chosen}"
        else:
            why_chosen_formatted = why_chosen
        
        return Feedback(
            feedback_type=FeedbackType.INCORRECT,
            is_correct=False,
            why_correct=why_correct,
            why_chosen=why_chosen_formatted,
            next_step=next_step,
            remediation_link=docs_link,
            bridge_question=bridge
        )
    
    def generate_teaching_explanation(
        self,
        topic: str,
        context: str
    ) -> str:
        """
        Generate a teaching explanation before asking MCQ.
        Used when user mastery is too low (Teaching Mode).
        
        Args:
            topic: Knowledge component to explain
            context: What the user is trying to build
            
        Returns:
            Teaching explanation text
        """
        explanations = {
            "validation": """
**Validation** is about checking that inputs meet your requirements before processing them.

Key concepts:
- **Input validation**: Check data at the boundary (when it enters your system)
- **Types**: Format checks, range checks, business rule checks
- **Fail fast**: Reject bad data early with clear error messages

For your task, we need to decide *how strict* the validation should be.
""",
            "error_handling": """
**Error Handling** determines how your code responds when something goes wrong.

Key concepts:
- **Exceptions**: Raise specific errors with clear messages
- **Return values**: Some prefer returning error codes or None
- **Logging**: Record errors for debugging

Good error handling makes debugging 10x easier for you and your team.
""",
            "input_type": """
**Input Types** define what data your function accepts.

Key concepts:
- **Type hints**: Document expected types (`def foo(x: int) -> str`)
- **Duck typing**: Python doesn't enforce types, but hints help
- **Runtime validation**: Check types at runtime for safety

Choosing the right input types makes your code more predictable.
""",
            "output_format": """
**Output Format** defines what your function returns.

Key concepts:
- **Consistency**: Always return the same type
- **Semantics**: Return value should clearly indicate success/failure
- **Documentation**: Docstrings should explain return values

Consistent return types make your functions easier to use.
""",
            "performance": """
**Performance** is about how fast and efficiently your code runs.

Key concepts:
- **YAGNI**: You Ain't Gonna Need It - don't optimize prematurely
- **Profile first**: Measure before optimizing
- **Big-O**: Understand algorithmic complexity

Write readable code first, then optimize the bottlenecks.
""",
            "dependency": """
**Dependencies** are external libraries your code relies on.

Key concepts:
- **Tradeoffs**: Libraries save time but add maintenance burden
- **Security**: Dependencies can have vulnerabilities
- **Vendoring**: Copying code vs installing packages

Choose well-maintained libraries with good security track records.
""",
            "security": """
**Security** protects your application from malicious users.

Key concepts:
- **Never trust user input**: Always validate and sanitize
- **OWASP Top 10**: Common vulnerabilities to avoid
- **Defense in depth**: Multiple layers of protection

Security is not optional - build it in from the start.
""",
            "architecture": """
**Architecture** is how you organize and structure your code.

Key concepts:
- **Separation of concerns**: Each module does one thing well
- **Patterns**: MVC, layered architecture, etc.
- **Maintainability**: Can others understand and modify this?

Good architecture makes your code easier to test and change.
""",
        }
        
        base = explanations.get(topic, f"Let me explain **{topic.replace('_', ' ')}**...")
        
        return f"""
Before we decide, let me explain this concept:

{base}

Now, let's choose the best approach for **{context}**.
"""
    
    def generate_summary_confirmation(
        self,
        decisions: List[dict]
    ) -> str:
        """
        Generate a summary for user confirmation before coding.
        
        Args:
            decisions: List of {decision, choice, rationale} dicts
            
        Returns:
            Formatted summary text
        """
        lines = ["## Summary of Your Choices\n"]
        
        for i, d in enumerate(decisions, 1):
            lines.append(f"**{i}. {d['decision']}**: {d['choice']}")
            lines.append(f"   *Rationale*: {d['rationale']}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append("**Ready to implement with these decisions?** (yes/no)")
        
        return "\n".join(lines)
    
    def generate_reinforcement_intro(self) -> str:
        """Generate intro text for reinforcement MCQs."""
        return """
## 📚 Reinforcement Check

Now that the code is complete, let's make sure you understand the key decisions.
These questions help reinforce what we learned:
"""
    
    def generate_completion_message(
        self,
        goal: str,
        decisions_count: int,
        accuracy: float
    ) -> str:
        """
        Generate completion message after successful session.
        
        Args:
            goal: Original user goal
            decisions_count: Number of decisions made
            accuracy: MCQ accuracy percentage
            
        Returns:
            Celebration/summary message
        """
        accuracy_pct = int(accuracy * 100)
        
        if accuracy_pct >= 80:
            emoji = "🌟"
            comment = "Excellent understanding!"
        elif accuracy_pct >= 60:
            emoji = "👍"
            comment = "Good progress!"
        else:
            emoji = "💪"
            comment = "Keep practicing!"
        
        return f"""
## {emoji} Session Complete!

**Goal**: {goal}
**Decisions Made**: {decisions_count}
**Accuracy**: {accuracy_pct}%

{comment}

Your progress has been saved to `.vibe/`. Next time you code, I'll remember what you've learned.
"""
