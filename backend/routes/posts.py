from flask import Blueprint, request, jsonify
from models import Post, Category, Tag, db, post_tags
from auth import token_required, optional_token
from datetime import datetime
from sqlalchemy import or_, desc
import re

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')

def create_slug(title):
    """Create URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

def ensure_unique_slug(slug, post_id=None):
    """Ensure slug is unique by adding number if necessary"""
    original_slug = slug
    counter = 1
    
    while True:
        query = Post.query.filter_by(slug=slug)
        if post_id:
            query = query.filter(Post.id != post_id)
        
        if not query.first():
            return slug
        
        slug = f"{original_slug}-{counter}"
        counter += 1

@posts_bp.route('', methods=['GET'])
@optional_token
def get_posts(current_user):
    """Get all posts with pagination and filtering"""
    try:
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)  # Max 100 per page
        
        # Filters
        status = request.args.get('status', 'published')
        category_id = request.args.get('category_id', type=int)
        tag_id = request.args.get('tag_id', type=int)
        author_id = request.args.get('author_id', type=int)
        search = request.args.get('search', '').strip()
        
        # Build query
        query = Post.query
        
        # Status filter - only show published posts to non-owners
        if current_user:
            # Logged in users can see their own drafts
            query = query.filter(
                or_(
                    Post.status == status,
                    Post.author_id == current_user.id
                )
            )
        else:
            # Public users only see published posts
            query = query.filter_by(status='published')
        
        # Category filter
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        # Tag filter
        if tag_id:
            query = query.filter(Post.tags.any(Tag.id == tag_id))
        
        # Author filter
        if author_id:
            query = query.filter_by(author_id=author_id)
        
        # Search filter
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Post.title.like(search_pattern),
                    Post.content.like(search_pattern),
                    Post.excerpt.like(search_pattern)
                )
            )
        
        # Order by published date, newest first
        query = query.order_by(desc(Post.created_at))
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        posts = [post.to_dict() for post in pagination.items]
        
        return jsonify({
            'posts': posts,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch posts: {str(e)}'}), 500

@posts_bp.route('/<int:post_id>', methods=['GET'])
@optional_token
def get_post(current_user, post_id):
    """Get single post by ID"""
    try:
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Check access permissions
        if post.status != 'published':
            if not current_user or post.author_id != current_user.id:
                return jsonify({'error': 'Post not found'}), 404
        
        # Increment view count
        post.view_count += 1
        db.session.commit()
        
        return jsonify({
            'post': post.to_dict(include_content=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch post: {str(e)}'}), 500

@posts_bp.route('/slug/<slug>', methods=['GET'])
@optional_token
def get_post_by_slug(current_user, slug):
    """Get single post by slug"""
    try:
        post = Post.query.filter_by(slug=slug).first()
        
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Check access permissions
        if post.status != 'published':
            if not current_user or post.author_id != current_user.id:
                return jsonify({'error': 'Post not found'}), 404
        
        # Increment view count
        post.view_count += 1
        db.session.commit()
        
        return jsonify({
            'post': post.to_dict(include_content=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch post: {str(e)}'}), 500

@posts_bp.route('', methods=['POST'])
@token_required
def create_post(current_user):
    """Create a new post"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        if not data.get('content'):
            return jsonify({'error': 'Content is required'}), 400
        
        title = data['title'].strip()
        content = data['content'].strip()
        
        # Create slug from title
        slug = create_slug(data.get('slug', title))
        slug = ensure_unique_slug(slug)
        
        # Create excerpt if not provided
        excerpt = data.get('excerpt', '')
        if not excerpt and content:
            # Take first 200 characters as excerpt
            excerpt = content[:200] + '...' if len(content) > 200 else content
        
        # Create post
        post = Post(
            title=title,
            slug=slug,
            content=content,
            excerpt=excerpt,
            featured_image=data.get('featured_image'),
            status=data.get('status', 'draft'),
            author_id=current_user.id,
            category_id=data.get('category_id')
        )
        
        # Set published date if publishing
        if post.status == 'published' and not post.published_at:
            post.published_at = datetime.utcnow()
        
        db.session.add(post)
        db.session.flush()  # Get post ID
        
        # Add tags
        if data.get('tags'):
            for tag_data in data['tags']:
                if isinstance(tag_data, int):
                    tag = Tag.query.get(tag_data)
                elif isinstance(tag_data, str):
                    tag_name = tag_data.strip()
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag_slug = create_slug(tag_name)
                        tag = Tag(name=tag_name, slug=tag_slug)
                        db.session.add(tag)
                
                if tag and tag not in post.tags:
                    post.tags.append(tag)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Post created successfully',
            'post': post.to_dict(include_content=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create post: {str(e)}'}), 500

@posts_bp.route('/<int:post_id>', methods=['PUT'])
@token_required
def update_post(current_user, post_id):
    """Update a post"""
    try:
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Check ownership
        if post.author_id != current_user.id and not current_user.is_admin:
            return jsonify({'error': 'Unauthorized to edit this post'}), 403
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            post.title = data['title'].strip()
            # Update slug if title changed
            if 'slug' in data:
                new_slug = create_slug(data['slug'])
            else:
                new_slug = create_slug(post.title)
            post.slug = ensure_unique_slug(new_slug, post.id)
        
        if 'content' in data:
            post.content = data['content'].strip()
        
        if 'excerpt' in data:
            post.excerpt = data['excerpt'].strip()
        
        if 'featured_image' in data:
            post.featured_image = data['featured_image']
        
        if 'category_id' in data:
            post.category_id = data['category_id']
        
        # Update status and set published date
        if 'status' in data:
            old_status = post.status
            post.status = data['status']
            
            # Set published date when first published
            if post.status == 'published' and old_status != 'published':
                post.published_at = datetime.utcnow()
        
        # Update tags
        if 'tags' in data:
            post.tags = []  # Clear existing tags
            for tag_data in data['tags']:
                if isinstance(tag_data, int):
                    tag = Tag.query.get(tag_data)
                elif isinstance(tag_data, str):
                    tag_name = tag_data.strip()
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag_slug = create_slug(tag_name)
                        tag = Tag(name=tag_name, slug=tag_slug)
                        db.session.add(tag)
                
                if tag:
                    post.tags.append(tag)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Post updated successfully',
            'post': post.to_dict(include_content=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update post: {str(e)}'}), 500

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    """Delete a post"""
    try:
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Check ownership
        if post.author_id != current_user.id and not current_user.is_admin:
            return jsonify({'error': 'Unauthorized to delete this post'}), 403
        
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({'message': 'Post deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete post: {str(e)}'}), 500
