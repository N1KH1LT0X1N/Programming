"""
State Manager for Vibe Coding Tutor
Handles all .vibe/ folder read/write operations.
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any


@dataclass
class Decision:
    """A resolved design decision."""
    decision: str
    choice: str
    rationale: str
    mcq_number: int


@dataclass
class MCQLog:
    """A logged MCQ interaction."""
    number: int
    timestamp: str
    topic: str
    question: str
    options: List[str]
    user_answer: str
    is_correct: bool
    feedback: str
    elo_change: int


@dataclass
class UserProfile:
    """User skill profile with Elo rating."""
    level: str  # beginner, intermediate, advanced
    elo_rating: int
    knowledge_components: Dict[str, Dict[str, Any]]
    history: Dict[str, int]


@dataclass
class VibeContext:
    """Full context restored from .vibe/ files."""
    goal: str
    current_phase: str
    pending_decisions: List[str]
    resolved_decisions: List[Decision]
    recent_mcqs: List[MCQLog]
    user_profile: UserProfile
    has_pending_mcq: bool
    pending_mcq_topic: Optional[str]


class StateManager:
    """
    Manages the .vibe/ persistent state folder.
    
    Directory structure (V2):
    .vibe/
    ├── task_plan.md
    ├── findings.md
    ├── progress.md
    ├── user_profile.json
    ├── backups/
    ├── plans/              # NEW in V2: TDD implementation plans
    └── debug_sessions/     # NEW in V2: Systematic debugging logs
    """
    
    VIBE_DIR = ".vibe"
    BACKUP_DIR = "backups"
    PLANS_DIR = "plans"                    # V2: TDD implementation plans
    DEBUG_SESSIONS_DIR = "debug_sessions"  # V2: Debugging session logs
    
    # V2: Phase emojis for display
    PHASE_EMOJIS = {
        "Discovery": "🔍",
        "Vibe Check": "🎓",
        "Confirmation": "✅",
        "Planning": "📋",
        "Execution": "🛠️",
        "Verification": "✔️",
        "Debugging": "🔧",
        "Complete": "🎉"
    }
    
    def __init__(self, workspace_root: str):
        """
        Initialize with workspace root path.
        
        Args:
            workspace_root: Absolute path to the project root
        """
        self.workspace_root = Path(workspace_root)
        self.vibe_path = self.workspace_root / self.VIBE_DIR
        self.templates_path = Path(__file__).parent.parent / "templates"
    
    def exists(self) -> bool:
        """Check if .vibe/ folder exists."""
        return self.vibe_path.exists()
    
    def init_vibe_folder(self, goal: str) -> None:
        """
        Create .vibe/ folder and initialize all files from templates.
        
        Args:
            goal: User's original coding request
        """
        # Create directories
        self.vibe_path.mkdir(exist_ok=True)
        (self.vibe_path / self.BACKUP_DIR).mkdir(exist_ok=True)
        
        # Initialize task_plan.md
        task_plan = f"""# Task Plan

## Goal
{goal}

## Phases
- [x] 🔍 Discovery
- [ ] 🎓 Vibe Check
- [ ] ✅ Confirmation
- [ ] 🛠️ Implementation
- [ ] 📚 Reinforcement

## Current Phase
🎓 Vibe Check

## Status
10% Complete
"""
        self._write_file("task_plan.md", task_plan)
        
        # Initialize findings.md
        findings = f"""# Findings

## User Requirements
- Goal: {goal}

## Pending Decisions
- [ ] (To be identified during Vibe Check)

## Resolved Decisions
| Decision | Choice | Rationale | MCQ# |
|:---|:---|:---|:---|

## Constraints
- *none yet*

## ⚠️ Technical Debt
- *none yet*
"""
        self._write_file("findings.md", findings)
        
        # Initialize progress.md
        timestamp = datetime.now().isoformat()
        progress = f"""# Progress Log

## Session Started: {timestamp}

