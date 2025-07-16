from http.server import BaseHTTPRequestHandler
import hmac
import hashlib
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Configuração de segurança
        WEBHOOK_SECRET = "SUA_CHAVE_SECRETA"  # ⚠️ MESMA do Dashboard LivePix
        BOT_URL = "https://seubot.com/webhook"  # URL do seu bot externo
        
        # 2. Verificar assinatura
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        signature = self.headers['X-Livepix-Signature']
        
        # 3. Cálculo HMAC
        hmac_calculado = hmac.new(
            WEBHOOK_SECRET.encode(),
            post_data,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, hmac_calculado):
            self.send_response(403)
            return self.wfile.write(b"Assinatura inválida")

        # 4. Processar evento
        data = json.loads(post_data)
        if data['event'] == 'payment.completed':
            payment_id = data['resource']['externalReference']
            
            # 5. Encaminhar para seu backend (opcional)
            import requests
            requests.post(BOT_URL, json={
                "payment_id": payment_id,
                "status": "paid"
            }, timeout=5)

        # 6. Responder sucesso
        self.send_response(200)
        self.wfile.write(b"Webhook processado")
