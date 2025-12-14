import json
import os
from datetime import datetime
from typing import Dict, Any, List
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Обрабатывает сообщения поддержки: получение всех сообщений и отправка новых
    '''
    method: str = event.get('httpMethod', 'GET')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-Admin-Key',
                'Access-Control-Max-Age': '86400'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        if method == 'GET':
            cur.execute('''
                SELECT id, text, sender, timestamp, is_read 
                FROM support_messages 
                ORDER BY timestamp ASC
            ''')
            messages = cur.fetchall()
            
            result = []
            for msg in messages:
                result.append({
                    'id': str(msg['id']),
                    'text': msg['text'],
                    'sender': msg['sender'],
                    'timestamp': msg['timestamp'].isoformat(),
                    'isRead': msg['is_read']
                })
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'messages': result}),
                'isBase64Encoded': False
            }
        
        elif method == 'POST':
            body_data = json.loads(event.get('body', '{}'))
            text = body_data.get('text', '').strip()
            
            headers = event.get('headers', {})
            admin_key = headers.get('x-admin-key') or headers.get('X-Admin-Key')
            expected_admin_key = os.environ.get('ADMIN_KEY')
            
            if expected_admin_key and admin_key == expected_admin_key:
                sender = 'admin'
            else:
                sender = 'user'
            
            if not text:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Text is required'}),
                    'isBase64Encoded': False
                }
            
            cur.execute('''
                INSERT INTO support_messages (text, sender, timestamp)
                VALUES (%s, %s, NOW())
                RETURNING id, text, sender, timestamp
            ''', (text, sender))
            
            new_message = cur.fetchone()
            conn.commit()
            
            return {
                'statusCode': 201,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'id': str(new_message['id']),
                    'text': new_message['text'],
                    'sender': new_message['sender'],
                    'timestamp': new_message['timestamp'].isoformat()
                }),
                'isBase64Encoded': False
            }
        
        return {
            'statusCode': 405,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Method not allowed'}),
            'isBase64Encoded': False
        }
    
    finally:
        cur.close()
        conn.close()