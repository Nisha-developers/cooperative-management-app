import React from 'react'
import HeroSection from '../../components/landing/HeroSection'
import AboutSection from '../../components/landing/AboutSection'
import ServicesOverview from '../../components/landing/ServicesOverview'
import FAQ from '../../components/landing/faq'
import ContactUs from '../../components/landing/ContactUs'
import Footer from '../../components/layout/Footer'

const LandingPage = () => {
  return (
    <div>
    <HeroSection />
    <AboutSection />
    <ServicesOverview />
    <FAQ />
    <ContactUs />
    <Footer/>
    </div>
  )
}

export default LandingPage