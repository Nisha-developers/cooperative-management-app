import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from '@/context/AuthContext'
import { NotificationProvider } from '@/context/NotificationContext'

// Public
import LandingPage from '@/pages/public/LandingPage'
import ContactPage from '@/pages/public/ContactPage'
import NotFoundPage from '@/pages/public/NotFoundPage'

// Auth
import LoginPage from '@/pages/auth/LoginPage'
import RegisterPage from '@/pages/auth/RegisterPage'

// User
import UserDashboardPage from '@/pages/user/UserDashboardPage'
import ApartmentsPage from '@/pages/user/ApartmentsPage'
import ApartmentDetailPage from '@/pages/user/ApartmentDetailPage'
import BookingRequestPage from '@/pages/user/BookingRequestPage'
import PaymentUploadPage from '@/pages/user/PaymentUploadPage'
import UserNotificationsPage from '@/pages/user/UserNotificationsPage'
import UserProfilePage from '@/pages/user/UserProfilePage'

// Admin
import AdminDashboardPage from '@/pages/admin/AdminDashboardPage'
import ManageApartmentsPage from '@/pages/admin/ManageApartmentsPage'
import AddEditApartmentPage from '@/pages/admin/AddEditApartmentPage'
import ViewBookingRequestsPage from '@/pages/admin/ViewBookingRequestsPage'
import ReviewPaymentsPage from '@/pages/admin/ReviewPaymentsPage'
import ManageUsersPage from '@/pages/admin/ManageUsersPage'

import ProtectedRoute from '@/components/auth/ProtectedRoute'
import AdminRoute from '@/components/auth/AdminRoute'

function App() {
  return (
    <AuthProvider>
      <NotificationProvider>
        <Routes>
          {/* Public */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/contact" element={<ContactPage />} />

          {/* Auth */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* User (protected) */}
          <Route path="/dashboard" element={<ProtectedRoute><UserDashboardPage /></ProtectedRoute>} />
          <Route path="/apartments" element={<ProtectedRoute><ApartmentsPage /></ProtectedRoute>} />
          <Route path="/apartments/:id" element={<ProtectedRoute><ApartmentDetailPage /></ProtectedRoute>} />
          <Route path="/booking/:id" element={<ProtectedRoute><BookingRequestPage /></ProtectedRoute>} />
          <Route path="/payment/:bookingId" element={<ProtectedRoute><PaymentUploadPage /></ProtectedRoute>} />
          <Route path="/notifications" element={<ProtectedRoute><UserNotificationsPage /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><UserProfilePage /></ProtectedRoute>} />

          {/* Admin (protected + admin role) */}
          <Route path="/admin" element={<AdminRoute><AdminDashboardPage /></AdminRoute>} />
          <Route path="/admin/apartments" element={<AdminRoute><ManageApartmentsPage /></AdminRoute>} />
          <Route path="/admin/apartments/new" element={<AdminRoute><AddEditApartmentPage /></AdminRoute>} />
          <Route path="/admin/apartments/edit/:id" element={<AdminRoute><AddEditApartmentPage /></AdminRoute>} />
          <Route path="/admin/bookings" element={<AdminRoute><ViewBookingRequestsPage /></AdminRoute>} />
          <Route path="/admin/payments" element={<AdminRoute><ReviewPaymentsPage /></AdminRoute>} />
          <Route path="/admin/users" element={<AdminRoute><ManageUsersPage /></AdminRoute>} />

          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </NotificationProvider>
    </AuthProvider>
  )
}

export default App
