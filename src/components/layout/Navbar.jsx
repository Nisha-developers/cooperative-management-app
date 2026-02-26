// Importation of All the react Components begins
import React, { useState, useEffect, useRef } from 'react'
import { CiMenuBurger } from "react-icons/ci"
import { IoIosClose } from "react-icons/io"
import { createPortal } from "react-dom"
import { Link } from 'react-router-dom'
import { FaCaretUp } from "react-icons/fa";
import Dropdown from '../ui/Dropdown'
// Importation of All the react Components Ends

const navLinks = [
  { label: 'About us', href: '#aboutus' },
  { label: 'Our Services', href: '#services' },
  // { label: 'Cooperative', href: '#cooperative' }, 
  // // { label: 'Apartment', href: '#apartments' },
]
const secondBatch = [
  { label: 'FAQ', href: '#faq' },
  { label: 'Contact us', href: '#contactus' },
]
const cooperativeItems = [
  { label: "Credit and Thrift", href: "credit" },
  { label: "Agricultural", href: "#agric" },
];

const apartmentItems = [
  { label: "Buy Apartment", href: "#buy" },
  { label: "Rent Apartment", href: "#rent" },
];

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const [activeSection, setActiveSection] = useState("")
  const menuRef = useRef(null)

  // Listen for scroll to add background blur + shadow
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 30)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // IntersectionObserver — sets activeSection to whichever section is in view
  useEffect(() => {
    const sections = document.querySelectorAll("section[id]")

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id)
          }
        })
      },
      {
        rootMargin: "-40% 0px -55% 0px",
        threshold: 0,
      }
    )

    sections.forEach((section) => observer.observe(section))
    return () => observer.disconnect()
  }, [])
