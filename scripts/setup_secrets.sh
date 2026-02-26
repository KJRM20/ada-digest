#!/bin/bash

# Script de configuración de secretos OAuth para Render
# 
# Render no soporta archivos de secretos en el build, por lo que
# los archivos OAuth de Gmail deben subirse manualmente vía Shell.
#
# PREREQUISITOS:
# 1. Servicio de Ada ya desplegado en Render
# 2. Archivos locales .secrets/client_secret.json y .secrets/gmail-token.json
#
# INSTRUCCIONES:
#
# Paso 1: Acceder al Shell de Render
# ===================================
# 1. Ve a tu servicio en Render Dashboard: https://dashboard.render.com
# 2. Selecciona "ada-scheduler"
# 3. Click en "Shell" en el menú lateral
# 4. Espera a que cargue la terminal interactiva
#
# Paso 2: Crear directorio .secrets
# ==================================
# En el shell de Render, ejecuta:
#
#   mkdir -p .secrets
#
# Paso 3: Crear archivos de secretos
# ===================================
# Copia el contenido de tus archivos locales y créalos en Render:
#
# Para client_secret.json:
#   cat > .secrets/client_secret.json << 'EOF'
#   {
#     "installed": {
#       "client_id": "TU_CLIENT_ID.apps.googleusercontent.com",
#       "project_id": "tu-proyecto",
#       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#       "token_uri": "https://oauth2.googleapis.com/token",
#       "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#       "client_secret": "TU_CLIENT_SECRET",
#       "redirect_uris": ["http://localhost"]
#     }
#   }
#   EOF
#
# Para gmail-token.json:
#   cat > .secrets/gmail-token.json << 'EOF'
#   {
#     "access_token": "tu-access-token",
#     "client_id": "TU_CLIENT_ID.apps.googleusercontent.com",
#     "client_secret": "TU_CLIENT_SECRET",
#     "refresh_token": "tu-refresh-token",
#     "token_expiry": "2026-01-01T00:00:00Z",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "user_agent": null,
#     "revoke_uri": "https://oauth2.googleapis.com/revoke",
#     "id_token": null,
#     "id_token_jwt": null,
#     "token_response": { ... },
#     "scopes": ["https://www.googleapis.com/auth/gmail.send"],
#     "token_info_uri": "https://oauth2.googleapis.com/tokeninfo",
#     "invalid": false,
#     "_class": "OAuth2Credentials",
#     "_module": "oauth2client.client"
#   }
#   EOF
#
# Paso 4: Verificar archivos creados
# ===================================
#   ls -la .secrets/
#   cat .secrets/client_secret.json | head -n 5
#
# Paso 5: Reiniciar el servicio
# ==============================
# 1. Ve a "Settings" en el dashboard
# 2. Click en "Manual Deploy" → "Clear build cache & deploy"
# 3. Espera a que el servicio reinicie
# 4. Verifica logs para confirmar que simplegmail carga los tokens
#
# NOTAS:
# ======
# - Los archivos en .secrets/ NO persisten entre deployments
# - Si haces redeploy, debes repetir este proceso
# - Alternativamente, usa variables de entorno con el JSON completo
#   (menos seguro pero persiste entre deployments)
#
# ALTERNATIVA: Variables de entorno
# ==================================
# Si prefieres usar env vars en lugar de archivos:
#
# 1. En Render Dashboard → Environment → Add Environment Variable
# 2. GMAIL_CLIENT_SECRET_JSON = (pega el JSON completo de client_secret.json)
# 3. GMAIL_TOKEN_JSON = (pega el JSON completo de gmail-token.json)
# 4. Modifica el código para leer de env vars en lugar de archivos

echo "⚠️  Este es un script de DOCUMENTACIÓN, no ejecutable directamente."
echo "📖 Lee las instrucciones arriba y ejecútalas manualmente en Render Shell."
