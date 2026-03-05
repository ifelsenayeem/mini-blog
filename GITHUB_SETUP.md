# GitHub Repository Setup Guide

Follow these steps to create a GitHub repository for the Mini Blog Training project.

## Method 1: Using GitHub CLI (Recommended)

### Prerequisites
Install GitHub CLI: https://cli.github.com/

### Steps

```bash
# 1. Navigate to project directory
cd /Users/mohammednayeem/Documents/coding/mini-blog-training

# 2. Make setup script executable
chmod +x setup.sh

# 3. Initialize git repository
git init

# 4. Add all files
git add .

# 5. Create initial commit
git commit -m "feat: initial commit - complete mini blog training application

- Add React frontend with Tailwind CSS
- Add Flask backend with MySQL
- Add authentication and JWT
- Add blog posts, comments, categories, tags
- Add Docker support
- Add deployment guides for EC2, ECS, Lambda
- Add comprehensive documentation"

# 6. Create GitHub repository and push (you'll be prompted to login)
gh repo create mini-blog-training --public --source=. --remote=origin --push

# 7. Open repository in browser
gh repo view --web
```

## Method 2: Using GitHub Web Interface

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name:** `mini-blog-training`
   - **Description:** `A well-designed mini-blog application for training purposes - React frontend + Flask backend`
   - **Visibility:** Public or Private
   - **Initialize:** Do NOT initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

### Step 2: Push Local Code to GitHub

```bash
# 1. Navigate to project directory
cd /Users/mohammednayeem/Documents/coding/mini-blog-training

# 2. Make setup script executable
chmod +x setup.sh

# 3. Initialize git repository
git init

# 4. Add all files
git add .

# 5. Create initial commit
git commit -m "feat: initial commit - complete mini blog training application

- Add React frontend with Tailwind CSS
- Add Flask backend with MySQL
- Add authentication and JWT
- Add blog posts, comments, categories, tags
- Add Docker support
- Add deployment guides for EC2, ECS, Lambda
- Add comprehensive documentation"

# 6. Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/mini-blog-training.git

# 7. Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Upload

Visit your repository at: `https://github.com/YOUR_USERNAME/mini-blog-training`

## Method 3: Using Git GUI

If you prefer a graphical interface:

1. **GitHub Desktop:**
   - Download: https://desktop.github.com/
   - File → Add Local Repository → Select project folder
   - Publish repository to GitHub

2. **VS Code:**
   - Open project in VS Code
   - Click Source Control icon (Ctrl+Shift+G)
   - Initialize Repository
   - Commit all files
   - Publish to GitHub

## Repository Settings (Optional)

After creating the repository, configure these settings:

### 1. Add Topics

Go to repository → About (gear icon) → Add topics:
- `react`
- `flask`
- `python`
- `javascript`
- `mysql`
- `blog`
- `training`
- `aws`
- `docker`
- `fullstack`

### 2. Add Repository Description

About → Edit → Description:
```
A well-designed mini-blog application for training purposes featuring React frontend, Flask backend, MySQL database, and multiple deployment options (EC2, Lambda, ECS)
```

### 3. Enable GitHub Pages (Optional)

For documentation:
- Settings → Pages
- Source: Deploy from a branch
- Branch: main, /docs folder
- Save

### 4. Add Branch Protection Rules

Settings → Branches → Add rule:
- Branch name pattern: `main`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging

### 5. Enable GitHub Actions

GitHub Actions are already configured in `.github/workflows/ci-cd.yml`.
They will run automatically on push and pull requests.

### 6. Add Repository Secrets (for CI/CD)

If deploying to AWS via GitHub Actions:

Settings → Secrets and variables → Actions → New repository secret:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `DB_PASSWORD`
- `SECRET_KEY`
- `JWT_SECRET_KEY`

## Next Steps

1. **Clone on another machine:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/mini-blog-training.git
   cd mini-blog-training
   ./setup.sh
   ```

2. **Invite collaborators:**
   - Settings → Collaborators → Add people

3. **Create issues for features:**
   - Issues → New issue
   - Use labels: `enhancement`, `bug`, `documentation`

4. **Set up project board:**
   - Projects → New project
   - Choose template or start from scratch

5. **Enable discussions:**
   - Settings → Features → Discussions

## Git Workflow Best Practices

### Creating Feature Branches

```bash
# Create and switch to new branch
git checkout -b feature/add-user-profiles

# Make changes and commit
git add .
git commit -m "feat: add user profile page"

# Push to GitHub
git push origin feature/add-user-profiles

# Create Pull Request on GitHub
```

### Keeping Fork Updated

```bash
# Add upstream remote (if you forked)
git remote add upstream https://github.com/ORIGINAL_OWNER/mini-blog-training.git

# Fetch and merge updates
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### Commit Message Format

Follow conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

Examples:
```
feat(auth): add password reset functionality
fix(posts): resolve pagination bug
docs(readme): update installation instructions
refactor(api): improve error handling
```

## Troubleshooting

### Authentication Issues

If you get authentication errors:

```bash
# Use personal access token instead of password
# Generate at: https://github.com/settings/tokens

# Or use SSH
git remote set-url origin git@github.com:YOUR_USERNAME/mini-blog-training.git
```

### Large Files

If you have files > 100MB:

```bash
# Use Git LFS
git lfs install
git lfs track "*.zip"
git lfs track "*.tar.gz"
git add .gitattributes
```

### Committed Secrets by Mistake

```bash
# Remove from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
```

**Better:** Use environment variables and never commit `.env` files.

## Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub CLI](https://cli.github.com/manual/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Support

If you have questions:
1. Check existing [Issues](https://github.com/YOUR_USERNAME/mini-blog-training/issues)
2. Create a new issue with the `question` label
3. Join [Discussions](https://github.com/YOUR_USERNAME/mini-blog-training/discussions)

Happy coding! 🚀
