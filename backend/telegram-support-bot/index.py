import json
import os
import requests
from typing import Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = '529416354'

def send_telegram_message(text: str):
    if not TELEGRAM_BOT_TOKEN:
        return
    
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    try:
        requests.post(url, json={
            'chat_id': TELEGRAM_CHAT_ID,
            'text': text,
            'parse_mode': 'HTML'
        }, timeout=5)
    except Exception as e:
        print(f'Telegram send error: {e}')

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Webhook для Telegram бота - обрабатывает команды и отправляет ответы в чат поддержки
    '''
    method: str = event.get('httpMethod', 'POST')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    if method == 'POST':
        body_data = json.loads(event.get('body', '{}'))
        
        if 'message' not in body_data:
            return {'statusCode': 200, 'body': 'OK', 'isBase64Encoded': False}
        
        message = body_data['message']
        chat_id = str(message.get('chat', {}).get('id', ''))
        text = message.get('text', '').strip()
        
        if chat_id != TELEGRAM_CHAT_ID:
            return {'statusCode': 200, 'body': 'Unauthorized', 'isBase64Encoded': False}
        
        if not text:
            return {'statusCode': 200, 'body': 'OK', 'isBase64Encoded': False}
        
        if text.startswith('/'):
            if text == '/start':
                send_telegram_message('👋 Бот поддержки активен!\n\nОтправляйте сообщения, и они появятся в чате поддержки как ответы администратора.')
            elif text == '/history':
                conn = get_db_connection()
                cur = conn.cursor(cursor_factory=RealDictCursor)
                try:
                    cur.execute('''
                        SELECT text, sender, timestamp 
                        FROM support_messages 
                        ORDER BY timestamp DESC 
                        LIMIT 10
                    ''')
                    messages = cur.fetchall()
                    
                    if messages:
                        history_text = '📋 <b>Последние 10 сообщений:</b>\n\n'
                        for msg in reversed(messages):
                            sender_icon = '👤' if msg['sender'] == 'user' else '🛠'
                            time_str = msg['timestamp'].strftime('%H:%M')
                            history_text += f'{sender_icon} <b>{time_str}</b>: {msg["text"]}\n'
                        send_telegram_message(history_text)
                    else:
                        send_telegram_message('Нет сообщений в истории')
                finally:
                    cur.close()
                    conn.close()
            
            return {'statusCode': 200, 'body': 'OK', 'isBase64Encoded': False}
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute('''
                INSERT INTO support_messages (text, sender, timestamp)
                VALUES (%s, %s, NOW())
            ''', (text, 'admin'))
            conn.commit()
            
            send_telegram_message(f'✅ Сообщение отправлено в чат поддержки:\n\n"{text}"')
        finally:
            cur.close()
            conn.close()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'status': 'ok'}),
        'isBase64Encoded': False
    }
