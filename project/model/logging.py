import os
import requests
from datetime import datetime


def insert_logging(summary: str, binds: list, description: str = '', level: str = 'info'):
    try:
        requests.post(os.getenv('API_HOST') +'logging', json={
            'summary': summary,
            'description': description,
            'created_at': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'level': level, 
            'binds': binds
        })
        
    except requests.exceptions.RequestException as e:
        pass