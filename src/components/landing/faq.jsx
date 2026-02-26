import { useState } from "react";
import { AnimateOnScroll, StaggerWrapper, StaggerItem, fadeUp, fadeLeft, scaleIn, slideUp } from '../../animations/AnimateOnScroll'

const faqs = [
  {
    id: "01",
    question: "How do I register as a member of Bethel Cooperative?",
    answer: "Registration is simple. Visit our website, click on 'Register', fill in your personal details, and submit your application. Once reviewed and approved by our admin team, you will receive a confirmation and gain full access to your member dashboard.",
  },
  {
    id: "02",
    question: "How do I book or request an apartment?",
    answer: "After logging into your dashboard, browse available apartments uploaded by our admin. Select your preferred unit, fill in the booking request form, and submit. Our team will review your request and get back to you with the next steps.",
  },
  {
    id: "03",
    question: "How do I make payment and confirm my rent or purchase?",
    answer: "Once your booking is approved, make payment to the cooperative's designated account. Then log into your dashboard and upload your proof of payment. Our admin will manually verify and confirm your payment, after which your apartment status will be updated.",
  },
  {
    id: "04",
    question: "How does the agricultural dividend work?",
    answer: "Members who participate in our agricultural arm are entitled to annual dividends. Dividends are calculated by the admin at the end of each year based on contributions and cooperative performance. The payout is displayed on your dashboard at year end.",
  },
  {
    id: "05",
    question: "When am I eligible to apply for a cooperative loan?",
    answer: "You become eligible for a loan after a minimum of six consecutive months of savings with the cooperative. You will need to submit a guarantor form, a valid ID card, a passport photograph, and a next-of-kin form. All applications are reviewed and approved by our admin.",
  },
  {
    id: "06",
    question: "How will I know if my payment or application was approved?",
    answer: "You will receive a notification directly on your dashboard showing whether your payment proof or application has been approved or declined. Our admin team reviews all submissions promptly and keeps you informed at every stage.",
  },
  {
    id: "07",
    question: "Can I buy a property outright through the cooperative?",
    answer: "Yes. We offer full property purchase options within Bethel Garden Estate, Obada-Oko. Browse available listings, submit a purchase request, upload your payment evidence, and our admin will handle the verification and ownership transfer process.",
  },
  {
    id: "08",
    question: "How do I contact Bethel Cooperative for support?",
    answer: "You can reach us by phone at +2347051598561 or +2347037350984, or via WhatsApp at +447533990688. You can also visit us at First Bethel Housing Support Services Ltd, Bethel Garden Estate, Obada-Oko, Abeokuta, Ogun State.",
  },
];

export default function FAQ() {
  const [activeIndex, setActiveIndex] = useState(null);
  const toggle = (id) => setActiveIndex(activeIndex === id ? null : id);

  return (
    <section id="faq" className="bg-cooperative-cream pb-10 px-6">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <AnimateOnScroll variant={fadeUp} delay={0}>
          <p className="header-title-light">FAQ</p>
        </AnimateOnScroll>

        <AnimateOnScroll variant={fadeUp} delay={0.15}>
          <div className="text-center mb-4">
            <h2 className="text-cooperative-dark font-extrabold leading-tight text-4xl md:text-5xl">
              Got{" "}
              <span className="text-cooperative-orange italic">Questions?</span>
            </h2>
            <p className="text-cooperative-dark/50 text-base max-w-xl mx-auto mt-4 leading-relaxed">
              Everything you need to know about membership, housing, payments, and
              cooperative services — answered clearly.
            </p>
          </div>
        </AnimateOnScroll>

        <AnimateOnScroll variant={scaleIn} delay={0.25}>
          <div className="flex items-center justify-center gap-3 mt-8 mb-14">
            <div className="h-px w-16 bg-cooperative-brown/30" />
            <div className="w-2 h-2 bg-cooperative-brown rotate-45" />
            <div className="h-px w-16 bg-cooperative-brown/30" />
          </div>
        </AnimateOnScroll>

        {/* FAQ Items — stagger in */}
        <StaggerWrapper className="space-y-3" stagger={0.08} delay={0.1}>
          {faqs.map((faq) => {
            const isOpen = activeIndex === faq.id;
            return (
              <StaggerItem key={faq.id} variant={fadeLeft} duration={0.5}>
                <div
                  onClick={() => toggle(faq.id)}
                  className={`cursor-pointer border overflow-hidden transition-colors duration-300
                    ${isOpen
                      ? "bg-cooperative-brown border-cooperative-orange"
                      : "bg-white border-cooperative-dark/10"
                    }`}
                >
                  <div className="flex items-center justify-between px-7 py-5 gap-4">
                    <div className="flex items-center gap-5">
                      <span className={`text-xs font-black tracking-widest shrink-0 transition-colors duration-300 ${isOpen ? "text-cooperative-cream" : "text-cooperative-orange"}`}>
                        {faq.id}
                      </span>
                      <h3 className={`font-bold text-base md:text-lg leading-snug ${isOpen? 'text-cooperative-cream': 'text-cooperative-dark'}  transition-colors duration-300 `}>
                        {faq.question}
                      </h3>
                    </div>
                    <div className={`shrink-0 w-7 h-7 border flex items-center justify-center transition-all duration-300 ${isOpen ? "border-cooperative-dark/30 text-cooperative-dark rotate-45" : "border-cooperative-orange text-cooperative-orange rotate-0"}`}>
                      <svg viewBox="0 0 16 16" fill="none" className="w-3 h-3">
                        <path d="M8 2v12M2 8h12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      </svg>
                    </div>
                  </div>
                  <div className="overflow-hidden transition-all duration-500" style={{ maxHeight: isOpen ? "300px" : "0px" }}>
                    <div className="px-7 pb-6 pt-0">
                      <div className={`h-px w-full mb-4 ${isOpen ? "bg-cooperative-cream" : "bg-cooperative-dark/10"}`} />
                      <p className={`text-sm leading-relaxed ${isOpen ? "text-cooperative-cream" : "text-cooperative-dark/60"}`}>
                        {faq.answer}
                      </p>
                    </div>
                  </div>
                </div>
              </StaggerItem>
            );
          })}
        </StaggerWrapper>

      

      </div>
    </section>
  );
}