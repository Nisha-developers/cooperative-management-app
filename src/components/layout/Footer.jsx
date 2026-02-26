import { useState } from "react";
import { AnimateOnScroll, StaggerWrapper, StaggerItem, fadeUp, fadeLeft, fadeRight, scaleIn } from '../../animations/AnimateOnScroll'

const footerLinks = {
  Services: [
    { label: "Apartment Rentals", href: "#" },
    { label: "Property Purchase", href: "#" },
    { label: "Agricultural Dividends", href: "#" },
    { label: "Loan & Thrift", href: "#" },
  ],
  Company: [
    { label: "About Us", href: "#" },
    { label: "How It Works", href: "#" },
    { label: "FAQ", href: "#" },
    { label: "Contact Us", href: "#" },
  ],
  Members: [
    { label: "Register", href: "#" },
    { label: "Login", href: "#" },
    { label: "Dashboard", href: "#" },
    { label: "Upload Payment", href: "#" },
  ],
};

const socials = [
  {
    label: "Facebook",
    href: "#",
    icon: (
      <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
        <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z" />
      </svg>
    ),
  },
  {
    label: "WhatsApp",
    href: "https://wa.me/447533990688",
    icon: (
      <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z" />
        <path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.118 1.528 5.856L.057 23.57a.75.75 0 00.912.912l5.753-1.461A11.945 11.945 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.907 0-3.693-.502-5.24-1.38l-.374-.217-3.884.987.997-3.835-.237-.386A9.96 9.96 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z" />
      </svg>
    ),
  },
  {
    label: "Instagram",
    href: "#",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-4 h-4">
        <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
        <circle cx="12" cy="12" r="4" />
        <circle cx="17.5" cy="6.5" r="0.5" fill="currentColor" />
      </svg>
    ),
  },
];