// Add a handler to clear active section when dropdown opens
function handleDropdownOpen() {
  setActiveSection("")
}
  // Close mobile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setIsOpen(false)
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
      document.body.style.overflow = ''
    }
  }, [isOpen])

  // Close mobile menu on ESC key
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') setIsOpen(false)
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  function handleToggle() {
    setIsOpen((prev) => !prev)
  }

  function handleNavClick() {
    setIsOpen(false)
  }

  return (
    <>
      {/* ─── DESKTOP + TABLET NAVBAR ─── */}
      <header
        className={`fixed top-0 left-0 right-0 z-[999] transition-all duration-500 ease-in-out
          ${scrolled
            ? 'bg-cooperative-dark/90 backdrop-blur-xl shadow-lg shadow-cooperative-dark/20 py-2'
            : 'bg-transparent py-4'
          }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center">

          {/* ─── LOGO ─── */}
          <Link to="/" className="group flex flex-col leading-tight">
            <span className={`font-extrabold text-cooperative-cream transition-all duration-300
              ${scrolled ? 'text-lg custom-1000:text-xl' : 'text-[19px] custom-1000:text-2xl'}`}>
              Bethel Housing
            </span>
           
            <span className={`font-extrabold text-cooperative-orange transition-all duration-300
              group-hover:tracking-wider
              ${scrolled ? 'text-sm custom-1000:text-base' : 'text-[15px] custom-1000:text-lg'}`}>
              Cooperative
            </span>
          </Link>

          {/* ─── DESKTOP NAV LINKS ─── */}
          <nav className="hidden custom-1000:flex items-center gap-x-1">
            {navLinks.map((link, index) => (
              <a
                key={link.href}
                href={link.href}
                onClick={handleNavClick}
                className={`relative px-3 py-2 text-sm font-medium rounded-lg
                  transition-all duration-300 ease-out
                  hover:bg-cooperative-cream/10
                  ${activeSection === link.href.replace('#', '')
                    ? 'text-cooperative-orange'
                    : 'text-cooperative-cream/85 hover:text-cooperative-cream'
                  }
                  before:content-[''] before:absolute before:bottom-0 before:left-1/2
                  before:-translate-x-1/2 before:h-[2px] before:rounded-full
                  before:bg-cooperative-orange before:transition-all before:duration-300
                  ${activeSection === link.href.replace('#', '') ? 'before:w-[60%]' : 'before:w-0 hover:before:w-[40%]'}
                `}
                style={{ animationDelay: `${index * 80}ms` }}
              >
                {link.label}
              </a>
            ))}
             <Dropdown label='Cooperative' items={cooperativeItems}  onOpen={handleDropdownOpen}/>
             <Dropdown label='Apartment' items={apartmentItems} onOpen={handleDropdownOpen} />
             {secondBatch.map((link, index) => (
              <a
                key={link.href}
                href={link.href}
                onClick={handleNavClick}
                className={`relative px-3 py-2 text-sm font-medium rounded-lg
                  transition-all duration-300 ease-out
                  hover:bg-cooperative-cream/10
                  ${activeSection === link.href.replace('#', '')
                    ? 'text-cooperative-orange'
                    : 'text-cooperative-cream/85 hover:text-cooperative-cream'
                  }
                  before:content-[''] before:absolute before:bottom-0 before:left-1/2
                  before:-translate-x-1/2 before:h-[2px] before:rounded-full
                  before:bg-cooperative-orange before:transition-all before:duration-300
                  ${activeSection === link.href.replace('#', '') ? 'before:w-[60%]' : 'before:w-0 hover:before:w-[40%]'}
                `}
                style={{ animationDelay: `${index * 80}ms` }}
              >
                {link.label}
              </a>
            ))}
             
          </nav>

          {/* ─── RIGHT SIDE: BUTTONS + HAMBURGER ─── */}
          <div className="flex items-center gap-x-3">
            {/* Sign In — ghost button */}
            <Link
              to="/login"
              className="hidden sm:inline-flex px-5 py-2 text-sm font-medium text-cooperative-cream
                border border-cooperative-orange/40 rounded-lg
                bg-cooperative-cream/5 backdrop-blur-sm
                hover:border-cooperative-orange hover:bg-cooperative-orange/10
                hover:shadow-[0_0_20px_rgba(255,125,0,0.15)]
                active:scale-95 transition-all duration-300"
            >
              Sign in
            </Link>

            {/* Sign Up — solid button */}
            <Link
              to="/register"
              className="hidden sm:inline-flex px-5 py-2 text-sm font-medium text-white
                bg-cooperative-orange rounded-lg
                hover:bg-cooperative-brown hover:shadow-lg hover:shadow-cooperative-orange/25
                active:scale-95 transition-all duration-300"
            >
              Sign up
            </Link>

            {/* ─── HAMBURGER (mobile) ─── */}
            <button
              onClick={handleToggle}
              aria-label="Toggle menu"
              className={`custom-1000:hidden p-2 rounded-lg border border-cooperative-orange/40
                bg-cooperative-cream/5 backdrop-blur-sm text-cooperative-cream text-xl
                hover:border-cooperative-orange hover:bg-cooperative-orange/10
                active:scale-90 transition-all duration-300
                ${isOpen ? 'rotate-90 opacity-0 scale-75' : 'rotate-0 opacity-100 scale-100'}`}
            >
              <CiMenuBurger />
            </button>
          </div>
        </div>
      </header>

      {/* ─── MOBILE MENU (Portal) ─── */}
      {createPortal(
        <>
          {/* Overlay backdrop */}
          <div
            className={`custom-1000:hidden fixed inset-0 bg-cooperative-dark/60 backdrop-blur-sm
              transition-opacity duration-400 z-[9998]
              ${isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}
            onClick={() => setIsOpen(false)}
          />

          {/* Slide-down menu panel */}
          <div
            ref={menuRef}
            className={`custom-1000:hidden fixed top-0 left-0 right-0 
              bg-gradient-to-b from-cooperative-cream to-cooperative-cream/95
              backdrop-blur-xl shadow-2xl shadow-cooperative-dark/30
              transition-all duration-500 ease-[cubic-bezier(0.23,1,0.32,1)]
              overflow-hidden z-[100000000000]
              ${isOpen
                ? 'max-h-[100vh] opacity-100 translate-y-0'
                : 'max-h-0 opacity-0 -translate-y-4'}`}
          >
            {/* Menu Header */}
            <div className="flex justify-between items-center px-5 pt-5 pb-3">
              <div className="leading-tight">
                <span className="block text-[19px] font-extrabold text-cooperative-dark">
                  Bethel Housing
                </span>
                <span className="block text-cooperative-orange font-extrabold text-[15px]">
                  Cooperative
                </span>
              </div>
              <button
                onClick={handleToggle}
                aria-label="Close menu"
                className="p-1 rounded-lg text-cooperative-dark hover:bg-cooperative-dark/10
                  active:scale-90 transition-all duration-200"
              >
                <IoIosClose className="text-4xl" />
              </button>
            </div>

            {/* Divider */}
            <div className="mx-5 h-px bg-gradient-to-r from-transparent via-cooperative-dark/15 to-transparent" />

            {/* Nav Links */}
            <nav className="px-3 pt-3 pb-2">
              {navLinks.map((link, index) => (
                <a
                  key={link.href}
                  href={link.href}
                  onClick={handleNavClick}
                  className={`block px-4 py-3.5 rounded-xl text-[15px] font-medium
                    transition-all duration-300 ease-out
                    ${activeSection === link.href.replace('#', '')
                      ? 'bg-cooperative-teal/10 text-cooperative-teal translate-x-1'
                      : 'text-cooperative-dark/75 hover:bg-cooperative-dark/5 hover:text-cooperative-dark hover:translate-x-1'
                    }`}
                  style={{
                    transitionDelay: isOpen ? `${index * 60 + 100}ms` : '0ms',
                    opacity: isOpen ? 1 : 0,
                    transform: isOpen ? 'translateY(0)' : 'translateY(-8px)',
                  }}
                >
                  <span className="flex items-center gap-3">
                    <span
                      className={`w-1.5 h-1.5 rounded-full transition-all duration-300
                        ${activeSection === link.href.replace('#', '')
                          ? 'bg-cooperative-teal scale-125'
                          : 'bg-cooperative-dark/20'}`}
                    />
                    {link.label}
                  </span>
                </a>
              ))}
               <Dropdown label='Cooperative' items={cooperativeItems}  onOpen={handleDropdownOpen} isMobile = {true}/>
             <Dropdown label='Apartment' items={apartmentItems} onOpen={handleDropdownOpen} isMobile = {true}/>
               {secondBatch.map((link, index) => (
                <a
                  key={link.href}
                  href={link.href}
                  onClick={handleNavClick}
                  className={`block px-4 py-3.5 rounded-xl text-[15px] font-medium
                    transition-all duration-300 ease-out
                    ${activeSection === link.href.replace('#', '')
                      ? 'bg-cooperative-teal/10 text-cooperative-teal translate-x-1'
                      : 'text-cooperative-dark/75 hover:bg-cooperative-dark/5 hover:text-cooperative-dark hover:translate-x-1'
                    }`}
                  style={{
                    transitionDelay: isOpen ? `${index * 60 + 100}ms` : '0ms',
                    opacity: isOpen ? 1 : 0,
                    transform: isOpen ? 'translateY(0)' : 'translateY(-8px)',
                  }}
                >
                  <span className="flex items-center gap-3">
                    <span
                      className={`w-1.5 h-1.5 rounded-full transition-all duration-300
                        ${activeSection === link.href.replace('#', '')
                          ? 'bg-cooperative-teal scale-125'
                          : 'bg-cooperative-dark/20'}`}
                    />
                    {link.label}
                  </span>
                </a>
              ))}
            </nav>

            {/* Divider */}
            <div className="mx-5 h-px bg-gradient-to-r from-transparent via-cooperative-dark/15 to-transparent" />

            {/* Mobile CTA Buttons */}
            <div
              className="px-5 pt-4 pb-6 flex flex-col gap-3 sm:hidden"
              style={{
                transitionDelay: isOpen ? '500ms' : '0ms',
                opacity: isOpen ? 1 : 0,
                transform: isOpen ? 'translateY(0)' : 'translateY(-8px)',
                transition: 'all 400ms ease-out',
              }}
            >
              <Link
                to="/login"
                onClick={() => setIsOpen(false)}
                className="w-full py-3 text-center text-sm font-semibold text-cooperative-teal
                  border-2 border-cooperative-teal/30 rounded-xl
                  hover:border-cooperative-teal hover:bg-cooperative-teal/5
                  active:scale-[0.98] transition-all duration-300"
              >
                Sign in
              </Link>
              <Link
                to="/register"
                onClick={() => setIsOpen(false)}
                className="w-full py-3 text-center text-sm font-semibold text-white
                  bg-cooperative-orange rounded-xl
                  hover:bg-cooperative-brown hover:shadow-lg hover:shadow-cooperative-orange/20
                  active:scale-[0.98] transition-all duration-300"
              >
                Sign up
              </Link>
            </div>
          </div>
        </>,
        document.body
      )}
    </>
  )
}

export default Navbar