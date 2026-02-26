import React from 'react'
import image3 from '../../assets/images/Gemini_Generated_Image_lb8753lb8753lb87.png'
import { AnimateOnScroll, StaggerWrapper, StaggerItem, fadeLeft, fadeRight, fadeUp, scaleIn } from '../../animations/AnimateOnScroll'

const stats = [
  { value: "35+", label: "Years of Service" },
  { value: "500+", label: "Members Served" },
  { value: "OGCS 5426", label: "Registered Cooperative" },
]

const AboutSection = () => {
  return (
    <section id="aboutus" className="bg-cooperative-cream px-6 pb-10">
      <div className="max-w-6xl mx-auto">

        {/* Section label */}
        <AnimateOnScroll variant={fadeUp} delay={0}>
          <p className="header-title-light">About Us</p>
        </AnimateOnScroll>

        {/* Main content grid */}
        <div className="flex flex-col custom-1000:flex-row custom-1000:items-stretch gap-12 custom-1000:gap-16">

          {/* Left — Text slides in from left */}
          <AnimateOnScroll variant={fadeLeft} delay={0.1} duration={0.7} className="flex-1 flex flex-col justify-center">

            <h1 className="text-cooperative-dark font-extrabold text-3xl sm:text-4xl leading-tight mb-6">
              Flawless Housing, Credit & Agric Solutions Combined with{" "}
              <span className="text-cooperative-teal">World-Class Expertise</span>
            </h1>

            <div className="h-[3px] w-12 bg-cooperative-orange mb-7" />

            <p className="text-cooperative-dark/70 leading-relaxed tracking-wide text-sm sm:text-base mb-5">
              Since its inception,{" "}
              <span className="text-cooperative-brown font-semibold">
                Bethel Obada-Oko Cooperative Housing Society Limited (OGCS 5426)
              </span>{" "}
              has been dedicated to providing{" "}
              <span className="text-cooperative-brown font-semibold">
                comprehensive housing, financial, and agricultural solutions
              </span>{" "}
              with a commitment to making every process as smooth and enjoyable as
              the outcomes themselves. From{" "}
              <span className="text-cooperative-brown font-semibold">
                apartment rentals to house purchases, credit & thrift programs, and
                agric contributions
              </span>
              , our team combines{" "}
              <span className="text-cooperative-brown font-semibold">
                decades of expertise, genuine enthusiasm, and a collaborative approach
              </span>
              , ensuring every member experiences a seamless, personalized journey
              from start to finish.
            </p>

            <p className="text-cooperative-dark/70 leading-relaxed tracking-wide text-sm sm:text-base mb-8">
              Built on{" "}
              <span className="text-cooperative-brown font-semibold">
                integrity, transparency, and open communication
              </span>
              , we believe in earning trust the traditional way — through consistent
              support and exceptional service. Under the active leadership of our
              management team, we are more than a cooperative; we are{" "}
              <span className="text-cooperative-brown font-semibold">partners</span>,
              working tirelessly to help each member{" "}
              <span className="text-cooperative-brown font-semibold">
                achieve their housing dreams, grow their savings, and benefit from our
                agric initiatives
              </span>
              .
            </p>

            {/* Stats — stagger each box */}
            <StaggerWrapper className="flex flex-wrap gap-px bg-cooperative-dark/10 border border-cooperative-dark/10 w-fit" stagger={0.1} delay={0.2}>
              {stats.map((stat) => (
                <StaggerItem key={stat.label} variant={scaleIn}>
                  <div className="bg-cooperative-cream px-6 py-4 text-center min-w-[110px]">
                    <p className="text-cooperative-orange font-extrabold text-xl leading-none mb-1">
                      {stat.value}
                    </p>
                    <p className="text-cooperative-dark/50 text-[0.65rem] uppercase tracking-widest">
                      {stat.label}
                    </p>
                  </div>
                </StaggerItem>
              ))}
            </StaggerWrapper>
          </AnimateOnScroll>

          {/* Right — Image slides in from right */}
          <AnimateOnScroll variant={fadeRight} delay={0.2} duration={0.7} className="flex-1 flex items-stretch custom-1000:max-w-[480px]">
            <div className="relative w-full">
              <img
                src={image3}
                alt="Bethel Cooperative Housing"
                className="relative z-10 w-full h-full object-cover rounded-3xl shadow-xl"
                style={{ minHeight: "320px", maxHeight: "520px" }}
              />

              {/* Floating badge scales in */}
              <AnimateOnScroll variant={scaleIn} delay={0.5} className="absolute top-5 left-5 z-20">
                <div className="bg-cooperative-dark px-4 py-2">
                  <p className="text-cooperative-orange text-[0.6rem] uppercase tracking-[0.2rem] font-bold">
                    Est. 1989
                  </p>
                  <p className="text-cooperative-cream text-xs font-extrabold leading-tight">
                    Trusted by<br />Hundreds of Members
                  </p>
                </div>
              </AnimateOnScroll>
            </div>
          </AnimateOnScroll>

        </div>
      </div>
    </section>
  )
}

export default AboutSection