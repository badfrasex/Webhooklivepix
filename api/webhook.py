from http.server import BaseHTTPRequestHandler
import os
import json
import requests
import hmac
import hashlib

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('content-length'))
        body = self.rfile.read(length)
        payload = json.loads(body)

        # Se quiser segurança com HMAC, adicione aqui

        valor = payload.get("valor")
        produto = payload.get("descricao", "Produto")
        nome = payload.get("cliente", {}).get("nome", "Cliente")
        bot_token = os.getenv("7200052677:AAH5flHQqewPMCV9Q8N9hoTlKSjNxciV9lg")
        chat_id = os.getenv("7722803509")

        msg = f"💸 Pagamento confirmado!\n👤 {nome}\n📦 Produto: {produto}\n💰 Valor: R${valor:.2f}"
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage", params={
            "chat_id": chat_id,
            "text": msg
        })

        self.send_response(200)
        self.end_headers()
