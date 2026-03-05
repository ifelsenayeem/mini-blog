# Mini Blog Frontend

React-based frontend for the Mini Blog training application.

## Technology Stack

- **React 18** - UI library
- **React Router** - Navigation
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **React Quill** - Rich text editor
- **date-fns** - Date formatting

## Project Structure

```
frontend/
├── public/              # Static files
│   └── index.html      # HTML template
├── src/
│   ├── components/     # Reusable components
│   │   └── Header.js   # Navigation header
│   ├── context/        # React context
│   │   └── AuthContext.js  # Authentication context
│   ├── pages/          # Page components
│   │   ├── Home.js     # Home page
│   │   ├── Login.js    # Login page
│   │   ├── Register.js # Registration page
│   │   ├── PostDetail.js    # Single post view
│   │   └── CreateEditPost.js # Post editor
│   ├── services/       # API services
│   │   └── api.js      # API client
│   ├── App.js          # Main app component
│   ├── index.js        # Entry point
│   └── index.css       # Global styles
├── package.json
├── tailwind.config.js
└── Dockerfile
```

## Setup Instructions

### 1. Prerequisites

- Node.js 18 or higher
- npm or yarn

### 2. Install Dependencies

```bash
npm install
# or
yarn install
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
nano .env
```

Required environment variables:
- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:5000/api)

### 4. Run Development Server

```bash
npm start
# or
yarn start
```

The app will open at `http://localhost:3000`

### 5. Build for Production

```bash
npm run build
# or
yarn build
```

Production files will be in the `build/` directory.

## Features

### Authentication
- User registration
- User login
- Protected routes
- JWT token management
- Automatic token refresh

### Blog Posts
- List all posts
- View single post
- Create new post
- Edit existing post
- Delete post
- Rich text editor
- Image support
- Categories and tags
- Post status (draft/published)

### Comments
- View comments
- Add comments
- Nested replies
- Real-time updates

### User Interface
- Responsive design
- Mobile-friendly
- Clean and modern UI
- Loading states
- Error handling
- Form validation

## Available Scripts

### `npm start`
Runs the app in development mode at [http://localhost:3000](http://localhost:3000)

### `npm test`
Launches the test runner in interactive watch mode.

### `npm run build`
Builds the app for production to the `build` folder.

### `npm run eject`
**Warning:** This is a one-way operation. Ejects from Create React App.

## Component Guide

### AuthContext

Provides authentication state and functions throughout the app:

```jsx
import { useAuth } from './context/AuthContext';

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuth();
  
  // Use authentication state
}
```

### API Service

All API calls are centralized in `services/api.js`:

```javascript
import { postsAPI } from './services/api';

// Get posts
const response = await postsAPI.getPosts({ page: 1, per_page: 10 });

// Create post
const newPost = await postsAPI.createPost({
  title: 'My Post',
  content: '<p>Content</p>',
  status: 'published'
});
```

### Protected Routes

Use the `ProtectedRoute` component for authentication-required pages:

```jsx
import { Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
}
```

## Styling

### Tailwind CSS

The project uses Tailwind CSS for styling. Common patterns:

```jsx
// Button
<button className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
  Click me
</button>

// Card
<div className="bg-white rounded-lg shadow-sm p-6">
  Card content
</div>

// Input
<input className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-primary-500" />
```

### Custom Colors

Primary color palette (blue) is defined in `tailwind.config.js`:
- `primary-50` to `primary-900`

### Typography Plugin

The `@tailwindcss/typography` plugin provides prose styles for blog content:

```jsx
<div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: content }} />
```

## State Management

Currently uses React Context API for:
- Authentication state
- User data

For larger applications, consider:
- Redux
- Zustand
- Recoil

## Form Handling

Forms use controlled components:

```jsx
const [formData, setFormData] = useState({ title: '', content: '' });

const handleChange = (e) => {
  setFormData({ ...formData, [e.target.name]: e.target.value });
};
```

## Error Handling

API errors are handled with try-catch blocks:

```jsx
try {
  await postsAPI.createPost(data);
} catch (error) {
  setError(error.response?.data?.error || 'An error occurred');
}
```

## Docker

```bash
# Build image
docker build -t miniblog-frontend .

# Run container
docker run -p 3000:80 miniblog-frontend
```

## Deployment

### Static Hosting

Deploy the `build/` folder to:
- AWS Amplify
- Netlify
- Vercel
- GitHub Pages
- S3 + CloudFront

### Nginx

Serve with nginx:

```nginx
server {
    listen 80;
    root /var/www/html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## Performance Optimization

### Code Splitting

```jsx
import { lazy, Suspense } from 'react';

const PostDetail = lazy(() => import('./pages/PostDetail'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <PostDetail />
    </Suspense>
  );
}
```

### Memoization

```jsx
import { useMemo, useCallback } from 'react';

const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
const memoizedCallback = useCallback(() => doSomething(a, b), [a, b]);
```

### Image Optimization

- Use WebP format
- Lazy load images
- Implement responsive images

## Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Color contrast
- Focus indicators

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

**Blank page after build:**
- Check browser console for errors
- Verify API URL is correct
- Check CORS settings on backend

**API calls failing:**
- Verify backend is running
- Check REACT_APP_API_URL
- Inspect network tab in browser

**Styling not working:**
- Rebuild: `npm run build`
- Clear cache
- Check Tailwind configuration

## Future Enhancements

- [ ] Dark mode
- [ ] Internationalization (i18n)
- [ ] PWA features
- [ ] Offline support
- [ ] Push notifications
- [ ] Social sharing
- [ ] Analytics integration
- [ ] SEO optimization
- [ ] Unit tests
- [ ] E2E tests

## Testing

```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage

# E2E tests with Cypress
npm run cypress:open
```

## Contributing

This is a training project. Practice adding features like:
- User profiles
- Post bookmarking
- Search functionality
- Infinite scroll
- Image upload
- Social login
- Real-time notifications
