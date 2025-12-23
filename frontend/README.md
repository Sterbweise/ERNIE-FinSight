# ERNIE FinSight Frontend

Modern React + TypeScript frontend for crypto whitepaper analyzer.

## Setup

1. **Install Dependencies**
```bash
npm install
```

2. **Configure Environment (Optional)**
Create a `.env` file if you need to override the API URL:
```
VITE_API_URL=http://localhost:8000
```

3. **Run Development Server**
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Build for Production

```bash
npm run build
npm run preview
```

## Features

### Upload Page
- Drag-and-drop PDF upload interface
- Real-time upload progress tracking
- Beautiful animations with Framer Motion
- Processing status indicators
- Error handling

### Results Page
- Dashboard-style layout with cards
- Three-tab navigation (Overview, Details, Analysis)
- Executive summary hero section
- Key metrics highlights
- Detailed sections:
  - Value propositions
  - Use cases
  - Technology stack
  - Tokenomics breakdown
  - Roadmap visualization
  - Team & partnerships
  - Risk factors
  - Competitive advantages
  - Overall assessment
- Smooth scroll animations
- Export functionality (placeholder)

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Lucide React** - Beautiful icons

## Design System

### Colors
- Navy: `#0A1128` (background)
- Electric Blue: `#00D9FF` (primary)
- Purple: `#7B2CBF` (accent)
- Gradients: Electric-to-Purple for CTAs

### Typography
- Font: Inter (Google Fonts)
- Headings: Bold, large sizes
- Body: Regular weight, good line height

### Components
- Glassmorphism cards
- Gradient buttons
- Smooth hover effects
- Loading animations
- Skeleton loaders

## Project Structure

```
src/
├── pages/
│   ├── Upload.tsx       # Main upload interface
│   └── Results.tsx      # Analysis results dashboard
├── services/
│   └── api.ts          # API integration
├── App.tsx             # Main app component
├── main.tsx            # Entry point
└── index.css           # Global styles
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

- `POST /api/upload` - Upload whitepaper
- `GET /api/status/{task_id}` - Check processing status
- `GET /api/result/{task_id}` - Retrieve results

The API service includes automatic polling for task completion.

## Development

### Code Style
- TypeScript strict mode enabled
- ESLint for code quality
- Functional components with hooks
- Type-safe API calls

### Adding New Features
1. Create components in `src/components/`
2. Add types to `src/services/api.ts`
3. Update routes in `App.tsx`
4. Style with Tailwind classes

## Notes

- Optimized for desktop viewing
- Mobile responsive (basic)
- Animations enhance UX without blocking
- Error boundaries for graceful failures

