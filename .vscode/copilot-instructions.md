# GitHub Pull Request Workflow Rules

## Project Context

This is a **Python/Django REST Framework** application.

### Technology Stack
- **Backend Framework**: Django with Django REST Framework (DRF)
- **Language**: Python
- **API Style**: RESTful APIs

### Code Standards
- Follow PEP 8 style guidelines for Python code
- Use Django and DRF best practices (CBVs, serializers, viewsets)
- Maintain consistent naming conventions for models, views, serializers, and URLs
- Write docstrings for complex functions and classes
- Keep business logic in models or service layers, not in views

### Testing Expectations
- Write unit tests for models, serializers, and business logic
- Include API endpoint tests for views
- Ensure migrations are included for model changes
- Test authentication and permission requirements

### Common Patterns
- Use DRF serializers for data validation and transformation
- Implement proper permission classes for API endpoints
- Use Django's ORM efficiently (avoid N+1 queries)
- Follow REST principles for endpoint design
- Use appropriate HTTP status codes in responses

### PR Requirements
- Include database migrations if models are modified
- Update API documentation if endpoints change
- Consider backwards compatibility for API changes
- Note any new dependencies in requirements.txt

## Push and PR Creation Workflow

When I ask you to push commits and create a PR, follow these steps:

1. **Push the feature branch**
   - Push the current branch to GitHub using the GitHub MCP server
   - Confirm the push was successful

2. **Generate and review diff**
   - Run `git diff main` (or `git diff main...HEAD` for three-dot diff) to show changes between the feature branch and main
   - If the diff output is truncated or I need more detail, use `cat` or other tools to examine the full diff
   - Wait for my review of the diff before proceeding

3. **Create Pull Request**
   - Open a new pull request from the feature branch to main
   - **PR Title**: Use a clear, concise title that summarizes the changes
   - **PR Description**: Include the following sections:
     
     ### Changes
     - Provide a detailed description of what was changed and why
     - List key modifications, new features, or bug fixes
     - Reference any relevant issue numbers
     
     ### Technical Details
     - Highlight important implementation details
     - Note any architectural decisions or trade-offs
     - Mention dependencies added or updated
     
     ### Testing Steps
     - Provide step-by-step instructions for testing the changes
     - Include any setup requirements or test data needed
     - List expected outcomes for each test scenario
     - Mention any edge cases to verify
     
     ### Additional Notes
     - Note any breaking changes or migration steps
     - Mention areas that need special review attention
     - Include screenshots or examples if helpful

4. **Confirmation**
   - Provide the PR URL and number
   - Summarize what was included in the PR

## Usage Examples

**Example request**: "Push this and create a PR"
**Example request**: "Push my changes and open a pull request"
**Example request**: "Ready to push and PR this feature"

## Notes
- Always wait for my confirmation after showing the diff before creating the PR
- If I say "cat the output", examine the full diff content before proceeding
- For complex changes, be extra thorough in the testing steps section
- Tailor the level of detail to the size and complexity of the changes
- Ask any clarifying questions that you have