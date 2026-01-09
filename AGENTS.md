# Cloud Atlas AI Agent Guidance

This project uses Cloud Atlas AI tools for task management, metacognitive review, and knowledge capture.

## ba - Task Tracking

**When to use:**
- Creating and tracking discrete work items
- Managing task lifecycle (ready → claimed → in-progress → done)
- Linking work to sessions for context
- Reviewing completed work and open tasks

**Protocol:**

1. **Create tasks:**
   ```bash
   ba create "Task description" -t task
   ba create "Spike to investigate X" -t spike
   ba create "Bug: Fix Y" -t bug
   ```

2. **Mark tasks ready:**
   ```bash
   ba ready  # Interactive selection
   ba ready <task-id>
   ```

3. **Claim and work:**
   ```bash
   ba claim <task-id> --session $SESSION_ID
   # Do the work
   ba done <task-id>
   ```

4. **Review status:**
   ```bash
   ba list
   ba show <task-id>
   ```

## superego - Metacognitive Advisor

**When to use:**
- Before commits or PRs for code quality review
- At decision points when you want feedback on approach
- When you feel uncertain about implementation choices
- To catch potential issues early

**Protocol:**

Current mode: **pull** (less intrusive, you control when to review)

1. **Request review:**
   ```bash
   /superego:code  # For code review
   /superego:learning  # For teaching/learning review
   /superego:writing  # For documentation review
   ```

2. **Pre-commit review:**
   Superego will automatically review before commits/PRs

3. **Manual review at decision points:**
   Call superego when you want feedback on your approach or implementation

## wm - Working Memory

**When to use:**
- Automatically captures learnings and context throughout sessions
- No manual invocation needed for basic operation
- Review and manage accumulated knowledge

**Protocol:**

1. **Automatic capture:**
   Working memory runs automatically during sessions

2. **Review state:**
   ```bash
   /wm:review  # See current working memory state
   ```

3. **Manual operations:**
   ```bash
   /wm:dive-prep  # Prepare deep context for focused work
   /wm:compress  # Synthesize state to higher-level patterns
   /wm:distill  # Extract learnings from all sessions
   /wm:pause  # Pause/resume automatic capture
   ```

## Integration

These tools work together:
- **ba** tracks what you're working on
- **superego** provides feedback before commits
- **wm** captures what you learn along the way

Example workflow:
1. Create task: `ba create "Add feature X" -t task`
2. Mark ready: `ba ready`
3. Claim: `ba claim <id> --session $SESSION_ID`
4. Work on it...
5. Review: `/superego:code` (if needed)
6. Complete: `ba done <id>`
7. Knowledge captured automatically by wm
