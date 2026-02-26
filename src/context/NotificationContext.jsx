import { createContext, useContext, useState } from 'react'

const NotificationContext = createContext(null)

export function NotificationProvider({ children }) {
  const [notifications, setNotifications] = useState([])
  const unreadCount = notifications.filter(n => !n.read).length

  const markAllRead = () =>
    setNotifications(prev => prev.map(n => ({ ...n, read: true })))

  return (
    <NotificationContext.Provider value={{ notifications, setNotifications, unreadCount, markAllRead }}>
      {children}
    </NotificationContext.Provider>
  )
}

export const useNotifications = () => useContext(NotificationContext)
