# Assignments for CS146S: The Modern Software Developer

This is the home of the assignments for [CS146S: The Modern Software Developer](https://themodernsoftware.dev), taught at Stanford University fall 2025.

## Repo Setup
These steps work with Python 3.12.

1. Install Anaconda
   - Download and install: [Anaconda Individual Edition](https://www.anaconda.com/download)
   - Open a new terminal so `conda` is on your `PATH`.

2. Create and activate a Conda environment (Python 3.12)
   ```bash
   conda create -n cs146s python=3.12 -y
   conda activate cs146s
   ```

3. Install Poetry
   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```

4. Install project dependencies with Poetry (inside the activated Conda env)
   From the repository root:
   ```bash
   poetry install --no-interaction
   ```

---

## Course Review

### Course Overview

CS146S: The Modern Software Developer is a hands-on course exploring how AI tools transform software development workflows. Over 8 weeks, students progress from fundamental LLM prompting to building production-ready applications across multiple technology stacks.

### Weekly Assignments Summary

| Week | Topic | Key Deliverables |
|------|-------|------------------|
| 1 | Prompting Techniques | K-shot, Chain-of-thought, Tool calling, Self-consistency, RAG, Reflexion |
| 2 | AI-Assisted Development | LLM extraction with Ollama, structured outputs, unit tests |
| 3 | MCP Server | Custom weather server with STDIO/HTTP transport, authentication |
| 4 | Claude Code Automations | CLAUDE.md guidance, slash commands for testing and docs |
| 5 | Advanced Automations | Multi-agent workflows, React frontend, 99 total tests |
| 6 | Security Scanning | Semgrep analysis, SQL injection/XSS/command injection fixes |
| 7 | Code Review & AI | CRUD endpoints, Tag model, pagination tests, AI code review |
| 8 | Multi-Stack Apps | Same app in Django, FastAPI, and Express |

### Key Learnings

1. **Prompt Engineering** - Understanding different prompting strategies (K-shot, chain-of-thought, self-consistency) and when to apply each technique for optimal LLM outputs.

2. **AI-Assisted Coding** - Using Claude Code and similar tools to accelerate development while maintaining code quality through testing and review.

3. **MCP Protocol** - Building Model Context Protocol servers that integrate with AI clients, supporting both local (STDIO) and remote (HTTP) transports.

4. **Automation Design** - Creating reusable slash commands and workflows that encode best practices and reduce repetitive tasks.

5. **Security Awareness** - Identifying and fixing common vulnerabilities (SQL injection, XSS, command injection, SSRF) using static analysis tools like Semgrep.

6. **Code Review with AI** - Comparing AI-generated code reviews (GitHub Copilot, Graphite Diamond) with manual reviews, understanding their complementary strengths.

7. **Multi-Stack Development** - Implementing the same application across Django, FastAPI, and Express, understanding framework-specific patterns and trade-offs.

### Technology Stack

**Languages**: Python, JavaScript/TypeScript

**Frameworks**: FastAPI, Django, Django REST Framework, Express, React, Vite

**Tools**: Claude Code, Ollama, Semgrep, pytest, Git, GitHub/Gitea

**Databases**: SQLite, SQLAlchemy ORM

### Best Practices Learned

- **Test-Driven Development**: Write tests first, verify coverage ≥80%
- **Immutable Data Patterns**: Avoid mutation, create new objects
- **Security-First Design**: Validate inputs, parameterize queries, escape outputs
- **Documentation**: Keep CLAUDE.md and README updated for AI context
- **Code Review**: Use AI reviews as first pass, manual review for architecture decisions

### Course Outcomes

This course transforms students from traditional developers into modern software engineers who can effectively leverage AI tools to:
- Write better code faster with AI assistance
- Design robust automations that encode team practices
- Build secure applications with security scanning integrated into CI/CD
- Work across multiple technology stacks with confidence
- Conduct effective code reviews combining AI and human insight

---

## Author

**Tomson** - CS146S Fall 2025
