import React from 'react'

import imagesHero from '../../assets/images/vecteezy_modern-architectural-design-urban-setting-building-structure_60006151-removebg-preview.png'
import MarqueeTicker from './MarqueeTicker';
import Navbar from '../layout/Navbar';

const HeroSection = () => {
  return (
    <div className='bg-gradient-to-b from-cooperative-dark via-cooperative-teal to-cooperative-cream min-h-screen px-4 sm:px-6 lg:px-1'>
   <Navbar/>
      {/* Hero Container */}
      <div className='flex flex-col self-center items-center text-center custom-1000:justify-between  custom-1000:text-left gap-y-6 custom-1000:flex-row custom-1000:px-10 pt-[2rem]'>
        {/* Left Container */}
          <div className='custom-1000:w-[50%] custom-1000:px-6 sm:px-20'>
            <div className='text-[14px] text-gray-200/60  font-thin mt-[6.7rem] '>Trusted by 2,500+ cooperative members</div>
            <h1 className='font-bold text-[clamp(1.5rem,5vw,3rem)] text-cooperative-cream'>Find your dream apartment Join a trusted cooperative</h1>
            <p className='text-cooperative-cream'>Affordable apartments and houses, flexible payment plans, and transparent cooperative benefits all in one trusted platform. Join thousands of members building their future together.</p>
            <div className='mt-8'>
            <button className='block mx-auto  custom-1000:mx-0 custom-1000:w-[15rem] w-[15rem] sm:w-[30rem]  bg-cooperative-cream py-3 mb-2 rounded-lg'>Contact us</button>
            <button className='block mx-auto w-[15rem] sm:w-[30rem] custom-1000:mx-0  custom-1000:w-[15rem] bg-cooperative-orange py-3 rounded-lg text-cooperative-cream hover:bg-orange-800'>Check out houses options</button>
          </div>
          </div>
          
          {/* Left Container */}
          {/* Right container begins */}
          <img src={imagesHero} alt=""  className="
    w-full custom-1000:w-1/2
    h-[350px] custom-1000:h-[450px]
    object-cover
    [mask-image:linear-gradient(to_right,transparent,black_25%),linear-gradient(to_bottom,black_70%,transparent)]
    [mask-composite:intersect]
    [webkit-mask-image:linear-gradient(to_right,transparent,black_25%),linear-gradient(to_bottom,black_70%,transparent)]
    [webkit-mask-composite:destination-in]
 sm:mt-4 sm:h-[500px] sm:w-[80%] sm:block sm:mx-auto pr-8"  />
          {/* Right container ends */}
      </div>
      {/* Hero Container */}
      <MarqueeTicker />
    </div>
  )
}

export default HeroSection