from flask import Blueprint, request, jsonify
from models import Category, Tag, db
from auth import token_required, admin_required
import re

categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')
tags_bp = Blueprint('tags', __name__, url_prefix='/api/tags')

def create_slug(name):
    """Create URL-friendly slug from name"""
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

# ===== CATEGORIES =====

@categories_bp.route('', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = Category.query.order_by(Category.name).all()
        return jsonify({
            'categories': [cat.to_dict() for cat in categories]
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch categories: {str(e)}'}), 500

@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get single category"""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        return jsonify({
            'category': category.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch category: {str(e)}'}), 500

@categories_bp.route('', methods=['POST'])
@token_required
@admin_required
def create_category(current_user):
    """Create a new category (admin only)"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        name = data['name'].strip()
        slug = create_slug(data.get('slug', name))
        
        # Check if category already exists
        if Category.query.filter_by(name=name).first():
            return jsonify({'error': 'Category already exists'}), 400
        
        if Category.query.filter_by(slug=slug).first():
            return jsonify({'error': 'Slug already exists'}), 400
        
        category = Category(
            name=name,
            slug=slug,
            description=data.get('description', '').strip()
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create category: {str(e)}'}), 500

@categories_bp.route('/<int:category_id>', methods=['PUT'])
@token_required
@admin_required
def update_category(current_user, category_id):
    """Update a category (admin only)"""
    try:
        category = Category.query.get(category_id)
        
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            name = data['name'].strip()
            # Check if name is taken by another category
            existing = Category.query.filter_by(name=name).first()
            if existing and existing.id != category_id:
                return jsonify({'error': 'Category name already exists'}), 400
            category.name = name
        
        if 'slug' in data:
            slug = create_slug(data['slug'])
            # Check if slug is taken by another category
            existing = Category.query.filter_by(slug=slug).first()
            if existing and existing.id != category_id:
                return jsonify({'error': 'Slug already exists'}), 400
            category.slug = slug
        
        if 'description' in data:
            category.description = data['description'].strip()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Category updated successfully',
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update category: {str(e)}'}), 500

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_category(current_user, category_id):
    """Delete a category (admin only)"""
    try:
        category = Category.query.get(category_id)
        
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Check if category has posts
        if category.posts.count() > 0:
            return jsonify({'error': 'Cannot delete category with posts'}), 400
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({'message': 'Category deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete category: {str(e)}'}), 500

# ===== TAGS =====

@tags_bp.route('', methods=['GET'])
def get_tags():
    """Get all tags"""
    try:
        tags = Tag.query.order_by(Tag.name).all()
        return jsonify({
            'tags': [tag.to_dict() for tag in tags]
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch tags: {str(e)}'}), 500

@tags_bp.route('/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    """Get single tag"""
    try:
        tag = Tag.query.get(tag_id)
        if not tag:
            return jsonify({'error': 'Tag not found'}), 404
        
        return jsonify({
            'tag': tag.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch tag: {str(e)}'}), 500

@tags_bp.route('', methods=['POST'])
@token_required
def create_tag(current_user):
    """Create a new tag"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        name = data['name'].strip()
        slug = create_slug(data.get('slug', name))
        
        # Check if tag already exists
        existing_tag = Tag.query.filter_by(name=name).first()
        if existing_tag:
            return jsonify({
                'message': 'Tag already exists',
                'tag': existing_tag.to_dict()
            }), 200
        
        if Tag.query.filter_by(slug=slug).first():
            return jsonify({'error': 'Slug already exists'}), 400
        
        tag = Tag(name=name, slug=slug)
        
        db.session.add(tag)
        db.session.commit()
        
        return jsonify({
            'message': 'Tag created successfully',
            'tag': tag.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create tag: {str(e)}'}), 500

@tags_bp.route('/<int:tag_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_tag(current_user, tag_id):
    """Delete a tag (admin only)"""
    try:
        tag = Tag.query.get(tag_id)
        
        if not tag:
            return jsonify({'error': 'Tag not found'}), 404
        
        db.session.delete(tag)
        db.session.commit()
        
        return jsonify({'message': 'Tag deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete tag: {str(e)}'}), 500