export default function Footer() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (email) {
      setSubmitted(true);
      setEmail("");
    }
  };

  return (
    <footer className="bg-cooperative-dark border-t border-white/5">

      {/* Top CTA band */}
      <div className="border-b border-white/5 py-12 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">

          <AnimateOnScroll variant={fadeLeft} delay={0.1}>
            <div>
              <p className="text-cooperative-orange text-xs tracking-[0.2rem] uppercase mb-1">
                Stay in the loop
              </p>
              <h3 className="text-cooperative-cream font-extrabold text-2xl md:text-3xl">
                Get updates from{" "}
                <span className="text-cooperative-orange italic">Bethel Cooperative</span>
              </h3>
            </div>
          </AnimateOnScroll>

          <AnimateOnScroll variant={fadeRight} delay={0.2}>
            <form onSubmit={handleSubmit} className="flex w-full md:w-auto gap-0">
              {submitted ? (
                <p className="text-cooperative-orange text-sm font-bold uppercase tracking-widest py-3">
                  ✓ Thank you for subscribing!
                </p>
              ) : (
                <>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email"
                    className="bg-white/5 border border-white/10 text-cooperative-cream placeholder:text-cooperative-cream/30 text-sm px-5 py-3 outline-none focus:border-cooperative-orange transition-colors duration-200 w-full md:w-64"
                  />
                  <button
                    type="submit"
                    className="bg-cooperative-orange text-cooperative-dark font-bold uppercase tracking-widest text-xs px-6 py-3 hover:opacity-90 transition-opacity duration-200 shrink-0"
                  >
                    Subscribe
                  </button>
                </>
              )}
            </form>
          </AnimateOnScroll>

        </div>
      </div>

      {/* Main footer body */}
      <div className="max-w-6xl mx-auto px-6 py-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">

        {/* Brand column — slides from left */}
        <AnimateOnScroll variant={fadeLeft} delay={0.1} duration={0.65} className="lg:col-span-1">
          <div className="mb-5">
            <p className="text-cooperative-orange font-black text-xs tracking-[0.2rem] uppercase mb-1">
              Est. 1989 · OGCS 5426
            </p>
            <h2 className="text-cooperative-cream font-extrabold text-xl leading-tight">
              Bethel<br />
              <span className="text-cooperative-orange">Cooperative</span>
            </h2>
            <p className="text-cooperative-cream/30 text-[0.65rem] uppercase tracking-widest mt-1">
              Housing Society Limited
            </p>
          </div>
          <div className="h-[2px] w-8 bg-cooperative-orange mb-5" />
          <p className="text-cooperative-cream/50 text-sm leading-relaxed mb-6">
            Providing trusted housing, agricultural investment, and financial
            services to members across Ogun State since 1989.
          </p>
          <div className="space-y-2 text-sm text-cooperative-cream/40">
            <p>Bethel Garden Estate,</p>
            <p>Obada-Oko, Abeokuta,</p>
            <p>Ogun State, Nigeria.</p>
          </div>
        </AnimateOnScroll>

        {/* Link columns — each fades up with increasing delay */}
        {Object.entries(footerLinks).map(([group, links], groupIndex) => (
          <AnimateOnScroll key={group} variant={fadeUp} delay={0.15 + groupIndex * 0.1} duration={0.6}>
            <div>
              <h4 className="text-cooperative-cream font-bold text-sm uppercase tracking-[0.15rem] mb-6">
                {group}
              </h4>
              <StaggerWrapper className="space-y-3" stagger={0.07} delay={0.1}>
                {links.map((link) => (
                  <StaggerItem key={link.label} variant={fadeUp} duration={0.4}>
                    <li className="list-none">
                      <a
                        href={link.href}
                        className="text-cooperative-cream/40 text-sm hover:text-cooperative-orange transition-colors duration-200 flex items-center gap-2 group"
                      >
                        <span className="w-0 group-hover:w-3 h-px bg-cooperative-orange transition-all duration-300 overflow-hidden" />
                        {link.label}
                      </a>
                    </li>
                  </StaggerItem>
                ))}
              </StaggerWrapper>
            </div>
          </AnimateOnScroll>
        ))}

      </div>

      {/* Contact bar */}
      <AnimateOnScroll variant={fadeUp} delay={0.1}>
        <div className="border-t border-white/5 py-6 px-6">
          <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">

            {/* Phone links stagger from left */}
            <StaggerWrapper className="flex flex-wrap items-center gap-6 text-sm" stagger={0.08} delay={0.05}>
              <StaggerItem variant={fadeLeft} duration={0.4}>
                <a href="tel:+2347051598561" className="text-cooperative-cream/40 hover:text-cooperative-orange transition-colors duration-200">
                  +234 705 159 8561
                </a>
              </StaggerItem>
              <StaggerItem variant={fadeLeft} duration={0.4}>
                <span className="text-white/10 hidden md:block">|</span>
              </StaggerItem>
              <StaggerItem variant={fadeLeft} duration={0.4}>
                <a href="tel:+2347037350984" className="text-cooperative-cream/40 hover:text-cooperative-orange transition-colors duration-200">
                  +234 703 735 0984
                </a>
              </StaggerItem>
              <StaggerItem variant={fadeLeft} duration={0.4}>
                <span className="text-white/10 hidden md:block">|</span>
              </StaggerItem>
              <StaggerItem variant={fadeLeft} duration={0.4}>
                <a href="https://wa.me/447533990688" className="text-cooperative-orange font-bold hover:text-cooperative-cream transition-colors duration-200">
                  WhatsApp
                </a>
              </StaggerItem>
            </StaggerWrapper>

            {/* Socials scale in one by one */}
            <StaggerWrapper className="flex items-center gap-3" stagger={0.08} delay={0.1}>
              {socials.map((s) => (
                <StaggerItem key={s.label} variant={scaleIn} duration={0.4}>
                  <a
                    href={s.href}
                    aria-label={s.label}
                    className="w-8 h-8 border border-white/10 flex items-center justify-center text-cooperative-cream/40 hover:border-cooperative-orange hover:text-cooperative-orange transition-all duration-200"
                  >
                    {s.icon}
                  </a>
                </StaggerItem>
              ))}
            </StaggerWrapper>

          </div>
        </div>
      </AnimateOnScroll>

      {/* Bottom bar */}
      <AnimateOnScroll variant={fadeUp} delay={0.15}>
        <div className="border-t border-white/5 py-5 px-6">
          <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-2 text-xs text-cooperative-cream/25">
            <p>
              © {new Date().getFullYear()} Bethel Obada Oko (Abeokuta) Cooperative Housing Society Limited. All rights reserved.
            </p>
            <p>
              www.bethelhousingcooperative.com
            </p>
          </div>
        </div>
      </AnimateOnScroll>

    </footer>
  );
}