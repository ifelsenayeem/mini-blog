from flask import Blueprint, request, jsonify
from models import Comment, Post, db
from auth import token_required, optional_token
from sqlalchemy import desc

comments_bp = Blueprint('comments', __name__, url_prefix='/api/comments')

@comments_bp.route('', methods=['GET'])
def get_comments():
    """Get comments for a specific post"""
    try:
        post_id = request.args.get('post_id', type=int)
        
        if not post_id:
            return jsonify({'error': 'post_id is required'}), 400
        
        # Verify post exists
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Get top-level comments (no parent)
        comments = Comment.query.filter_by(
            post_id=post_id,
            parent_id=None,
            is_approved=True
        ).order_by(desc(Comment.created_at)).all()
        
        return jsonify({
            'comments': [comment.to_dict(include_replies=True) for comment in comments]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch comments: {str(e)}'}), 500

@comments_bp.route('', methods=['POST'])
@token_required
def create_comment(current_user):
    """Create a new comment"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('post_id'):
            return jsonify({'error': 'post_id is required'}), 400
        
        if not data.get('content'):
            return jsonify({'error': 'content is required'}), 400
        
        post_id = data['post_id']
        content = data['content'].strip()
        parent_id = data.get('parent_id')
        
        # Verify post exists
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Only allow comments on published posts
        if post.status != 'published':
            return jsonify({'error': 'Cannot comment on unpublished posts'}), 400
        
        # Verify parent comment exists if provided
        if parent_id:
            parent = Comment.query.get(parent_id)
            if not parent or parent.post_id != post_id:
                return jsonify({'error': 'Invalid parent comment'}), 400
        
        # Create comment
        comment = Comment(
            content=content,
            author_id=current_user.id,
            post_id=post_id,
            parent_id=parent_id,
            is_approved=True  # Auto-approve for now
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'message': 'Comment created successfully',
            'comment': comment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create comment: {str(e)}'}), 500

@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@token_required
def update_comment(current_user, comment_id):
    """Update a comment"""
    try:
        comment = Comment.query.get(comment_id)
        
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        
        # Check ownership
        if comment.author_id != current_user.id and not current_user.is_admin:
            return jsonify({'error': 'Unauthorized to edit this comment'}), 403
        
        data = request.get_json()
        
        if 'content' in data:
            comment.content = data['content'].strip()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Comment updated successfully',
            'comment': comment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update comment: {str(e)}'}), 500

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, comment_id):
    """Delete a comment"""
    try:
        comment = Comment.query.get(comment_id)
        
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        
        # Check ownership
        if comment.author_id != current_user.id and not current_user.is_admin:
            return jsonify({'error': 'Unauthorized to delete this comment'}), 403
        
        db.session.delete(comment)
        db.session.commit()
        
        return jsonify({'message': 'Comment deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete comment: {str(e)}'}), 500
