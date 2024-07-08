FROM node:18-alpine AS client-builder
WORKDIR /app
COPY ./cardMakerFE .
RUN rm -rf .svelte-kit build node_modules && \
    npm ci && \
    npm run build && \
    npm prune --production

FROM python:3.12
WORKDIR /app
COPY ./api /app
COPY --from=client-builder /app/build /client
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
EXPOSE 8000
VOLUME [ "/app" ]
CMD ["python", "main.py"]