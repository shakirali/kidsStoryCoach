# Kids Story Creator - Testing and Evaluation

> **Note**: This document describes testing and evaluation requirements for the Kids Story Creator. For agent architecture, see [Agents.md](./Agents.md). For implementation details, see [AgentsFramework.md](./AgentsFramework.md).

## Evaluation Strategy

### Per-Agent Evaluations

**1. Content Moderation Agent**:
- True positive rate: correctly flags inappropriate content
- False positive rate: incorrectly flags appropriate content
- Response time
- Kid-friendliness of rejection messages

**2. Story Title Generator Agent**:
- Relevance to story concept
- Age-appropriateness
- Creativity score
- Title length (should be concise)

**3. Book Cover Illustration Agent**:
- Visual quality
- Theme relevance
- Age-appropriateness
- Color vibrancy and appeal

**4. Story Page Generator Agent**:
- Grammar/punctuation correction accuracy
- Preservation of child's original language
- Minimal intervention score (less editing is better)
- Content flow from previous pages

**5. Page Illustration Agent**:
- Visual quality
- Story relevance
- Style consistency across pages
- Age-appropriateness

### End-to-End Evaluations

- Complete workflow success rate
- Average story creation time
- User satisfaction (simulated or parent feedback)
- Content safety coverage
- System reliability and error handling

## Testing and Evaluation Requirements

**MANDATORY**: All code must be covered by unit tests and evaluations. This is a core quality requirement.

### Unit Testing Requirements

**Code Coverage**:
- Minimum 80% code coverage for all agent implementations
- All agent classes must have unit tests
- All utility functions must have unit tests
- All session management functions must have unit tests
- Critical paths (error handling, content moderation) require 100% coverage

**Unit Test Scope**:
- **Agent Tests**: Each agent must have unit tests covering:
  - Input validation
  - Output format validation
  - Error handling and edge cases
  - Integration with Google ADK framework
  - Session data read/write operations
  
- **Workflow Tests**: Sequential workflow agents must have tests covering:
  - Correct execution order
  - Session state propagation between agents
  - Error propagation and handling
  - Workflow completion scenarios

- **Session Management Tests**: Session service integration must have tests covering:
  - Session creation and initialization
  - Session data storage and retrieval
  - Session timeout handling
  - Session cleanup and expiration
  - Multi-session isolation

- **Frontend Tests**: Gradio UI components must have tests covering:
  - User input validation
  - UI state management
  - Error message display
  - Export functionality (if enabled)

- **Utility Tests**: All utility functions must have tests covering:
  - Image processing functions
  - Text validation functions
  - File handling functions
  - Export functions

**Test Framework**:
- Use Python testing framework (e.g., pytest, unittest)
- Tests should be isolated and independent
- Mock external dependencies (OpenAI API, Google ADK services)
- Use fixtures for common test data and setup

### Integration Testing Requirements

**Integration Test Scope**:
- Agent-to-agent communication via session service
- Sequential workflow execution
- Frontend-to-backend communication
- End-to-end story creation workflow
- Error recovery and fallback mechanisms

**Test Scenarios**:
- Complete story creation flow (name → concept → title → cover → pages → completion)
- Content moderation rejection and retry flow
- API failure and retry scenarios
- Session timeout and recovery
- Export functionality (if enabled)

### Evaluation Requirements

**Per-Agent Evaluations** (see Evaluation Strategy section above):
- All agents must have evaluation metrics defined
- Evaluation tests must validate agent outputs against criteria
- Evaluation results must be logged and tracked

**Evaluation Test Coverage**:
- Content Moderation Agent: Test with appropriate and inappropriate content samples
- Story Title Generator Agent: Test title generation quality and relevance
- Book Cover Illustration Agent: Test image generation quality and appropriateness
- Story Page Generator Agent: Test grammar correction and voice preservation
- Page Illustration Agent: Test image quality and style consistency

**Automated Evaluation**:
- Evaluation tests should run as part of CI/CD pipeline
- Evaluation metrics should be tracked over time
- Regression tests should detect quality degradation

### Test Organization

**Test Structure**:
- Unit tests should mirror source code structure
- Tests should be in `tests/` directory with same folder hierarchy as `src/`
- Integration tests should be in `tests/integration/`
- Evaluation tests should be in `tests/evaluation/`

**Test Naming Convention**:
- Unit tests: `test_<module_name>.py`
- Integration tests: `test_integration_<feature>.py`
- Evaluation tests: `test_evaluation_<agent_name>.py`

### Continuous Testing

**CI/CD Integration**:
- All tests must pass before code merge
- Code coverage reports must be generated and reviewed
- Evaluation metrics must be tracked and reported
- Test failures must block deployment

**Test Maintenance**:
- Tests must be updated when code changes
- Deprecated tests must be removed
- Test performance should be monitored
- Flaky tests must be fixed or removed

