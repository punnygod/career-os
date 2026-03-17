FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install --production

# Copy built app
COPY .next ./.next
COPY public ./public
COPY next.config.js ./

EXPOSE 3000

CMD ["npm", "start"]