---
"""
        self._write_file("progress.md", progress)
        
        # Initialize user_profile.json
        profile = {
            "level": "beginner",
            "elo_rating": 1200,
            "knowledge_components": {},
            "history": {
                "total_mcqs": 0,
                "correct": 0,
                "incorrect": 0
            }
        }
        self._write_json("user_profile.json", profile)
    
    def read_context(self) -> VibeContext:
        """
        Read and parse all .vibe/ files to restore context.
        
        Returns:
            VibeContext with all restored state
        """
        # Read task_plan.md
        task_plan = self._read_file("task_plan.md")
        goal = self._extract_goal(task_plan)
        current_phase = self._extract_current_phase(task_plan)
        
        # Read findings.md
        findings = self._read_file("findings.md")
        pending_decisions = self._extract_pending_decisions(findings)
        resolved_decisions = self._extract_resolved_decisions(findings)
        
        # Read last 20 lines of progress.md
        progress = self._read_file("progress.md")
        recent_mcqs = self._extract_recent_mcqs(progress)
        has_pending, pending_topic = self._check_pending_mcq(progress)
        
        # Read user_profile.json
        profile_data = self._read_json("user_profile.json")
        user_profile = UserProfile(
            level=profile_data.get("level", "beginner"),
            elo_rating=profile_data.get("elo_rating", 1200),
            knowledge_components=profile_data.get("knowledge_components", {}),
            history=profile_data.get("history", {"total_mcqs": 0, "correct": 0, "incorrect": 0})
        )
        
        return VibeContext(
            goal=goal,
            current_phase=current_phase,
            pending_decisions=pending_decisions,
            resolved_decisions=resolved_decisions,
            recent_mcqs=recent_mcqs,
            user_profile=user_profile,
            has_pending_mcq=has_pending,
            pending_mcq_topic=pending_topic
        )
    
    def log_mcq(
        self,
        mcq_number: int,
        topic: str,
        question: str,
        options: List[str],
        user_answer: str,
        correct_index: int,
        feedback: str,
        elo_change: int
    ) -> None:
        """
        Append MCQ interaction to progress.md.
        
        Args:
            mcq_number: Sequential MCQ number
            topic: Knowledge component tag
            question: The question text
            options: List of 4 options (A, B, C, D)
            user_answer: User's selected option letter
            correct_index: Index of correct answer (0-3)
            feedback: Explanation text
            elo_change: Points gained/lost
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        correct_letter = chr(65 + correct_index)  # 0->A, 1->B, etc.
        is_correct = user_answer.upper() == correct_letter
        
        # Format options with checkmark on correct answer
        formatted_options = []
        for i, opt in enumerate(options):
            letter = chr(65 + i)
            mark = " ✓" if i == correct_index else ""
            formatted_options.append(f"- {letter}) {opt}{mark}")
        
        result_emoji = "✅" if is_correct else "❌"
        
        entry = f"""
### MCQ #{mcq_number} — {timestamp}
**Topic**: {topic}
**Question**: {question}
{chr(10).join(formatted_options)}

**User Answer**: {user_answer.upper()} {result_emoji}
**Feedback**: {feedback}
**Elo Change**: {'+' if elo_change >= 0 else ''}{elo_change}

---
"""
        self._append_file("progress.md", entry)
    
    def update_finding(self, decision: str, choice: str, rationale: str, mcq_number: int) -> None:
        """
        Move a decision from Pending to Resolved in findings.md.
        
        Args:
            decision: The decision point name
            choice: What the user chose
            rationale: Why this choice was made
            mcq_number: Associated MCQ number
        """
        findings = self._read_file("findings.md")
        
        # Remove from pending (if exists)
        pending_marker = f"- [ ] {decision}"
        findings = findings.replace(pending_marker, "")
        
        # Add to resolved table
        new_row = f"| {decision} | {choice} | {rationale} | #{mcq_number} |"
        
        # Find the table and add row
        lines = findings.split("\n")
        new_lines = []
        table_found = False
        
        for line in lines:
            new_lines.append(line)
            if "|:---|:---|:---|:---|" in line and not table_found:
                new_lines.append(new_row)
                table_found = True
        
        self._write_file("findings.md", "\n".join(new_lines))
    
    def add_pending_decision(self, decision: str) -> None:
        """Add a new pending decision to findings.md."""
        findings = self._read_file("findings.md")
        
        # Find "## Pending Decisions" section and add
        marker = "## Pending Decisions"
        if marker in findings:
            parts = findings.split(marker)
            parts[1] = f"\n- [ ] {decision}" + parts[1]
            findings = marker.join(parts)
            self._write_file("findings.md", findings)
    
    def update_user_profile(
        self,
        new_elo: int,
        knowledge_tag: str,
        is_correct: bool
    ) -> None:
        """
        Update user profile with new Elo and mastery scores.
        
        Args:
            new_elo: Updated Elo rating
            knowledge_tag: Knowledge component that was tested
            is_correct: Whether user answered correctly
        """
        profile = self._read_json("user_profile.json")
        
        # Update Elo
        profile["elo_rating"] = new_elo
        
        # Update history
        profile["history"]["total_mcqs"] += 1
        if is_correct:
            profile["history"]["correct"] += 1
        else:
            profile["history"]["incorrect"] += 1
        
        # Update knowledge component mastery
        if knowledge_tag not in profile["knowledge_components"]:
            profile["knowledge_components"][knowledge_tag] = {
                "mastery": 0.5,
                "last_seen": None,
                "attempts": 0,
                "correct": 0
            }
        
        kc = profile["knowledge_components"][knowledge_tag]
        kc["attempts"] += 1
        if is_correct:
            kc["correct"] += 1
        kc["mastery"] = kc["correct"] / kc["attempts"]
        kc["last_seen"] = datetime.now().isoformat()
        
        # Update level based on Elo
        if profile["elo_rating"] < 1000:
            profile["level"] = "beginner"
        elif profile["elo_rating"] < 1400:
            profile["level"] = "intermediate"
        else:
            profile["level"] = "advanced"
        
        self._write_json("user_profile.json", profile)
    
    def update_phase(self, phase: str, progress_percent: int) -> None:
        """Update current phase in task_plan.md."""
        task_plan = self._read_file("task_plan.md")
        
        # Update current phase
        lines = task_plan.split("\n")
        new_lines = []
        for i, line in enumerate(lines):
            if line.startswith("## Current Phase"):
                new_lines.append(line)
                new_lines.append(phase)
                # Skip the old phase line
                continue
            elif line.startswith("## Status"):
                new_lines.append(line)
                new_lines.append(f"{progress_percent}% Complete")
                continue
            new_lines.append(line)
        
        self._write_file("task_plan.md", "\n".join(new_lines))
    
    def log_safety_override(self) -> None:
        """Log when user bypasses Vibe Check."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add to progress.md
        entry = f"""
