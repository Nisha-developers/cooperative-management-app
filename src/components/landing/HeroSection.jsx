import React from 'react'
import imagesHero from '../../assets/images/WhatsApp_Image_2026-02-25_at_6.57.20_PM-removebg-preview.png';

import MarqueeTicker from './MarqueeTicker';
import Navbar from '../layout/Navbar';

const HeroSection = () => {
  return (
    <div className='relative h-screen px-4 sm:px-6 lg:px-1 overflow-hidden'>

      {/* Background Image */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${imagesHero})` }}
      />

      {/* Gradient Overlay — blends image into dark green, open at top-center */}
      <div
        className="absolute inset-0"
        style={{
          background: `rgba(0, 30, 0, 0.5)`,
        }}
      />

      {/* Content sits above overlays */}
      <div className="relative z-[1000000000]">
        <Navbar />

        {/* Hero Container */}
        <div className='flex flex-col self-center items-center text-center h-screen pt-[2rem]'>

          {/* Left Container */}
          <div className='custom-1000:w-[50%] custom-1000:px-0 sm:px-20'>
            <div className='text-[14px] text-gray-200/60 font-thin mt-[6.7rem]'>
              Trusted by 2,500+ cooperative members
            </div>
            <h1 className='font-bold text-[clamp(1.5rem,5vw,3rem)] text-cooperative-cream'>
              Find your dream apartment Join a trusted cooperative
            </h1>
            <p className='text-cooperative-cream'>
              Affordable apartments and houses, flexible payment plans, and transparent cooperative
              benefits all in one trusted platform. Join thousands of members building their future together.
            </p>
            <div className='mt-8 custom-1000:flex custom-1000:gap-6 custom-1000:justify-center'>
              <button className='block mx-auto custom-1000:mx-0 custom-1000:w-[15rem] w-[15rem] sm:w-[30rem] bg-cooperative-cream py-3 mb-2 rounded-lg'>
                Contact us
              </button>
              <button className='block mx-auto custom-1000:mx-0 custom-1000:w-[15rem] w-[15rem] sm:w-[30rem]  bg-cooperative-orange text-cooperative-cream py-3 mb-2 rounded-lg hover:bg-orange-800'>
                Check out houses options
              </button>
            </div>
          </div>

          {/* Right side — empty, image is the background */}
          <div className='custom-1000:w-[50%] custom-1000:h-[350px]' />

        </div>
      </div>

      <div className="relative z-10">
        <MarqueeTicker />
      </div>

    </div>
  )
}

export default HeroSection