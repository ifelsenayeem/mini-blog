import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { postsAPI, commentsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { format } from 'date-fns';

const PostDetail = () => {
  const { slug } = useParams();
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [commentText, setCommentText] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchPost();
  }, [slug]);

  const fetchPost = async () => {
    try {
      setLoading(true);
      const response = await postsAPI.getPostBySlug(slug);
      setPost(response.data.post);
      
      // Fetch comments
      const commentsResponse = await commentsAPI.getComments(response.data.post.id);
      setComments(commentsResponse.data.comments);
      
      setError('');
    } catch (err) {
      setError('Post not found');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    setSubmitting(true);
    try {
      await commentsAPI.createComment({
        post_id: post.id,
        content: commentText,
      });
      setCommentText('');
      // Refresh comments
      const commentsResponse = await commentsAPI.getComments(post.id);
      setComments(commentsResponse.data.comments);
    } catch (err) {
      alert('Failed to post comment');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this post?')) return;

    try {
      await postsAPI.deletePost(post.id);
      navigate('/');
    } catch (err) {
      alert('Failed to delete post');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="container mx-auto px-4 py-12 text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Post Not Found</h2>
        <Link to="/" className="text-primary-600 hover:text-primary-700">
          Go back to home
        </Link>
      </div>
    );
  }

  const canEdit = user && (user.id === post.author.id || user.is_admin);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <article className="container mx-auto px-4 max-w-4xl">
        {/* Post Header */}
        <div className="bg-white rounded-lg shadow-sm p-8 mb-6">
          {post.category && (
            <span className="inline-block text-sm font-semibold text-primary-600 bg-primary-50 px-3 py-1 rounded mb-4">
              {post.category.name}
            </span>
          )}
          
          <h1 className="text-4xl font-bold text-gray-900 mb-4">{post.title}</h1>
          
          <div className="flex items-center justify-between border-b pb-4 mb-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                <span className="text-gray-600 font-medium">
                  {post.author?.username?.charAt(0).toUpperCase()}
                </span>
              </div>
              <div>
                <p className="font-medium text-gray-900">{post.author?.full_name || post.author?.username}</p>
                <p className="text-sm text-gray-500">
                  {post.published_at && format(new Date(post.published_at), 'MMMM dd, yyyy')}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-6 text-sm text-gray-500">
              <span>👁 {post.view_count} views</span>
              <span>💬 {comments.length} comments</span>
            </div>
          </div>

          {canEdit && (
            <div className="flex space-x-2 mb-6">
              <Link
                to={`/edit-post/${post.id}`}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
              >
                Edit Post
              </Link>
              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
              >
                Delete Post
              </button>
            </div>
          )}

          {post.featured_image && (
            <img
              src={post.featured_image}
              alt={post.title}
              className="w-full h-96 object-cover rounded-lg mb-6"
            />
          )}

          <div
            className="prose max-w-none"
            dangerouslySetInnerHTML={{ __html: post.content }}
          />

          {post.tags && post.tags.length > 0 && (
            <div className="mt-6 pt-6 border-t">
              <div className="flex flex-wrap gap-2">
                {post.tags.map((tag) => (
                  <span
                    key={tag.id}
                    className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full"
                  >
                    #{tag.name}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Comments Section */}
        <div className="bg-white rounded-lg shadow-sm p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Comments ({comments.length})
          </h2>

          {isAuthenticated ? (
            <form onSubmit={handleCommentSubmit} className="mb-8">
              <textarea
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                placeholder="Write a comment..."
                rows="4"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
              <button
                type="submit"
                disabled={submitting || !commentText.trim()}
                className="mt-2 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition disabled:opacity-50"
              >
                {submitting ? 'Posting...' : 'Post Comment'}
              </button>
            </form>
          ) : (
            <div className="mb-8 p-4 bg-gray-50 rounded-lg text-center">
              <p className="text-gray-600">
                <Link to="/login" className="text-primary-600 hover:text-primary-700">
                  Log in
                </Link>{' '}
                to post a comment
              </p>
            </div>
          )}

          <div className="space-y-6">
            {comments.map((comment) => (
              <Comment key={comment.id} comment={comment} />
            ))}
          </div>
        </div>
      </article>
    </div>
  );
};

const Comment = ({ comment }) => {
  return (
    <div className="flex space-x-4">
      <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center flex-shrink-0">
        <span className="text-gray-600 font-medium text-sm">
          {comment.author?.username?.charAt(0).toUpperCase()}
        </span>
      </div>
      <div className="flex-1">
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="font-medium text-gray-900">{comment.author?.username}</span>
            <span className="text-sm text-gray-500">
              {format(new Date(comment.created_at), 'MMM dd, yyyy')}
            </span>
          </div>
          <p className="text-gray-700">{comment.content}</p>
        </div>
      </div>
    </div>
  );
};

export default PostDetail;
