# API Documentation

Base URL: `http://localhost:5000/api`

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "bio": "Tech enthusiast"
  }
}
```

### Posts

#### Get All Posts
```http
GET /api/posts?page=1&per_page=10&status=published&category_id=1&search=tech
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 10, max: 100)
- `status` (str): Filter by status (published/draft)
- `category_id` (int): Filter by category
- `tag_id` (int): Filter by tag
- `author_id` (int): Filter by author
- `search` (str): Search in title and content

**Response (200):**
```json
{
  "posts": [
    {
      "id": 1,
      "title": "Getting Started with React",
      "slug": "getting-started-with-react",
      "excerpt": "Learn the basics of React...",
      "featured_image": "https://example.com/image.jpg",
      "status": "published",
      "view_count": 150,
      "author": {
        "id": 1,
        "username": "johndoe"
      },
      "category": {
        "id": 1,
        "name": "Technology"
      },
      "tags": [
        {"id": 1, "name": "react"},
        {"id": 2, "name": "javascript"}
      ],
      "comment_count": 5,
      "published_at": "2026-03-05T10:30:00",
      "created_at": "2026-03-05T10:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

#### Get Single Post
```http
GET /api/posts/1
GET /api/posts/slug/getting-started-with-react
```

**Response (200):**
```json
{
  "post": {
    "id": 1,
    "title": "Getting Started with React",
    "slug": "getting-started-with-react",
    "content": "<h1>Introduction</h1><p>React is...</p>",
    "excerpt": "Learn the basics of React...",
    "featured_image": "https://example.com/image.jpg",
    "status": "published",
    "view_count": 151,
    "author": {...},
    "category": {...},
    "tags": [...],
    "comment_count": 5
  }
}
```

#### Create Post
```http
POST /api/posts
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My First Post",
  "content": "<p>This is my first blog post</p>",
  "excerpt": "A brief introduction",
  "category_id": 1,
  "tags": ["tutorial", "beginner"],
  "status": "published",
  "featured_image": "https://example.com/image.jpg"
}
```

**Response (201):**
```json
{
  "message": "Post created successfully",
  "post": {...}
}
```

#### Update Post
```http
PUT /api/posts/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "<p>Updated content</p>",
  "status": "published"
}
```

**Response (200):**
```json
{
  "message": "Post updated successfully",
  "post": {...}
}
```

#### Delete Post
```http
DELETE /api/posts/1
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "message": "Post deleted successfully"
}
```

### Comments

#### Get Comments for Post
```http
GET /api/comments?post_id=1
```

**Response (200):**
```json
{
  "comments": [
    {
      "id": 1,
      "content": "Great post!",
      "author": {
        "id": 2,
        "username": "jane"
      },
      "post_id": 1,
      "parent_id": null,
      "is_approved": true,
      "created_at": "2026-03-05T11:00:00",
      "replies": [
        {
          "id": 2,
          "content": "Thanks!",
          "author": {...},
          "parent_id": 1,
          "created_at": "2026-03-05T11:30:00"
        }
      ]
    }
  ]
}
```

#### Create Comment
```http
POST /api/comments
Authorization: Bearer <token>
Content-Type: application/json

{
  "post_id": 1,
  "content": "Great article!",
  "parent_id": null
}
```

**Response (201):**
```json
{
  "message": "Comment created successfully",
  "comment": {...}
}
```

### Categories

#### Get All Categories
```http
GET /api/categories
```

**Response (200):**
```json
{
  "categories": [
    {
      "id": 1,
      "name": "Technology",
      "slug": "technology",
      "description": "All about tech",
      "post_count": 15
    }
  ]
}
```

#### Create Category (Admin only)
```http
POST /api/categories
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Travel",
  "slug": "travel",
  "description": "Travel stories and tips"
}
```

### Tags

#### Get All Tags
```http
GET /api/tags
```

**Response (200):**
```json
{
  "tags": [
    {
      "id": 1,
      "name": "react",
      "slug": "react"
    }
  ]
}
```

#### Create Tag
```http
POST /api/tags
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "nodejs",
  "slug": "nodejs"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Title is required"
}
```

### 401 Unauthorized
```json
{
  "error": "Token is missing"
}
```

### 403 Forbidden
```json
{
  "error": "Admin privileges required"
}
```

### 404 Not Found
```json
{
  "error": "Post not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Rate Limiting

Currently not implemented, but recommended for production:
- 100 requests per minute for authenticated users
- 20 requests per minute for anonymous users

## Pagination

All list endpoints support pagination with the following parameters:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 100)

Response includes pagination metadata:
```json
{
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 100,
    "pages": 10,
    "has_next": true,
    "has_prev": false
  }
}
```
