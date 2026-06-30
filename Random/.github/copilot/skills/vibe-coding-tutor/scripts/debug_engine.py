"""
Debug Engine for Vibe Coding Tutor V2
Implements 4-Phase Systematic Debugging protocol from Superpowers.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, Any
import re


class DebugPhase(Enum):
    """The 4 phases of systematic debugging."""
    ROOT_CAUSE = "root_cause"
    PATTERN_ANALYSIS = "pattern_analysis"
    HYPOTHESIS = "hypothesis"
    IMPLEMENTATION = "implementation"


@dataclass
class Hypothesis:
    """A debugging hypothesis."""
    statement: str
    test_performed: str
    result: str  # "confirmed", "rejected", "pending"
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DebugSession:
    """Tracks a complete debugging session."""
    session_id: str
    error_message: str
    stack_trace: str
    started_at: datetime
    current_phase: DebugPhase
    hypotheses: List[Hypothesis] = field(default_factory=list)
    fixes_attempted: int = 0
    root_cause_identified: bool = False
    root_cause_description: Optional[str] = None
    fix_applied: Optional[str] = None
    is_resolved: bool = False
    file_path: Optional[Path] = None


class DebugEngine:
    """
    Manages systematic debugging sessions.
    
    Follows the Superpowers 4-Phase protocol:
    1. Root Cause Investigation - Read error, reproduce, trace data flow
    2. Pattern Analysis - Find working example, compare differences
    3. Hypothesis Testing - Single theory, minimal test
    4. Implementation - Failing test, fix, verify
    
    Escalates to architecture review after 3+ failed fixes.
    """
    
    MAX_FIXES_BEFORE_ESCALATION = 3
    
    # Phase guidance text
    PHASE_GUIDANCE = {
        DebugPhase.ROOT_CAUSE: """
**Phase 1: Root Cause Investigation**

Before attempting ANY fix, you MUST:
1. Read the error message carefully - it often contains the answer
2. Reproduce the issue consistently - exact steps
3. Check recent changes (git diff, git log -5)
4. Trace the data flow back to the source

**DO NOT propose fixes until you understand the root cause.**

Questions to answer:
- What is the exact error message?
- Can you reproduce it every time?
- What changed recently that could cause this?
- Where does the bad value originate?
""",
        DebugPhase.PATTERN_ANALYSIS: """
**Phase 2: Pattern Analysis**

Now that you understand what's happening:
1. Find a working example of similar code in the codebase
2. Compare: What's different between working and broken?
3. List every difference, no matter how small
4. Don't assume "that can't matter" - list it anyway

Questions to answer:
- Is there similar code that works?
- What are the differences?
- Are all dependencies/config the same?
""",
        DebugPhase.HYPOTHESIS: """
**Phase 3: Hypothesis Testing**

Time to form and test theories:
1. Form ONE clear hypothesis: "I think X is the cause because Y"
2. Design the SMALLEST possible test to prove/disprove it
3. Test ONE variable at a time
4. If rejected, form a NEW hypothesis - don't stack fixes

Current hypothesis format:
- "I think [specific cause] is the root cause because [evidence]"
- "I will test this by [minimal change/observation]"
- "If correct, I expect [specific outcome]"
""",
        DebugPhase.IMPLEMENTATION: """
**Phase 4: Implementation**

Root cause identified. Time to fix:
1. Write a failing test that reproduces the bug
2. Verify the test fails (proves it catches the bug)
3. Implement a SINGLE fix addressing the root cause
4. Verify the test now passes
5. Verify no other tests broke
6. Commit with descriptive message

