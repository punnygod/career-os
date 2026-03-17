FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
# Next.js requires typescript to load next.config.ts at runtime
RUN npm install --production && npm install typescript @types/node @types/react --no-save

# Copy built app
COPY .next ./.next
COPY public ./public
# Use wildcard to avoid not found errors if the extension varies
COPY next.config.* ./

EXPOSE 3000

CMD ["npm", "start"]