# Verdinho 🌱

A modern plant identification and recommendation application built with SvelteKit, AI-powered plant analysis, and interactive maps.

## 🚀 Quick Start with Docker (Recommended for non-developers)

If you're not familiar with web development or just want to quickly run the application, use Docker:

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system
- [Docker Compose](https://docs.docker.com/compose/install/) (usually comes with Docker Desktop)

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd verdinho
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

3. **Edit the `.env` file and add your API keys:**
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   VITE_API_URL=http://127.0.0.1:8000
   ```

4. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

5. **Access the application:**
   Open your browser and go to `http://localhost:3000`

6. **Stop the application:**
   ```bash
   docker-compose down
   ```

## 🛠️ Local Development Setup

For developers who want to run the project locally and make modifications:

### Prerequisites

- [Node.js](https://nodejs.org/) (version 18 or higher)
- [pnpm](https://pnpm.io/) package manager
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd verdinho
   ```

2. **Install dependencies:**
   ```bash
   pnpm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

4. **Configure your environment variables in `.env`:**
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   VITE_API_URL=http://127.0.0.1:8000
   ```

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Your Google Gemini API key for AI plant identification | ✅ Yes | - |
| `VITE_API_URL` | Backend API URL for plant data services | ✅ Yes | `http://127.0.0.1:8000` |

#### Getting a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key" and create a new API key
4. Copy the API key and paste it in your `.env` file

### Available Scripts

```bash
# Start development server
pnpm dev

# Start development server and open in browser
pnpm dev -- --open

# Build for production
pnpm build

# Preview production build
pnpm preview

# Format code
pnpm format

# Lint code
pnpm lint

# Type checking
pnpm check

# Database operations (if using database features)
pnpm db:push    # Push schema changes
pnpm db:migrate # Run migrations
pnpm db:studio  # Open database studio
```

### Development Workflow

1. **Start the development server:**
   ```bash
   pnpm dev
   ```

2. **Open your browser:**
   Navigate to `http://localhost:5173` (or the port shown in your terminal)

3. **Make your changes:**
   The server will automatically reload when you save files

## 🏗️ Project Structure

```
verdinho/
├── src/
│   ├── lib/
│   │   ├── components/     # Reusable UI components
│   │   ├── server/        # Server-side utilities
│   │   ├── stores/        # Svelte stores for state management
│   │   └── types/         # TypeScript type definitions
│   ├── routes/            # SvelteKit routes and API endpoints
│   │   └── api/          # API routes
│   └── services/         # External service integrations
├── static/               # Static assets
├── docker-compose.yml    # Docker Compose configuration
├── dockerfile           # Docker image definition
└── package.json         # Project dependencies and scripts
```

## 🐳 Docker Details

### Development with Docker

If you want to use Docker for development:

```bash
# Build the Docker image
docker build -t verdinho .

# Run the container
docker run -p 3000:3000 --env-file .env verdinho
```

### Docker Compose Services

- **verdinho-app**: The main application container
  - Exposes port 3000
  - Automatically loads environment variables from `.env`
  - Restarts automatically unless stopped

## 🔧 Troubleshooting

### Common Issues

1. **Port already in use:**
   - Change the port in docker-compose.yml: `ports: - '3001:3000'`
   - Or stop the service using the port

2. **Environment variables not loading:**
   - Make sure your `.env` file is in the root directory
   - Check that variable names match exactly (case-sensitive)
   - Restart the development server after changing environment variables

3. **Docker build fails:**
   - Make sure Docker is running
   - Try rebuilding without cache: `docker-compose build --no-cache`

4. **API key issues:**
   - Verify your Gemini API key is valid
   - Check API quotas in Google AI Studio
   - Ensure the key has proper permissions

### Getting Help

1. Check the browser console for error messages
2. Check Docker logs: `docker-compose logs verdinho-app`
3. Check development server logs in your terminal

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests and linting: `pnpm lint && pnpm check`
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to your branch: `git push origin feature-name`
7. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
