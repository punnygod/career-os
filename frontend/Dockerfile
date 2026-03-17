FROM node:18-alpine

WORKDIR /app

ENV NODE_ENV=production

# Copy only needed files
COPY package*.json ./
RUN npm install --omit=dev

# Copy built app
COPY .next ./.next
COPY public ./public
COPY node_modules ./node_modules

EXPOSE 3000

CMD ["npm", "start"]