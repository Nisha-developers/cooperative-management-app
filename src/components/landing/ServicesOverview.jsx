import { useState } from "react";
import { AnimateOnScroll, StaggerWrapper, StaggerItem, fadeUp, scaleIn, slideUp } from '../../animations/AnimateOnScroll'

const services = [
  {
    id: "01",
    icon: (
      <svg viewBox="0 0 48 48" fill="none" className="w-10 h-10" stroke="currentColor" strokeWidth="1.5">
        <path d="M6 42V20L24 6l18 14v22" />
        <rect x="16" y="28" width="7" height="14" />
        <rect x="25" y="28" width="7" height="14" />
        <path d="M24 6v36" strokeDasharray="2 3" />
      </svg>
    ),
    title: "Apartment Rentals",
    tagline: "Shelter You Can Trust",
    description: "Browse cooperative-verified rental apartments in Obada-Oko and surrounding areas. Every unit is vetted, priced fairly, and managed with full transparency from listing to lease.",
    steps: ["View Available Units", "Submit Booking Request", "Upload Proof of Payment", "Receive Admin Confirmation"],
    cta: "Browse Rentals",
  },
  {
    id: "02",
    icon: (
      <svg viewBox="0 0 48 48" fill="none" className="w-10 h-10" stroke="currentColor" strokeWidth="1.5">
        <path d="M8 40h32M12 40V20h24v20" />
        <path d="M4 24L24 8l20 16" />
        <rect x="18" y="28" width="12" height="12" />
        <circle cx="24" cy="16" r="3" />
      </svg>
    ),
    title: "Property Purchase",
    tagline: "Own Your Tomorrow",
    description: "Acquire land or completed homes within Bethel Garden Estate. Our cooperative purchase workflow walks you through every document, payment stage, and ownership transfer.",
    steps: ["Select Property Listing", "Complete Purchase Form", "Submit Payment Evidence", "Admin Sale Verification"],
    cta: "View Properties",
  },
  {
    id: "03",
    icon: (
      <svg viewBox="0 0 48 48" fill="none" className="w-10 h-10" stroke="currentColor" strokeWidth="1.5">
        <path d="M24 4l4 8 9 1.3-6.5 6.3 1.5 9L24 24l-8 4.6 1.5-9L11 13.3 20 12z" />
        <path d="M8 44v-8a4 4 0 014-4h24a4 4 0 014 4v8" />
        <path d="M16 32v12M32 32v12" />
      </svg>
    ),
    title: "Agricultural Dividends",
    tagline: "Grow With the Cooperative",
    description: "Members participate in the cooperative's agricultural arm and receive annual dividends calculated and distributed by administration. Transparent records, fair returns, communal growth.",
    steps: ["Enroll as a Member", "Track Contribution Status", "Dividend Computed Annually", "Receive Year-End Payout"],
    cta: "Learn More",
  },
  {
    id: "04",
    icon: (
      <svg viewBox="0 0 48 48" fill="none" className="w-10 h-10" stroke="currentColor" strokeWidth="1.5">
        <rect x="8" y="10" width="32" height="28" rx="3" />
        <path d="M16 10V6M32 10V6" />
        <path d="M8 20h32" />
        <path d="M16 28h4M24 28h8M16 34h6" />
      </svg>
    ),
    title: "Loan & Thrift Services",
    tagline: "Financial Support, Member-First",
    description: "After six months of consistent savings, members become eligible for cooperative loans. Backed by guarantor forms, ID verification, and next-of-kin records.",
    steps: ["6-Month Savings Eligibility", "Submit Guarantor & ID Forms", "Admin Review & Approval", "Loan Disbursement"],
    cta: "Check Eligibility",
  },
];