### ⚠️ SAFETY_OVERRIDE — {timestamp}
User requested immediate code generation, bypassing Vibe Check protocol.

---
"""
        self._append_file("progress.md", entry)
        
        # Add technical debt warning to findings.md
        findings = self._read_file("findings.md")
        debt_section = "## ⚠️ Technical Debt"
        if debt_section in findings:
            findings = findings.replace(
                f"{debt_section}\n- *none yet*",
                f"{debt_section}\n- [{timestamp}] Code generated without full Vibe Check"
            )
            self._write_file("findings.md", findings)
    
    def backup(self) -> str:
        """
        Create a backup of all .vibe/ files.
        
        Returns:
            Path to the backup folder
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.vibe_path / self.BACKUP_DIR / timestamp
        backup_path.mkdir(parents=True, exist_ok=True)
        
        for file in ["task_plan.md", "findings.md", "progress.md", "user_profile.json"]:
            src = self.vibe_path / file
            if src.exists():
                shutil.copy2(src, backup_path / file)
        
        return str(backup_path)
    
    def restore_from_backup(self, backup_name: str) -> bool:
        """
        Restore .vibe/ files from a backup.
        
        Args:
            backup_name: Name of backup folder (timestamp)
            
        Returns:
            True if successful, False otherwise
        """
        backup_path = self.vibe_path / self.BACKUP_DIR / backup_name
        if not backup_path.exists():
            return False
        
        for file in ["task_plan.md", "findings.md", "progress.md", "user_profile.json"]:
            src = backup_path / file
            if src.exists():
                shutil.copy2(src, self.vibe_path / file)
        
        return True
    
    # ========== V2 Methods: Plan Management ==========
    
    def ensure_plans_dir(self) -> Path:
        """Ensure plans directory exists and return path."""
        plans_path = self.vibe_path / self.PLANS_DIR
        plans_path.mkdir(exist_ok=True)
        return plans_path
    
    def ensure_debug_sessions_dir(self) -> Path:
        """Ensure debug sessions directory exists and return path."""
        debug_path = self.vibe_path / self.DEBUG_SESSIONS_DIR
        debug_path.mkdir(exist_ok=True)
        return debug_path
    
    def get_active_plan(self) -> Optional[Path]:
        """
        Get the most recent plan file.
        
        Returns:
            Path to most recent plan, or None if no plans exist
        """
        plans_path = self.vibe_path / self.PLANS_DIR
        if not plans_path.exists():
            return None
        plans = sorted(plans_path.glob("*.md"), reverse=True)
        return plans[0] if plans else None
    
    def get_active_debug_session(self) -> Optional[Path]:
        """
        Get the most recent unresolved debug session.
        
        Returns:
            Path to open debug session, or None if none open
        """
        debug_path = self.vibe_path / self.DEBUG_SESSIONS_DIR
        if not debug_path.exists():
            return None
        sessions = sorted(debug_path.glob("*.md"), reverse=True)
        for session in sessions:
            content = session.read_text(encoding="utf-8")
            if "**Status:** OPEN" in content:
                return session
        return None
    
    def get_restoration_context(self) -> Dict[str, Any]:
        """
        Get full restoration context including plans and debug sessions.
        Used when restoring state after context loss.
        
        Returns:
            Dict with current_phase, active_plan, active_debug_session, etc.
        """
        context = {
            "vibe_exists": self.exists(),
            "current_phase": None,
            "goal": None,
            "active_plan": None,
            "active_plan_progress": None,
            "active_debug_session": None,
            "pending_mcq": False,
            "user_level": None
        }
        
        if not self.exists():
            return context
        
        # Get current Vibe context
        try:
            vibe_context = self.read_context()
            context["current_phase"] = vibe_context.current_phase
            context["goal"] = vibe_context.goal
            context["pending_mcq"] = vibe_context.has_pending_mcq
            context["user_level"] = vibe_context.user_profile.level
        except Exception:
            pass
        
        # Check for active plan
        active_plan = self.get_active_plan()
        if active_plan:
            context["active_plan"] = str(active_plan)
            # Try to get progress
            try:
                content = active_plan.read_text(encoding="utf-8")
                total = content.count("## [ ] Task") + content.count("## [x] Task")
                completed = content.count("## [x] Task")
                context["active_plan_progress"] = f"{completed}/{total} tasks complete"
            except Exception:
                pass
        
        # Check for active debug session
        active_debug = self.get_active_debug_session()
        if active_debug:
            context["active_debug_session"] = str(active_debug)
        
        return context
    
    def get_phase_with_emoji(self, phase: str) -> str:
        """Get phase name with emoji prefix."""
        emoji = self.PHASE_EMOJIS.get(phase, "")
        return f"{emoji} {phase}" if emoji else phase
    
    def log_phase_transition(self, from_phase: str, to_phase: str, reason: str = "") -> None:
        """
        Log a phase transition to progress.md.
        
        Args:
            from_phase: Previous phase
            to_phase: New phase
            reason: Why the transition occurred
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"""
### Phase Transition — {timestamp}
**From:** {self.get_phase_with_emoji(from_phase)}
**To:** {self.get_phase_with_emoji(to_phase)}
{f"**Reason:** {reason}" if reason else ""}