If the fix doesn't work:
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1 with new information
- If >= 3: STOP and question the architecture
"""
    }
    
    def __init__(self, vibe_path: Path):
        """
        Initialize with .vibe/ directory path.
        
        Args:
            vibe_path: Path to .vibe/ folder
        """
        self.vibe_path = Path(vibe_path)
        self.sessions_path = self.vibe_path / "debug_sessions"
        self.sessions_path.mkdir(exist_ok=True)
    
    def start_session(
        self,
        error_message: str,
        stack_trace: str = ""
    ) -> DebugSession:
        """
        Start a new debugging session.
        
        Args:
            error_message: The error message/test failure
            stack_trace: Full stack trace if available
            
        Returns:
            New DebugSession in ROOT_CAUSE phase
        """
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        session = DebugSession(
            session_id=session_id,
            error_message=error_message,
            stack_trace=stack_trace,
            started_at=datetime.now(),
            current_phase=DebugPhase.ROOT_CAUSE
        )
        
        # Save initial session file
        self._save_session(session)
        
        return session
    
    def advance_phase(self, session: DebugSession) -> DebugPhase:
        """
        Move to the next debugging phase.
        
        Args:
            session: Current session
            
        Returns:
            New phase (or same if at IMPLEMENTATION)
        """
        phase_order = [
            DebugPhase.ROOT_CAUSE,
            DebugPhase.PATTERN_ANALYSIS,
            DebugPhase.HYPOTHESIS,
            DebugPhase.IMPLEMENTATION
        ]
        
        current_idx = phase_order.index(session.current_phase)
        if current_idx < len(phase_order) - 1:
            session.current_phase = phase_order[current_idx + 1]
            self._save_session(session)
        
        return session.current_phase
    
    def record_hypothesis(
        self,
        session: DebugSession,
        statement: str,
        test: str = "",
        result: str = "pending"
    ) -> None:
        """
        Record a hypothesis in the session.
        
        Args:
            session: Current session
            statement: The hypothesis (e.g., "I think X is causing Y")
            test: How we'll test this hypothesis
            result: "confirmed", "rejected", or "pending"
        """
        hypothesis = Hypothesis(
            statement=statement,
            test_performed=test,
            result=result
        )
        session.hypotheses.append(hypothesis)
        self._save_session(session)
    
    def update_hypothesis_result(
        self,
        session: DebugSession,
        hypothesis_index: int,
        result: str
    ) -> None:
        """
        Update the result of a hypothesis.
        
        Args:
            session: Current session
            hypothesis_index: Index of hypothesis to update
            result: "confirmed" or "rejected"
        """
        if 0 <= hypothesis_index < len(session.hypotheses):
            session.hypotheses[hypothesis_index].result = result
            self._save_session(session)
    
    def record_fix_attempt(
        self,
        session: DebugSession,
        fix_description: str,
        success: bool
    ) -> bool:
        """
        Record a fix attempt.
        
        Args:
            session: Current session
            fix_description: What was tried
            success: Did it work?
            
        Returns:
            True if escalation threshold reached (≥3 failures)
        """
        session.fixes_attempted += 1
        
        if success:
            session.fix_applied = fix_description
            session.is_resolved = True
        
        self._save_session(session)
        
        return session.fixes_attempted >= self.MAX_FIXES_BEFORE_ESCALATION and not success
    
    def check_escalation(self, session: DebugSession) -> bool:
        """
        Check if session should escalate to architecture review.
        
        Returns:
            True if 3+ fixes have failed
        """
        return (
            session.fixes_attempted >= self.MAX_FIXES_BEFORE_ESCALATION
            and not session.is_resolved
        )
    
    def set_root_cause(
        self,
        session: DebugSession,
        description: str
    ) -> None:
        """
        Mark root cause as identified.
        
        Args:
            session: Current session
            description: What the root cause is
        """
        session.root_cause_identified = True
        session.root_cause_description = description
        self._save_session(session)
    
    def close_session(
        self,
        session: DebugSession,
        resolution: str
    ) -> None:
        """
        Close a debugging session.
        
        Args:
            session: Current session
            resolution: How it was resolved
        """
        session.is_resolved = True
        session.fix_applied = resolution
        self._save_session(session)
    
    def get_active_session(self) -> Optional[DebugSession]:
        """Get the most recent unresolved session."""
        if not self.sessions_path.exists():
            return None
            
        sessions = sorted(self.sessions_path.glob("*.md"), reverse=True)
        for session_file in sessions:
            content = session_file.read_text(encoding="utf-8")
            if "**Status:** OPEN" in content:
                return self._parse_session(session_file)
        return None
    
    def get_phase_guidance(self, phase: DebugPhase) -> str:
        """Get guidance text for current phase."""
        return self.PHASE_GUIDANCE.get(phase, "")
    
    def _save_session(self, session: DebugSession) -> Path:
        """Save session to markdown file."""
        filename = f"{session.session_id}.md"
        filepath = self.sessions_path / filename
        session.file_path = filepath
        
        status = "RESOLVED" if session.is_resolved else "OPEN"
        
        # Truncate error message for title
        error_title = session.error_message[:50].replace('\n', ' ')
        if len(session.error_message) > 50:
            error_title += "..."
        
        lines = [
            f"# Debug Session: {error_title}",
            "",
            f"**Session ID:** {session.session_id}",
            f"**Started:** {session.started_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Status:** {status}",
            f"**Current Phase:** {session.current_phase.value}",
            f"**Fixes Attempted:** {session.fixes_attempted}/{self.MAX_FIXES_BEFORE_ESCALATION}",
            "",
            "---",
            "",
            "## Error Details",
            "",
            "```",
            session.error_message,
            "```",
            ""
        ]
        
        if session.stack_trace:
            lines.extend([
                "## Stack Trace",
                "",
                "```",
                session.stack_trace,
                "```",
                ""
            ])
        
        # Phase 1 checklist
        rc_check = "x" if session.root_cause_identified else " "
        lines.extend([
            "---",
            "",
            "## Phase 1: Root Cause Investigation",
            "",
            f"- [{rc_check}] Read error message completely",
            "- [ ] Reproduce consistently",
            "- [ ] Check recent changes",
            "- [ ] Trace data flow",
            ""
        ])
        
        if session.root_cause_description:
            lines.extend([
                f"**Root Cause Identified:** {session.root_cause_description}",
                ""
            ])
        
        # Phase 2
        lines.extend([
            "---",
            "",
            "## Phase 2: Pattern Analysis",
            "",
            "- [ ] Find working example",
            "- [ ] Compare differences",
            "",
        ])
        
        # Phase 3 with hypothesis table
        lines.extend([
            "---",
            "",
            "## Phase 3: Hypothesis Testing",
            "",
            "| # | Hypothesis | Test | Result |",
            "|---|------------|------|--------|"
        ])
        
        for i, h in enumerate(session.hypotheses, 1):
            statement = h.statement.replace('|', '\\|')
            test = h.test_performed.replace('|', '\\|')
            lines.append(f"| {i} | {statement} | {test} | {h.result} |")
        
        if not session.hypotheses:
            lines.append("| 1 | *none yet* | | pending |")
        
        # Phase 4
        lines.extend([
            "",
            "---",
            "",
            "## Phase 4: Implementation",
            "",
            "- [ ] Create failing test reproducing bug",
            "- [ ] Implement single fix",
            "- [ ] Verify fix",
            "- [ ] Commit",
            ""
        ])
        
        if session.fix_applied:
            lines.append(f"**Fix Applied:** {session.fix_applied}")
            lines.append("")
        
        if session.is_resolved:
            lines.append("**Status:** ✅ RESOLVED")
        elif session.fixes_attempted >= self.MAX_FIXES_BEFORE_ESCALATION:
            lines.extend([
                "",
                "> [!CAUTION]",
                "> **ESCALATION REQUIRED**: 3+ fixes have failed without resolution.",
                "> ",
                "> Stop and question the architecture before attempting more fixes.",
                "> - Is this pattern fundamentally sound?",
                "> - Are we sticking with it through inertia?",
                "> - Should we refactor vs. continue fixing symptoms?"
            ])
        
        # Session log
        lines.extend([
            "",
            "---",
            "",
            "## Session Log",
            "",
            "| Timestamp | Event |",
            "|-----------|-------|",
            f"| {session.started_at.strftime('%H:%M')} | Session started |"
        ])
        
        for h in session.hypotheses:
            lines.append(f"| {h.timestamp.strftime('%H:%M')} | Hypothesis: {h.statement[:30]}... |")
        
        if session.is_resolved:
            lines.append(f"| {datetime.now().strftime('%H:%M')} | Session resolved |")
        
        filepath.write_text("\n".join(lines), encoding="utf-8")
        return filepath
    
    def _parse_session(self, filepath: Path) -> DebugSession:
        """Parse a session file back into DebugSession object."""
        content = filepath.read_text(encoding="utf-8")
        
        # Extract session ID from filename
        session_id = filepath.stem
        
        # Extract error message
        error_match = re.search(r"## Error Details\s+```\s*\n(.+?)\n```", content, re.DOTALL)
        error_message = error_match.group(1).strip() if error_match else ""
        
        # Extract stack trace
        stack_match = re.search(r"## Stack Trace\s+```\s*\n(.+?)\n```", content, re.DOTALL)
        stack_trace = stack_match.group(1).strip() if stack_match else ""
        
        # Extract current phase
        phase_match = re.search(r"\*\*Current Phase:\*\* (\w+)", content)
        phase_str = phase_match.group(1) if phase_match else "root_cause"
        try:
            current_phase = DebugPhase(phase_str)
        except ValueError:
            current_phase = DebugPhase.ROOT_CAUSE
        
        # Extract fixes attempted
        fixes_match = re.search(r"\*\*Fixes Attempted:\*\* (\d+)", content)
        fixes = int(fixes_match.group(1)) if fixes_match else 0
        
        # Check if resolved
        is_resolved = "**Status:** RESOLVED" in content or "✅ RESOLVED" in content
        
        # Extract root cause if identified
        rc_match = re.search(r"\*\*Root Cause Identified:\*\* (.+)", content)
        root_cause = rc_match.group(1) if rc_match else None
        
        # Extract fix if applied
        fix_match = re.search(r"\*\*Fix Applied:\*\* (.+)", content)
        fix_applied = fix_match.group(1) if fix_match else None
        
        # Parse hypotheses from table
        hypotheses = []
        hyp_pattern = r"\| (\d+) \| ([^|]+) \| ([^|]*) \| (\w+) \|"
        for match in re.finditer(hyp_pattern, content):
            if "*none yet*" not in match.group(2):
                hypotheses.append(Hypothesis(
                    statement=match.group(2).strip(),
                    test_performed=match.group(3).strip(),
                    result=match.group(4).strip()
                ))
        
        return DebugSession(
            session_id=session_id,
            error_message=error_message,
            stack_trace=stack_trace,
            started_at=datetime.now(),  # Approximate
            current_phase=current_phase,
            hypotheses=hypotheses,
            fixes_attempted=fixes,
            root_cause_identified=root_cause is not None,
            root_cause_description=root_cause,
            fix_applied=fix_applied,
            is_resolved=is_resolved,
            file_path=filepath
        )
    
    def generate_debug_mcq(self, topic: str, phase: DebugPhase) -> Dict[str, Any]:
        """
        Generate a teaching MCQ about debugging concepts.
        
        Args:
            topic: What is being debugged
            phase: Current debug phase
            
        Returns:
            Dict with question, options, correct_index, explanations
        """
        if phase == DebugPhase.ROOT_CAUSE:
            return {
                "question": f"Before fixing the {topic} bug, what should you do first?",
                "options": [
                    "A) Complete root cause investigation (read error, reproduce, trace)",
                    "B) Try the most obvious fix and see if it works",
                    "C) Add more logging and hope the bug reveals itself",
                    "D) Ask someone else to fix it"
                ],
                "correct_index": 0,
                "explanations": {
                    0: "Correct! Root cause investigation prevents wasted effort on symptom fixes.",
                    1: "This is guess-and-check debugging - it's slower than systematic investigation.",
                    2: "Logging helps, but it's part of investigation, not a replacement for it.",
                    3: "Understanding the bug yourself is the best way to learn."
                }
            }
        elif phase == DebugPhase.HYPOTHESIS:
            return {
                "question": "When testing a debugging hypothesis, how many changes should you make at once?",
                "options": [
                    "A) One - test one variable at a time",
                    "B) As many as needed to fix the issue",
                    "C) Two or three related changes",
                    "D) It doesn't matter"
                ],
                "correct_index": 0,
                "explanations": {
                    0: "Correct! Testing one variable at a time isolates what actually worked.",
                    1: "Multiple changes make it impossible to know which one fixed the issue.",
                    2: "Even related changes should be tested separately.",
                    3: "It matters a lot - this is key to systematic debugging."
                }
            }
        else:
            return {
                "question": f"What should you do after fixing the {topic} bug?",
                "options": [
                    "A) Write a test that reproduces the bug, then verify it passes",
                    "B) Manually test once and move on",
                    "C) Close the ticket immediately",
                    "D) Hope it doesn't happen again"
                ],
                "correct_index": 0,
                "explanations": {
                    0: "Correct! A regression test ensures the bug can't return silently.",
                    1: "Manual testing isn't recorded and can't be re-run automatically.",
                    2: "Without verification, you don't know if it's actually fixed.",
                    3: "Hope is not a debugging strategy."
                }
            }
