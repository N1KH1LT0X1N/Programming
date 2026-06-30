"""
Curriculum Tracker for Vibe Coding Tutor
Implements adaptive difficulty using Elo rating system.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import math


@dataclass
class KnowledgeComponent:
    """A single knowledge component (skill tag)."""
    name: str
    mastery: float          # 0.0 to 1.0
    last_seen: Optional[datetime]
    attempts: int
    correct: int
    
    @property
    def accuracy(self) -> float:
        """Calculate accuracy for this component."""
        if self.attempts == 0:
            return 0.5  # Neutral starting point
        return self.correct / self.attempts
    
    @property
    def days_since_seen(self) -> Optional[int]:
        """Days since last practice."""
        if self.last_seen is None:
            return None
        return (datetime.now() - self.last_seen).days


@dataclass 
class UserSkillModel:
    """Complete model of user's skill state."""
    elo_rating: int
    level: str              # beginner, intermediate, advanced
    knowledge_components: Dict[str, KnowledgeComponent]
    total_mcqs: int
    correct_answers: int
    incorrect_answers: int
    
    @property
    def overall_accuracy(self) -> float:
        """Overall accuracy across all MCQs."""
        if self.total_mcqs == 0:
            return 0.5
        return self.correct_answers / self.total_mcqs
    
    def get_weak_components(self, threshold: float = 0.5) -> List[KnowledgeComponent]:
        """Get components with mastery below threshold."""
        return [
            kc for kc in self.knowledge_components.values()
            if kc.mastery < threshold
        ]
    
    def get_stale_components(self, days: int = 7) -> List[KnowledgeComponent]:
        """Get components not practiced recently (for spaced repetition)."""
        stale = []
        for kc in self.knowledge_components.values():
            if kc.last_seen is not None:
                if kc.days_since_seen and kc.days_since_seen >= days:
                    stale.append(kc)
        return stale


