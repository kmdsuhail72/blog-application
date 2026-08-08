# Frontend Service

This is the frontend service for the Blog Platform.
It is built with React, Vite, TypeScript, Tailwind CSS, and React Query.

## Purpose

- User-facing blog interface
- Account registration and login
- Email verification flow
- Post browsing, creation, and editing
- File upload support

## Stack

- React 19
- Vite
- TypeScript
- Tailwind CSS
- React Router
- React Hook Form
- React Query
- Axios

## Local development

### Install dependencies

```powershell
cd frontend
npm install
```

### Run development server

```powershell
npm run dev
```

By default, Vite runs on `http://localhost:5173`.

### Build for production

```powershell
npm run build
```

### Preview production build

```powershell
npm run preview
```

## Docker

This app is containerized with Docker and served through NGINX.

### Build and run

```powershell
docker compose up -d --build frontend
```

## Environment

The frontend uses `VITE_API_URL` to route API calls.
For the local Docker Compose setup, use:

```env
VITE_API_URL=/api
```

## Key files

- `frontend/src/api/auth.ts` — auth requests
- `frontend/src/context/AuthContext.tsx` — auth state management
- `frontend/src/components/forms/RegisterForm.tsx` — registration UI
- `frontend/src/main.tsx` — app bootstrap
- `frontend/vite.config.ts` — Vite configuration

## Architecture

This frontend is a single-page app that talks to the backend via `/api`.
The backend is proxied by NGINX at `http://localhost:8080`.

## Notes

- The frontend is served on port `80` inside the container and exposed via NGINX on port `8080`.
- React Router handles client-side navigation.
- JWT tokens are managed by the auth context and sent to protected endpoints.
