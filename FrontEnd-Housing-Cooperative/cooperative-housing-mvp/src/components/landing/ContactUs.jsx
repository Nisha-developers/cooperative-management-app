import { AnimateOnScroll, StaggerWrapper, StaggerItem, fadeUp, fadeLeft, fadeRight, scaleIn } from '../../animations/AnimateOnScroll'

export default function ContactUs() {
  return (
    <section className="bg-cooperative-teal py-10 px-6" id="contactus">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <AnimateOnScroll variant={fadeUp} delay={0}>
          <p
            className="text-cooperative-cream font-bold text-[20px] tracking-[1rem] text-center pt-[2rem] pb-[2rem]"
            style={{ textTransform: "uppercase" }}
          >
            CONTACT US
          </p>
        </AnimateOnScroll>

        <AnimateOnScroll variant={fadeUp} delay={0.15}>
          <div className="text-center mb-4">
            <h2 className="text-cooperative-cream font-extrabold leading-tight text-4xl md:text-5xl">
              Let's{" "}
              <span className="text-cooperative-orange italic">Talk</span>
            </h2>
            <p className="text-cooperative-cream/60 text-base max-w-xl mx-auto mt-4 leading-relaxed">
              Visit us, call us, or send a message. We're always available to guide
              you through your housing and cooperative journey.
            </p>
          </div>
        </AnimateOnScroll>

        {/* Divider */}
        <AnimateOnScroll variant={scaleIn} delay={0.25}>
          <div className="flex items-center justify-center gap-3 mt-8 mb-14">
            <div className="h-px w-16 bg-cooperative-orange/40" />
            <div className="w-2 h-2 bg-cooperative-orange rotate-45" />
            <div className="h-px w-16 bg-cooperative-orange/40" />
          </div>
        </AnimateOnScroll>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {/* LEFT — slides in from left */}
          <AnimateOnScroll variant={fadeLeft} delay={0.1} duration={0.7}>
            <div className="flex flex-col gap-6">

              {/* Contact Info Cards — stagger */}
              <StaggerWrapper className="grid grid-cols-1 sm:grid-cols-2 gap-4" stagger={0.1} delay={0.15}>

                {/* Address */}
                <StaggerItem variant={fadeUp} duration={0.5}>
                  <div className="bg-cooperative-dark p-6 border border-white/5">
                    <div className="text-cooperative-orange mb-3">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-7 h-7">
                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" />
                        <circle cx="12" cy="9" r="2.5" />
                      </svg>
                    </div>
                    <p className="text-cooperative-orange text-[0.65rem] uppercase tracking-[0.15rem] mb-1">Address</p>
                    <p className="text-cooperative-cream font-semibold text-sm leading-relaxed">
                      Bethel Garden Estate,<br />Obada-Oko, Abeokuta,<br />Ogun State, Nigeria.
                    </p>
                  </div>
                </StaggerItem>

                {/* Phone */}
                <StaggerItem variant={fadeUp} duration={0.5}>
                  <div className="bg-cooperative-dark p-6 border border-white/5">
                    <div className="text-cooperative-orange mb-3">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-7 h-7">
                        <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 11a19.79 19.79 0 01-3.07-8.67A2 2 0 012 .27h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 8.1a16 16 0 006.29 6.29l1.2-1.2a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" />
                      </svg>
                    </div>
                    <p className="text-cooperative-orange text-[0.65rem] uppercase tracking-[0.15rem] mb-1">Phone</p>
                    <a href="tel:+2347051598561" className="text-cooperative-cream font-semibold text-sm block hover:text-cooperative-orange transition-colors">
                      +234 705 159 8561
                    </a>
                    <a href="tel:+2347037350984" className="text-cooperative-cream font-semibold text-sm block hover:text-cooperative-orange transition-colors mt-1">
                      +234 703 735 0984
                    </a>
                  </div>
                </StaggerItem>

                {/* WhatsApp */}
                <StaggerItem variant={fadeUp} duration={0.5}>
                  <div className="bg-cooperative-dark p-6 border border-white/5">
                    <div className="text-cooperative-orange mb-3">
                      <svg viewBox="0 0 24 24" fill="currentColor" className="w-7 h-7">
                        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z" />
                        <path d="M12 0C5.373 0 0 5.373 0 12c0 2.117.549 4.107 1.51 5.842L.057 23.428a.5.5 0 00.609.61l5.647-1.444A11.934 11.934 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.933 9.933 0 01-5.068-1.383l-.362-.214-3.753.959.984-3.67-.235-.376A9.96 9.96 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z" />
                      </svg>
                    </div>
                    <p className="text-cooperative-orange text-[0.65rem] uppercase tracking-[0.15rem] mb-1">WhatsApp</p>
                    <a
                      href="https://wa.me/447533990688"
                      target="_blank"
                      rel="noreferrer"
                      className="text-cooperative-cream font-semibold text-sm block hover:text-cooperative-orange transition-colors"
                    >
                      +44 753 399 0688
                    </a>
                  </div>
                </StaggerItem>

                {/* Registration */}
                <StaggerItem variant={fadeUp} duration={0.5}>
                  <div className="bg-cooperative-dark p-6 border border-white/5">
                    <div className="text-cooperative-orange mb-3">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-7 h-7">
                        <rect x="2" y="7" width="20" height="14" rx="2" />
                        <path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2" />
                        <path d="M12 12v4M10 14h4" />
                      </svg>
                    </div>
                    <p className="text-cooperative-orange text-[0.65rem] uppercase tracking-[0.15rem] mb-1">Registration</p>
                    <p className="text-cooperative-cream font-semibold text-sm leading-relaxed">
                      OGCS 5426<br />
                      <span className="text-cooperative-cream/50 font-normal">Est. 1989</span>
                    </p>
                  </div>
                </StaggerItem>

              </StaggerWrapper>

              {/* Social Media */}
              <AnimateOnScroll variant={fadeUp} delay={0.2}>
                <div className="bg-cooperative-dark border border-white/5 px-6 py-5">
                  <p className="text-cooperative-orange text-[0.65rem] uppercase tracking-[0.2rem] mb-4">Follow & Connect</p>
                  <StaggerWrapper className="flex items-center gap-3 flex-wrap" stagger={0.08} delay={0.05}>

                    <StaggerItem variant={scaleIn} duration={0.4}>
                      <a
                        href="https://wa.me/447533990688"
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center gap-2 bg-cooperative-teal/30 border border-cooperative-teal/40 px-4 py-2 text-cooperative-cream text-xs font-bold uppercase tracking-wider hover:bg-cooperative-orange hover:border-cooperative-orange hover:text-cooperative-dark transition-all duration-200"
                      >
                        <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
                          <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                        </svg>
                        Facebook
                      </a>
                    </StaggerItem>

                    <StaggerItem variant={scaleIn} duration={0.4}>
                      <a
                        href="https://wa.me/447533990688"
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center gap-2 bg-cooperative-teal/30 border border-cooperative-teal/40 px-4 py-2 text-cooperative-cream text-xs font-bold uppercase tracking-wider hover:bg-cooperative-orange hover:border-cooperative-orange hover:text-cooperative-dark transition-all duration-200"
                      >
                        <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
                          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347zM12 0C5.373 0 0 5.373 0 12c0 2.117.549 4.107 1.51 5.842L.057 23.428a.5.5 0 00.609.61l5.647-1.444A11.934 11.934 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22a9.933 9.933 0 01-5.068-1.383l-.362-.214-3.753.959.984-3.67-.235-.376A9.96 9.96 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z" />
                        </svg>
                        WhatsApp
                      </a>
                    </StaggerItem>

                    <StaggerItem variant={scaleIn} duration={0.4}>
                      <a
                        href="tel:+2347051598561"
                        className="flex items-center gap-2 bg-cooperative-teal/30 border border-cooperative-teal/40 px-4 py-2 text-cooperative-cream text-xs font-bold uppercase tracking-wider hover:bg-cooperative-orange hover:border-cooperative-orange hover:text-cooperative-dark transition-all duration-200"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-4 h-4">
                          <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 11a19.79 19.79 0 01-3.07-8.67A2 2 0 012 .27h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 8.1a16 16 0 006.29 6.29l1.2-1.2a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" />
                        </svg>
                        Call Us
                      </a>
                    </StaggerItem>

                  </StaggerWrapper>
                </div>
              </AnimateOnScroll>

              {/* Map */}
              <AnimateOnScroll variant={scaleIn} delay={0.25}>
                <div className="border border-white/5 overflow-hidden" style={{ height: "280px" }}>
                  <iframe
                    title="Bethel Garden Estate Location"
                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3960.5!2d3.2835!3d7.0926!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x103a5165ad8d5f8d%3A0x96b64f7dc8bc0b44!2sObada-Oko%2C%20Abeokuta%2C%20Ogun%20State!5e0!3m2!1sen!2sng!4v1708000000000!5m2!1sen!2sng"
                    width="100%"
                    height="100%"
                    style={{ border: 0, filter: "hue-rotate(160deg) saturate(0.6) brightness(0.85)" }}
                    allowFullScreen=""
                    loading="lazy"
                    referrerPolicy="no-referrer-when-downgrade"
                  />
                </div>
              </AnimateOnScroll>

            </div>
          </AnimateOnScroll>

          {/* RIGHT — Form slides in from right */}
          <AnimateOnScroll variant={fadeRight} delay={0.2} duration={0.7}>
            <div className="bg-cooperative-dark border border-white/5 px-8 py-10 flex flex-col justify-between">

              <div>
                <p className="text-cooperative-orange text-[0.65rem] uppercase tracking-[0.2rem] mb-2">Send a Message</p>
                <h3 className="text-cooperative-cream font-extrabold text-2xl md:text-3xl mb-1">
                  We'd Love to <span className="text-cooperative-orange italic">Hear From You</span>
                </h3>
                <p className="text-cooperative-cream/40 text-sm mb-8 leading-relaxed">
                  Fill in the form below and a member of our team will respond to you as soon as possible.
                </p>
              </div>

              {/* Form fields stagger in */}
              <StaggerWrapper className="flex flex-col gap-5" stagger={0.07} delay={0.1}>

                <StaggerItem variant={fadeUp} duration={0.45}>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="flex flex-col gap-1">
                      <label className="text-cooperative-cream/50 text-[0.65rem] uppercase tracking-[0.15rem]">First Name</label>
                      <input
                        type="text"
                        placeholder="e.g. Emeka"
                        className="bg-cooperative-teal/10 border border-white/10 text-cooperative-cream placeholder:text-cooperative-cream/20 text-sm px-4 py-3 outline-none focus:border-cooperative-orange transition-colors duration-200"
                      />
                    </div>
                    <div className="flex flex-col gap-1">
                      <label className="text-cooperative-cream/50 text-[0.65rem] uppercase tracking-[0.15rem]">Last Name</label>
                      <input
                        type="text"
                        placeholder="e.g. Adeyemi"
                        className="bg-cooperative-teal/10 border border-white/10 text-cooperative-cream placeholder:text-cooperative-cream/20 text-sm px-4 py-3 outline-none focus:border-cooperative-orange transition-colors duration-200"
                      />
                    </div>
                  </div>
                </StaggerItem>

                <StaggerItem variant={fadeUp} duration={0.45}>
                  <div className="flex flex-col gap-1">
                    <label className="text-cooperative-cream/50 text-[0.65rem] uppercase tracking-[0.15rem]">Email Address</label>
                    <input
                      type="email"
                      placeholder="you@example.com"
                      className="bg-cooperative-teal/10 border border-white/10 text-cooperative-cream placeholder:text-cooperative-cream/20 text-sm px-4 py-3 outline-none focus:border-cooperative-orange transition-colors duration-200"
                    />
                  </div>
                </StaggerItem>

                <StaggerItem variant={fadeUp} duration={0.45}>
                  <div className="flex flex-col gap-1">
                    <label className="text-cooperative-cream/50 text-[0.65rem] uppercase tracking-[0.15rem]">Phone Number</label>
                    <input
                      type="tel"
                      placeholder="+234 800 000 0000"
                      className="bg-cooperative-teal/10 border border-white/10 text-cooperative-cream placeholder:text-cooperative-cream/20 text-sm px-4 py-3 outline-none focus:border-cooperative-orange transition-colors duration-200"
                    />
                  </div>
                </StaggerItem>

                <StaggerItem variant={fadeUp} duration={0.45}>
                  <div className="flex flex-col gap-1">
                    <label className="text-cooperative-cream/50 text-[0.65rem] uppercase tracking-[0.15rem]">Subject</label>
                    <select className="bg-cooperative-teal/10 border border-white/10 text-cooperative-cream text-sm px-4 py-3 outline-none focus:border-cooperative-orange transition-colors duration-200 appearance-none">
                      <option value="" className="bg-cooperative-dark">Select a subject</option>
                      <option value="housing" className="bg-cooperative-dark">Housing Inquiry</option>
                      <option value="purchase" className="bg-cooperative-dark">Property Purchase</option>
                      <option value="loan" className="bg-cooperative-dark">Loan & Thrift</option>
                      <option value="agric" className="bg-cooperative-dark">Agricultural Dividend</option>
                      <option value="membership" className="bg-cooperative-dark">Membership</option>
                      <option value="other" className="bg-cooperative-dark">Other</option>
                    </select>
                  </div>
                </StaggerItem>

                <StaggerItem variant={fadeUp} duration={0.45}>
                  <div className="flex flex-col gap-1">
                    <label className="text-cooperative-cream/50 text-[0.65rem] uppercase tracking-[0.15rem]">Message</label>
                    <textarea
                      rows={5}
                      placeholder="Tell us how we can help you..."
                      className="bg-cooperative-teal/10 border border-white/10 text-cooperative-cream placeholder:text-cooperative-cream/20 text-sm px-4 py-3 outline-none focus:border-cooperative-orange transition-colors duration-200 resize-none"
                    />
                  </div>
                </StaggerItem>

                <StaggerItem variant={scaleIn} duration={0.45}>
                  <button
                    type="submit"
                    className="bg-cooperative-orange text-cooperative-dark font-black uppercase tracking-widest text-sm px-8 py-4 hover:bg-cooperative-cream transition-colors duration-200 mt-1 w-full"
                  >
                    Send Message →
                  </button>
                </StaggerItem>

              </StaggerWrapper>
            </div>
          </AnimateOnScroll>

        </div>

        {/* Bottom bar */}
        <AnimateOnScroll variant={fadeUp} delay={0.1}>
          <div className="mt-10 border-t border-white/10 pt-6 flex flex-col md:flex-row items-center justify-between gap-3">
            <p className="text-cooperative-cream/30 text-xs tracking-wide">
              © {new Date().getFullYear()} Bethel Obada Oko Cooperative Housing Society Limited · OGCS 5426
            </p>
            <p className="text-cooperative-cream/30 text-xs tracking-wide">
              First Bethel Housing Support Services Ltd · Abeokuta, Ogun State
            </p>
          </div>
        </AnimateOnScroll>

      </div>
    </section>
  );
}