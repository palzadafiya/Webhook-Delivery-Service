# Webhook Delivery Service

A robust backend system that functions as a reliable webhook delivery service. This service ingests incoming webhooks, queues them, and attempts delivery to subscribed target URLs, handling failures with retries and providing visibility into the delivery status.

## Deployed links
- **API Link**: http://13.200.222.126:8000/
- **Swagger docs**: http://13.200.222.126:8000/docs

## Features

- **Subscription Management**: CRUD operations for webhook subscriptions
- **Webhook Ingestion**: Accepts incoming webhook payloads with signature verification
- **Asynchronous Delivery**: Background workers process delivery tasks
- **Retry Mechanism**: Exponential backoff with configurable max attempts
- **Delivery Logging**: Comprehensive logging of delivery attempts
- **Log Retention**: Automatic cleanup of old logs
- **Status & Analytics**: Endpoints for monitoring delivery status
- **Event Type Filtering**: Filter webhooks based on event types
- **Payload Signature Verification**: Secure webhook delivery with HMAC-SHA256

## Architecture

### Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Cache & Queue**: Redis
- **Task Queue**: Celery
- **Containerization**: Docker & Docker Compose

### Components

1. **API Service**: Handles HTTP requests and manages subscriptions
2. **Worker Service**: Processes webhook deliveries asynchronously
3. **Database**: Stores subscriptions and delivery logs
4. **Redis**: Caches subscription data and serves as Celery broker

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd webhook-delivery-service
```

2. Create a .env file from the example:
```bash
cp .env.example .env
```
- Edit the .env file to fill in your actual configuration values (e.g., database username, password, secret key, etc.)

3. Start the services:
```bash
docker-compose up -d
```

4. Run database migrations:
```bash
docker-compose run --rm api alembic upgrade head
```

5. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

6. Useful Commands:
- Stop all services
  ```bash
  docker-compose down
  ```
- View logs
  ```bash
  docker-compose logs -f
  ```
  
## API Endpoints

### Subscription Management

- `POST /subscriptions/`: Create a new subscription
- `GET /subscriptions/{subscription_id}`: Get subscription details
- `PUT /subscriptions/{subscription_id}`: Update subscription
- `DELETE /subscriptions/{subscription_id}`: Delete subscription
- `POST /subscriptions/generate-signature`: Generate webhook signature

### Webhook Ingestion

- `POST /ingest/{subscription_id}`: Submit a webhook payload

### Status & Analytics

- `GET /status/{webhook_id}`: Get delivery status for a webhook
- `GET /status/logs/{subscription_id}`: Get delivery logs for a subscription

## Database Schema

### Subscriptions Table
- `id`: Primary key
- `target_url`: Webhook delivery URL
- `secret_key`: Optional secret for signature verification
- `event_types`: Array of allowed event types
- `is_active`: Subscription status
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Delivery Logs Table
- `id`: Primary key
- `subscription_id`: Foreign key to subscriptions
- `webhook_id`: Unique identifier for the webhook
- `event_type`: Type of event
- `payload`: Webhook payload
- `attempt_number`: Retry attempt count
- `status_code`: HTTP response code
- `response_body`: Response from target URL
- `error_message`: Error details if any
- `is_success`: Delivery status
- `created_at`: Creation timestamp

## Indexing Strategy

- Subscriptions: `is_active`, `created_at`
- Delivery Logs: `subscription_id`, `webhook_id`, `created_at`, `is_success`, `event_type`

## Retry Strategy

The service implements exponential backoff for retries:
1. Initial attempt
2. 10 seconds delay
3. 20 seconds delay
4. 40 seconds delay
5. 80 seconds delay
6. 160 seconds delay

Maximum retry attempts are configurable (default: 5).

## Log Retention

Delivery logs are automatically cleaned up after a configurable period (default: 72 hours).

## Cost Estimation

Assuming deployment on AWS:
- EC2 t2.micro (Free Tier): $0/month
- RDS PostgreSQL (Free Tier): $0/month
- ElastiCache Redis (Free Tier): $0/month

Total estimated monthly cost: $0 (Free Tier)

## Testing

Run tests using:
```bash
docker-compose run --rm api pytest
```

## Deployment

The application is containerized and can be deployed to any cloud provider supporting Docker. Example deployment to AWS ECS:

1. Create an ECS cluster
2. Create a task definition
3. Deploy the containers
4. Set up load balancing
5. Configure auto-scaling

## Assumptions

1. Webhook payloads are in JSON format
2. Target URLs support HTTPS
3. Target URLs respond within 10 seconds
4. Event types are case-sensitive
5. Maximum payload size is 1MB

## Credits

- FastAPI: https://fastapi.tiangolo.com/
- Celery: https://docs.celeryq.dev/
- SQLAlchemy: https://www.sqlalchemy.org/
- Docker: https://www.docker.com/

## License

MIT License 