---
"""
        self._append_file("progress.md", entry)
    
    def log_iron_law_violation(self, law: str, context: str) -> None:
        """
        Log when an Iron Law is about to be violated (for SAFETY_OVERRIDE).
        
        Args:
            law: Which Iron Law (TDD, Debugging, Verification, Vibe Check)
            context: What the user requested
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"""
### ⚠️ SAFETY_OVERRIDE — {timestamp}
**Iron Law:** {law}
**User Request:** {context}
**Action:** Proceeding with override, technical debt logged.

---
"""
        self._append_file("progress.md", entry)
        
        # Also add to findings.md technical debt section
        findings = self._read_file("findings.md")
        debt_section = "## ⚠️ Technical Debt"
        if debt_section in findings:
            debt_entry = f"- [{timestamp}] {law} override: {context[:50]}..."
            findings = findings.replace(
                f"{debt_section}\n- *none yet*",
                f"{debt_section}\n{debt_entry}"
            )
            # If already has entries, append
            if "- *none yet*" not in findings and debt_section in findings:
                parts = findings.split(debt_section)
                if len(parts) == 2:
                    parts[1] = f"\n{debt_entry}" + parts[1]
                    findings = debt_section.join(parts)
            self._write_file("findings.md", findings)
    
    # Private helper methods
    
    def _write_file(self, filename: str, content: str) -> None:
        """Write content to a file in .vibe/."""
        filepath = self.vibe_path / filename
        filepath.write_text(content, encoding="utf-8")
    
    def _read_file(self, filename: str) -> str:
        """Read content from a file in .vibe/."""
        filepath = self.vibe_path / filename
        if filepath.exists():
            return filepath.read_text(encoding="utf-8")
        return ""
    
    def _append_file(self, filename: str, content: str) -> None:
        """Append content to a file in .vibe/."""
        filepath = self.vibe_path / filename
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(content)
    
    def _write_json(self, filename: str, data: dict) -> None:
        """Write JSON data to a file in .vibe/."""
        filepath = self.vibe_path / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    
    def _read_json(self, filename: str) -> dict:
        """Read JSON data from a file in .vibe/."""
        filepath = self.vibe_path / filename
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _extract_goal(self, task_plan: str) -> str:
        """Extract goal from task_plan.md."""
        lines = task_plan.split("\n")
        for i, line in enumerate(lines):
            if line.strip() == "## Goal":
                if i + 1 < len(lines):
                    return lines[i + 1].strip()
        return ""
    
    def _extract_current_phase(self, task_plan: str) -> str:
        """Extract current phase from task_plan.md."""
        lines = task_plan.split("\n")
        for i, line in enumerate(lines):
            if line.strip() == "## Current Phase":
                if i + 1 < len(lines):
                    return lines[i + 1].strip()
        return "🔍 Discovery"
    
    def _extract_pending_decisions(self, findings: str) -> List[str]:
        """Extract pending decisions from findings.md."""
        decisions = []
        in_pending = False
        
        for line in findings.split("\n"):
            if "## Pending Decisions" in line:
                in_pending = True
                continue
            if in_pending and line.startswith("##"):
                break
            if in_pending and line.startswith("- [ ]"):
                decision = line.replace("- [ ]", "").strip()
                if decision and decision != "(To be identified during Vibe Check)":
                    decisions.append(decision)
        
        return decisions
    
    def _extract_resolved_decisions(self, findings: str) -> List[Decision]:
        """Extract resolved decisions from findings.md table."""
        decisions = []
        in_table = False
        
        for line in findings.split("\n"):
            if "|:---|:---|:---|:---|" in line:
                in_table = True
                continue
            if in_table and line.startswith("|"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 4 and parts[0] != "*none yet*":
                    decisions.append(Decision(
                        decision=parts[0],
                        choice=parts[1],
                        rationale=parts[2],
                        mcq_number=int(parts[3].replace("#", "")) if parts[3].replace("#", "").isdigit() else 0
                    ))
            elif in_table and not line.startswith("|"):
                break
        
        return decisions
    
    def _extract_recent_mcqs(self, progress: str, limit: int = 5) -> List[MCQLog]:
        """Extract recent MCQs from progress.md."""
        # This is a simplified parser - in production, use regex
        mcqs = []
        # Parse MCQ sections from progress.md
        # For now, return empty list - the full parser would be more complex
        return mcqs
    
    def _check_pending_mcq(self, progress: str) -> tuple[bool, Optional[str]]:
        """Check if there's an unanswered MCQ in progress.md."""
        # Look for MCQ entries without "User Answer" line
        lines = progress.split("\n")
        current_topic = None
        has_answer = True
        
        for line in lines:
            if line.startswith("### MCQ #"):
                has_answer = False
                current_topic = None
            elif line.startswith("**Topic**:"):
                current_topic = line.replace("**Topic**:", "").strip()
            elif line.startswith("**User Answer**:"):
                has_answer = True
        
        if not has_answer and current_topic:
            return True, current_topic
        
        return False, None
