FROM node:22-alpine

WORKDIR /app

# Instala dependencias en una capa aparte para aprovechar la caché de Docker:
# solo se reinstalan si cambia package.json o package-lock.json
COPY package.json package-lock.json ./
RUN npm ci

# El código fuente se monta como volumen en desarrollo (ver docker-compose.yml),
# esta copia sirve para poder usar la imagen también sin compose
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
