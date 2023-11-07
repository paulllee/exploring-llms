CHAT_CSS: str = """
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .message {
  color: #fff;
}
</style>
"""

BOT_TEMPLATE: str = """
<div class="chat-message bot">
    <div class="message">AI: {{MSG}}</div>
</div>
"""

USER_TEMPLATE: str = """
<div class="chat-message user">
    <div class="message">You: {{MSG}}</div>
</div>
"""
