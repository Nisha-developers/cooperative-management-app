# 🏡 CoopHousing — Cooperative Housing MVP

A React + Tailwind CSS frontend for a cooperative housing management platform.

---

## 📦 Tech Stack

| Tool | Purpose |
|------|---------|
| React 18 | UI Framework |
| React Router v6 | Routing |
| Tailwind CSS | Styling |
| Zustand | State management |
| Axios | API calls |
| React Hot Toast | Notifications |
| date-fns | Date formatting |
| Vite | Build tool |

---

## 🚀 Getting Started

```bash
# 1. Install dependencies
npm install

# 2. Copy env file and fill in your API URL
cp .env.example .env

# 3. Start development server
npm run dev
```

---

## 📁 Folder Structure

```
src/
├── assets/              # Images & icons
├── components/
│   ├── ui/              # Shared UI: Button, Input, Modal, etc.
│   ├── layout/          # Navbar, Footer, Sidebar, Layouts
│   ├── landing/         # Landing page sections
│   ├── auth/            # Auth forms + route guards
│   ├── user/            # User-facing components
│   └── admin/           # Admin panel components
├── pages/
│   ├── public/          # Landing, Contact, 404
│   ├── auth/            # Login, Register
│   ├── user/            # Dashboard, Apartments, Booking, Payment
│   └── admin/           # Admin dashboard & management pages
├── context/             # AuthContext, NotificationContext
├── hooks/               # Custom React hooks
├── services/            # API service layer (axios)
├── store/               # Zustand stores
├── utils/               # Helpers, constants, formatters
└── router/              # Route definitions
```

---

## 🗺️ Route Map

| Route | Page | Access |
|-------|------|--------|
| `/` | Landing Page | Public |
| `/contact` | Contact | Public |
| `/login` | Login | Public |
| `/register` | Register | Public |
| `/dashboard` | User Dashboard | User |
| `/apartments` | Browse Apartments | User |
| `/apartments/:id` | Apartment Detail | User |
| `/booking/:id` | Booking Request | User |
| `/payment/:bookingId` | Upload Payment Proof | User |
| `/notifications` | Notifications | User |
| `/profile` | User Profile | User |
| `/admin` | Admin Dashboard | Admin |
| `/admin/apartments` | Manage Apartments | Admin |
| `/admin/apartments/new` | Add Apartment | Admin |
| `/admin/apartments/edit/:id` | Edit Apartment | Admin |
| `/admin/bookings` | View Booking Requests | Admin |
| `/admin/payments` | Review Payment Proofs | Admin |
| `/admin/users` | Manage Users | Admin |

---

## 🎨 Design System

Colors defined in `tailwind.config.js`:
- `cooperative-green` — Primary brand green
- `cooperative-gold` — Accent / highlights
- `cooperative-cream` — Background
- `cooperative-dark` — Text

---

## 📋 Plans Covered

- ✅ **MVP Base Plan** — User auth, apartments, booking, payment proof upload, admin panel
- 🔲 **Standard Plan** — Agric section, expanded landing, notifications
- 🔲 **Premium Plan** — Loan system, email notifications, advanced admin