class CurriculumTracker:
    """
    Tracks and adapts to user skill level.
    
    Uses Elo rating system for difficulty adjustment:
    - Users start at 1200 Elo
    - Questions have difficulty ratings (800-1600)
    - Answering correctly against hard questions = big Elo gain
    - Answering incorrectly against easy questions = big Elo loss
    """
    
    # Elo system constants
    K_FACTOR = 32           # Learning rate (higher = faster adaptation)
    INITIAL_ELO = 1200
    MIN_ELO = 800
    MAX_ELO = 1600
    
    # Level thresholds
    BEGINNER_MAX = 1000
    INTERMEDIATE_MAX = 1400
    
    # Question selection weights
    WEAK_WEIGHT = 0.70      # 70% from weak areas
    STALE_WEIGHT = 0.20     # 20% from stale topics (spaced repetition)
    EXPLORE_WEIGHT = 0.10   # 10% random exploration
    
    def __init__(self, user_profile: Optional[Dict] = None):
        """
        Initialize tracker with optional existing profile.
        
        Args:
            user_profile: Existing user_profile.json data
        """
        if user_profile:
            self.skill_model = self._load_from_profile(user_profile)
        else:
            self.skill_model = UserSkillModel(
                elo_rating=self.INITIAL_ELO,
                level="beginner",
                knowledge_components={},
                total_mcqs=0,
                correct_answers=0,
                incorrect_answers=0
            )
    
    def _load_from_profile(self, profile: Dict) -> UserSkillModel:
        """Load skill model from user_profile.json data."""
        kcs = {}
        for name, data in profile.get("knowledge_components", {}).items():
            last_seen = None
            if data.get("last_seen"):
                try:
                    last_seen = datetime.fromisoformat(data["last_seen"])
                except (ValueError, TypeError):
                    pass
            
            kcs[name] = KnowledgeComponent(
                name=name,
                mastery=data.get("mastery", 0.5),
                last_seen=last_seen,
                attempts=data.get("attempts", 0),
                correct=data.get("correct", 0)
            )
        
        history = profile.get("history", {})
        
        return UserSkillModel(
            elo_rating=profile.get("elo_rating", self.INITIAL_ELO),
            level=profile.get("level", "beginner"),
            knowledge_components=kcs,
            total_mcqs=history.get("total_mcqs", 0),
            correct_answers=history.get("correct", 0),
            incorrect_answers=history.get("incorrect", 0)
        )
    
    def calculate_elo_change(
        self,
        user_elo: int,
        question_difficulty: int,
        is_correct: bool
    ) -> int:
        """
        Calculate Elo change after answering a question.
        
        Args:
            user_elo: User's current Elo rating
            question_difficulty: Question's difficulty rating
            is_correct: Whether user answered correctly
            
        Returns:
            The change in Elo (positive or negative)
        """
        # Expected probability of correct answer
        expected = 1 / (1 + math.pow(10, (question_difficulty - user_elo) / 400))
        
        # Actual result
        actual = 1.0 if is_correct else 0.0
        
        # Elo change
        change = int(self.K_FACTOR * (actual - expected))
        
        return change
    
    def update_elo(
        self,
        question_difficulty: int,
        is_correct: bool
    ) -> Tuple[int, int]:
        """
        Update user's Elo after answering.
        
        Args:
            question_difficulty: Difficulty of the question
            is_correct: Whether user was correct
            
        Returns:
            Tuple of (new_elo, elo_change)
        """
        change = self.calculate_elo_change(
            self.skill_model.elo_rating,
            question_difficulty,
            is_correct
        )
        
        new_elo = self.skill_model.elo_rating + change
        
        # Clamp to bounds
        new_elo = max(self.MIN_ELO, min(self.MAX_ELO, new_elo))
        
        self.skill_model.elo_rating = new_elo
        
        # Update level
        if new_elo < self.BEGINNER_MAX:
            self.skill_model.level = "beginner"
        elif new_elo < self.INTERMEDIATE_MAX:
            self.skill_model.level = "intermediate"
        else:
            self.skill_model.level = "advanced"
        
        return new_elo, change
    
    def update_knowledge_component(
        self,
        tag: str,
        is_correct: bool
    ) -> float:
        """
        Update mastery for a knowledge component.
        
        Args:
            tag: Knowledge component tag (e.g., "validation")
            is_correct: Whether user answered correctly
            
        Returns:
            New mastery level (0.0 to 1.0)
        """
        if tag not in self.skill_model.knowledge_components:
            self.skill_model.knowledge_components[tag] = KnowledgeComponent(
                name=tag,
                mastery=0.5,
                last_seen=None,
                attempts=0,
                correct=0
            )
        
        kc = self.skill_model.knowledge_components[tag]
        kc.attempts += 1
        if is_correct:
            kc.correct += 1
        kc.last_seen = datetime.now()
        
        # Update mastery as accuracy
        kc.mastery = kc.correct / kc.attempts
        
        # Update total stats
        self.skill_model.total_mcqs += 1
        if is_correct:
            self.skill_model.correct_answers += 1
        else:
            self.skill_model.incorrect_answers += 1
        
        return kc.mastery
    
    def select_question_difficulty(self) -> int:
        """
        Select appropriate question difficulty for user.
        
        Returns:
            Difficulty rating (800-1600)
        """
        # Target slightly above user's level for learning
        target = self.skill_model.elo_rating + 50
        
        # Add some variance
        import random
        variance = random.randint(-100, 100)
        
        difficulty = target + variance
        
        # Clamp
        return max(self.MIN_ELO, min(self.MAX_ELO, difficulty))
    
    def select_knowledge_component(
        self,
        available_tags: List[str]
    ) -> str:
        """
        Select which knowledge component to focus on.
        
        Uses weighted selection:
        - 70% weak areas
        - 20% stale topics
        - 10% random exploration
        
        Args:
            available_tags: Tags relevant to current request
            
        Returns:
            Selected tag to focus on
        """
        import random
        
        if not available_tags:
            return "general"
        
        # Get weak and stale components that match available tags
        weak = [
            kc for kc in self.skill_model.get_weak_components()
            if kc.name in available_tags
        ]
        stale = [
            kc for kc in self.skill_model.get_stale_components()
            if kc.name in available_tags
        ]
        
        # Weighted random selection
        roll = random.random()
        
        if roll < self.WEAK_WEIGHT and weak:
            # Select from weak (prioritize lowest mastery)
            weak.sort(key=lambda kc: kc.mastery)
            return weak[0].name
        elif roll < self.WEAK_WEIGHT + self.STALE_WEIGHT and stale:
            # Select from stale (prioritize oldest)
            stale.sort(key=lambda kc: kc.days_since_seen or 0, reverse=True)
            return stale[0].name
        else:
            # Random exploration
            return random.choice(available_tags)
    
    def should_skip_mcqs(self) -> bool:
        """
        Check if user is advanced enough to skip MCQs (Express Mode).
        
        Returns:
            True if all relevant components have mastery > 0.8
        """
        if not self.skill_model.knowledge_components:
            return False
        
        high_mastery = all(
            kc.mastery > 0.8 
            for kc in self.skill_model.knowledge_components.values()
        )
        
        return high_mastery and self.skill_model.elo_rating > self.INTERMEDIATE_MAX
    
    def should_teach_first(self, tag: str) -> bool:
        """
        Check if user needs teaching before MCQ (Teaching Mode).
        
        Args:
            tag: Knowledge component being tested
            
        Returns:
            True if mastery < 0.2 for this tag
        """
        if tag not in self.skill_model.knowledge_components:
            # New topic, might need teaching
            return self.skill_model.elo_rating < self.BEGINNER_MAX
        
        return self.skill_model.knowledge_components[tag].mastery < 0.2
    
    def get_recommendation(self) -> str:
        """
        Get a learning recommendation for the user.
        
        Returns:
            Human-readable recommendation string
        """
        weak = self.skill_model.get_weak_components(threshold=0.4)
        stale = self.skill_model.get_stale_components(days=14)
        
        if weak:
            weak_names = ", ".join([kc.name.replace("_", " ") for kc in weak[:3]])
            return f"Focus on: {weak_names}"
        elif stale:
            stale_names = ", ".join([kc.name.replace("_", " ") for kc in stale[:3]])
            return f"Review: {stale_names} (not practiced recently)"
        else:
            return "Great progress! Keep practicing."
    
    def export_profile(self) -> Dict:
        """
        Export skill model to user_profile.json format.
        
        Returns:
            Dict suitable for JSON serialization
        """
        kcs = {}
        for name, kc in self.skill_model.knowledge_components.items():
            kcs[name] = {
                "mastery": round(kc.mastery, 3),
                "last_seen": kc.last_seen.isoformat() if kc.last_seen else None,
                "attempts": kc.attempts,
                "correct": kc.correct
            }
        
        return {
            "level": self.skill_model.level,
            "elo_rating": self.skill_model.elo_rating,
            "knowledge_components": kcs,
            "history": {
                "total_mcqs": self.skill_model.total_mcqs,
                "correct": self.skill_model.correct_answers,
                "incorrect": self.skill_model.incorrect_answers
            }
        }
