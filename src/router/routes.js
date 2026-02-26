export const ROUTES = {
  HOME: '/',
  CONTACT: '/contact',
  LOGIN: '/login',
  REGISTER: '/register',

  // User
  DASHBOARD: '/dashboard',
  APARTMENTS: '/apartments',
  APARTMENT_DETAIL: '/apartments/:id',
  BOOKING: '/booking/:id',
  PAYMENT_UPLOAD: '/payment/:bookingId',
  NOTIFICATIONS: '/notifications',
  PROFILE: '/profile',

  // Admin
  ADMIN: '/admin',
  ADMIN_APARTMENTS: '/admin/apartments',
  ADMIN_APARTMENTS_NEW: '/admin/apartments/new',
  ADMIN_APARTMENTS_EDIT: '/admin/apartments/edit/:id',
  ADMIN_BOOKINGS: '/admin/bookings',
  ADMIN_PAYMENTS: '/admin/payments',
  ADMIN_USERS: '/admin/users',
}
