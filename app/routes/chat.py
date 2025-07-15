
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from typing import List, Dict, Optional
from app.utils.Redis import ConversationStore
from app.utils.LLMModel import ChatGLM
from app.utils.EmbbedingModel import ChatEmbeddings
from uuid import uuid4

from app.utils.auth import token_required

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')


# Initialize components
def get_llm():
    """Initialize and return the LLM instance"""
    return ChatGLM(
        model=current_app.config['LLM_MODEL'],
        api_key=current_app.config['LLM_API_KEY'],
        base_url=current_app.config['LLM_BASE_URL'],
        system_prompt=current_app.config['LLM_SYSTEM_PROMPT']
    )


def get_embedding_model():
    """Initialize and return the embedding model"""
    return ChatEmbeddings(
        model=current_app.config['EMBEDDING_MODEL'],
        api_key=current_app.config['LLM_API_KEY'],
        base_url=current_app.config['LLM_BASE_URL']
    )


def get_conversation_store():
    """Initialize and return the conversation store"""
    return ConversationStore(
        host=current_app.config['REDIS_HOST'],
        port=current_app.config['REDIS_PORT'],
        db=current_app.config['REDIS_DB']
    )


@chat_bp.route('/conversations', methods=['GET'])
@token_required
def get_conversations():
    """Get all conversations for a user"""
    user_id = request.current_user_id
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    store = get_conversation_store()
    conversations = store.get_user_conversations(user_id)
    return jsonify({'conversations': conversations})


@chat_bp.route('/conversation', methods=['GET'])
@token_required
def get_conversation():
    """Get a specific conversation"""
    user_id = request.current_user_id
    conversation_id = request.args.get('conversation_id', type=str)

    if not user_id or not conversation_id:
        return jsonify({'error': 'user_id and conversation_id are required'}), 400

    store = get_conversation_store()
    conversation = store.get_single_conversation(user_id, conversation_id)

    if conversation is None:
        return jsonify({'error': 'Conversation not found'}), 404

    return jsonify({'conversation': conversation})


@chat_bp.route('/conversation', methods=['DELETE'])
def delete_conversation():
    """Delete a conversation"""
    user_id = request.json.get('user_id', type=str)
    conversation_id = request.json.get('conversation_id', type=str)

    if not user_id or not conversation_id:
        return jsonify({'error': 'user_id and conversation_id are required'}), 400

    store = get_conversation_store()
    success = store.delete_conversation(user_id, conversation_id)

    return jsonify({'success': success})


@chat_bp.route('/send', methods=['POST'])
@token_required
def send_message():
    """
    Send a message and get response
    Request format:
    {
        "user_id": "user123",
        "conversation_id": "optional_existing_id",
        "message": "Hello, how are you?",
        "new_conversation": false
    }
    """
    data = request.json
    user_id = request.current_user_id
    message = data.get('message')
    conversation_id = data.get('conversation_id', str(uuid4()))
    if not conversation_id:
        conversation_id = str(uuid4())
    new_conversation = data.get('new_conversation', False)

    if not user_id or not message:
        return jsonify({'error': 'user_id and message are required'}), 400

    # Initialize components
    llm = get_llm()
    store = get_conversation_store()

    # Get or initialize conversation history
    if new_conversation:
        conversation_history = []
    else:
        conversation_history = store.get_single_conversation(user_id, conversation_id) or []

    # Add user message to history
    conversation_history.append({
        'role': 'user',
        'content': message,
        'timestamp': datetime.now().isoformat(),
    })

    try:
        # Convert to ChatMessage format for LLM
        chat_messages = [
            ChatMessage(role=msg['role'], content=msg['content'])
            for msg in conversation_history
        ]

        # Get LLM response
        response = llm.chat(chat_messages)

        # Add assistant response to history
        conversation_history.append({
            'role': 'assistant',
            'content': response.message.content,
            'timestamp': datetime.now().isoformat(),
        })

        # Store updated conversation
        store.store_conversation(user_id, conversation_id, conversation_history)

        return jsonify({
            'conversation_id': conversation_id,
            'response': response.message.content,
            'history': conversation_history,
            'metadata': {
                'prompt_tokens': response.additional_kwargs.get('prompt_tokens'),
                'completion_tokens': response.additional_kwargs.get('completion_tokens'),
                'total_tokens': response.additional_kwargs.get('token_counts')
            }
        })

    except Exception as e:
        current_app.logger.error(f"Error in chat: {str(e)}")
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/stream', methods=['POST'])
def stream_message():
    """
    Stream chat response
    Request format same as /send but returns SSE stream
    """
    # Similar implementation to /send but with streaming
    # Would require Server-Sent Events (SSE) implementation
    pass


# Helper class for ChatMessage
class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content