export default function ServicesOverview() {
  const [activeService, setActiveService] = useState(null);

  return (
    <section id="services" className="bg-cooperative-dark px-6 pb-10">

      {/* Header */}
      <div className="max-w-6xl mx-auto">
        <AnimateOnScroll variant={fadeUp} delay={0}>
          <p className="header-title-dark">OUR SERVICES</p>
        </AnimateOnScroll>

        <AnimateOnScroll variant={fadeUp} delay={0.15}>
          <div className="text-center mb-4">
            <h2 className="text-cooperative-cream font-extrabold leading-tight text-4xl md:text-5xl">
              Everything You Need,{" "}
              <span className="text-cooperative-orange italic">Under One Roof</span>
            </h2>
            <p className="text-cooperative-cream/50 text-base max-w-xl mx-auto mt-4 leading-relaxed">
              Bethel Cooperative Housing Society delivers housing, investment, and financial
              services built on decades of trust and community-first values.
            </p>
          </div>
        </AnimateOnScroll>

        <AnimateOnScroll variant={scaleIn} delay={0.25}>
          <div className="flex items-center justify-center gap-3 mt-8 mb-14">
            <div className="h-px w-16 bg-cooperative-orange/30" />
            <div className="w-2 h-2 bg-cooperative-orange rotate-45" />
            <div className="h-px w-16 bg-cooperative-orange/30" />
          </div>
        </AnimateOnScroll>
      </div>

      {/* Cards — stagger in */}
      <StaggerWrapper
        className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4"
        stagger={0.13}
        delay={0.1}
      >
        {services.map((service) => (
          <StaggerItem key={service.id} variant={slideUp} duration={0.65}>
            <ServiceCard
              service={service}
              isActive={activeService === service.id}
              onToggle={() =>
                setActiveService(activeService === service.id ? null : service.id)
              }
            />
          </StaggerItem>
        ))}
      </StaggerWrapper>

     

    </section>
  );
}

function ServiceCard({ service, isActive, onToggle }) {
  return (
    <div
      onClick={onToggle}
      style={{ backgroundColor: isActive ? "#FFECD1" : "#2E7D32" }}
      className="relative cursor-pointer px-8 py-8 overflow-hidden border border-white/5 transition-colors duration-300 h-full"
    >
      <span className="absolute top-3 right-5 text-[5rem] font-black leading-none select-none pointer-events-none text-white/5">
        {service.id}
      </span>
      <div className={`mb-5 transition-colors duration-300 ${isActive ? "text-cooperative-dark" : "text-cooperative-orange"}`}>
        {service.icon}
      </div>
      <p className={`text-[0.65rem] uppercase tracking-[0.2rem] mb-1 transition-colors duration-300 ${isActive ? "text-cooperative-dark/60" : "text-cooperative-teal"}`}>
        {service.tagline}
      </p>
      <h3 className={`text-xl font-extrabold mb-3 leading-snug transition-colors duration-300 ${isActive ? "text-cooperative-dark" : "text-cooperative-cream"}`}>
        {service.title}
      </h3>
      <div className={`h-[2px] w-10 mb-4 transition-colors duration-300 ${isActive ? "bg-cooperative-dark" : "bg-cooperative-orange"}`} />
      <p className={`text-sm leading-relaxed mb-5 transition-colors duration-300 ${isActive ? "text-cooperative-dark/80" : "text-cooperative-cream/60"}`}>
        {service.description}
      </p>
      <div className="overflow-hidden transition-all duration-500" style={{ maxHeight: isActive ? "300px" : "0px" }}>
        <p className={`text-[0.65rem] uppercase tracking-[0.15rem] mb-3 ${isActive ? "text-cooperative-dark/50" : "text-cooperative-orange/60"}`}>
          How It Works
        </p>
        <ol className="space-y-2 mb-5">
          {service.steps.map((step, i) => (
            <li key={i} className={`flex items-start gap-3 text-sm ${isActive ? "text-cooperative-dark" : "text-cooperative-cream/80"}`}>
              <span className={`min-w-[22px] h-[22px] text-[0.65rem] font-black flex items-center justify-center shrink-0 mt-0.5 ${isActive ? "bg-cooperative-dark text-cooperative-orange" : "bg-cooperative-orange text-cooperative-dark"}`}>
                {i + 1}
              </span>
              {step}
            </li>
          ))}
        </ol>
      </div>
      <div className={`flex items-center gap-2 text-[0.75rem] font-bold uppercase tracking-widest transition-colors duration-300 ${isActive ? "text-cooperative-dark" : "text-cooperative-orange"}`}>
        {service.cta}
        <svg viewBox="0 0 20 20" fill="currentColor" className={`w-3.5 h-3.5 transition-transform duration-300 ${isActive ? "translate-x-1" : ""}`}>
          <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </div>
      {!isActive && (
        <p className="absolute bottom-3 right-4 text-[0.6rem] text-white/20 tracking-wide">tap to expand</p>
      )}
    </div>
  );
}