# Contributing to Mini Blog Training

Thank you for your interest in contributing! This is a training project designed to help developers learn full-stack development.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/mini-blog-training.git`
3. Create a branch: `git checkout -b feature/my-feature`
4. Make your changes
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Open a Pull Request

## Development Setup

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python setup_db.py
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your settings
npm start
```

### Docker Setup

```bash
docker-compose up --build
```

## Project Structure

```
mini-blog-training/
├── backend/           # Python Flask API
├── frontend/          # React application
├── docs/             # Documentation
└── docker-compose.yml
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Use type hints where appropriate

```python
def create_post(user_id: int, title: str, content: str) -> Post:
    """
    Create a new blog post.
    
    Args:
        user_id: The ID of the post author
        title: Post title
        content: Post content in HTML
        
    Returns:
        The created Post object
    """
    post = Post(author_id=user_id, title=title, content=content)
    db.session.add(post)
    db.session.commit()
    return post
```

### JavaScript/React (Frontend)

- Use functional components
- Use hooks for state management
- Keep components small and focused
- Use meaningful component and variable names
- Add PropTypes or TypeScript

```jsx
import PropTypes from 'prop-types';

function PostCard({ post, onDelete }) {
  return (
    <div className="post-card">
      <h2>{post.title}</h2>
      <button onClick={() => onDelete(post.id)}>Delete</button>
    </div>
  );
}

PostCard.propTypes = {
  post: PropTypes.shape({
    id: PropTypes.number.isRequired,
    title: PropTypes.string.isRequired,
  }).isRequired,
  onDelete: PropTypes.func.isRequired,
};
```

## Git Workflow

### Branch Naming

- `feature/` - New features (e.g., `feature/add-user-profiles`)
- `fix/` - Bug fixes (e.g., `fix/login-redirect`)
- `docs/` - Documentation (e.g., `docs/update-readme`)
- `refactor/` - Code refactoring (e.g., `refactor/api-service`)

### Commit Messages

Follow conventional commits format:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(posts): add pagination to posts list

fix(auth): resolve token expiration bug

docs(readme): update installation instructions
```

## Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/
```

Write tests for:
- API endpoints
- Database models
- Authentication logic
- Helper functions

Example:
```python
def test_create_post(client, auth_token):
    response = client.post(
        '/api/posts',
        json={
            'title': 'Test Post',
            'content': 'Test content'
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201
    assert 'post' in response.json
```

### Frontend Tests

```bash
cd frontend
npm test
```

Write tests for:
- Components
- Utility functions
- API calls
- User interactions

Example:
```jsx
import { render, screen } from '@testing-library/react';
import PostCard from './PostCard';

test('renders post title', () => {
  const post = { id: 1, title: 'Test Post' };
  render(<PostCard post={post} />);
  expect(screen.getByText('Test Post')).toBeInTheDocument();
});
```

## Documentation

- Update README.md when adding features
- Add inline comments for complex logic
- Update API documentation for new endpoints
- Add deployment notes if needed

## Pull Request Process

1. **Update documentation** - README, API docs, etc.
2. **Add tests** - Ensure new code is tested
3. **Check code style** - Run linters
4. **Update CHANGELOG** - Document changes
5. **Describe your PR** - Explain what and why
6. **Request review** - Tag relevant reviewers

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
```

## Feature Ideas

Looking for something to work on? Try these:

### Beginner-Friendly
- [ ] Add user avatars
- [ ] Implement post likes
- [ ] Add post preview before publishing
- [ ] Create footer component
- [ ] Add loading spinners
- [ ] Implement toast notifications

### Intermediate
- [ ] Add user profiles
- [ ] Implement bookmarking
- [ ] Add search functionality
- [ ] Create admin dashboard
- [ ] Add email notifications
- [ ] Implement draft auto-save

### Advanced
- [ ] Add real-time comments
- [ ] Implement full-text search (Elasticsearch)
- [ ] Add image upload to S3
- [ ] Create analytics dashboard
- [ ] Implement rate limiting
- [ ] Add API versioning
- [ ] Create GraphQL endpoint
- [ ] Implement OAuth (Google, GitHub)

## Code Review Guidelines

When reviewing PRs:

### What to Look For
- ✅ Code is readable and maintainable
- ✅ No security vulnerabilities
- ✅ Tests are comprehensive
- ✅ Documentation is updated
- ✅ No commented-out code
- ✅ Error handling is proper
- ✅ Performance considerations

### Providing Feedback
- Be constructive and respectful
- Explain the reasoning behind suggestions
- Offer solutions, not just problems
- Use examples when helpful
- Acknowledge good work

Example:
```markdown
Nice implementation! One suggestion:

Instead of:
```python
if user is not None and user.is_active == True:
```

Consider:
```python
if user and user.is_active:
```

This is more Pythonic and concise.
```

## Getting Help

- **Documentation**: Check the docs/ folder
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions
- **Questions**: Tag your issue with 'question'

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Expected Behavior

- Be respectful and inclusive
- Welcome newcomers
- Give and receive constructive feedback
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information

## Recognition

Contributors will be recognized in:
- README.md contributors section
- GitHub contributors page
- Release notes

## Questions?

Feel free to open an issue with the 'question' label!

Happy coding! 🚀
