import redis
import json
from typing import List, Dict, Optional


class ConversationStore:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 2):
        """初始化Redis连接"""
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True  # 自动解码字节数据为字符串
        )

    def get_redis_client(self):
        """获取Redis客户端实例"""
        return self.redis_client

    def store_conversation(self, user_id: str, conversation_id: str, messages: List[Dict]) -> bool:
        """
        存储用户的一次对话历史
        :param user_id: 用户ID
        :param conversation_id: 对话ID
        :param messages: 消息列表，格式如 [{"role": "user", "content": "hello"}, ...]
        :return: 是否存储成功
        """
        try:
            # 使用哈希结构存储对话，key格式为 user:{user_id}:conversations
            key = f"user:{user_id}:conversations"
            # 将消息列表转为JSON字符串存储
            self.redis_client.hset(key, conversation_id, json.dumps(messages))
            return True
        except Exception as e:
            print(f"存储对话历史失败: {e}")
            return False

    def get_user_conversations(self, user_id: str) -> List[Dict]:
        """
        获取用户的所有对话历史
        :param user_id: 用户ID
        :return: 字典格式 {conversation_id: messages}
        """
        try:
            key = f"user:{user_id}:conversations"
            # 获取用户的所有对话
            conversations = self.redis_client.hgetall(key)
            # 将JSON字符串转换回Python对象
            return [{"id": conv_id, "messages": json.loads(messages), "lastTime": json.loads(messages)[-1]["timestamp"]} for conv_id, messages in conversations.items()]
        except Exception as e:
            print(f"获取用户对话历史失败: {e}")
            return []

    def get_single_conversation(self, user_id: str, conversation_id: str) -> Optional[List[Dict]]:
        """
        获取用户的特定对话历史
        :param user_id: 用户ID
        :param conversation_id: 对话ID
        :return: 消息列表或None(如果不存在)
        """
        try:
            key = f"user:{user_id}:conversations"
            messages_json = self.redis_client.hget(key, conversation_id)
            if messages_json:
                return json.loads(messages_json)
            return None
        except Exception as e:
            print(f"获取特定对话历史失败: {e}")
            return None

    def delete_conversation(self, user_id: str, conversation_id: str) -> bool:
        """
        删除用户的特定对话
        :param user_id: 用户ID
        :param conversation_id: 对话ID
        :return: 是否删除成功
        """
        try:
            key = f"user:{user_id}:conversations"
            deleted = self.redis_client.hdel(key, conversation_id)
            return deleted > 0
        except Exception as e:
            print(f"删除对话失败: {e}")
            return False

if __name__  == '__main__':
    # 创建Redis客户端实例
    redis_client = ConversationStore()

    # 存储对话
    user_id = 1
    conversation_id = 'test_conversation'
    messages = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "How are you?"},
        {"role": "assistant", "content": "I'm doing well, thanks!"}
    ]
    # redis_client.store_conversation(user_id, conversation_id, messages)
    print(redis_client.get_user_conversations(user_id))
    # print(redis_client.get_single_conversation(user_id, conversation_id))
    # print(redis_client.delete_conversation(user_id, conversation_id))
    # print(redis_client.get_user_conversations(user_id))