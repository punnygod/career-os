FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --production

# Copy built app
COPY .next ./.next
COPY public ./public
# Use wildcard to avoid not found errors if the extension varies
COPY next.config.* ./

EXPOSE 3000

CMD ["npm", "start"]