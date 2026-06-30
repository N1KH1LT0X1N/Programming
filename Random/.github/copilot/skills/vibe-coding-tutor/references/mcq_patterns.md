# MCQ Design Patterns

Reference guide for generating pedagogically-sound MCQs.

## The 4-Option Pattern

Every MCQ follows this structure:

| Option | Role | Purpose |
|:---|:---|:---|
| **A** | Best Practice | Industry-standard approach that handles edge cases |
| **B** | Naive Mistake | Common beginner error that targets a misconception |
| **C** | Tradeoff | Valid approach but has costs (complexity, dependencies) |
| **D** | Custom | Lets user specify their own approach |

## Distractor Design Rules

1. **Similar Length**: All options should be roughly the same length
2. **Plausible**: Distractors must seem reasonable to non-experts
3. **No Giveaways**: Avoid options like "All of the above" or "None of the above"
4. **Homogeneous Grammar**: All options should have consistent grammatical structure

## The Misconception Pattern

For Option B (Naive Mistake), target common misconceptions:

| Topic | Common Misconception |
|:---|:---|
| Validation | Just checking for obvious cases (e.g., only @ in email) |
| Error Handling | Returning None instead of raising exceptions |
| Performance | Premature optimization |
| Input Types | Accepting any type without validation |
| Security | Trusting user input |

## Feedback Structure

After each answer, provide:

1. **Is Correct?**: Clear ✅ or ❌ indicator
2. **Why Correct**: 1-2 sentences explaining the best answer
3. **Why Chosen Wrong**: If incorrect, explain why their choice was problematic
4. **Bridge Question**: Help them understand the concept (for wrong answers)
5. **Next Step**: Concrete action to take

## Difficulty Calibration

Use Elo ratings:

| Difficulty | Elo Range | Description |
|:---|:---|:---|
| Easy | 800-1000 | Fundamental concepts |
| Medium | 1000-1200 | Standard best practices |
| Hard | 1200-1400 | Tradeoffs and edge cases |
| Expert | 1400-1600 | Architecture and advanced patterns |

## Example MCQ

**Topic**: Validation  
**Question**: How strict should email validation be?

- **A)** RFC 5322 compliant regex with domain validation ✓
  - *Best practice: Handles edge cases like subdomains and special characters*
  
- **B)** Check if it contains @ and .
  - *Naive: Misses many invalid formats like "user@" or "@domain.com"*
  
- **C)** Use the email-validator library
  - *Tradeoff: Robust but adds a dependency to manage*
  
- **D)** Custom validation (let me specify)
  - *User choice: Allows specific requirements*

**Correct**: A  
**Difficulty**: 1100
