"""
Plan Engine for Vibe Coding Tutor V2
Generates Superpowers-style TDD implementation plans.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Literal
import re


@dataclass
class TDDStep:
    """A single step in the TDD cycle."""
    step_type: Literal["write_test", "verify_fail", "write_code", "verify_pass", "refactor", "commit"]
    description: str
    code_snippet: Optional[str] = None
    command: Optional[str] = None
    expected_output: Optional[str] = None


@dataclass
class TDDTask:
    """A single TDD task with Red-Green-Refactor steps."""
    number: int
    name: str
    description: str
    files_to_create: List[str] = field(default_factory=list)
    files_to_modify: List[str] = field(default_factory=list)
    test_file: str = ""
    steps: List[TDDStep] = field(default_factory=list)
    is_complete: bool = False
    is_teaching_moment: bool = False  # MCQ checkpoint after this task


@dataclass
class ImplementationPlan:
    """Complete implementation plan."""
    goal: str
    language: str
    decisions: List[Dict[str, str]]
    tasks: List[TDDTask]
    created_at: datetime
    file_path: Optional[Path] = None


class PlanEngine:
    """
    Generates and manages TDD implementation plans.
    
    Plans follow Superpowers conventions:
    - Bite-sized tasks (2-5 minutes each)
    - Explicit TDD steps (fail → pass → commit)
    - Teaching Moments every 2-3 tasks
    """
    
    TEACHING_MOMENT_INTERVAL = 2  # MCQ every N tasks
    
    # Test commands by language
    TEST_COMMANDS = {
        "python": "pytest -v",
        "javascript": "npm test",
        "typescript": "npm test",
        "go": "go test -v",
        "rust": "cargo test",
        "java": "mvn test",
        "csharp": "dotnet test",
        "ruby": "rspec",
    }
    
    # File extensions by language
    FILE_EXTENSIONS = {
        "python": "py",
        "javascript": "js",
        "typescript": "ts",
        "go": "go",
        "rust": "rs",
        "java": "java",
        "csharp": "cs",
        "ruby": "rb",
    }
    
    def __init__(self, vibe_path: Path):
        """
        Initialize with .vibe/ directory path.
        
        Args:
            vibe_path: Path to .vibe/ folder
        """
        self.vibe_path = Path(vibe_path)
        self.plans_path = self.vibe_path / "plans"
        self.plans_path.mkdir(exist_ok=True)
    
    def generate_plan(
        self,
        goal: str,
        decisions: List[Dict[str, str]],
        language: str = "python"
    ) -> ImplementationPlan:
        """
        Generate a TDD implementation plan from Vibe Check decisions.
        
        Args:
            goal: User's original request
            decisions: List of {decision, choice, rationale} from findings.md
            language: Programming language (python, javascript, etc.)
            
        Returns:
            ImplementationPlan with tasks and TDD steps
        """
        language = language.lower()
        tasks = self._generate_tasks(goal, decisions, language)
        
        # Mark teaching moments
        for i, task in enumerate(tasks):
            if (i + 1) % self.TEACHING_MOMENT_INTERVAL == 0:
                task.is_teaching_moment = True
        
        plan = ImplementationPlan(
            goal=goal,
            language=language,
            decisions=decisions,
            tasks=tasks,
            created_at=datetime.now()
        )
        
        return plan
    
    def _generate_tasks(
        self,
        goal: str,
        decisions: List[Dict[str, str]],
        language: str
    ) -> List[TDDTask]:
        """Generate TDD tasks based on goal and decisions."""
        tasks = []
        task_num = 1
        
        test_cmd = self._get_test_command(language)
        test_file = self._get_test_path(goal, language)
        impl_file = self._get_impl_path(goal, language)
        
        # Task 1: Core function with basic test
        tasks.append(TDDTask(
            number=task_num,
            name="Core Implementation",
            description=f"Implement the basic {goal} functionality",
            files_to_create=[impl_file, test_file],
            test_file=test_file,
            steps=[
                TDDStep(
                    step_type="write_test",
                    description="Write failing test for basic case",
                    code_snippet=self._generate_test_stub(goal, language)
                ),
                TDDStep(
                    step_type="verify_fail",
                    description="Run test, verify it fails with expected error",
                    command=f"{test_cmd} {test_file}",
                    expected_output="FAIL - function not defined"
                ),
                TDDStep(
                    step_type="write_code",
                    description="Write minimal code to pass the test",
                    code_snippet=self._generate_impl_stub(goal, language)
                ),
                TDDStep(
                    step_type="verify_pass",
                    description="Run test, verify it passes",
                    command=f"{test_cmd} {test_file}",
                    expected_output="PASS (1 passed)"
                ),
                TDDStep(
                    step_type="commit",
                    description="Commit working code",
                    command=f'git add . && git commit -m "feat: add core {self._slugify(goal)}"'
                )
            ]
        ))
        task_num += 1
        
        # Generate tasks for each decision
        for decision in decisions:
            decision_name = decision.get("decision", "Unknown")
            choice = decision.get("choice", "")
            
            tasks.append(TDDTask(
                number=task_num,
                name=f"Handle {decision_name}",
                description=f"Implement {decision_name}: {choice}",
                files_to_modify=[impl_file, test_file],
                test_file=test_file,
                steps=[
                    TDDStep(
                        step_type="write_test",
                        description=f"Write test for {decision_name} behavior",
                        code_snippet=f"# Test for {decision_name}: {choice}"
                    ),
                    TDDStep(
                        step_type="verify_fail",
                        description="Verify test fails before implementing",
                        command=f"{test_cmd} {test_file}",
                        expected_output="FAIL"
                    ),
                    TDDStep(
                        step_type="write_code",
                        description=f"Implement {decision_name} handling based on choice: {choice}"
                    ),
                    TDDStep(
                        step_type="verify_pass",
                        description="Verify all tests pass",
                        command=f"{test_cmd} {test_file}",
                        expected_output="PASS"
                    ),
                    TDDStep(
                        step_type="commit",
                        description="Commit changes",
                        command=f'git add . && git commit -m "feat: add {self._slugify(decision_name)}"'
                    )
                ]
            ))
            task_num += 1
        
        return tasks
    
    def _get_test_command(self, language: str) -> str:
        """Get test command for language."""
        return self.TEST_COMMANDS.get(language, "pytest -v")
    
    def _get_file_extension(self, language: str) -> str:
        """Get file extension for language."""
        return self.FILE_EXTENSIONS.get(language, "py")
    
    def _get_test_path(self, goal: str, language: str) -> str:
        """Generate test file path."""
        slug = self._slugify(goal)[:30]
        ext = self._get_file_extension(language)
        return f"tests/test_{slug}.{ext}"
    
    def _get_impl_path(self, goal: str, language: str) -> str:
        """Generate implementation file path."""
        slug = self._slugify(goal)[:30]
        ext = self._get_file_extension(language)
        return f"src/{slug}.{ext}"
    
    def _slugify(self, text: str) -> str:
        """Convert text to slug format."""
        return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')
    
    def _generate_test_stub(self, goal: str, language: str) -> str:
        """Generate test stub code."""
        func_name = self._slugify(goal)[:20]
        
        if language == "python":
            return f'''def test_{func_name}_basic():
    """Test basic {goal} functionality."""
    # Arrange
    input_value = "test_input"
    expected = "expected_output"
    
    # Act
    result = {func_name}(input_value)
    
    # Assert
    assert result == expected'''
        
        elif language in ("javascript", "typescript"):
            return f'''describe('{goal}', () => {{
  it('should handle basic case', () => {{
    const input = 'test_input';
    const expected = 'expected_output';
    
    const result = {func_name}(input);
    
    expect(result).toBe(expected);
  }});
}});'''
        
        elif language == "go":
            return f'''func Test{func_name.title().replace("_", "")}Basic(t *testing.T) {{
    input := "test_input"
    expected := "expected_output"
    
    result := {func_name}(input)
    
    if result != expected {{
        t.Errorf("got %s, want %s", result, expected)
    }}
}}'''
        
        else:
            return f"# TODO: Write test for {goal}"
    
    def _generate_impl_stub(self, goal: str, language: str) -> str:
        """Generate implementation stub code."""
        func_name = self._slugify(goal)[:20]
        
        if language == "python":
            return f'''def {func_name}(input_value):
    """
    {goal}
    
    Args:
        input_value: The input to process
        
    Returns:
        The processed result
    """
    # TODO: Implement
    return "expected_output"'''
        
        elif language in ("javascript", "typescript"):
            return f'''/**
 * {goal}
 * @param {{string}} input - The input to process
 * @returns {{string}} The processed result
 */
function {func_name}(input) {{
    // TODO: Implement
    return 'expected_output';
}}

module.exports = {{ {func_name} }};'''
        
        elif language == "go":
            return f'''// {func_name} {goal}
func {func_name}(input string) string {{
    // TODO: Implement
    return "expected_output"
}}'''
        
        else:
            return f"# TODO: Implement {goal}"
    
    def save_plan(self, plan: ImplementationPlan, topic: str) -> Path:
        """
        Save plan to .vibe/plans/ directory.
        
        Args:
            plan: The implementation plan
            topic: Short topic name for filename
            
        Returns:
            Path to saved plan file
        """
        date_str = plan.created_at.strftime("%Y-%m-%d")
        slug = self._slugify(topic)[:30]
        filename = f"{date_str}-{slug}.md"
        filepath = self.plans_path / filename
        
        markdown = self._plan_to_markdown(plan)
        filepath.write_text(markdown, encoding="utf-8")
        
        plan.file_path = filepath
        return filepath
    
    def _plan_to_markdown(self, plan: ImplementationPlan) -> str:
        """Convert plan to markdown format."""
        lines = [
            f"# {plan.goal} Implementation Plan",
            "",
            "> **For Agent:** REQUIRED: Use TDD (Red-Green-Refactor) for each task. Follow the Iron Laws.",
            "",
            f"**Goal:** {plan.goal}",
            f"**Language:** {plan.language}",
            f"**Created:** {plan.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## Decisions Made (from Vibe Check)",
            "",
            "| Decision | Choice | Rationale |",
            "|:---|:---|:---|"
        ]
        
        for d in plan.decisions:
            decision = d.get('decision', '').replace('|', '\\|')
            choice = d.get('choice', '').replace('|', '\\|')
            rationale = d.get('rationale', '').replace('|', '\\|')
            lines.append(f"| {decision} | {choice} | {rationale} |")
        
        lines.extend(["", "---", ""])
        
        for task in plan.tasks:
            status = "[x]" if task.is_complete else "[ ]"
            lines.append(f"## {status} Task {task.number}: {task.name}")
            lines.append("")
            lines.append(f"**Description:** {task.description}")
            
            if task.files_to_create:
                lines.append(f"**Files to Create:** `{'`, `'.join(task.files_to_create)}`")
            if task.files_to_modify:
                lines.append(f"**Files to Modify:** `{'`, `'.join(task.files_to_modify)}`")
            if task.test_file:
                lines.append(f"**Test File:** `{task.test_file}`")
            lines.append("")
            
            for i, step in enumerate(task.steps, 1):
                step_title = step.step_type.replace('_', ' ').title()
                lines.append(f"### Step {i}: {step_title}")
                lines.append("")
                lines.append(step.description)
                
                if step.code_snippet:
                    lines.append("")
                    lines.append(f"```{plan.language}")
                    lines.append(step.code_snippet)
                    lines.append("```")
                
                if step.command:
                    lines.append("")
                    lines.append(f"**Run:** `{step.command}`")
                
                if step.expected_output:
                    lines.append(f"**Expected:** {step.expected_output}")
                
                lines.append("")
            
            if task.is_teaching_moment:
                lines.extend([
                    "---",
                    "",
                    "## 🎓 Teaching Moment",
                    "",
                    "*[Reinforcement MCQ will be generated here by quiz_engine]*",
                    ""
                ])
            
            lines.extend(["---", ""])
        
        # Final verification section
        lines.extend([
            "## Final Verification",
            "",
            "After all tasks complete:",
            "",
            "1. Run full test suite:",
            f"   ```bash",
            f"   {self._get_test_command(plan.language)}",
            f"   ```",
            "",
            "2. Verify all tests pass with evidence",
            "",
            "3. Final commit:",
            "   ```bash",
            f'   git add . && git commit -m "feat: complete {self._slugify(plan.goal)}"',
            "   ```",
            ""
        ])
        
        return "\n".join(lines)
    
    def get_active_plan(self) -> Optional[Path]:
        """Get the most recent plan file."""
        if not self.plans_path.exists():
            return None
        plans = sorted(self.plans_path.glob("*.md"), reverse=True)
        return plans[0] if plans else None
    
    def parse_plan(self, plan_path: Path) -> ImplementationPlan:
        """Parse an existing plan file into ImplementationPlan object."""
        content = plan_path.read_text(encoding="utf-8")
        
        # Extract goal from title
        goal_match = re.search(r"^# (.+) Implementation Plan", content, re.MULTILINE)
        goal = goal_match.group(1) if goal_match else ""
        
        # Extract language
        lang_match = re.search(r"\*\*Language:\*\* (\w+)", content)
        language = lang_match.group(1) if lang_match else "python"
        
        # Extract tasks and completion status
        tasks = []
        task_pattern = r"## \[([ x])\] Task (\d+): (.+)"
        for match in re.finditer(task_pattern, content):
            is_complete = match.group(1) == "x"
            number = int(match.group(2))
            name = match.group(3)
            tasks.append(TDDTask(
                number=number,
                name=name,
                description="",
                is_complete=is_complete
            ))
        
        return ImplementationPlan(
            goal=goal,
            language=language,
            decisions=[],
            tasks=tasks,
            created_at=datetime.now(),
            file_path=plan_path
        )
    
    def get_current_task(self, plan: ImplementationPlan) -> Optional[TDDTask]:
        """Find the first incomplete task."""
        for task in plan.tasks:
            if not task.is_complete:
                return task
        return None
    
    def mark_task_complete(self, plan_path: Path, task_number: int) -> None:
        """Mark a task as complete in the plan file."""
        content = plan_path.read_text(encoding="utf-8")
        pattern = rf"## \[ \] Task {task_number}:"
        replacement = f"## [x] Task {task_number}:"
        content = re.sub(pattern, replacement, content)
        plan_path.write_text(content, encoding="utf-8")
    
    def get_plan_progress(self, plan: ImplementationPlan) -> Dict[str, Any]:
        """Get progress statistics for a plan."""
        total = len(plan.tasks)
        completed = sum(1 for t in plan.tasks if t.is_complete)
        
        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "remaining_tasks": total - completed,
            "percent_complete": (completed / total * 100) if total > 0 else 0,
            "current_task": self.get_current_task(plan)
        }
